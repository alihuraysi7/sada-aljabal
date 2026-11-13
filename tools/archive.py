#!/usr/bin/env python3
"""يحفظ عدد اليوم في الأرشيف ويعيد بناء archive.html.  python3 tools/archive.py YYYY-MM-DD  (من جذر المستودع)
ينسخ index.html و cover.jpg و issue.pdf إلى issues/DATE/ ويصحح روابط الأصول المشتركة."""
import sys, os, re, shutil, glob, html
root=os.getcwd(); d=sys.argv[1]
dst=os.path.join(root,"issues",d); os.makedirs(dst,exist_ok=True)
s=open("index.html",encoding="utf-8").read()
for a in ("logo.png","manifest.webmanifest","icon-192.png","apple-touch-icon.png","archive.html","sw.js"):
    s=s.replace(f'"{a}"',f'"../../{a}"')
s=s.replace("navigator.serviceWorker.register('sw.js')","navigator.serviceWorker.register('../../sw.js')")
open(os.path.join(dst,"index.html"),"w",encoding="utf-8").write(s)
for f in ("cover.jpg","issue.pdf"):
    if os.path.exists(f): shutil.copy(f,os.path.join(dst,f))
rows=[]
for p in sorted(glob.glob("issues/*/index.html"),reverse=True):
    day=p.split("/")[1]; t=open(p,encoding="utf-8").read()
    m=re.search(r'<meta property="og:title" content="([^"]+)"',t); title=m.group(1) if m else day
    m=re.search(r'<meta name="description" content="([^"]+)"',t); desc=m.group(1) if m else ""
    rows.append(f'<a class="it" href="issues/{day}/"><img src="issues/{day}/cover.jpg" alt="" loading="lazy"><div><b>{html.escape(title)}</b><span>{html.escape(desc)}</span></div></a>')
page=f'''<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>أرشيف صدى الجبل</title><link rel="icon" href="logo.png"><link rel="manifest" href="manifest.webmanifest"><meta name="theme-color" content="#1f6b4a">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Aref+Ruqaa:wght@700&family=Noto+Naskh+Arabic:wght@400;700&family=Reem+Kufi:wght@500;700&display=swap">
<style>:root{{--paper:#fbf8f1;--ink:#1d1d27;--muted:#6a6a75;--line:#e6e0d2;color-scheme:light}}
body{{margin:0;background:var(--paper);color:var(--ink);font-family:'Noto Naskh Arabic',serif}}
header{{text-align:center;padding:22px 14px 12px;background:linear-gradient(180deg,#d9f0fb,var(--paper))}}
header img{{width:80px;height:80px;border-radius:50%}} h1{{font-family:'Aref Ruqaa',serif;font-size:44px;margin:4px 0}}
header p{{font-family:'Reem Kufi',sans-serif;margin:0;color:var(--muted)}} header a{{font-family:'Reem Kufi',sans-serif;color:#1f6b4a;font-weight:700}}
main{{max-width:760px;margin:0 auto;padding:12px 14px 30px;display:grid;gap:12px}}
.it{{display:grid;grid-template-columns:90px 1fr;gap:12px;align-items:center;background:#fff;border-radius:16px;padding:10px;text-decoration:none;color:inherit;box-shadow:0 2px 0 var(--line)}}
.it img{{width:90px;height:112px;object-fit:cover;border-radius:10px}} .it b{{display:block;font-size:17px;line-height:1.5}} .it span{{font-size:14px;color:var(--muted);line-height:1.6}}
</style></head><body><header><img src="logo.png" alt="شعار صدى الجبل"><h1>أرشيف صدى الجبل</h1><p>كل الأعداد السابقة · <a href="./">عدد اليوم</a></p></header>
<main>{"".join(rows)}</main><script>window.goatcounter={{path:function(){{return location.pathname}},no_onload:location.hostname!=="alihuraysi7.github.io"}};</script>
<script data-goatcounter="https://sada-aljabal.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>
</body></html>'''
open("archive.html","w",encoding="utf-8").write(page)
print(len(rows),"issues")
