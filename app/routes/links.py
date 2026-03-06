from flask import Blueprint, request, jsonify
from app.models import Link
from app.extensions import db
from app.utils.decorators import token_required

links_bp = Blueprint('links', __name__, url_prefix='/links')

@links_bp.route('/get', methods=['GET'])
def get_links():
    """获取友链列表"""
    links = Link.query.order_by(Link.created_at.desc()).all()
    return jsonify([link.to_dict() for link in links])


@links_bp.route('/add', methods=['POST'])
@token_required
def create_link():
    """创建新友链"""
    data = request.get_json()

    name = data.get('name').strip()
    url = data.get('url').strip()
    description = data.get('description').strip()
    icon = data.get('icon').strip()

    new_link = Link(
        name=name,
        url=url,
        description=description,
        icon=icon
    )
    
    db.session.add(new_link)
    db.session.commit()

    return jsonify(new_link.to_dict()), 201

@links_bp.route('/delete', methods=['POST'])
@token_required
def delete_link():
    """删除友链"""
    data = request.get_json()
    link_id = data.get('id')
    link = Link.query.get_or_404(link_id)
    if not link:
        return jsonify({"error": "友链不存在"}), 404
    db.session.delete(link)
    db.session.commit()

    return jsonify({"message": "友链已删除"})

@links_bp.route('/update', methods=['POST'])
@token_required
def update_link():
    """更新友链"""
    #获取请求数据
    data = request.get_json()
    #提取链接ID
    link_id = data.get('id')
    #查询链接并更新数据
    link = Link.query.get_or_404(link_id)
    if not link:
        return jsonify({"error": "友链不存在"}), 404
    #更新链接属性，如果请求数据中没有对应属性，则保持原值不变，并去除字符串两端的空白
    link.name = data.get('name', link.name).strip()
    link.url = data.get('url', link.url).strip()
    link.description = data.get('description', link.description).strip()
    link.icon = data.get('icon', link.icon).strip()

    db.session.commit()

    return jsonify(link.to_dict())   