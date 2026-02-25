# iFlow API 自动更新系统

一个基于 GitHub Actions 的自动化解决方案，用于自动管理 iFlow API 密钥的过期检测和重置。

## 🚀 核心功能

### 🔄 自动 API 密钥管理
- **自动检测过期状态**: 实时监控 API 密钥的 `hasExpired` 状态
- **即将过期检测**: 当 API 密钥的 `expireTime` 与当天日期相同时，视为即将过期并自动重置
- **固定时间执行**: 每日凌晨0:00 (UTC+8) 自动执行，确保及时更新
- **简单可靠**: 移除复杂调度逻辑，提高稳定性

### 🌐 浏览器自动化
- **智能重置**: 当 API 密钥过期或即将过期时，自动模拟浏览器操作点击重置按钮
- **页面加载优化**: 增加页面加载等待时间，确保页面完全渲染
- **反检测机制**: 随机 User-Agent、操作延迟等
- **无头模式运行**: 在 GitHub Actions 环境中无界面运行

### ⚡ GitHub Actions 自动化
- **定时触发执行**: 每日固定时间执行完整流程
- **详细日志记录**: 完整的执行日志和错误追踪
- **UTC+8 时区支持**: 统一使用北京时间，确保时间准确性

## 📁 项目结构

```
iflowapi/
├── .github/
│   └── workflows/
│       └── auto-update-api.yml    # GitHub Actions 工作流配置
├── auto_update_api.py            # 主程序 - 完整的自动更新流程
├── requirements.txt              # Python 依赖包列表
├── LICENSE                      # MIT 许可证
└── README.md                   # 项目说明文档
```

## 🛠️ 快速开始

### 1. 环境准备

#### 克隆项目
```bash
git clone https://github.com/admin6a/iflowapi
cd iflowapi
```

#### 安装依赖
```bash
# 创建虚拟环境
python -m venv .venv

# 激活虚拟环境
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 2. 环境变量配置

#### 必需环境变量
```bash
# iFlow 平台认证
IFLOW_COOKIE=your_iflow_cookie_here
```

### 3. GitHub Secrets 配置

在 GitHub 仓库的 **Settings > Secrets and variables > Actions** 中配置：

| Secret Name | Description | Required | Example |
|-------------|-------------|----------|----------|
| `IFLOW_COOKIE` | iFlow 平台登录 Cookie | ✅ Yes | `your_cookie_here` |

## 🔧 核心模块详解

### auto_update_api.py - 主程序

**主要功能**:
- API 密钥信息获取和解析
- 过期状态检测和处理
- 浏览器自动化重置操作
- UTC+8 时区时间处理

**执行流程**:
1. 获取 API 密钥信息
2. 检测过期状态
3. 如果过期，执行浏览器模拟重置操作
4. 如果未过期，检查是否即将过期（expireTime与当天日期相同）
5. 如果即将过期，执行浏览器模拟重置操作
6. 如果未过期且不即将过期，跳过重置操作
7. 记录执行结果

## ⚙️ GitHub Actions 工作流

### 执行策略

#### 直接执行 (update-api-key)
- **简单直接**: 每日固定时间执行完整流程
- **完整流程**: 包含所有功能模块
- **稳定可靠**: 移除复杂调度逻辑

### 执行频率

- **定时触发**: 每日凌晨0:00 (UTC+8) 执行 (`0 16 * * *`)
- **固定执行**: 每次都会完整执行，确保及时更新

## 🔍 使用示例

### 本地测试

```bash
# 设置环境变量
export IFLOW_COOKIE="your_cookie_here"

# 运行主程序
python auto_update_api.py
```

## 🐛 故障排除

### 常见问题

#### 1. 环境变量未设置
**症状**: `IFLOW_COOKIE环境变量未设置`
**解决**: 检查 GitHub Secrets 或本地环境变量配置

#### 2. API 认证失败
**症状**: `API请求失败` 或认证错误
**解决**: 更新 IFLOW_COOKIE 值

#### 3. 浏览器操作失败
**症状**: `未找到按钮元素` 或 `浏览器模拟操作失败`
**解决**: 
- 检查 IFLOW_COOKIE 是否有效
- 确认 iFlow 平台页面结构未发生变化
- 查看调试截图和页面源码

### 日志分析

程序提供详细的日志输出，包括：
- 执行时间点（UTC+8）
- API 响应状态
- 过期检测结果
- 即将过期检测结果
- 浏览器操作步骤
- 执行结果状态

## 📈 监控和维护

### 执行状态监控

GitHub Actions 提供完整的执行历史：
- 成功/失败状态
- 执行时间统计
- 详细的日志输出

### 定期维护

1. **Cookie 更新**: 定期检查并更新 IFLOW_COOKIE
2. **依赖更新**: 定期更新 Python 依赖包
3. **页面结构监控**: 关注 iFlow 平台页面结构变化，及时调整选择器

## 🔒 安全考虑

### 隐私保护
- 所有敏感信息通过环境变量管理
- GitHub Secrets 提供安全的机密存储
- 代码中无硬编码的隐私信息

### 反检测机制
- 随机 User-Agent 轮换
- 操作延迟模拟人类行为
- 随机执行时间避免模式检测

## 📄 许可证

本项目采用 [MIT 许可证](LICENSE)，允许自由使用、修改和分发。

## 🤝 贡献指南

欢迎提交 [Issue](https://github.com/admin6a/iflowapi/issues) 和 [Pull Request](https://github.com/admin6a/iflowapi/pulls) 来改进项目！

### 开发环境设置

1. Fork 项目仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 📞 支持

如果您遇到问题或有建议：

1. 查看 [故障排除](#故障排除) 部分
2. 检查 [GitHub Issues](https://github.com/admin6a/iflowapi/issues) 是否有类似问题
3. 创建新的 [Issue](https://github.com/admin6a/iflowapi/issues) 描述您的问题

---

**注意**: 使用本项目需要遵守 iFlow 平台的使用条款和相关法律法规。
