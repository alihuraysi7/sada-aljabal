#!/usr/bin/env python3
"""توقعات اليوم لمدينة جازان والمحافظات الجبلية من Open-Meteo.  python3 tools/weather.py YYYY-MM-DD
يطبع JSON: [{"name","elev","max","min","rain","code","label"}] — درجات مئوية، rain = أعلى احتمال مطر خلال اليوم (٪)."""
import json, sys, urllib.request
D = sys.argv[1]
C = [("جازان",16.889,42.551),("فيفاء",17.264,43.104),("الدائر",17.338,43.137),("العارضة",17.050,43.083),
     ("العيدابي",17.230,42.940),("هروب",17.380,43.200),("الريث",17.580,42.850)]
def label(c):
    if c <= 1: return "صحو غالباً"
    if c <= 3: return "غائم جزئياً"
    if c in (45, 48): return "ضباب"
    if 51 <= c <= 57: return "رذاذ"
    if 61 <= c <= 67: return "أمطار"
    if 80 <= c <= 82: return "زخات مطر"
    if c >= 95: return "عواصف رعدية"
    return "متقلب"
u = ("https://api.open-meteo.com/v1/forecast?latitude=" + ",".join(str(c[1]) for c in C) +
     "&longitude=" + ",".join(str(c[2]) for c in C) +
     "&daily=temperature_2m_max,temperature_2m_min,precipitation_probability_max,weather_code"
     f"&timezone=Asia%2FRiyadh&start_date={D}&end_date={D}")
r = json.load(urllib.request.urlopen(u, timeout=30)); r = r if isinstance(r, list) else [r]
out = []
for c, x in zip(C, r):
    d = x["daily"]
    out.append({"name": c[0], "elev": x.get("elevation"), "max": round(d["temperature_2m_max"][0]),
                "min": round(d["temperature_2m_min"][0]), "rain": d["precipitation_probability_max"][0],
                "code": d["weather_code"][0], "label": label(d["weather_code"][0])})
print(json.dumps(out, ensure_ascii=False))
