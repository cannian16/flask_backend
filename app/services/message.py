import hashlib
import re

def email_hash(messages):
    """为留言列表生成邮箱哈希"""
    processed_messages = []
    for message in messages:
        message_dict = message.to_dict()
        
        # 生成邮箱 SHA256 哈希
        email = message_dict['email']
        email_hash = hashlib.sha256(email.lower().encode()).hexdigest()
        message_dict['email_hash'] = email_hash
        del message_dict['email']  # 可选：是否返回原始邮箱
        processed_messages.append(message_dict)
    return processed_messages

def validate_data(data):
    """验证留言数据的合法性"""
    username = data.get('username', '').strip()
    website_url = data.get('website_url', '').strip()
    content = data.get('content', '').strip()
    email = data.get('email', '').strip()
    
    # 验证用户名
    if not (1 <= len(username) <= 20):
        return False, "用户名长度需在1-20位之间"
    
    # 2. 验证邮箱格式 (简单的正则)
    email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(email_pattern, email):
        return False, "邮箱格式不正确"
      
    # 3. 验证内容
    if not content or len(content) > 200:
        return False, "内容不能为空且不能超过200字"
    # 4. 验证网址格式（可选）
    if website_url:
        url_pattern = r'^(https?://)?([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}(/.*)?$'
        if not re.match(url_pattern, website_url):
            return False, "网址格式不正确"
    
    return True, None
