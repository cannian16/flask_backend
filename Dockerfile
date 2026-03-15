# 使用官方 slim 基础镜像
FROM python:3.14-slim

# 设置工作目录
WORKDIR /flask_backend

# 先复制 requirements.txt 以利用 Docker 的层缓存
# 这样只有修改依赖时才会重新安装
COPY requirements.txt .

# 直接在全局环境安装依赖（或者你可以创建一个 venv）
# 既然用 pip，直接安装到全局系统镜像里是最简单的做法
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目所有代码
COPY . . 

# 暴露端口
EXPOSE 5000

# 启动命令
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:create_app()"]