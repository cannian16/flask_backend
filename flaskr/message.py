from flask import Blueprint, jsonify, request, current_app
from flaskr.db import get_db
import re
from datetime import datetime

bp = Blueprint('messages', __name__, url_prefix='/messages')

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
        SELECT id, username, website_url, content, created_at 
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
    
    return jsonify({
        'messages': [dict(msg) for msg in messages],
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
    data = request.get_json()
    
    # 验证必需字段
    if not data:
        return jsonify({'error': '请求数据不能为空'}), 400
    
    username = data.get('username', '').strip()
    website_url = data.get('website_url', '').strip()
    content = data.get('content', '').strip()
    
    # 数据验证
    if not username:
        return jsonify({'error': '用户名不能为空'}), 400
    
    if not validate_username(username):
        return jsonify({'error': '用户名格式不正确（2-50个字符，只能包含字母、数字、下划线、中文）'}), 400
    
    if not content:
        return jsonify({'error': '留言内容不能为空'}), 400
    
    if len(content) > 1000:
        return jsonify({'error': '留言内容不能超过1000个字符'}), 400
    
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
            INSERT INTO message (username, website_url, content, ip_address, user_agent)
            VALUES (?, ?, ?, ?, ?)
            ''',
            (username, website_url, content, ip_address, user_agent)
        )
        db.commit()
        
        # 返回新创建的留言
        new_message = db.execute(
            'SELECT id, username, website_url, content, created_at FROM message WHERE id = ?',
            (cursor.lastrowid,)
        ).fetchone()
        
        return jsonify(dict(new_message)), 201
        
    except Exception as e:
        current_app.logger.error(f'创建留言失败: {str(e)}')
        return jsonify({'error': '服务器内部错误'}), 500
