import os
from functools import wraps
from flask import request, jsonify

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # 实时从系统环境拿，或者从你的 config 类拿
        expected_token = os.getenv("ADMIN_TOKEN")
        
        # 安全检查：如果服务器忘了配置环境变量，为了安全，拒绝所有请求
        if not expected_token:
            return jsonify({"message": "环境变量中没有配置管理员密钥"}), 500
            
        token = request.headers.get('X-API-KEY')
        
        if token != expected_token:
            return jsonify({"message": "管理员密钥错误"}), 403
            
        return f(*args, **kwargs)
    return decorated