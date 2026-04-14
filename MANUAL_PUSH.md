# 🚀 手动推送到GitHub - 详细步骤

由于当前环境无法交互式输入认证信息，请按照以下步骤手动推送：

## 📋 方法1: 使用Personal Access Token（推荐）

### 步骤1: 生成GitHub Token

1. **访问GitHub设置**:
   ```
   https://github.com/settings/tokens
   ```

2. **生成新Token**:
   - 点击 "Generate new token" → "Generate new token (classic)"
   - Note: `zhejiang-punishment-spider`
   - Expiration: `90 days` 或 `No expiration`
   - 勾选权限: `repo` (这个最重要)
   - 点击 "Generate token"

3. **复制Token**:
   - ⚠️ **重要**: 立即复制token，只显示一次！

### 步骤2: 推送代码

打开终端，复制粘贴以下命令：

```bash
cd "/Users/lizhendong/Desktop/claude code/爬虫脚本"
git push -u origin main
```

### 步骤3: 输入认证信息

当提示时：
- **Username**: `lizhendong`
- **Password**: 粘贴刚才复制的 **Personal Access Token**

✅ 完成！代码将开始上传。

---

## 🔐 方法2: 使用SSH密钥（最安全）

### 步骤1: 生成SSH密钥

运行以下命令：

```bash
cd "/Users/lizhendong/Desktop/claude code/爬虫脚本"
chmod +x setup_github_ssh.sh
./setup_github_ssh.sh
```

### 步骤2: 添加SSH密钥到GitHub

1. 脚本会显示您的SSH公钥，复制它
2. 访问: https://github.com/settings/ssh/new
3. 粘贴公钥并保存

### 步骤3: 推送代码

```bash
cd "/Users/lizhendong/Desktop/claude code/爬虫脚本"
git remote set-url origin git@github.com:lizhendong/zhejiang-punishment-spider.git
git push -u origin main
```

---

## ⚡ 快速命令（准备好Token后）

```bash
# 进入目录
cd "/Users/lizhendong/Desktop/claude code/爬虫脚本"

# 推送（会提示输入用户名和token）
git push -u origin main
```

---

## 🆘 常见问题

### Q: 推送时提示 "Authentication failed"
**A**: 确保使用的是 **Personal Access Token**，不是GitHub密码

### Q: Token在哪里生成？
**A**: https://github.com/settings/tokens

### Q: 忘记复制Token怎么办？
**A**: 删除旧的，重新生成一个新的

### Q: SSH方式更安全吗？
**A**: 是的，SSH密钥更安全，推荐长期使用

---

## 📊 上传内容确认

**仓库名称**: `zhejiang-punishment-spider`
**GitHub地址**: `https://github.com/lizhendong/zhejiang-punishment-spider`
**文件数量**: 17个文件
**代码行数**: 2,575行

---

**准备好了吗？选择一种方法，5分钟内完成上传！** 🚀
