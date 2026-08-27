# 项目记忆 - webw (PaoMian Hax)

## 项目概述
PaoMian Hax（泡面辅助）官网，提供 CrossFire（穿越火线）游戏第三方辅助工具下载。
域名：www.paomfz.com，纯静态网站，无后端。
**托管实测（2026-08-27）＝ Cloudflare（非 GitHub Pages）**：DNS→172.66.40.151，Server: cloudflare，CF 默认 robots/404；GitHub /pages API 返回 404（仓库未启用 GH Pages）。线上文件哈希≠本地 git（疑 Cloudflare Pages 直传混淆构建），**git 仓库仅源码留档，非发布通道**——发布链路与 git 存在漂移，为待治理 P0。仓库体积 1.4GB（历史二进制污染）。

## 技术栈
- 前端：纯 HTML + CSS + JS，**无任何外部依赖**（旧 jQuery / UIkit / widget 体系已全部移除）
- 设计系统：CSS variables（25+ 个设计 token） + `prefers-color-scheme` 浅/深色自动切换
- 玻璃效果：backdrop-filter saturate(220%) blur(40px) + 渐变受光描边（padding-box/border-box）+ 多层 radial-gradient 环境光 + 噪点纹理
- 动效：按钮镜面扫光、卡片 hover 玻璃高亮、Hero 视差渐隐、macOS 弹窗 spring 弹出
- 部署：纯静态，HTML+CSS+JS 全部内联在 index.html，单文件 35KB 即可托管

## 关键文件
- `index.html`：**35KB 自包含单文件**（HTML+CSS+JS 内联），macOS Liquid Glass v3 风格，无外部依赖
- `download.html`：下载页（VN/WE/PH 三服；**VN 线上实测 404 死链**；PH 已换 9D759C3.zip 但本地未提交）。2026-08-27 扩大下载点击区：卡片上半部分（flag / 标题 / 版本 / 状态）点击触发下载，Intro 按钮与密码区除外。
- `404.html`：**已落地 Apple Liquid Glass（visionOS 风格）2026-08-27**，v2 优化：玻璃厚度折射边（外白描边+底内暗边）、`mask-image` 羽化光泽、背景增粉/青多层让玻璃透色、子面板层次折射（顶高光+底内暗边）、hover 浮起+scale；`backdrop-filter:saturate(200%)`。HTML 结构不变（仿浏览器窗口），仅替换 `<style>`；旧实色全清；脚本保留。原版备份 `.workbuddy/backups/404.html.bak-20260827`，CSS 副本 `.workbuddy/tmp/404-liquid-glass.css`。注意：线上 CF 仍返默认 404，本地改版需走 Cloudflare 发布链路才会生效（见 P0 发布漂移）
- `down/`：6 个 ZIP ≈130MB（ph×2 / we×1 / speed×3；speed/ 3 份字节相同，7A638484/2B4CA307 为历史残留）
- `static/`：仅 music.mp3(3.2MB) 被引用；images/ 13 文件全为死文件

## 协作偏好
- 视觉/改版类任务：**先输出页面结构分析 + Liquid Glass 改造方案映射（复用现有 class），获用户确认后再落地代码，不要直接覆盖**。用户明确区分"分析+方案"与"改代码"两步。

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
- **2026-08-27** 深度分析 v2：`.workbuddy/reports/project-deep-analysis-20260827-v2.html`（含线上全站 URL 实测表、部署架构真相、仓库膨胀分析）
- **2026-08-27** `404.html` 重构为 Apple Liquid Glass：复用现有 class（.wrap/.main/.header-tabs/.header-url/.main-content 及控件），新增 `:root` 设计令牌、`.wrap::before/::after` 双 ambient 光晕、`.main::before/::after` 受光高光+shine 扫过；保留 URL 回填与 5 秒跳转脚本。临时 CSS 副本 `.workbuddy/tmp/404-liquid-glass.css`
