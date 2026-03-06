from flask import Blueprint, request, jsonify
from app.models import Tool
from app.extensions import db
from app.utils.decorators import token_required

tools_bp = Blueprint('tools', __name__, url_prefix='/tools')
@tools_bp.route('/get', methods=['GET'])
def get_tools():
    """获取工具列表"""
    tools = Tool.query.order_by(Tool.id.desc()).all()
    return jsonify([tool.to_dict() for tool in tools])

@tools_bp.route('/add', methods=['POST'])
@token_required
def create_tool():
    """创建新工具"""
    data = request.get_json()

    title = data.get('title').strip()
    subtitle = data.get('subtitle').strip()
    url = data.get('url').strip()
    imgUrl = data.get('imgUrl').strip()
    content = data.get('content').strip()

    new_tool = Tool(
        title=title,
        subtitle=subtitle,
        url=url,
        imgUrl=imgUrl,
        content=content
    )
    
    db.session.add(new_tool)
    db.session.commit()

    return jsonify(new_tool.to_dict()), 201

@tools_bp.route('/delete', methods=['POST'])
@token_required
def delete_tool():
    """删除工具"""
    data = request.get_json()
    tool_id = data.get('id')
    tool = Tool.query.get_or_404(tool_id)
    if not tool:
        return jsonify({"error": "工具不存在"}), 404
    db.session.delete(tool)
    db.session.commit()

    return jsonify({"message": "工具已删除"})

@tools_bp.route('/update', methods=['POST'])
@token_required
def update_tool():  
    """更新工具"""
    #获取请求数据
    data = request.get_json()
    #提取工具ID
    tool_id = data.get('id')
    #查询工具并更新数据
    tool = Tool.query.get_or_404(tool_id)
    if not tool:
        return jsonify({"error": "工具不存在"}), 404

    tool.title = data.get('title', tool.title).strip()
    tool.subtitle = data.get('subtitle', tool.subtitle).strip()
    tool.url = data.get('url', tool.url).strip()
    tool.imgUrl = data.get('imgUrl', tool.imgUrl).strip()
    tool.content = data.get('content', tool.content).strip()

    db.session.commit()

    return jsonify(tool.to_dict())

@tools_bp.route('/addlist', methods=['POST'])
@token_required
def add_tools():
    """批量添加工具"""
    tools_data = request.get_json()
    new_tools = []
    for tool_data in tools_data:
        title = tool_data.get('title').strip()
        subtitle = tool_data.get('subtitle').strip()
        url = tool_data.get('url').strip()
        imgUrl = tool_data.get('imgUrl').strip()
        content = tool_data.get('content').strip()
        new_tool = Tool(title=title, subtitle=subtitle, url=url, imgUrl=imgUrl, content=content)
        new_tools.append(new_tool)
    if new_tools:
        db.session.add_all(new_tools)
        db.session.commit()

    return jsonify({"message": f"成功添加 {len(new_tools)} 个工具"}), 201