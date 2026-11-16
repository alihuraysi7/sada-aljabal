#!/usr/bin/env python3
"""يملأ قسم الطقس في index.html وخانة الطقس في cover.json من مخرجات tools/weather.py.
python3 tools/weather.py YYYY-MM-DD > /tmp/wx.json && python3 tools/fillweather.py /tmp/wx.json  (من جذر المستودع)"""
import json, re, sys
W = json.load(open(sys.argv[1], encoding="utf-8"))
ar = lambda x: str(x).translate(str.maketrans("0123456789", "٠١٢٣٤٥٦٧٨٩"))
SUN = '<svg viewBox="0 0 64 64" aria-hidden="true"><circle cx="32" cy="32" r="13" fill="#fff3b0"/><g stroke="#fff3b0" stroke-width="4" stroke-linecap="round"><path d="M32 6v8M32 50v8M6 32h8M50 32h8M13 13l6 6M45 45l6 6M13 51l6-6M45 19l6-6"/></g></svg>'
CLOUD = '<svg viewBox="0 0 64 64" aria-hidden="true"><circle cx="22" cy="20" r="9" fill="#ffd34d"/><path d="M16 42a11 11 0 0 1 3-21 14 14 0 0 1 27 4 9 9 0 0 1-1 17Z" fill="#fff"/></svg>'
RAIN = '<svg viewBox="0 0 64 64" aria-hidden="true"><circle cx="22" cy="20" r="9" fill="#ffd34d"/><path d="M16 42a11 11 0 0 1 3-21 14 14 0 0 1 27 4 9 9 0 0 1-1 17Z" fill="#fff"/><g stroke="#cfe9ff" stroke-width="3.4" stroke-linecap="round"><path d="M22 48l-3 7M32 48l-3 7M42 48l-3 7"/></g></svg>'
STORM = '<svg viewBox="0 0 64 64" aria-hidden="true"><path d="M14 38a11 11 0 0 1 3-21 14 14 0 0 1 27 4 9 9 0 0 1-1 17Z" fill="#fff"/><path d="M32 38l-5 9h6l-4 9" stroke="#ffd34d" stroke-width="3.4" fill="none" stroke-linejoin="round"/><g stroke="#cfe9ff" stroke-width="3.2" stroke-linecap="round"><path d="M20 44l-3 7M44 44l-3 7"/></g></svg>'
def look(w):
    c, p = w["code"], w["rain"] or 0
    if c >= 95: return "rainy", STORM
    if c >= 51 or p >= 50: return "rainy", RAIN
    if c <= 1 and p < 40: return "sunny", SUN
    return "mild", CLOUD
FULL = {"الدائر": "الدائر بني مالك"}
j = W[0]; cls, ic = look(j)
html = f'''<div class="wx">
    <div class="c {cls} wide">
      <div><div class="city">مدينة جازان</div><span class="alt">الساحل</span><div class="t num">{ar(j["max"])}° <small>/ {ar(j["min"])}°</small></div><span class="rain">{j["label"]} · مطر {ar(j["rain"])}٪</span></div>
      {ic}
    </div>
'''
for w in W[1:]:
    cls, ic = look(w)
    html += f'''    <div class="c {cls}">
      <div class="city">{FULL.get(w["name"], w["name"])}</div>
      {ic}
      <div class="t num">{ar(w["max"])}° <small>/ {ar(w["min"])}°</small></div>
      <span class="rain">مطر {ar(w["rain"])}٪</span>
    </div>
'''
html += '  </div>'
s = open("index.html", encoding="utf-8").read()
i = s.index('<div class="wx">'); k = s.index('\n  <p class="wx-note">', i)
s = s[:i] + html + s[k:]
cold = min(W[1:], key=lambda w: w["max"]); warm = max(W[1:], key=lambda w: w["max"])
wet = sorted(W[1:], key=lambda w: -(w["rain"] or 0))[:3]
note = (f'أبرد المحافظات اليوم {FULL.get(cold["name"], cold["name"])} ({ar(cold["max"])}°/{ar(cold["min"])}°)، وأدفؤها {FULL.get(warm["name"], warm["name"])} ({ar(warm["max"])}°). '
        f'أعلى فرص المطر في {"، ".join(FULL.get(w["name"], w["name"]) for w in wet)} ({ar(min(w["rain"] for w in wet))}–{ar(max(w["rain"] for w in wet))}٪). القراءات تقريبية لمراكز المحافظات، والقمم أبرد منها.')
s = re.sub(r'<p class="wx-note">.*?</p>', f'<p class="wx-note">{note}</p>', s, count=1, flags=re.S)
s = re.sub(r'(<div class="src">)(التنبيه:|آخر تنبيه:|التوقعات:)', r'\1التوقعات: <a href="https://open-meteo.com" target="_blank" rel="noopener">Open-Meteo</a> · \2', s, count=1) if 'Open-Meteo' not in s else s
open("index.html", "w", encoding="utf-8").write(s)
cv = json.load(open("cover.json", encoding="utf-8"))
cv["weather"] = [[w["name"], f'{ar(w["max"])}°/{ar(w["min"])}°'] for w in W]
open("cover.json", "w", encoding="utf-8").write(json.dumps(cv, ensure_ascii=False, indent=1) + "\n")
print("ok")
