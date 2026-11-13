#!/usr/bin/env python3
"""يحوّل صفحة «صدى الجبل» إلى PDF بمقاس الجوال (صفحة طويلة واحدة بعرض 440px) بخطوط عربية مضمّنة.
python3 makepdf.py page.html issue.pdf [--max-pages 2]
ينزّل الخطوط من npm (@fontsource) ويحتاج playwright في node_modules بالمجلد الحالي ومتصفح /opt/pw-browsers/chromium."""
import os, re, sys, subprocess, tarfile, glob, argparse, tempfile
HERE=os.path.dirname(os.path.abspath(__file__)); FONTDIR=os.path.join(HERE,"fonts")
FAMILIES=[("Amiri","amiri",[400,700]),("Aref Ruqaa","aref-ruqaa",[700]),
          ("Noto Naskh Arabic","noto-naskh-arabic",[400,600,700]),("Reem Kufi","reem-kufi",[500,700])]
PRINT_CSS="""html,body{-webkit-print-color-adjust:exact;print-color-adjust:exact}
.btn{display:none!important}
.card:hover{transform:none}
.story,.match,.wx .c,table,.numday,.lead aside{break-inside:avoid}
.sec-title{break-after:avoid}"""
def ensure_fonts():
    os.makedirs(FONTDIR,exist_ok=True)
    for _,base,_ in FAMILIES:
        if glob.glob(os.path.join(FONTDIR,f"{base}-arabic-*.woff2")): continue
        subprocess.run(["npm","pack",f"@fontsource/{base}","--silent"],cwd=FONTDIR,check=True,capture_output=True)
        for tgz in glob.glob(os.path.join(FONTDIR,f"fontsource-{base}-*.tgz")):
            with tarfile.open(tgz) as t:
                for m in t.getmembers():
                    if re.search(r"-(arabic|latin)-\d+-normal\.woff2$",m.name):
                        m.name=os.path.basename(m.name); t.extract(m,FONTDIR,filter='data')
            os.remove(tgz)
def faces():
    out=[]
    for fam,base,ws in FAMILIES:
        for w in ws:
            for sub in ("arabic","latin"):
                f=os.path.join(FONTDIR,f"{base}-{sub}-{w}-normal.woff2")
                if os.path.exists(f): out.append(f"@font-face{{font-family:'{fam}';font-weight:{w};src:url('file://{f}') format('woff2')}}")
    return "\n".join(out)
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("html"); ap.add_argument("pdf"); ap.add_argument("--max-pages",type=int,default=2)
    a=ap.parse_args(); ensure_fonts()
    s=open(a.html,encoding="utf-8").read()
    s=re.sub(r'<link rel="(stylesheet|preconnect)" href="https://fonts\.[^>]*>',"",s)
    s=s.replace("<style>","<style>\n"+faces()+"\n"+PRINT_CSS+"</style>\n<style>",1)
    tmp=os.path.join(tempfile.mkdtemp(),"print.html"); open(tmp,"w",encoding="utf-8").write(s)
    js="""const {chromium}=require('playwright');(async()=>{
 const [tmp,out,maxp]=process.argv.slice(2);
 const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});
 const p=await b.newPage({viewport:{width:440,height:900}});
 await p.goto('file://'+tmp);await p.waitForTimeout(800);await p.evaluate(()=>document.fonts.ready);
 await p.emulateMedia({media:'screen'});let chosen=null;
 const H=await p.evaluate(()=>document.documentElement.scrollHeight);
 const buf=await p.pdf({width:'440px',height:(H+4)+'px',printBackground:true,margin:{top:'0',bottom:'0',left:'0',right:'0'}});
 const pages=(buf.toString('latin1').match(/\\/Type\\s*\\/Page[^s]/g)||[]).length; chosen={sc:1,pages,buf,H};
 require('fs').writeFileSync(out,chosen.buf);console.log(JSON.stringify({scale:chosen.sc,pages:chosen.pages}));await b.close();})();"""
    jsf=os.path.join(os.path.dirname(tmp),"pdf.js"); open(jsf,"w").write(js)
    env=dict(os.environ); env["NODE_PATH"]=env.get("NODE_PATH","")+":"+os.path.join(os.getcwd(),"node_modules")
    r=subprocess.run(["node",jsf,tmp,os.path.abspath(a.pdf),str(a.max_pages)],capture_output=True,text=True,env=env)
    if r.returncode: sys.exit(r.stderr)
    print(r.stdout.strip())
if __name__=="__main__": main()
