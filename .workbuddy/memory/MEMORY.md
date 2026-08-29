# 项目记忆 - webw (PaoMian Hax)

## 项目概述
PaoMian Hax（泡面辅助）官网，提供 CrossFire（穿越火线）游戏第三方辅助工具下载。
域名：www.paomfz.com，纯静态网站，无后端。
### 部署架构（2026-08-29 实测定论，**推翻 08-27 的 Cloudflare Pages 结论**）
**用户 → Cloudflare（DNS + 反向代理，172.66.40.151，CF-RAY: HKG）→ 回源 GitHub Pages（Fastly · japaneast）**
- 铁证：`X-GitHub-Request-Id` + `x-github-edge-region: japaneast` + `Via: 1.1 varnish` + `X-Served-By: cache-nrt-*` + `X-Fastly-Request-ID`。这套组合只有 GitHub Pages 会有
- Cloudflare 上**无独立站点副本**，纯转发层
- CI：`.github/workflows/deploy-pages.yml`，push main 触发；**实测提交后 59 秒完成部署，链路健康**
- 08-28 的 v4 改版从未 commit，故从未上线 —— 此前登记的「发布漂移 P0」**已于 2026-08-29 撤销**
- ⚠ **P0 隐患**：CI 里有 `rm -f CNAME`，注释称"仅部署 github.io、保留 Cloudflare 主站"，但该前提不存在（主站就在 GH Pages）。每次部署都在删自定义域名凭证，随时可能解绑 → 全站 404

### 待治理问题（完整版见 2026-08-29 分析报告 v3）
- **P0** VN 下载死链：`download.html:431` → `/down/vn/PaoMianHax-Vn-211103-2(Pass123).zip` 线上 404，本地无 `down/vn/` 目录
- **P0** 10 个 `target="_blank"` 缺 `rel="noopener noreferrer"`（index 6 + download 4）
- **P1** 死文件 69.1MB（`down/ph/7A638484.zip` + `down/speed/`×3）+ `static/images/` 13 个零引用文件
- **P1** `.git` 1.5GB / 433 个 loose object / **in-pack: 0**（从未 gc）；历史 20+ 个 31MB 级 ZIP blob
- 404.html 缺 DOCTYPE、viewport 禁用缩放、`lang="en"` 但正文中文；download.html 缺 h1
- 零安全响应头（HSTS/CSP/XFO/XCTO/Referrer-Policy 全无）；无 sitemap.xml / robots.txt
- 仓库体积 1.6GB（历史二进制污染）

## 技术栈
- 前端：纯 HTML + CSS + JS，**无任何外部依赖**（旧 jQuery / UIkit / widget 体系已全部移除）
- 设计系统：CSS variables 设计 token，**不做深浅自动切换**（无 `prefers-color-scheme` 分支）
- **视觉语言 v6 深色磨砂玻璃（2026-08-29 15:46 ＝ 当前版本）**
  - `--bg-base:#0b0c12`、`--glass-bg:rgba(255,255,255,.055)`、`--blur:saturate(140%) blur(28px)`
  - **磨砂三要素**：低飽和 `saturate(140%)`（液态玻璃 250% 会显艳）+ 中等 `blur(28px)` + **重噪点 `.055`**（砂感主要来源）
  - 玻璃厚度：顶部受光高光 `.14` + **底部内亮边 `rgba(255,255,255,.06)`**（深底与白底相反）
  - 阴影回到深色重投影 `rgba(0,0,0,.42~.55)`
  - hover 可用高 `brightness(1.22~1.28)` —— 深底上提亮有效，不会过曝（白底则必须压到 1.03）
  - 环境光 `.30–.42`，深底上可以比白底浓
  - 上一版快照 `.workbuddy/backups/*.bak-20260829-1540`
- **v5 白色高透明玻璃（2026-08-29 15:30，已被 v6 取代）**：快照 `*.bak-20260829-1540`
  - 白底玻璃靠「顶部强高光 .88 + 底部内暗边 rgba(31,38,79,.10)」；hover 必须压到 `brightness(1.03~1.04)`
- **v3 深色液态玻璃（v5 之前）**：深底 #090a12 + `saturate(250%)` 高饱和；快照 `*.bak-20260828` ≡ `*.bak-20260829-1530`
- **v4 Editorial Material System（2026-08-28，已撤销）**：快照 `*.bak-20260829`
- ⚠ **404.html 仍是浅色 Apple Liquid Glass（2026-08-27 版），与 v6 深色不同调** —— 三页现不一致，需统一时另行改造
- 部署：纯静态，HTML+CSS+JS 全部内联，单文件即可托管

## 关键文件
- `index.html`：**35KB 自包含单文件**（HTML+CSS+JS 内联），**v6 深色磨砂玻璃**，无外部依赖
- `download.html`：下载页（VN/WE/PH 三服）。2026-08-27 扩大下载点击区：卡片上半部分（flag / 标题 / 版本 / 状态）点击触发下载，Intro 按钮与密码区除外。**VN 是 100% 死链**（指向 `/down/vn/PaoMianHax-Vn-211103-2(Pass123).zip`，线上 404 且本地无 `down/vn/` 目录）；WE→5C72CA.zip、PH→9D759C3.zip 均已在用且已提交 git。
- `404.html`：**已落地 Apple Liquid Glass（visionOS 风格）2026-08-27**，v2 优化：玻璃厚度折射边（外白描边+底内暗边）、`mask-image` 羽化光泽、背景增粉/青多层让玻璃透色、子面板层次折射（顶高光+底内暗边）、hover 浮起+scale；`backdrop-filter:saturate(200%)`。HTML 结构不变（仿浏览器窗口），仅替换 `<style>`；旧实色全清；脚本保留。原版备份 `.workbuddy/backups/404.html.bak-20260827`，CSS 副本 `.workbuddy/tmp/404-liquid-glass.css`。**GitHub Pages 会自动采用根目录 404.html 作自定义 404 页**，push 后即生效，无需额外配置。已知缺陷：**缺 `<!DOCTYPE html>`（三页唯一）、viewport 禁用缩放、`lang="en"` 但正文中文**
- `down/`：6 个 ZIP ≈129MB（ph×2 / we×1 / speed×3）。**在用仅 2 个**（ph/9D759C3.zip 31.1MB + we/5C72CA.zip 29.1MB）；**死文件 4 个共 69.1MB**（ph/7A638484.zip + speed/ 3 份 12.7MB 字节相同）
- `static/`：仅 `music.mp3`(3.1MB) 与 `favicon.ico` 被引用；`images/` 13 个文件（≈785KB）**全部零引用**

## 协作偏好
- 视觉/改版类任务：**先输出页面结构分析 + Liquid Glass 改造方案映射（复用现有 class），获用户确认后再落地代码，不要直接覆盖**。用户明确区分"分析+方案"与"改代码"两步。
- **还原/回退诉求：先摆时间线 + 备份快照列表让用户确认落点，再执行**。用户口中的「昨天的页面」指改动发生**之前**的状态，而非字面日期当天（2026-08-29 实测）。回退前必先快照当前版本。

## 代码质量问题记录
**已修复（2026-08-25 重写）**：~~HTML 结构错乱~~、~~3 份 jQuery 并存~~、~~缺 meta description/OG/lang~~、~~autoplay music.mp3~~、~~无 .gitignore~~

**仍待处理（2026-08-29 复核）**：
1. 404.html 缺 DOCTYPE、viewport 禁用缩放、lang 标注错误
2. download.html 缺 h1；keywords 黑帽堆砌（index 20+ 重复变体，建议整行删除）
3. 10 个 `target="_blank"` 缺 `rel="noopener noreferrer"`
4. 三页 CSS 高度重复（index↔download 约 60% 复制），建议抽 `static/site.css`
5. git 提交信息多为「1」，无法追溯变更意图
6. 支付渠道 `mall.909net.cn`（境内域名）与页脚 "Except China" 声明矛盾（合规风险）；且 index 页脚**漏写** "(Except China)"，两页声明不一致
7. `.workbuddy/` 26 个文件被 git 跟踪（含 reports/ 11MB 截图），`.gitignore` 漏了 `reports/` 与 `tmp/`

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
- **2026-08-28 18:17** 三页改版 v4 Editorial Material System（去玻璃化），改前备份 `*.bak-20260828`
- **2026-08-29 14:54 v4 已撤销，全站回退 v3**：从 `*.bak-20260828` 还原（已验证 ≡ git HEAD `a5ecca3`，仅行尾差异），回退前快照 `*.bak-20260829`。校验：`git status` 三页无差异；v3 特征复现（index 16× backdrop-filter / 3× 大圆角 / 10× radial-gradient；download 16×；404 10×）；HTML 闭合与 JS 元素 id 全部正常
