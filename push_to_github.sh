#!/bin/bash

# 推送到GitHub的脚本

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  推送到GitHub"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 检查是否已经配置了remote
if git remote | grep -q "origin"; then
    echo "✅ Remote已配置"
    git remote -v
else
    echo "❓ 需要配置GitHub仓库地址"
    echo ""
    echo "请先在GitHub上创建仓库: https://github.com/new"
    echo ""
    read -p "请输入你的GitHub用户名: " username
    read -p "请输入仓库名称 (默认: zhejiang-punishment-spider): " reponame

    if [ -z "$reponame" ]; then
        reponame="zhejiang-punishment-spider"
    fi

    echo ""
    echo "选择连接方式:"
    echo "  1. HTTPS (推荐新手)"
    echo "  2. SSH (推荐高级用户)"
    read -p "请选择 (1/2): " choice

    if [ "$choice" = "2" ]; then
        # SSH方式
        git remote add origin "git@github.com:${username}/${reponame}.git"
    else
        # HTTPS方式
        git remote add origin "https://github.com/${username}/${reponame}.git"
    fi

    echo ""
    echo "✅ Remote配置完成"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  准备推送"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 显示当前状态
echo "📊 当前状态:"
git branch -v
echo ""

echo "📝 准备推送的文件:"
git ls-files | head -10
echo "... (共 $(git ls-files | wc -l | tr -d ' ') 个文件)"
echo ""

read -p "确认推送? (y/n): " confirm

if [ "$confirm" != "y" ]; then
    echo "❌ 取消操作"
    exit 1
fi

echo ""
echo "🚀 开始推送..."
echo ""

# 设置主分支名称
git branch -M main

# 推送
if git push -u origin main; then
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  ✅ 推送成功！"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "🌐 访问你的仓库:"
    git remote get-url origin | sed 's/git@github.com:/https:\/\/github.com\//'
    echo ""
else
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  ❌ 推送失败"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "可能的原因:"
    echo "1. GitHub仓库尚未创建"
    echo "2. 认证信息错误"
    echo "3. 网络连接问题"
    echo ""
    echo "解决方法:"
    echo "• 查看详细指南: cat GITHUB_GUIDE.md"
    echo "• 检查GitHub: https://github.com/new"
    echo "• 检查认证: https://github.com/settings/tokens"
    echo ""
fi
