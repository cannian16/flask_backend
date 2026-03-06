from flask import Blueprint, request, jsonify
from app.models import Skill
from app.extensions import db
from app.utils.decorators import token_required

skills_bp = Blueprint('skills', __name__, url_prefix='/skills')

@skills_bp.route('/get', methods=['GET'])
def get_skills():
    """获取技能列表"""
    skills = Skill.query.order_by(Skill.id.asc()).all()
    return jsonify([skill.to_dict() for skill in skills])

@skills_bp.route('/add', methods=['POST'])
@token_required
def create_skill():
    """创建新技能"""
    data = request.get_json()

    name = data.get('name').strip()
    logo = data.get('logo').strip()
    url = data.get('url').strip()

    new_skill = Skill(
        name=name,
        logo=logo,
        url=url
    )
    
    db.session.add(new_skill)
    db.session.commit()

    return jsonify(new_skill.to_dict()), 201

@skills_bp.route('/addlist', methods=['POST'])
@token_required
def create_skills():
    """批量创建新技能"""
    skills_data = request.get_json()

    new_skills = []
    for skill_data in skills_data:
        name = skill_data.get('name').strip()
        logo = skill_data.get('logo').strip()
        url = skill_data.get('url').strip()

        new_skill = Skill(
            name=name,
            logo=logo,
            url=url
        )
        new_skills.append(new_skill)

    db.session.add_all(new_skills)
    db.session.commit()

    return jsonify([skill.to_dict() for skill in new_skills]), 201

@skills_bp.route('/delete', methods=['POST'])
@token_required
def delete_skill():
    """删除技能"""
    data = request.get_json()
    skill_id = data.get('id')
    skill = Skill.query.get_or_404(skill_id)
    if not skill:
        return jsonify({"error": "技能不存在"}), 404
    db.session.delete(skill)
    db.session.commit()

    return jsonify({"message": "技能已删除"})

@skills_bp.route('/update', methods=['POST'])
@token_required
def update_skill():
    """更新技能"""
    #获取请求数据
    data = request.get_json()
    #提取技能ID
    skill_id = data.get('id')
    #查询技能并更新数据
    skill = Skill.query.get_or_404(skill_id)
    if not skill:
        return jsonify({"error": "技能不存在"}), 404

    skill.name = data.get('name', skill.name).strip()
    skill.logo = data.get('logo', skill.logo).strip()
    skill.url = data.get('url', skill.url).strip()

    db.session.commit()

    return jsonify(skill.to_dict())