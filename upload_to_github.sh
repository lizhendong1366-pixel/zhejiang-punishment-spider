#!/bin/bash

# 爬虫脚本上传到GitHub脚本

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  爬虫脚本上传到 GitHub"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 进入爬虫脚本目录
cd "$(dirname "$0")"

echo "📂 当前目录: $(pwd)"
echo ""

# 检查是否已经是git仓库
if [ -d ".git" ]; then
    echo "⚠️  这个目录已经是git仓库"
    read -p "是否要重新初始化? (y/n): " reinit
    if [ "$reinit" = "y" ]; then
        rm -rf .git
        echo "✅ 已删除旧的git仓库"
    else
        echo "❌ 取消操作"
        exit 1
    fi
fi

# 初始化git仓库
echo "🔧 初始化git仓库..."
git init

# 添加所有文件
echo "📦 添加文件到git..."
git add .

# 提交
echo "💾 提交文件..."
git commit -m "Initial commit: 浙江省行政处罚数据爬虫

- 添加自动化爬虫脚本 (auto_spider.py)
- 添加简单版爬虫 (simple_spider.py)
- 添加多个调试工具脚本
- 添加完整使用文档 (README_spider.md)

功能特点:
- 支持自动翻页，已测试抓取100条记录
- 使用Playwright进行网页自动化
- 数据保存为CSV格式，方便分析
- 包含截图记录功能，便于调试"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  下一步操作指南"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "1️⃣  在GitHub上创建新仓库:"
echo "   • 访问: https://github.com/new"
echo "   • 仓库名称: zhejiang-punishment-spider (或其他)"
echo "   • 设置为 Public 或 Private"
echo "   • 不要初始化 README (我们已经有了)"
echo ""
echo "2️⃣  创建仓库后，GitHub会显示类似下面的命令:"
echo ""
echo "   ... or push an existing repository from the command line"
echo ""
echo "3️⃣  复制GitHub提供的命令并运行，类似于:"
echo ""
echo "   git remote add origin https://github.com/你的用户名/仓库名.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "✅ Git仓库已准备就绪！"
echo ""
echo "📝 仓库内容:"
git ls-files | head -10
echo "... (共 $(git ls-files | wc -l | tr -d ' ') 个文件)"
echo ""
echo "🌐 请按照上面的步骤在GitHub上创建仓库并推送代码"
echo ""
