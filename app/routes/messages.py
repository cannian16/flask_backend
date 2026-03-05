from flask import Blueprint, request, jsonify
from app.models.message import Message
import hashlib
from app.extensions import db

messages_bp = Blueprint('messages', __name__, url_prefix='/messages')

@messages_bp.route('/get', methods=['GET'])
def get_messages():
    """获取留言列表"""
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 20, type=int)
    
    pagination = Message.query.order_by(Message.created_at.desc()).paginate(page=page, per_page=limit, error_out=False)

    import app.services.message as message_service
    processed_messages = message_service.email_hash(pagination.items)

    return jsonify({
        'messages': processed_messages,
        'pagination': {
            'total': pagination.total,
            'page': page,
            'limit': limit,
            'pages': pagination.pages
        }
    })

@messages_bp.route('/add', methods=['POST'])
def create_message():
    """创建新留言"""
    data = request.get_json()

    print(f"收到数据: {data}")

    #验证数据合法性
    import app.services.message as message_service
    is_valid, error_message = message_service.validate_data(data)
    if not is_valid:
        return jsonify({'error': error_message}), 400
    
    username = data.get('username').strip()
    website_url = data.get('website_url','').strip()
    if not website_url:
        website_url = None
    content = data.get('content').strip()
    email = data.get('email').strip()

    new_message = Message(
        username=username,
        website_url=website_url,
        content=content,
        email=email,
        ip_address=request.remote_addr,
        user_agent=request.headers.get('User-Agent')
    )
    
    db.session.add(new_message)
    db.session.commit()
    
    return jsonify({'message': '留言创建成功', 'id': new_message.id}), 201