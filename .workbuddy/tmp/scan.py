# -*- coding: utf-8 -*-
import re, os, collections

PAGES = ['index.html','download.html','404.html']
os.chdir(r'D:/Github/webw')

local_files = set()
for root,dirs,fs in os.walk('.'):
    dirs[:] = [d for d in dirs if d not in ('.git','.workbuddy')]
    for f in fs:
        local_files.add(os.path.join(root,f).replace('\\','/').lstrip('./'))

print("="*70); print("1. 外链 / 内链 / 资源引用 扫描"); print("="*70)
all_ext, all_internal, all_targets = [], [], []
for p in PAGES:
    s = open(p, encoding='utf-8-sig').read()
    ext = re.findall(r'(?:href|src)="(https?://[^"]+)"', s)
    internal = re.findall(r'(?:href|src)="(?!https?:|#|mailto:|data:)([^"]+)"', s)
    tb = re.findall(r'<a\s[^>]*target="_blank"[^>]*>', s)
    noop = [t for t in tb if 'rel=' not in t]
    all_ext += [(p,u) for u in ext]; all_internal += [(p,u) for u in internal]
    all_targets += [(p,t) for t in noop]
    print(f"\n[{p}]  外链 {len(ext)} / 内链 {len(internal)} / target=_blank {len(tb)} (缺rel {len(noop)})")
    miss = [u for u in internal if u.split('?')[0] not in local_files]
    if miss: print("   [X] 本地缺失:", miss)

print("\n"+"="*70); print("2. target=_blank 缺 rel 明细"); print("="*70)
for p,t in all_targets:
    u = re.search(r'href="([^"]*)"', t)
    print(f"  {p:15s} -> {u.group(1) if u else '?'}")

print("\n"+"="*70); print("3. 外链域名汇总"); print("="*70)
doms = collections.Counter()
for p,u in all_ext:
    m = re.match(r'https?://([^/]+)', u)
    if m: doms[m.group(1)] += 1
for d,c in doms.most_common(): print(f"  {c:2d}x  {d}")

print("\n"+"="*70); print("4. 语义 / 无障碍 / head 检查"); print("="*70)
for p in PAGES:
    s = open(p, encoding='utf-8-sig').read()
    h1 = len(re.findall(r'<h1[\s>]', s)); img = re.findall(r'<img[^>]*>', s)
    noalt = [i for i in img if 'alt=' not in i]
    title = re.search(r'<title>(.*?)</title>', s)
    vps = re.findall(r'<meta name="viewport"[^>]*>', s)
    lang = re.search(r'<html[^>]*lang="([^"]*)"', s)
    print(f"\n[{p}]")
    print(f"  h1={h1}  img={len(img)}(缺alt {len(noalt)})")
    print(f"  title: {title.group(1)[:52] if title else '缺失'}")
    print(f"  lang: {lang.group(1) if lang else '缺失'}")
    print(f"  DOCTYPE: {'OK' if s.lstrip().lower().startswith('<!doctype') else '[X] 缺失'}")
    print(f"  viewport: {vps[0][:120] if vps else '[X] 缺失'}")
    for tag in ['aria-label','role=','<main','<header','<footer','<nav','<section','<article','<button']:
        print(f"    {tag:12s} x{len(re.findall(re.escape(tag), s))}")
