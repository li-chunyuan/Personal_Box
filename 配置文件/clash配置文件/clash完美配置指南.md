
# # 🌐 Clash / Clash Meta / Mihomo

# **全平台“完美配置”最高标准指南（专业级）**

> 目标：**稳定、高速、安全、无泄漏、无分流错误、兼容所有应用、维护成本低、切换最顺手、长期可用。**

---

# ## 1. 安装与版本选择（高级标准）

### **1.1 选择正确发行版**

* **Windows（强烈推荐）**

  * Mihomo Party / Clash Verge Rev
  * Clash for Windows (CFW) + Meta Core

* **macOS**

  * ClashX Pro（含 TUN），或 Mihomo Core + GUI

* **Android**

  * Clash Meta for Android (CMA)

* **iOS**

  * Stash（最接近 Clash）
  * Shadowrocket（兼容性非常好）

### **1.2 使用 Meta/Mihomo 核心**

理由：更强规则、更强分流、更快解析、更稳定。

### **1.3 启用自动更新 Core**

防止新规则、订阅无法适配。

---

# ## 2. 订阅配置（最高标准）

### **2.1 订阅链接**

* 使用服务商的 ClashMeta 专属链接（包含策略组）
* 必须开启 **自动更新**（建议：每 6-12 小时）

### **2.2 多订阅合并（可选）**

如果你有多个机场：

* 启用 **merge-subscriptions**（合并节点）
* 分类：`地区 / 类型 / 延迟 / 流媒体`

### **2.3 节点筛选标准**

* Ping < 250ms
* 下载速度 > 20-50Mbps
* 同时有：**至少一个高速、一个稳定、一个冷备用**

---

# ## 3. 系统模式（完美配置核心）

你必须完成以下三项：

### **3.1 开启 TUN 模式（透明代理）**

* 所有应用流量都能走 Clash
* 包括游戏、命令行、桌面软件

### **3.2 启用系统代理（浏览器友好）**

* 浏览器、非管理员程序无缝代理
* 与 TUN 可并存

### **3.3 Bypass 国内局域网流量**

必须在 bypass 列表写：

```
localhost
127.0.0.1
192.168.0.0/16
172.16.0.0/12
10.0.0.0/8
*.lan
```

避免代理内网，降低延迟。

---

# ## 4. DNS 配置（专业级无泄漏）

### **4.1 必须切换到 Clash 内置 DNS**

不能使用本机或 ISP DNS（会被劫持）

### **4.2 启用 Fake-IP（推荐）**

* 解析更快
* 分流更准确（对国内外域名）

### **4.3 DNS 服务器建议**

```
domestic:
  - 223.5.5.5
  - 119.29.29.29

foreign:
  - 1.1.1.1
  - 8.8.8.8
```

### **4.4 开启 DNS Cache**

* 减少重复解析
* 大幅提升速度

### **4.5 完整 DNS 泄漏检测**

访问：

* dnsleaktest.com
* browserleaks.com/ip

必须是代理出口 IP，不是中国 DNS。

---

# ## 5. 规则组（最顺手的策略体验）

你至少需要 8 大策略组：

### **5.1 必备策略组**

* 🎯 Direct（国内直连）
* 🌐 Proxy（主代理）
* 🚀 Auto / Fallback（自动切换）
* 📺 Media（Netflix/YouTube/HBO）
* 🌏 Global（国外全局）
* 🛑 AdBlock（广告拦截）
* 🎮 Game（游戏）
* 🇭🇰🇯🇵🇺🇸 故障转移区域组（按你订阅节点地区）

### **5.2 最推荐的策略结构**

```
Global → Auto → Proxy → Region Groups → Nodes
Media → Auto
Game → Region (低延迟)
AdBlock → Direct
China → Direct
LAN → Direct
```

### **5.3 多重自动化**

* 自动测速（定期运行）
* 自动 fallback
* 断流重连
* 节点按延迟排序

---

# ## 6. GeoIP + Geosite 规则（高级）

### 必须包含：

* China → 全部直连
* Apple → 直连（App Store 流畅）
* Microsoft → 直连（激活、更新更快）
* Google → 代理
* YouTube → Media
* Netflix → Media
* TikTok → 特殊规则（强制代理）
* Github → Proxy（避免国内仓库污染）

### 补充：国内常见域名 white list

* bilibili.com
* taobao、tmall
* jd.com
* douyin、kuaishou

---

# ## 7. 流量安全（专业级）

### **7.1 禁用 WebRTC（浏览器）**

否则可能泄漏 IP。

### **7.2 强制 HTTPS**

浏览器装 HTTPS Everywhere 功能。

### **7.3 防止 DNS Hijack**

开启：

```
dns:
  enhanced-mode: fake-ip
  fake-ip-range: 198.18.0.1/16
```

### **7.4 禁止 IPv6（如你的机场不支持）**

避免 IPv6 泄漏真实出口。

---

# ## 8. 使用体验优化（“顺手度”关键）

### **8.1 Quick Switch（快速切换）**

* 配置快捷键：

  * 开关系统代理
  * 切换节点
  * 切换规则模式
  * 重启 TUN

### **8.2 托盘图标策略快速切换**

右键即可换节点，不进界面。

### **8.3 分应用代理**

为下面应用指定专用节点：

* Steam（直连）
* GitHub（代理）
* 游戏（低延迟节点）
* 浏览器（代理）

### **8.4 自定义测速刷新时间**

建议每 30–60 分钟自动刷新。

---

# ## 9. 故障排查（强制项）

你要确保能自己检查以下问题：

* DNS 是否劫持
* TUN 是否启用
* 浏览器是否走代理
* 节点是否超时
* Youtube/Google 能否访问
* 国内应用是否误走代理
* Netflix 是否正确走 Media

---

# ## 10. 日常维护（最终完美度）

### **10.1 订阅定时更新**（最重要）

自动每 6–12 小时更新。

### **10.2 自动清理无效节点**

每周清理一次。

### **10.3 规则更新**

使用最新版的：

* Loyalsoldier rules
* Meta rules
* 名称规范化（providers）

---

# # ✔️ 最终：完美 Clash 配置标准（总结）

你至少完成以下全部项目：

* [ ] 使用 Meta/Mihomo 核心
* [ ] 自动更新订阅
* [ ] TUN + 系统代理同时开启
* [ ] 国内白名单 + 国外精确分流
* [ ] Fake-IP DNS + 无泄漏
* [ ] GeoIP/Geosite 精准分类
* [ ] 多策略组配置完善
* [ ] Adblock 去广告
* [ ] 节点自动测速 + 自动 fallback
* [ ] WebRTC 禁用 + HTTPS 强制
* [ ] 软件热键 + 快速切换
* [ ] 各类平台都流畅稳定

做到这些，你的 Clash 已经达到“专业级最佳体验”。

