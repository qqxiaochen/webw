# 项目记忆 - webw (PaoMian Hax)

## 项目概述
PaoMian Hax（泡面辅助）官网，提供 CrossFire（穿越火线）游戏第三方辅助工具下载。
域名：www.paomfz.com，纯静态网站，无后端。GitHub Pages 托管（qqxiaochen/webw），CNAME 绑定。

## 技术栈
- 前端：纯 HTML + CSS + JS，**无任何外部依赖**（旧 jQuery / UIkit / widget 体系已全部移除）
- 设计系统：CSS variables（25+ 个设计 token） + `prefers-color-scheme` 浅/深色自动切换
- 玻璃效果：backdrop-filter saturate(220%) blur(40px) + 渐变受光描边（padding-box/border-box）+ 多层 radial-gradient 环境光 + 噪点纹理
- 动效：按钮镜面扫光、卡片 hover 玻璃高亮、Hero 视差渐隐、macOS 弹窗 spring 弹出
- 部署：纯静态，HTML+CSS+JS 全部内联在 index.html，单文件 35KB 即可托管

## 关键文件
- `index.html`：**35KB 自包含单文件**（HTML+CSS+JS 内联），macOS Liquid Glass v3 风格，无外部依赖
- `download.html`：下载页（VN/WE/PH 三服；**VN 链接死链**，down/vn/ 目录不存在）
- 根 `core.css`（243KB）与 `static/css/core.css`（251KB）两份，根副本无人引用
- `static/`：含大量死文件（yii.js、APlayer、Meting、jquery-1.9.1、base.css、popup.css）
- `down/`：14 个 ZIP ≈394MB（speed/ 下 3 个 ZIP 字节相同）；`webw.zip` 400MB 未跟踪备份

## 代码质量问题记录
1. index.html HTML 结构错乱（`</body>` 提前闭合、SVG defs 截断），需重写
2. 3 份 jQuery 并存，footer.js 命名误导（实为 jQuery 库）
3. 无 meta description / OG / lang 属性，keywords 黑帽堆砌
4. 自动播放 3.2MB music.mp3，浏览器拦截且负体验
5. 无 .gitignore（webw.zip 400MB 有误提交风险）；git 提交信息多为「1」
6. 支付渠道 mall.909net.cn 为境内域名，与页脚 "Except China" 声明矛盾（合规风险）

## 改版记录
- **2026-08-25** index.html 完全重写 — macOS Liquid Glass 风格（自包含 35KB 单文件 v3）
  - 浮动玻璃导航：scroll 后收为 860px 悬浮 pill，移动端副标题收拢
  - 玻璃面板：backdrop-filter saturate(220%) blur(40px) + 渐变受光描边（160° 折射感） + 115° 镜面高光 + 底部内反光
  - 环境光：5 层 radial-gradient（蓝/紫/青/粉 + 中央亮斑） + 噪点纹理
  - 25+ 个 CSS variables + 浅/深色 mode 自动切换
  - macOS 弹窗：红黄绿交通灯 + 9 条 TOS 条款
  - 音乐开关：右下角浮动玻璃按钮，懒加载 mp3 默认关闭（原 autoplay 已去除）
  - 图标全部重绘为线性 SVG
  - 按钮动效：hover 镜面扫光 + 箭头右移；active 压感 spring
  - 卡片动效：hover translateY(-7px) + scale 1.022 + brightness 1.22 + saturate 1.12
  - 移动端专属：blur 降级保帧率、动画放慢、reveal 缩放进入、触摸按压反馈、hover:none 清理粘滞、env(safe-area-inset-bottom) 安全区
  - 验证：Edge 无头截图 5 张（浅/深/移动/弹窗/hover），JS 零错误
  - 旧版备份：`.workbuddy/backups/index.html.bak-20260825`
- 深度分析报告：`.workbuddy/reports/paomian-website-analysis.html`（2026-08-25，含 P0/P1/P2 优化路线图）
