# -*- coding: utf-8 -*-
import re, os
os.chdir(r'D:/Github/webw')
def css(p):
    s = open(p, encoding='utf-8-sig').read()
    m = re.search(r'<style[^>]*>(.*?)</style>', s, re.S)
    return m.group(1) if m else ''
a, b, c = css('index.html'), css('download.html'), css('404.html')
def rules(t):
    # 提取 "选择器 { 声明 }" 的规范化集合
    out = {}
    for m in re.finditer(r'([^{}]+)\{([^{}]*)\}', t):
        sel = ' '.join(m.group(1).split())
        if sel.startswith('@'): continue
        out.setdefault(sel, ' '.join(m.group(2).split()))
    return out
ra, rb = rules(a), rules(b)
common = set(ra) & set(rb)
same_decl = [s for s in common if ra[s] == rb[s]]
ca = sum(len(v) for v in ra.values()); cc = sum(len(ra[s]) for s in common)
print("="*66)
print("CSS 重复度分析（index vs download）")
print("="*66)
print(f"index    规则 {len(ra):3d} 条 / {len(a):6,d} 字符")
print(f"download 规则 {len(rb):3d} 条 / {len(b):6,d} 字符")
print(f"404      规则 {len(rules(c)):3d} 条 / {len(c):6,d} 字符")
print(f"\n选择器同名: {len(common)} 条")
print(f"选择器+声明完全相同: {len(same_decl)} 条")
print(f"download 中重复声明字符: {cc:,} / {sum(len(v) for v in rb.values()):,} = {cc/max(1,sum(len(v) for v in rb.values()))*100:.1f}%")
print(f"index 中重复声明字符: {cc:,} / {ca:,} = {cc/max(1,ca)*100:.1f}%")
print("\n=== download 独有规则 ===")
for s in sorted(set(rb)-set(ra)): print("  ", s[:80])
