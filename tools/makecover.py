#!/usr/bin/env python3
"""يصنع صورة غلاف «صدى الجبل» للمشاركة في واتساب (1080x1350).
python3 makecover.py index.html cover.json cover.png
cover.json: {"issue":"العدد الأول","date":"...","hijri":"...","headline":"...",
 "items":[{"tag":"العالم","color":"#2f6fde","text":"..."}, ...  (5 عناصر)],
 "weather":[["جازان","٣١°/٢٨°"],["فيفاء","٢٩°/٢٣°"], ... جازان + المحافظات الجبلية الست]}
يأخذ الشعار ورسم الخبر الرئيسي (svg.logo و svg.art) من index.html، والخطوط من tools/fonts (ينشئها makepdf.py)."""
import sys, os, re, json, subprocess, tempfile
HERE=os.path.dirname(os.path.abspath(__file__)); F=os.path.join(HERE,"fonts")
html,cj,out=sys.argv[1:4]
s=open(html,encoding="utf-8").read(); d=json.load(open(cj,encoding="utf-8"))
logo=re.search(r'<svg class="logo".*?</svg>',s,re.S).group(0)
art=re.search(r'<svg class="art".*?</svg>',s,re.S).group(0)
def ff(fam,file,w): 
    p=os.path.join(F,file); return f"@font-face{{font-family:'{fam}';font-weight:{w};src:url('file://{p}')}}" if os.path.exists(p) else ""
fonts="".join([ff("Aref Ruqaa","aref-ruqaa-arabic-700-normal.woff2",700),ff("Amiri","amiri-arabic-700-normal.woff2",700),
  ff("Reem Kufi","reem-kufi-arabic-700-normal.woff2",700),ff("Reem Kufi","reem-kufi-arabic-500-normal.woff2",500),
  ff("Noto Naskh Arabic","noto-naskh-arabic-arabic-600-normal.woff2",600)])
items="".join(f'<li><span class="t" style="background:{i["color"]}">{i["tag"]}</span><span>{i["text"]}</span></li>' for i in d["items"])
wx="".join(f'<span><b>{c}</b> {t}</span>' for c,t in d["weather"])
page=f"""<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><style>{fonts}
*{{box-sizing:border-box}}body{{margin:0;width:1080px;height:1350px;background:#fbf8f1;font-family:'Noto Naskh Arabic',serif;color:#1d1d27;overflow:hidden}}
.top{{height:300px;background:linear-gradient(180deg,#d9f0fb,#eaf6fc 60%,#fbf8f1);position:relative;display:flex;align-items:center;justify-content:center;gap:28px;padding-bottom:40px}}
.top svg.logo{{width:190px;height:190px}}
.name{{font-family:'Aref Ruqaa';font-size:130px;line-height:1}}
.slo{{display:inline-block;margin-top:10px;font-family:'Reem Kufi';font-weight:700;font-size:30px;color:#fff;background:#1f6b4a;border-radius:99px;padding:4px 26px}}
.hills{{position:absolute;left:0;right:0;bottom:0;width:100%;height:70px}}
.bar{{display:flex;justify-content:center;gap:16px;margin:4px 40px 0;font-family:'Reem Kufi';font-size:28px}}
.bar span{{background:#fff;border:2px solid #e6e0d2;border-radius:16px;padding:6px 20px}} .bar .y{{background:#f5b301;border-color:#f5b301;font-weight:700}}
.lead{{margin:18px 40px 0;max-height:300px;background:#fff;border-radius:28px;overflow:hidden;border-top:10px solid #e5533d;display:grid;grid-template-columns:1fr 1fr}}
.lead svg{{width:100%;height:100%;display:block}}
.lead h1{{font-family:'Amiri';font-weight:700;font-size:44px;line-height:1.35;margin:0;padding:24px 26px;display:flex;align-items:center}}
ul{{list-style:none;margin:18px 40px 0;padding:0;display:grid;gap:11px}}
li{{display:flex;gap:16px;align-items:center;background:#fff;border-radius:20px;padding:10px 18px;font-size:29px;line-height:1.4;font-weight:600}}
.t{{flex:none;color:#fff;font-family:'Reem Kufi';font-weight:700;font-size:24px;border-radius:12px;padding:4px 14px;min-width:150px;text-align:center}}
.wx{{margin:16px 40px 0;display:flex;flex-wrap:wrap;gap:10px;justify-content:center;font-family:'Reem Kufi';font-size:24px}}
.wx span{{background:linear-gradient(160deg,#4aa8e8,#2f62c9);color:#fff;border-radius:14px;padding:6px 14px}}
.cta{{position:absolute;bottom:0;left:0;right:0;height:84px;background:#1f9d55;color:#fff;font-family:'Reem Kufi';font-weight:700;font-size:34px;display:flex;align-items:center;justify-content:center}}
</style></head><body>
<div class="top">{logo}<div style="text-align:center"><div class="name">صدى الجبل</div><span class="slo">كن جزءاً من العالم</span></div>
<svg class="hills" viewBox="0 0 400 70" preserveAspectRatio="none"><path d="M0 70 V44 L40 26 L70 40 L110 14 L150 38 L190 22 L230 42 L270 18 L310 36 L350 20 L400 40 V70 Z" fill="#9dd6b4"/><path d="M0 70 V54 L50 40 L95 52 L140 34 L185 50 L235 36 L280 52 L330 38 L400 54 V70 Z" fill="#4fb07a"/><path d="M0 70 V62 C80 56 160 58 240 62 C300 65 350 60 400 62 V70 Z" fill="#fbf8f1"/></svg></div>
<div class="bar"><span class="y">{d['date']}</span><span>{d['hijri']}</span><span>{d['issue']}</span></div>
<div class="lead"><h1>{d['headline']}</h1>{art}</div>
<ul>{items}</ul><div class="wx">{wx}</div>
<div class="cta">اقرأ العدد كاملاً من الرابط في الرسالة</div></body></html>"""
tmp=os.path.join(tempfile.mkdtemp(),"cover.html"); open(tmp,"w",encoding="utf-8").write(page)
js="""const {chromium}=require('playwright');(async()=>{const [t,o]=process.argv.slice(2);
const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});const p=await b.newPage({viewport:{width:1080,height:1350}});
await p.goto('file://'+t);await p.waitForTimeout(600);await p.evaluate(()=>document.fonts.ready);
const ov=await p.evaluate(()=>[...document.querySelectorAll('li,h1')].filter(e=>e.scrollHeight>e.clientHeight+2).length+(document.querySelector('.wx').getBoundingClientRect().bottom>document.querySelector('.cta').getBoundingClientRect().top-6?100:0));
await p.screenshot({path:o});console.log(JSON.stringify({overflow:ov}));await b.close();})();"""
jsf=os.path.join(os.path.dirname(tmp),"c.js"); open(jsf,"w").write(js)
env=dict(os.environ); env["NODE_PATH"]=":".join(x for x in [os.environ.get("NODE_PATH",""),os.path.join(os.getcwd(),"node_modules"),os.path.expanduser("~/node_modules"),"/home/claude/node_modules"] if x)
r=subprocess.run(["node",jsf,tmp,os.path.abspath(out)],capture_output=True,text=True,env=env)
if r.returncode: sys.exit(r.stderr)
print(r.stdout.strip())
