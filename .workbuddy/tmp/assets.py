# -*- coding: utf-8 -*-
import os, hashlib, re
os.chdir(r'D:/Github/webw')
PAGES = ['index.html','download.html','404.html']
pages = {p: open(p, encoding='utf-8-sig').read() for p in PAGES}

print("="*72); print("A. down/ 下载包"); print("="*72)
tot = 0
for root, dirs, fs in os.walk('down'):
    for f in sorted(fs):
        p = (root+'/'+f).replace('\\','/')
        sz = os.path.getsize(p)
        ref = [k for k,v in pages.items() if f in v]
        h = hashlib.md5(open(p,'rb').read()).hexdigest()[:10] if sz < 40*1024*1024 else '-'
        tot += sz
        print(f"  {p:36s} {sz/1048576:6.1f}MB  md5:{h}  {'✓ '+','.join(ref) if ref else '✗ 死文件'}")
print(f"  合计 {tot/1048576:.1f} MB")
dead = 0
for root, dirs, fs in os.walk('down'):
    for f in fs:
        p = (root+'/'+f).replace('\\','/')
        if not any(f in v for v in pages.values()): dead += os.path.getsize(p)
print(f"  其中死文件 {dead/1048576:.1f} MB")

print("\n"+"="*72); print("B. static/ 资源引用"); print("="*72)
for root, dirs, fs in os.walk('static'):
    for f in sorted(fs):
        p = (root+'/'+f).replace('\\','/')
        sz = os.path.getsize(p)
        n = sum(v.count(f) for v in pages.values())
        print(f"  {p:34s} {sz/1024:8.1f}KB  引用 {n} 次 {'✗ 零引用' if n==0 else ''}")
