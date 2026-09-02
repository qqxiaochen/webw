# -*- coding: utf-8 -*-
import re, os
os.chdir(r'D:/Github/webw')
s = open('404.html', encoding='utf-8-sig').read()
i = s.find('<body')
body = s[i:]
body = re.sub(r'<svg class="wrap-bg".*?</svg>', '<!-- [SVG 背景装饰 已折叠，约 8KB，含 5 个 linearGradient + 装饰图形] -->', body, flags=re.S)
print("=== 404.html body 结构（SVG 已折叠）===")
print(f"总长 {len(body):,} 字符\n")
print(body[:4200])
