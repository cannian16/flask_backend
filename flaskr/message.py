from flask import Blueprint, jsonify, request, current_app
from flaskr.db import get_db
import re
from datetime import datetime
import hashlib

bp = Blueprint('messages', __name__, url_prefix='/messages')

def basic_security_checks():
    """基础安全检查"""
    # 1. 检查Referer防止跨站提交
    referer = request.headers.get('Referer', '')
    if not any(domain in referer for domain in ['blog.cannian.space', 'localhost:4321']):
        return False
    
    # 2. 检查User-Agent
    if not request.headers.get('User-Agent'):
        return False
    
    # 3. 限制频繁提交（简易版）
    ip = request.remote_addr
    db = get_db()
    recent_count = db.execute(
        "SELECT COUNT(*) FROM message WHERE ip_address = ? AND created_at > datetime('now', '-1 hour')",
        (ip,)
    ).fetchone()[0]
    
    return recent_count < 10  # 1小时内最多10条

def validate_email(email):
    """验证邮箱格式"""
    if not email:
        return True
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_website_url(url):
    """验证网站URL格式"""
    if not url:
        return True
    pattern = r'^https?://[^\s/$.?#].[^\s]*$'
    return re.match(pattern, url) is not None

def validate_username(username):
    """验证用户名格式"""
    if not username or len(username) < 2 or len(username) > 50:
        return False
    # 只允许字母、数字、下划线、中文
    pattern = r'^[a-zA-Z0-9_\u4e00-\u9fa5]+$'
    return re.match(pattern, username) is not None

@bp.route('/get', methods=['GET'])
def get_messages():
    """获取留言列表"""
    db = get_db()
    
    # 获取查询参数
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 20, type=int)
    username = request.args.get('username', '')
    
    # 计算偏移量
    offset = (page - 1) * limit
    
    # 构建查询条件
    query = '''
        SELECT id, username, website_url, content, created_at , email
        FROM message 
    '''
    params = []
    
    if username:
        query += ' WHERE username LIKE ?'
        params.append(f'%{username}%')
    
    query += ' ORDER BY created_at DESC LIMIT ? OFFSET ?'
    params.extend([limit, offset])
    
    # 执行查询
    messages = db.execute(query, params).fetchall()
    
    # 获取总数
    count_query = 'SELECT COUNT(*) FROM message'
    count_params = []
    
    if username:
        count_query += ' WHERE username LIKE ?'
        count_params.append(f'%{username}%')
    
    total = db.execute(count_query, count_params).fetchone()[0]
    # 处理数据，添加邮箱哈希
    processed_messages = []
    for msg in messages:
        message_dict = dict(msg)
        
        # 生成邮箱 SHA256
        email = msg['email']
        email_hash = hashlib.sha256(email.lower().encode()).hexdigest()
        message_dict['email_hash'] = email_hash
        
        # 移除原始邮箱（保护隐私）
        del message_dict['email']  # 可选：是否返回原始邮箱
        
        processed_messages.append(message_dict)
    
    return jsonify({
        'messages': processed_messages,
        'pagination': {
            'page': page,
            'limit': limit,
            'total': total,
            'pages': (total + limit - 1) // limit
        }
    })

@bp.route('/add', methods=['POST'])
def create_message():
    """创建新留言"""
    # 基础安全检查
    #if not basic_security_checks():
    #    return jsonify({'error': '提交过于频繁或非法请求'}), 400
    
    data = request.get_json()
    print(f"收到数据: {data}")
    # 验证必需字段
    if not data:
        return jsonify({'error': '请求数据不能为空'}), 400
    
    username = data.get('username', '').strip()
    website_url = data.get('website_url', '').strip()
    content = data.get('content', '').strip()
    email = data.get('email', '').strip()
    
    # 数据验证
    if not username:
        return jsonify({'error': '用户名不能为空'}), 400
    
    if not validate_username(username):
        return jsonify({'error': '用户名格式不正确（2-50个字符，只能包含字母、数字、下划线、中文）'}), 400
    
    if not email:
        return jsonify({'error': '邮箱不能为空'}), 400
    
    if not validate_email(email):
        return jsonify({'error': '邮箱格式不正确'}), 400
    
    if not content:
        return jsonify({'error': '留言内容不能为空'}), 400
    
    if len(content) > 200:
        return jsonify({'error': '留言内容不能超过200个字符'}), 400
    
    if website_url and not validate_website_url(website_url):
        return jsonify({'error': '网站URL格式不正确'}), 400
    
    db = get_db()
    
    try:
        # 获取客户端信息
        ip_address = request.remote_addr
        user_agent = request.headers.get('User-Agent', '')[:500]  # 限制长度
        
        # 插入留言
        cursor = db.execute(
            '''
            INSERT INTO message (username, website_url, content, ip_address, user_agent, email)
            VALUES (?, ?, ?, ?, ?, ?)
            ''',
            (username, website_url, content, ip_address, user_agent, email)
        )
        db.commit()
        
        # 返回新创建的留言
        new_message = db.execute(
            'SELECT id, username, website_url, content, email, created_at FROM message WHERE id = ?',
            (cursor.lastrowid,)
        ).fetchone()
        
        return jsonify(dict(new_message)), 201
        
    except Exception as e:
        current_app.logger.error(f'创建留言失败: {str(e)}')
        return jsonify({'error': '服务器内部错误'}), 500
