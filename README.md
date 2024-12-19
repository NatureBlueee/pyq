# 朋友圈记忆提取器 (WeChat Moments Extractor)

一个优雅的网页应用，用于从微信朋友圈备份的 HTML 文件中提取纯文本内容。支持按时间排序、Markdown 导出等功能。

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/yourusername/pyq-cleaner)

## ✨ 特点

- 🎨 现代化的用户界面设计
- 🌓 自动适应深色/浅色模式
- 📱 完全响应式设计，支持移动端
- 🔄 拖拽上传支持
- ⚡️ 快速的文本提取
- 📅 自动提取发布时间
- 📝 支持 Markdown 格式导出
- 📋 一键复制所有内容
- 🌈 优雅的动画效果

## 🚀 在线使用

访问：[https://your-app-url.vercel.app](https://your-app-url.vercel.app)

## 🛠️ 本地开发

### 环境要求

- Python 3.8+
- pip

### 安装步骤

1. 克隆仓库
```bash
git clone https://github.com/yourusername/pyq-cleaner.git
cd pyq-cleaner
```

2. 创建虚拟环境
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows
```

3. 安装依赖
```bash
pip install -r requirements.txt
```

4. 运行应用
```bash
python app.py
```

5. 访问 http://localhost:5000

## 📦 部署到 Vercel

1. Fork 这个仓库
2. 在 Vercel 中导入项目
3. 选择 Python 框架
4. 部署完成！

## 💡 使用说明

1. 在微信中导出朋友圈数据（HTML格式）
2. 访问网站，点击上传区域或直接拖拽文件
3. 等待处理完成
4. 查看提取的内容
5. 可以选择复制内容或下载为 Markdown 文件

## 🔧 技术栈

- 后端：Python + Flask
- 前端：HTML5 + CSS3 + JavaScript
- UI：Custom CSS with Bootstrap
- 部署：Vercel

## 📝 更新日志

### v1.0.0 (2024-01-19)
- 🎉 首次发布
- 支持文本提取
- 支持时间提取
- 支持 Markdown 导出
- 响应式设计
- 深色模式支持

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 🙏 致谢

- [Bootstrap](https://getbootstrap.com/)
- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/)
- [Flask](https://flask.palletsprojects.com/)
- [Vercel](https://vercel.com/) 