from flaskr import create_app

def main():
    """主函数，明确的应用入口"""
    print("启动 Flask 应用...")
    
    # 创建应用实例
    app = create_app()
    
    # 启动服务器
    app.run(debug=True, host='0.0.0.0', port=5000)

if __name__ == '__main__':
    main()  # 明确的程序入口