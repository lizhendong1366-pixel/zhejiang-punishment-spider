#!/bin/bash

# GitHub SSH密钥设置脚本

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  GitHub SSH密钥设置"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 检查是否已有SSH密钥
if [ -f ~/.ssh/id_ed25519 ]; then
    echo "✅ SSH密钥已存在"
    echo ""
    cat ~/.ssh/id_ed25519.pub
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  下一步: 添加SSH密钥到GitHub"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "1. 复制上面的公钥"
    echo "2. 访问: https://github.com/settings/ssh/new"
    echo "3. 粘贴公钥并保存"
    echo "4. 运行: git remote set-url origin git@github.com:lizhendong/zhejiang-punishment-spider.git"
    echo "5. 运行: git push -u origin main"
    echo ""
else
    echo "🔧 生成SSH密钥..."
    ssh-keygen -t ed25519 -C "lizhendong@haitao-law.com" -f ~/.ssh/id_ed25519 -N ""

    echo "✅ SSH密钥生成完成"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  下一步: 添加SSH密钥到GitHub"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "📋 您的SSH公钥:"
    echo ""
    cat ~/.ssh/id_ed25519.pub
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "1. 复制上面的公钥"
    echo "2. 访问: https://github.com/settings/ssh/new"
    echo "3. 粘贴公钥并保存"
    echo "4. 运行以下命令:"
    echo ""
    echo "   cd \"/Users/lizhendong/Desktop/claude code/爬虫脚本\""
    echo "   git remote set-url origin git@github.com:lizhendong/zhejiang-punishment-spider.git"
    echo "   git push -u origin main"
    echo ""
fi
