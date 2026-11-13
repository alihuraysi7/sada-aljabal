#!/usr/bin/env python3
"""مواقيت الصلاة (أم القرى) لجازان والمحافظات الجبلية. python3 prayer.py YYYY-MM-DD  ← يطبع JSON
يتطلب: pip install --break-system-packages adhanpy"""
import sys, json
from datetime import date
from zoneinfo import ZoneInfo
from adhanpy.PrayerTimes import PrayerTimes
from adhanpy.calculation.CalculationMethod import CalculationMethod
PLACES=[("جازان",16.889,42.551),("فيفاء",17.27,43.10),("الدائر",17.311,43.127),("العارضة",17.05,43.07),
        ("العيدابي",17.24,42.94),("هروب",17.45,43.05),("الريث",17.6025,42.8567)]
d=date.fromisoformat(sys.argv[1]) if len(sys.argv)>1 else date.today()
tz=ZoneInfo("Asia/Riyadh"); out=[]
for n,la,lo in PLACES:
    p=PrayerTimes((la,lo),d,calculation_method=CalculationMethod.UMM_AL_QURA,time_zone=tz)
    out.append({"name":n,"times":[t.strftime('%H:%M') for t in (p.fajr,p.sunrise,p.dhuhr,p.asr,p.maghrib,p.isha)]})
print(json.dumps(out,ensure_ascii=False))
