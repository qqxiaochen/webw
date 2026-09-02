# -*- coding: utf-8 -*-
"""老旧内核兼容性扫描：统计现代特性在三个页面中的出现位置"""
import re, io, os, sys

FILES = ["index.html", "download.html", "404.html"]

# (分类, 名称, 正则, 说明)
RULES = [
 ("JS-API", "Element.closest()",        r"\.closest\(", "IE11 无"),
 ("JS-API", "classList.toggle(双参)",   r"classList\.toggle\([^)]*,", "IE11 忽略第二参"),
 ("JS-API", "window.scrollY",           r"window\.scrollY", "IE11 无(需 pageYOffset)"),
 ("JS-API", "addEventListener options", r"addEventListener\([^;]*\{(passive|once|capture)", "IE11 无 options"),
 ("JS-API", "IntersectionObserver",     r"IntersectionObserver", "IE11/旧内核无"),
 ("JS-API", "requestAnimationFrame",    r"requestAnimationFrame", "IE10+ OK"),
 ("JS-API", "e.key === 'Escape'",       r"e\.key\s*===\s*'Escape'", "IE11 为 'Esc'"),
 ("JS-API", "scrollTo({对象参数})",      r"scrollTo\(\{", "IE11 无 ScrollToOptions"),
 ("JS-API", "Promise (.then/.catch)",   r"\.(then|catch)\(", "IE11 无原生 Promise"),
 ("JS-API", "new Audio()",              r"new Audio\(", "IE9+ OK"),
 ("JS-API", "querySelectorAll",         r"querySelectorAll\(", "IE8+ OK"),
 ("JS-API", "getElementsByClassName",   r"getElementsByClassName\(", "IE9+ OK"),
 ("JS-API", "setAttribute",             r"setAttribute\(", "OK"),

 ("JS-SYNTAX", "let/const 声明",        r"(^|[^.\w])(let|const)\s+\w+\s*=", "ES6 语法错误"),
 ("JS-SYNTAX", "箭头函数 =>",           r"=>", "ES6 语法错误"),
 ("JS-SYNTAX", "模板字符串 `",          r"`", "ES6 语法错误"),
 ("JS-SYNTAX", "for...of",              r"for\s*\(\s*(var|let|const)\s+\w+\s+of\s", "ES6 语法错误"),
 ("JS-SYNTAX", "展开运算符 ...",        r"\.\.\.[a-zA-Z_\(]", "ES6 语法错误"),
 ("JS-SYNTAX", "对象简写/解构",         r"\{\s*\w+\s*\}\s*=", "ES6 语法错误"),

 ("CSS", "CSS 自定义属性 :root --x",    r"^\s*--[\w-]+\s*:", "IE11 完全不支持"),
 ("CSS", "var() 引用",                  r"var\(--", "IE11 完全不支持"),
 ("CSS", "backdrop-filter",             r"backdrop-filter", "IE11/FF<103 无"),
 ("CSS", "display:grid",                r"display\s*:\s*grid", "IE11 仅 -ms-grid"),
 ("CSS", "grid-template-columns",       r"grid-template-columns", "IE11 无"),
 ("CSS", "flex 容器 gap",               r"(^|[;{])\s*gap\s*:", "IE11 flexbox 无 gap"),
 ("CSS", "position:sticky",             r"position\s*:\s*sticky", "IE11 无"),
 ("CSS", "min()/max()",                 r":\s*(min|max)\(", "Chrome79/Safari13.1 起"),
 ("CSS", "clamp()",                     r"clamp\(", "Chrome79/Safari13.1 起"),
 ("CSS", "aspect-ratio",                r"aspect-ratio", "Chrome88/Safari15 起"),
 ("CSS", "@supports",                   r"@supports", "IE11 无(降级块被整体丢弃)"),
 ("CSS", "100svh",                      r"100svh", "Safari15.4/Chrome108 起"),
 ("CSS", "env(safe-area",               r"env\(safe-area", "IE11 无"),
 ("CSS", "filter:blur/brightness",      r"filter\s*:\s*(blur|brightness|saturate)", "IE11 无 CSS filter"),
 ("CSS", "mix-blend-mode",              r"mix-blend-mode", "IE11 无"),
 ("CSS", "mask-image",                  r"mask-image", "IE11 无"),
 ("CSS", "background-clip:text",        r"background-clip\s*:\s*text", "需 -webkit- 前缀"),
 ("CSS", "-webkit-text-fill-color",     r"-webkit-text-fill-color", "IE11 无(配合 clip 可致隐形字)"),
 ("CSS", "scroll-behavior:smooth",      r"scroll-behavior\s*:\s*smooth", "IE11 无"),
 ("CSS", "will-change",                 r"will-change", "IE11 无"),
 ("CSS", "prefers-reduced-motion",      r"prefers-reduced-motion", "IE11 无"),
 ("CSS", "@media (hover:none)",         r"@media\s*\(hover\s*:\s*none\)", "IE11 无"),
 ("CSS", "SVG feTurbulence 噪点",       r"feTurbulence", "IE11 渲染不稳定"),
 ("CSS", "::before/::after 伪元素",      r"::(before|after)", "IE8 不支持双冒号"),

 ("HTML", "HTML5 语义标签",             r"<(main|article|nav|header|footer|section)[\s>]", "IE9+ OK / IE8 需 shiv"),
 ("HTML", "target=_blank 无 rel",       r"target=\"_blank\"(?![\s\S]{0,80}rel=)", "安全/兼容"),
 ("HTML", "iframe loading=lazy",        r"loading=\"lazy\"", "Chrome77+ 才生效"),
 ("HTML", "SVG xlink:href",             r"xlink:href", "旧 WebKit 需要(已正确使用)"),
 ("HTML", "viewport-fit=cover",         r"viewport-fit=cover", "仅 iOS11+"),
 ("HTML", "外部字体/CDN 引用",           r"(fonts\.googleapis|cdn\.|unpkg|jsdelivr)", "第三方依赖"),
]

def scan(path):
    src = io.open(path, encoding="utf-8-sig").read()
    lines = src.split("\n")
    out = {}
    for cat, name, pat, note in RULES:
        hits = []
        for i, ln in enumerate(lines, 1):
            if re.search(pat, ln):
                hits.append(i)
        if hits:
            out.setdefault(cat, []).append((name, len(hits), hits[:6], note))
    return out, len(lines)

summary = {}
for f in FILES:
    res, nlines = scan(f)
    print("=" * 68)
    print("%s  (%d 行)" % (f, nlines))
    print("=" * 68)
    for cat in ["JS-SYNTAX", "JS-API", "CSS", "HTML"]:
        if cat not in res:
            continue
        print("  [%s]" % cat)
        for name, cnt, hits, note in res[cat]:
            summary[(cat, name)] = summary.get((cat, name), 0) + cnt
            print("    %-32s x%-4d 行:%s   // %s" % (name, cnt, ",".join(map(str, hits)), note))
    print()

print("=" * 68)
print("三页合计 TOP 风险项")
print("=" * 68)
for (cat, name), cnt in sorted(summary.items(), key=lambda x: -x[1]):
    print("  %-28s %-14s x%d" % (cat, name, cnt))
