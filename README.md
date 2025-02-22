# 抽奖系统

一个简单的在线抽奖系统，支持：
- 实时抽奖
- 管理界面
- 数据持久化
- 防重复参与

## 安装

1. 克隆仓库
2. 安装依赖
3. 运行

## 使用

1. 访问 `http://localhost:5000` 即可进入抽奖页面
2. 管理员可以访问 `http://localhost:5000/admin` 进入管理界面
3. 管理员可以开始或停止抽奖，重置抽奖系统，查看参与人数和已抽取的号码

## 注意事项

- 抽奖系统使用 SQLite 数据库，数据存储在 `lottery.db` 文件中
- 管理员操作会直接影响到抽奖状态和数据，请谨慎操作
- 抽奖系统没有用户验证，任何人都可以参与抽奖，请确保抽奖活动的安全性

希望这个抽奖系统能给你带来乐趣和惊喜！如果有任何问题或建议，欢迎提出。

## 文件结构

- `app.py`: 主应用程序文件，包含 Flask 应用的配置和路由
- `templates/`: 包含 HTML 模板文件
- `static/`: 包含静态文件，如 CSS 和 JavaScript
- `requirements.txt`: 列出项目所需的依赖
- `.gitignore`: 列出不应提交到仓库的文件
- `README.md`: 项目说明和使用指南

## 依赖

- Flask: 用于构建 Web 应用
- SQLite3: 用于数据库操作

## 感谢

感谢所有为这个项目提供帮助的人！

