import os, json
from guides_data import G
LP='<div class="rows"><a class="row" href="/edto/" data-a="pilot student dispatcher engineer hobbyist"><span class="n">EDTO from scratch</span><span class="d">Why EDTO exists, how it is approved, how diversion circles and equal time points work, and polar routes.</span><span class="t">Learning path</span></a><a class="row" href="/oceanic/" data-a="pilot student dispatcher engineer hobbyist"><span class="n">Oceanic and North Atlantic flying</span><span class="d">Organised tracks, the TMI number, NAT high level airspace, clearances and contingencies.</span><span class="t">Learning path</span></a></div>'
GL='<div class="rows">'+"".join('<a class="row" href="/guides/%s/" data-a="pilot student dispatcher engineer hobbyist"><span class="n">%s</span><span class="d">%s</span><span class="t">Guide</span></a>'%(g["slug"],g["title"],g["desc"]) for g in G)+'</div>'
S = "https://flightplanpro.pages.dev"
GSC = "JARo9iKbe9vjR2gKSiOTNG7SJquxuAxdTHmrpQ-QSsc"
D = "2026-10-15"
O = "/mnt/user-data/outputs/flightplanpro"

def w(p, c):
    p = os.path.join(O, p.lstrip("/")); os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8").write(c)

def page(path, title, desc, body, ld=None):
    url = S + path
    ld = f'<script type="application/ld+json">{json.dumps(ld)}</script>' if ld else ""
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title><meta name="description" content="{desc}">
<meta name="google-site-verification" content="{GSC}">
<link rel="canonical" href="{url}"><meta name="robots" content="index,follow,max-snippet:-1,max-image-preview:large">
<meta property="og:type" content="website"><meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><meta property="og:url" content="{url}"><meta property="og:site_name" content="FlightPlanPro">
<meta name="twitter:card" content="summary"><meta name="theme-color" content="#0f2a3d">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='6' fill='%230f2a3d'/%3E%3Cpath d='M5 24 27 8' stroke='%23e0407f' stroke-width='3'/%3E%3C/svg%3E">
<link rel="stylesheet" href="/assets/style.css">{ld}</head><body>
<a class="skip" href="#m">Skip to content</a>
<header><div class="wrap bar"><a class="logo" href="/">FlightPlan<b>Pro</b></a>
<nav aria-label="Main"><a href="/metar/">METAR</a><a href="/taf/">TAF</a><a href="/tools/crew-duty-limits/">Crew duty</a><a href="/guides/">Guides</a><a href="/tools/">All tools</a><a class="cta" href="/flight-planner/">Plan a flight</a><a href="/about/">About</a></nav></div></header>
<main id="m" class="wrap">{body}</main>
<footer><div class="wrap"><p><b>Not for operational use.</b> FlightPlanPro tools are for training and planning reference only. Always verify against your aircraft's approved manual (AFM/POH), current weather and NOTAMs, and applicable regulations.</p>
<p><a href="/tools/">All tools</a> · <a href="/about/">About</a> · <a href="/data-sources/">Data and disclaimer</a> · <a href="/privacy/">Privacy</a> · <a href="/site-map/">Site map</a> · &copy; 2026 FlightPlanPro</p></div></footer></body></html>'''

def R(*a): return "R([" + ",".join(f"['{x}',{y}]" for x, y in a) + "])"
HM = "Math.floor(t)+' h '+f((t%1)*60)+' min'"

T = [
 dict(slug="crosswind-calculator", name="Crosswind & Headwind Calculator", kw="Crosswind Calculator",
  desc="Free crosswind and headwind component calculator. Enter runway heading, wind direction and speed to get instant wind components.",
  intro="Enter the runway heading and the wind to see the headwind (or tailwind) and crosswind component for takeoff and landing.",
  fields=[("rwy","Runway heading (°)",270),("wd","Wind direction, from (°)",300),("ws","Wind speed (kt)",15)],
  js="const a=(v.wd-v.rwy)*Math.PI/180,h=v.ws*Math.cos(a),x=v.ws*Math.sin(a);return "+R(("Headwind / tailwind","f(Math.abs(h))+' kt '+(h>=0?'headwind':'TAILWIND')"),("Crosswind","f(Math.abs(x))+' kt from the '+(x>=0?'right':'left')")),
  formula="Headwind = wind speed × cos(θ). Crosswind = wind speed × sin(θ), where θ is the angle between wind direction and runway heading. A negative headwind value is a tailwind.",
  faq=("How do I calculate crosswind?","Multiply the wind speed by the sine of the angle between the wind direction and the runway heading. A 20 kt wind at 30° off the runway gives about 10 kt of crosswind.")),
 dict(slug="wind-triangle-calculator", name="Wind Triangle Calculator", kw="Wind Triangle Calculator",
  desc="Free wind triangle calculator for pilots. Get true heading, wind correction angle and ground speed from TAS, course and wind.",
  intro="Solve the wind triangle: enter true airspeed, desired true course and the wind to get the heading to fly and your ground speed.",
  fields=[("tas","True airspeed (kt)",110),("crs","True course (°)",90),("wd","Wind direction, from (°)",150),("ws","Wind speed (kt)",20)],
  js="const a=(v.wd-v.crs)*Math.PI/180,s=v.ws/v.tas*Math.sin(a);if(Math.abs(s)>1)return R([['Error','Wind too strong for this airspeed']]);const k=Math.asin(s),g=v.tas*Math.cos(k)-v.ws*Math.cos(a),h=(v.crs+k*180/Math.PI+360)%360;return "+R(("True heading","f(h)+'°'"),("Wind correction angle","f(k*180/Math.PI,1)+'° '+(k>=0?'right':'left')"),("Ground speed","f(g)+' kt'")),
  formula="WCA = asin( (wind speed ÷ TAS) × sin(wind direction − course) ). Ground speed = TAS × cos(WCA) − wind speed × cos(wind direction − course). Heading = course + WCA. Convert to magnetic by applying variation.",
  faq=("What is the wind correction angle?","It is the angle you steer into the wind so the aircraft tracks the desired course over the ground. Positive means correct to the right.")),
 dict(slug="fuel-planning-calculator", name="Flight Fuel Planning Calculator", kw="Fuel Planning Calculator",
  desc="Free flight fuel planning calculator: trip, contingency, alternate, final reserve and block fuel from distance, speed and burn rate.",
  intro="Estimate block fuel from distance, ground speed and fuel burn. Use the same fuel unit (kg, lb or litres) for burn rate, alternate and taxi fuel.",
  fields=[("dist","Trip distance (NM)",300),("gs","Ground speed (kt)",120),("burn","Fuel burn per hour",40),("cont","Contingency (% of trip)",5),("alt","Alternate fuel",25),("res","Final reserve (min)",30),("taxi","Taxi fuel",3)],
  js="const t=v.dist/v.gs,tr=t*v.burn,c=tr*v.cont/100,rs=v.res/60*v.burn,b=v.taxi+tr+c+v.alt+rs;return "+R(("Trip time",HM),("Trip fuel","f(tr,1)"),("Contingency","f(c,1)"),("Final reserve","f(rs,1)"),("Block fuel","f(b,1)")),
  formula="Block fuel = taxi + trip + contingency + alternate + final reserve (+ any extra). Trip fuel = (distance ÷ ground speed) × burn rate. Contingency and reserve minima depend on your regulator and operation.",
  faq=("What is included in block fuel?","Taxi fuel, trip fuel, contingency fuel, alternate fuel, final reserve fuel and any extra fuel the commander decides to carry.")),
 dict(slug="density-altitude-calculator", name="Density Altitude Calculator", kw="Density Altitude Calculator",
  desc="Free density altitude calculator. Get pressure altitude, ISA deviation and density altitude from elevation, QNH and temperature.",
  intro="Enter airfield elevation, QNH and outside air temperature to see how hot, high and humid conditions affect performance.",
  fields=[("elev","Airfield elevation (ft)",500),("qnh","QNH (hPa)",1013),("oat","Outside air temp (°C)",35)],
  js="const p=v.elev+(1013.25-v.qnh)*27,i=15-1.98*p/1000,d=p+120*(v.oat-i);return "+R(("Pressure altitude","f(p)+' ft'"),("ISA temperature","f(i,1)+' °C'"),("ISA deviation","f(v.oat-i,1)+' °C'"),("Density altitude","f(d)+' ft'")),
  formula="Pressure altitude ≈ elevation + (1013.25 − QNH) × 27 ft. ISA temp = 15 − 1.98 °C per 1,000 ft. Density altitude ≈ pressure altitude + 120 × (OAT − ISA). This is the common rule-of-thumb approximation.",
  faq=("Why does density altitude matter?","Higher density altitude means thinner air: longer takeoff roll, weaker climb and higher true airspeed for the same indicated airspeed.")),
 dict(slug="great-circle-distance-calculator", name="Great-Circle Distance & Course Calculator", kw="Great Circle Distance Calculator",
  desc="Free great-circle distance calculator. Get distance in nautical miles, initial true course and flight time between two coordinates.",
  intro="Enter two points in decimal degrees (north and east positive) to get the shortest-path distance, initial course and time. Defaults: Karachi to Dubai.",
  fields=[("lat1","Departure latitude",24.9065),("lon1","Departure longitude",67.1608),("lat2","Arrival latitude",25.2528),("lon2","Arrival longitude",55.3644),("gs","Ground speed (kt)",450)],
  js="const r=Math.PI/180,p=v.lat1*r,q=v.lat2*r,l=(v.lon2-v.lon1)*r,h=Math.sin((q-p)/2)**2+Math.cos(p)*Math.cos(q)*Math.sin(l/2)**2,d=2*3440.065*Math.asin(Math.sqrt(h)),b=(Math.atan2(Math.sin(l)*Math.cos(q),Math.cos(p)*Math.sin(q)-Math.sin(p)*Math.cos(q)*Math.cos(l))/r+360)%360,t=v.gs>0?d/v.gs:0;return "+R(("Distance","f(d)+' NM ('+f(d*1.852)+' km)'"),("Initial true course","f(b)+'°'"),("Time at ground speed",HM)),
  formula="Haversine: a = sin²(Δφ/2) + cos φ1 · cos φ2 · sin²(Δλ/2); distance = 2R·asin(√a) with R = 3,440.065 NM. Initial course = atan2(sin Δλ · cos φ2, cos φ1 · sin φ2 − sin φ1 · cos φ2 · cos Δλ).",
  faq=("Why is the great-circle route shorter?","On a sphere the shortest path between two points is an arc of a great circle, which looks curved on a flat map.")),
 dict(slug="top-of-descent-calculator", name="Top of Descent Calculator", kw="Top of Descent Calculator",
  desc="Free top of descent calculator using the 3:1 rule. Find when to start descent and the descent rate for a 3° path.",
  intro="Use the 3-to-1 rule to find where to begin your descent and the rate of descent needed to hold a 3° path.",
  fields=[("alt","Current altitude (ft)",35000),("tgt","Target altitude (ft)",3000),("gs","Ground speed (kt)",420)],
  js="const l=v.alt-v.tgt,d=l/1000*3;return "+R(("Altitude to lose","f(l)+' ft'"),("Start descent","f(d,1)+' NM before the fix'"),("Descent rate (3°)","f(v.gs*5)+' ft/min'")),
  formula="Distance (NM) = altitude to lose (in thousands of feet) × 3. Rate of descent ≈ ground speed × 5 ft/min for a 3° path. Add distance to slow down if needed.",
  faq=("What is the 3:1 rule?","Plan 3 nautical miles of track for every 1,000 ft of altitude to lose, which gives roughly a 3° descent path.")),
dict(slug="mach-tas-calculator", name="Mach and True Airspeed Calculator", kw="Mach to TAS Calculator",
  desc="Free Mach to true airspeed calculator. Enter Mach number and static air temperature to get TAS and the speed of sound.",
  intro="Convert a Mach number into true airspeed using the outside static air temperature. For example, Mach 0.78 at -56.5 °C gives about 447 knots.",
  fields=[("m","Mach number",0.78),("sat","Static air temperature (°C)",-56.5)],
  js="if(v.sat+273.15<=0)return R([['Error','Temperature is below absolute zero']]);const a=38.967854*Math.sqrt(v.sat+273.15),t=v.m*a;return "+R(("Speed of sound","f(a)+' kt'"),("True airspeed","f(t)+' kt'"),("True airspeed (km/h)","f(t*1.852)+' km/h'")),
  formula="Speed of sound a = 38.9679 × √T knots, where T is the static air temperature in kelvin (°C + 273.15). True airspeed = Mach number × a. Use static air temperature (SAT), not total air temperature (TAT), which is higher because of ram rise.",
  faq=("What is the speed of sound at cruise altitude?","In standard conditions at 36,000 ft the temperature is about -56.5 °C and the speed of sound is about 573 knots, so Mach 0.78 is a true airspeed of about 447 knots.")),
dict(slug="equal-time-point-calculator", name="Equal Time Point (ETP) Calculator", kw="Equal Time Point Calculator",
  desc="Free equal time point calculator. Enter the distance between two airports, the diversion speed and the wind to find the ETP.",
  intro="Find the point where continuing and returning take the same time. Enter the distance between the two airports, your diversion speed and the wind along the route.",
  fields=[("d","Distance between the two airports (NM)",3000),("tas","Diversion speed, TAS (kt)",400),("w","Wind component from A to B (kt, + tailwind)",0)],
  js="const o=v.tas+v.w,h=v.tas-v.w;if(o<=0||h<=0)return R([['Error','Ground speed must stay above zero']]);const x=v.d*h/(o+h);return "+R(("Distance from airport A","f(x)+' NM'"),("Distance from airport B","f(v.d-x)+' NM'"),("Time from the ETP to either airport","f(x/h*60)+' min'")),
  formula="ETP distance from A = D × H ÷ (O + H), where D is the distance between the airports, O is the ground speed when continuing to B (speed + tailwind) and H is the ground speed when returning to A (speed − tailwind). The time to either airport from the ETP is then equal.",
  faq=("Why is the ETP not at the midpoint?","Wind along the route makes one direction slower than the other, so the point where the times are equal moves toward the airport that is harder to reach.")),
dict(slug="nat-tmi-calculator", name="NAT Track Message Number (TMI) Calculator", kw="NAT TMI Calculator",
  desc="Free NAT TMI calculator. Enter a date to get the three-digit Track Message Identification number based on the day of the year.",
  intro="The TMI of a NAT Track Message is based on the Julian calendar date for which the track system is effective. Enter a date to get the day-of-year number, and always confirm it against the date in the message itself.",
  fields=[("y","Year",2026),("m","Month (1-12)",10),("d","Day of month",22)],
  js="const k=new Date(Date.UTC(v.y,v.m-1,v.d));if(v.y<2000||k.getUTCMonth()!=v.m-1||k.getUTCDate()!=v.d)return R([['Error','Enter a valid date']]);const t=Math.round((k-Date.UTC(v.y,0,0))/864e5);return "+R(("TMI (day of the year)","String(t).padStart(3,'0')"),("If the message is re-issued","String(t).padStart(3,'0')+'A'")),
  formula="TMI = the day number of the year, written with three digits. 16 January is 016 and 5 March is 064 in a normal year. A letter is added when the message is re-issued, for example 032A.",
  faq=("What is the TMI used for?","Crews and controllers use it to confirm they are working from the same NAT Track Message, and it is included in abbreviated oceanic clearance readbacks.")),
]

JS = """<script>const f=(n,d=0)=>n.toFixed(d),R=a=>a.map(x=>'<div class="r"><span>'+x[0]+'</span><b>'+x[1]+'</b></div>').join('');
const F=document.getElementById('f'),O=document.getElementById('o');
function calc(v){%s}
function c(){const v={};[...F.elements].forEach(e=>{if(e.id)v[e.id]=parseFloat(e.value)});const mi=[...F.elements].filter(e=>e.id&&isNaN(parseFloat(e.value))).map(e=>e.parentElement.childNodes[0].textContent.trim());O.innerHTML=mi.length?'<p class="err">Missing information: '+mi.join(', ')+'. Enter the data to see results.</p>':calc(v)}
F.addEventListener('input',c);c()</script>"""

urls = ["/", "/tools/", "/about/"]
for t in T:
    p = f"/tools/{t['slug']}/"; urls.append(p)
    fl = "".join(f'<label for="{i}">{l}<input id="{i}" type="number" step="any" inputmode="decimal" value="{d}"></label>' for i, l, d in t["fields"])
    rel = "".join(f'<li><a href="/tools/{x["slug"]}/">{x["name"]}</a></li>' for x in T if x is not t)
    q, a = t["faq"]
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "WebApplication", "name": t["name"], "url": S + p, "applicationCategory": "UtilitiesApplication", "operatingSystem": "Any", "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}]},
        {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Home", "item": S + "/"}, {"@type": "ListItem", "position": 2, "name": "Tools", "item": S + "/tools/"}, {"@type": "ListItem", "position": 3, "name": t["name"], "item": S + p}]}]}
    body = f'''<nav class="crumb" aria-label="Breadcrumb"><a href="/">Home</a> / <a href="/tools/">Tools</a> / {t["name"]}</nav>
<h1>{t["name"]}</h1><p class="lead">{t["intro"]}</p>
<section class="calc"><form id="f" onsubmit="return false">{fl}</form><div id="o" class="out" aria-live="polite"></div></section>
<h2>Formula</h2><p>{t["formula"]}</p><h2>FAQ</h2><h3>{q}</h3><p>{a}</p>
<h2>More tools</h2><ul class="links">{rel}</ul>''' + JS % t["js"]
    w(p + "index.html", page(p, f'{t["kw"]} – Free Online Tool | FlightPlanPro', t["desc"], body, ld))

TAGS={'crosswind-calculator': 'pilot student', 'wind-triangle-calculator': 'student pilot hobbyist', 'fuel-planning-calculator': 'dispatcher pilot', 'density-altitude-calculator': 'pilot engineer student', 'great-circle-distance-calculator': 'dispatcher engineer hobbyist', 'top-of-descent-calculator': 'pilot student', 'mach-tas-calculator': 'pilot student engineer hobbyist', 'equal-time-point-calculator': 'pilot dispatcher student', 'nat-tmi-calculator': 'pilot dispatcher student'}
LAB={'pilot': 'Pilots', 'student': 'Students', 'dispatcher': 'Dispatchers', 'engineer': 'Engineers', 'hobbyist': 'Hobbyists'}
cards="".join('<a class="row" href="/tools/%s/" data-a="%s"><span class="n">%s</span><span class="d">%s.</span><span class="t">%s</span></a>'%(t["slug"],TAGS[t["slug"]],t["name"],t["desc"].split(".")[0],", ".join(LAB[k] for k in TAGS[t["slug"]].split())) for t in T)
EXTRA='<a class="row" href="/tools/metar-decoder/" data-a="pilot student dispatcher hobbyist"><span class="n">METAR Decoder</span><span class="d">Read any METAR in plain English with flight category.</span><span class="t">Pilots, Students, Dispatchers, Hobbyists</span></a><a class="row" href="/tools/notam-decoder/" data-a="pilot dispatcher student"><span class="n">NOTAM Decoder and Route Check</span><span class="d">Decode a NOTAM, map the area and check your route.</span><span class="t">Pilots, Dispatchers, Students</span></a>'
EXTRA+='<a class="row" href="/tools/crew-duty-limits/" data-a="pilot dispatcher student"><span class="n">Crew Duty Limits (FAA Part 117)</span><span class="d">Flight time, FDP, augmented crews and rest.</span><span class="t">Pilots, Dispatchers, Students</span></a>'
EXTRA+='<a class="row" href="/tools/load-sheet-and-balance/" data-a="pilot dispatcher student engineer"><span class="n">Load Sheet, CG Envelope and Trim</span><span class="d">Weights, balance, envelope graph and trim.</span><span class="t">Pilots, Dispatchers, Students, Engineers</span></a>'
EXTRA+='<a class="row" href="/tools/aviation-unit-converter/" data-a="pilot dispatcher student engineer hobbyist"><span class="n">Aviation Unit Converter</span><span class="d">Speed, distance, pressure, weight, fuel and temperature.</span><span class="t">Everyone</span></a>'
EXTRA+='<a class="row" href="/tools/edto-planner/" data-a="pilot dispatcher student"><span class="n">EDTO Flight Planner</span><span class="d">Circles, coverage, ETPs and weather on a map.</span><span class="t">Pilots, Dispatchers, Students</span></a>'
cards+=EXTRA
CHIPS='<div class="chips" role="group" aria-label="Filter tools by role"><button aria-pressed="true" data-f="all">All</button>'+"".join('<button aria-pressed="false" data-f="%s">%s</button>'%(k,v) for k,v in LAB.items())+'</div>'
FJS="<script>document.querySelectorAll('.chips button').forEach(b=>b.onclick=()=>{document.querySelectorAll('.chips button').forEach(x=>x.setAttribute('aria-pressed',x==b));const k=b.dataset.f;document.querySelectorAll('.row').forEach(r=>r.hidden=k!='all'&&!r.dataset.a.split(' ').includes(k))})</script>"
w("tools/index.html", page("/tools/", "Free Flight Planning Tools & Calculators | FlightPlanPro", "Free aviation calculators for pilots, students and dispatchers: crosswind, wind triangle, fuel, density altitude, great-circle and top of descent.",
  f'<h1>Flight planning tools</h1><p class="lead">Free calculators for pilots, student pilots and dispatchers. No sign-up, works on phone and desktop.</p>{CHIPS}<div class="rows">{cards}</div>{FJS}'))


SL=[("tas","True airspeed","kt",80,500,110),("crs","Course","°",0,359,90),("wd","Wind from","°",0,359,150),("ws","Wind speed","kt",0,80,20)]
SLH="".join('<label for="%s">%s <output><span id="%sv"></span> %s</output></label><input type="range" id="%s" min="%d" max="%d" value="%d">'%(a,b,a,c,a,d,e,f) for a,b,c,d,e,f in SL)
WJS="""<script>(()=>{const $=i=>document.getElementById(i),I=['tas','crs','wd','ws'],r=Math.PI/180,C=180;
function L(i,a,b,c,d){const e=$(i);e.setAttribute('x1',a);e.setAttribute('y1',b);e.setAttribute('x2',c);e.setAttribute('y2',d)}
let t='';for(let a=0;a<360;a+=10){const l=a%30?6:14,x=Math.sin(a*r),y=-Math.cos(a*r);t+='<line x1="'+(C+x*150)+'" y1="'+(C+y*150)+'" x2="'+(C+x*(150-l))+'" y2="'+(C+y*(150-l))+'"/>'}$('tk').innerHTML=t;
function u(){const v={};I.forEach(i=>{v[i]=+$(i).value;$(i+'v').textContent=v[i]});
const k=Math.asin(v.ws/v.tas*Math.sin((v.wd-v.crs)*r)),h=(v.crs+k/r+360)%360,ae=v.tas*Math.sin(h*r),an=v.tas*Math.cos(h*r),we=v.ws*Math.sin((v.wd+180)*r),wn=v.ws*Math.cos((v.wd+180)*r),q=135/(v.tas+v.ws),P=(e,n)=>[C+e*q,C-n*q],A=P(ae,an),G=P(ae+we,an+wn);
L('va',C,C,A[0],A[1]);L('vw',A[0],A[1],G[0],G[1]);L('vg',C,C,G[0],G[1]);
$('oh').textContent=Math.round(h)+'°';$('og').textContent=Math.round(Math.hypot(ae+we,an+wn))+' kt';$('oc').textContent=Math.abs(k/r).toFixed(1)+'° '+(k>=0?'right':'left')}
I.forEach(i=>$(i).addEventListener('input',u));u()})()</script>"""
PANEL='<div class="panel"><svg id="wt" viewBox="0 0 360 360" role="img" aria-label="Wind triangle: heading, wind and ground track vectors on a compass"><circle cx="180" cy="180" r="150" class="ring"/><g id="tk" class="tk"></g><text x="180" y="20" class="nn">N</text><line id="va" class="va"/><line id="vw" class="vw"/><line id="vg" class="vg"/><circle cx="180" cy="180" r="4" fill="#fff"/></svg><div class="ro"><div><small>Heading to fly</small><b id="oh"></b></div><div><small>Ground speed</small><b id="og"></b></div><div><small>Correction</small><b id="oc"></b></div></div><p class="key"><i class="k1"></i>Heading <i class="k2"></i>Wind <i class="k3"></i>Track over ground</p><div class="sl">'+SLH+'</div></div>'
hl = {"@context": "https://schema.org", "@graph": [{"@type": "WebSite", "name": "FlightPlanPro", "url": S + "/"}, {"@type": "Organization", "name": "FlightPlanPro", "url": S + "/"}]}
PROD='<div class="prod"><a class="pc" href="/flight-planner/"><svg viewBox="0 0 24 24"><circle cx="5" cy="18" r="2"/><circle cx="19" cy="6" r="2"/><path d="M7 17c5-1 3-9 10-10"/></svg><h3>Flight Planner</h3><p>Route, fuel, load sheet and an ICAO flight plan you can download as PDF.</p><span>Plan a flight</span></a><a class="pc" href="/metar/"><svg viewBox="0 0 24 24"><path d="M7 18h10a4 4 0 0 0 0-8 5 5 0 0 0-9.6-1A4 4 0 0 0 7 18z"/></svg><h3>METAR and TAF</h3><p>Live airport weather and forecasts, decoded into plain English.</p><span>Check weather</span></a><a class="pc" href="/tools/crew-duty-limits/"><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg><h3>Crew Duty Limits</h3><p>FAA Part 117 flight and duty limits for 2, 3 and 4 pilot crews.</p><span>Check limits</span></a><a class="pc" href="/tools/notam-decoder/"><svg viewBox="0 0 24 24"><path d="M12 3l10 18H2z"/><path d="M12 10v5M12 18v.5"/></svg><h3>NOTAM Decoder</h3><p>Decode a NOTAM, see the area on a map and check your route.</p><span>Decode a NOTAM</span></a><a class="pc" href="/tools/load-sheet-and-balance/"><svg viewBox="0 0 24 24"><path d="M4 19h16M7 19l2-8h6l2 8M12 5v6M8 5h8"/></svg><h3>Load Sheet and Trim</h3><p>Weights, CG envelope graph and trim setting on a printable load sheet.</p><span>Build a load sheet</span></a><a class="pc" href="/tools/edto-planner/"><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="4"/><path d="M12 3v3M12 18v3M3 12h3M18 12h3"/></svg><h3>EDTO Flight Planner</h3><p>Circles, route validation, equal time points and live weather.</p><span>Plan EDTO</span></a></div>'
w("index.html", page("/", "FlightPlanPro – Free Flight Planning Tools for Pilots & Dispatchers", "Free flight planning tools for pilots, dispatchers, students and hobbyists: flight plan generator, live METAR and TAF, crew duty limits, NOTAM decoder and calculators.",
  '<section class="hero2"><h1>Plan, check and brief every flight in one place</h1><p class="lead">Flight plans, live weather, crew duty limits and NOTAM checks for pilots, dispatchers, students and hobbyists. Free, fast, and no sign-up.</p><p><a class="btn" href="/flight-planner/">Plan a flight</a><a class="btn ghost" href="/metar/">Check weather</a></p></section>'
  +PROD+
  '<section class="hero"><div><h2 style="margin-top:0">Try it live: the wind triangle</h2><p class="lead">Drag the sliders to see the heading to fly, ground speed and wind correction angle update instantly.</p><p><a href="/tools/wind-triangle-calculator/">Open the full calculator</a></p></div>'+PANEL+'</section>'
  '<h2>All tools</h2>'+CHIPS+'<div class="rows">'+cards+'</div>'+FJS+
  '<h2>Learning paths</h2>'+LP+'<h2>Guides</h2>'+GL+'<h2>Why trust the numbers</h2><div class="trio"><p><b>Formulas on the page.</b> Each calculator explains its maths so you can check it.</p><p><b>Private by design.</b> Calculators run in your browser. Nothing you type is sent anywhere.</p><p><b>Honest limits.</b> These are planning aids. Approved aircraft data, weather and NOTAMs always come first.</p></div>'
  '<h2>FAQ</h2><h3>Are these tools free?</h3><p>Yes. Every tool is free and needs no account.</p><h3>Can I use them for real flights?</h3><p>They are training and reference aids. Use approved aircraft data, official weather and NOTAMs for operational decisions.</p>'+WJS, hl))

w("about/index.html", page("/about/", "About FlightPlanPro | Free Aviation Planning Tools", "About FlightPlanPro and its disclaimer: free aviation calculators for training and planning reference.",
  '<h1>About FlightPlanPro</h1><p class="lead">FlightPlanPro offers free flight planning calculators and guides for student pilots, pilots and dispatchers.</p><h2>Disclaimer</h2><p>Results are estimates for training and planning reference. They are not certified dispatch or flight-planning software and do not replace the aircraft flight manual, approved performance data, official weather, NOTAMs or regulations. The pilot in command and operator remain responsible for all decisions.</p><h2>Privacy</h2><p>Calculators run entirely in your browser; the values you enter are not sent anywhere.</p>'))

w("404.html", page("/404.html", "Page not found | FlightPlanPro", "Page not found.", '<h1>Page not found</h1><p class="lead">That page does not exist. <a href="/tools/">Browse the tools</a>.</p>').replace('content="index,follow', 'content="noindex,follow'))

w("assets/style.css", """:root{--bg:#e8eff3;--gl:rgba(10,37,64,.05);--ink:#0a2540;--mute:#4b6378;--card:#fff;--line:#c4d3dd;--blue:#0b5fa5;--mag:#d1126b;--amb:#f5a300;--sky:#5cc0ff;--hd:Bahnschrift,"DIN Alternate","Arial Nova Condensed","Roboto Condensed","Segoe UI",system-ui,sans-serif}
@media(prefers-color-scheme:dark){:root{--bg:#07121c;--gl:rgba(255,255,255,.04);--ink:#e8f0f6;--mute:#9ab0c1;--card:#0e2233;--line:#233f56;--blue:#6db3f0;--mag:#ff5c9d}}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:var(--bg) linear-gradient(var(--gl) 1px,transparent 1px) 0 0/48px 48px;color:var(--ink);font:17px/1.6 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
body{background-image:linear-gradient(var(--gl) 1px,transparent 1px),linear-gradient(90deg,var(--gl) 1px,transparent 1px);background-size:48px 48px}
.wrap{max-width:1040px;margin:0 auto;padding:0 20px}a{color:var(--blue)}a:focus-visible,input:focus-visible,button:focus-visible{outline:3px solid var(--mag);outline-offset:2px}
.skip{position:absolute;left:-999px}.skip:focus{left:8px;top:8px;background:#fff;color:#000;padding:8px;z-index:9}
header{background:#0a2540;border-bottom:3px solid var(--mag)}.bar{flex-wrap:wrap;display:flex;justify-content:space-between;align-items:center;min-height:58px}
.logo{font:700 1.35rem var(--hd);color:#fff;text-decoration:none;letter-spacing:.01em}.logo b{color:var(--sky)}nav{display:flex;flex-wrap:wrap}nav a{margin-left:16px;color:#d7e6f2;text-decoration:none;font-weight:600}nav a:hover{color:#fff}
h1,h2,h3{font-family:var(--hd);letter-spacing:-.005em}h1{font-size:clamp(2rem,5.2vw,3.1rem);line-height:1.08;margin:.9em 0 .4em}h2{margin:2.2em 0 .6em;font-size:1.55rem}h3{margin:1.2em 0 .2em;font-size:1.1rem}
p,li{max-width:68ch}.lead{font-size:1.15rem;color:var(--mute)}.note{font-size:.9rem;color:var(--mute)}.crumb{font-size:.9rem;color:var(--mute);margin-top:18px}
.btn{display:inline-block;background:var(--mag);color:#fff;padding:13px 24px;border-radius:6px;font-weight:700;text-decoration:none}.btn:hover{filter:brightness(1.1)}
.hero{display:grid;gap:28px;align-items:center;padding:8px 0 4px}@media(min-width:900px){.hero{grid-template-columns:1fr 440px}}
.panel{background:#0a2540;color:#fff;padding:18px;border-radius:10px;border:1px solid #1d4468}.panel svg{width:100%;max-width:340px;display:block;margin:0 auto}
.ring{fill:none;stroke:#5d7f9b;stroke-width:1.5}.tk line{stroke:#5d7f9b}.nn{fill:#cfe3f3;font:700 15px var(--hd);text-anchor:middle}
.va,.vw,.vg{stroke-width:3.5;stroke-linecap:round}.va{stroke:var(--sky)}.vw{stroke:var(--amb)}.vg{stroke:#ff5c9d;stroke-dasharray:8 6}
.ro{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-top:10px;text-align:center}.ro small{display:block;color:#9db6c8;font-size:.78rem}.ro b{font:700 1.7rem var(--hd);font-variant-numeric:tabular-nums}
.key{font-size:.8rem;color:#b9cddb;text-align:center;margin:8px auto}.key i{display:inline-block;width:14px;height:4px;margin:0 5px 2px 10px}.k1{background:var(--sky)}.k2{background:var(--amb)}.k3{background:#ff5c9d}
.sl{display:grid;gap:4px 18px;grid-template-columns:1fr 1fr}.panel label{display:flex;justify-content:space-between;font-size:.82rem;font-weight:600;color:#cfe3f3;margin-top:6px}.panel output{color:#fff;font-variant-numeric:tabular-nums}.panel input{grid-column:auto}
input[type=range]{padding:0;accent-color:var(--mag);background:none;border:0;width:100%}
.chips{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:14px}.chips button{font:600 .9rem system-ui;padding:7px 15px;border:1px solid var(--ink);background:transparent;color:var(--ink);border-radius:99px;cursor:pointer}.chips button[aria-pressed=true]{background:var(--ink);color:var(--bg)}
.rows{border-top:2px solid var(--ink)}.row{display:grid;gap:2px 28px;padding:16px 4px;border-bottom:1px solid var(--line);text-decoration:none;color:var(--ink);align-items:baseline}.row[hidden]{display:none}
@media(min-width:800px){.row{grid-template-columns:19rem 1fr 13rem}}.n{font:700 1.15rem var(--hd)}.d{color:var(--mute)}.t{font-size:.85rem;color:var(--blue)}@media(min-width:800px){.t{text-align:right}}.row:hover .n{color:var(--mag)}
.trio{display:grid;gap:20px}@media(min-width:800px){.trio{grid-template-columns:repeat(3,1fr)}}.trio p{margin:0;border-left:3px solid var(--mag);padding-left:14px;color:var(--mute)}.trio b{color:var(--ink)}
.calc{display:grid;gap:24px;background:var(--card);border:1px solid var(--line);border-top:4px solid var(--ink);padding:22px;border-radius:0 0 8px 8px}@media(min-width:760px){.calc{grid-template-columns:1fr 1fr}}
form{display:grid;gap:12px}label{display:grid;gap:4px;font-weight:600;font-size:.92rem}input{font:inherit;padding:10px;border:1px solid var(--line);background:var(--bg);color:var(--ink);border-radius:6px;width:100%}
.out{border-left:4px solid var(--mag);padding-left:18px;align-self:start}.r{display:flex;justify-content:space-between;align-items:baseline;gap:12px;padding:9px 0;border-bottom:1px solid var(--line)}.r span{color:var(--mute);font-size:.9rem}.r b{font:700 1.45rem var(--hd);text-align:right;font-variant-numeric:tabular-nums}
.links{padding-left:20px}footer{margin-top:60px;background:#0a2540;color:#b9cddb;padding:22px 0;font-size:.9rem}footer a{color:#d7e6f2}
.hero2{padding:36px 0 18px;max-width:780px}.hero2 h1{margin:0 0 .3em;font-size:clamp(2.2rem,6vw,3.6rem)}.btn+.btn{margin-left:10px}.btn.ghost{background:transparent;color:var(--ink);border:2px solid var(--ink);padding:11px 22px}
.prod{display:grid;gap:16px;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));margin:8px 0 12px}.pc{display:flex;flex-direction:column;gap:8px;background:var(--card);border:1px solid var(--line);border-top:4px solid var(--mag);padding:20px;border-radius:10px;text-decoration:none;color:var(--ink);transition:transform .15s,box-shadow .15s}.pc:hover{transform:translateY(-3px);box-shadow:0 10px 24px rgba(10,37,64,.16)}.pc svg{width:42px;height:42px;stroke:var(--blue);fill:none;stroke-width:1.7;stroke-linecap:round;stroke-linejoin:round}.pc h3{margin:0;font-size:1.25rem}.pc p{margin:0;color:var(--mute);font-size:.95rem}.pc span{margin-top:auto;padding-top:6px;font-weight:700;color:var(--mag)}
nav a.cta{background:var(--mag);color:#fff;padding:7px 14px;border-radius:6px}nav a.cta:hover{filter:brightness(1.1);color:#fff}
.err{color:#c62828;font-weight:700;margin:8px 0}.miss{border-color:#c62828!important;box-shadow:0 0 0 2px rgba(198,40,40,.25)}@media(prefers-color-scheme:dark){.err{color:#ff7b7b}}
@media(max-width:700px){.bar{flex-direction:column;align-items:flex-start;padding:8px 0;min-height:0}nav{flex-wrap:nowrap;overflow-x:auto;white-space:nowrap;width:100%;padding:4px 0 8px;-webkit-overflow-scrolling:touch}nav a{margin:0 16px 0 0;font-size:.92rem}nav a.cta{margin-right:0}.hero2 h1{font-size:2rem}}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}}""")


import os as _o
w("functions/api/wx.js", "const OK=/^[A-Z0-9]{3,4}$/;\nexport async function onRequestGet({request,waitUntil}){\nconst u=new URL(request.url),t=u.searchParams.get('t')==='taf'?'taf':'metar';\nconst ids=(u.searchParams.get('ids')||'').toUpperCase().split(',').filter(x=>OK.test(x)).slice(0,6).sort();\nif(!ids.length)return new Response('[]',{status:400,headers:{'Content-Type':'application/json'}});\nconst key=new Request(u.origin+'/api/wx?t='+t+'&ids='+ids.join(',')),c=caches.default;\nlet r=await c.match(key);\nif(!r){\nconst up=await fetch('https://aviationweather.gov/api/data/'+t+'?format=json&ids='+ids.join(',')+(t==='metar'?'&hours=3':''),{headers:{'User-Agent':'FlightPlanPro/1.0 (https://flightplanpro.pages.dev)'}});\nconst body=up.ok?((await up.text())||'[]'):'[]';\nr=new Response(body,{status:up.ok?200:502,headers:{'Content-Type':'application/json','Cache-Control':'public, max-age='+(up.ok?300:20),'Access-Control-Allow-Origin':'*'}});\nif(up.ok)waitUntil(c.put(key,r.clone()));\n}\nreturn r}\n")
urls.append("/flight-planner/")
w("flight-planner/index.html", page("/flight-planner/", "Flight Plan Generator: Fuel, Load Sheet, METAR/TAF | FlightPlanPro", "Free flight plan generator: route A to B with alternate C, fuel build-up, vertical flight plan, load sheet and live METAR/TAF. For training use.", open("/home/claude/fp_body.html").read()))

urls += ["/privacy/", "/data-sources/"]
w("privacy/index.html", page("/privacy/", "Privacy Policy | FlightPlanPro", "How FlightPlanPro handles data, cookies and advertising.",
 '<h1>Privacy policy</h1><p class="lead">Last updated 16 October 2026.</p><h2>What the calculators do with your input</h2><p>Calculator values stay in your browser. The flight planner sends only the airport codes you enter to our own server, to fetch weather.</p><h2>Logs</h2><p>Our host, Cloudflare, processes requests and may keep technical logs such as IP address and browser type for security and operation.</p><h2>Advertising and cookies</h2><p>We plan to show ads from Google AdSense. Google and its partners may use cookies to show and measure ads. Visitors in the European Economic Area, the United Kingdom and Switzerland will be asked for consent through a Google-certified consent banner. You can manage ad personalisation at adssettings.google.com.</p><h2>Analytics</h2><p>We use Google Search Console, which reports search performance for the site and does not identify individual visitors to us.</p><h2>Your rights</h2><p>You can ask what data we hold or ask us to delete it. Contact: [ADD-YOUR-CONTACT-EMAIL].</p>'))
w("data-sources/index.html", page("/data-sources/", "Data Sources and Disclaimer | FlightPlanPro", "Where FlightPlanPro data comes from, and why its results are for training and simulation only.",
 '<h1>Data sources and disclaimer</h1><p class="lead">FlightPlanPro is for training, education and flight simulation. It is not operational flight planning software.</p><h2>Sources</h2><ul><li><b>METAR and TAF:</b> NOAA Aviation Weather Center (aviationweather.gov), fetched through our server and cached for about five minutes.</li><li><b>Airports:</b> OurAirports (ourairports.com), public domain, updated periodically.</li><li><b>Aircraft values:</b> rounded training approximations. They are not from any aircraft flight manual.</li></ul><h2>Not included</h2><p>NOTAMs, airways, FIR data and winds aloft are not mirrored here. For NOTAMs always use the official source for the country concerned.</p><h2>Disclaimer</h2><p>Results are estimates and may be wrong. Do not use them for real flights, dispatch, load control or any safety decision. Always use current official weather, NOTAMs, approved aircraft data and applicable regulations. FlightPlanPro is not affiliated with ICAO, the FAA, EASA, NOAA or any aircraft manufacturer, and gives no warranty of any kind.</p>'))

urls += ["/tools/metar-decoder/", "/tools/notam-decoder/"]
import json as _j
w("tools/metar-decoder/index.html", page("/tools/metar-decoder/", "METAR Decoder: Read Aviation Weather Reports | FlightPlanPro", "Free METAR decoder. Paste any METAR or fetch the latest for an airport and read wind, visibility, cloud, pressure and flight category in plain English.", open("/home/claude/metar_body.html").read(), _j.loads('{"@context":"https://schema.org","@type":"WebApplication","name":"METAR Decoder","url":"https://flightplanpro.pages.dev/tools/metar-decoder/","applicationCategory":"UtilitiesApplication","operatingSystem":"Any","offers":{"@type":"Offer","price":"0","priceCurrency":"USD"}}')))
w("tools/notam-decoder/index.html", page("/tools/notam-decoder/", "NOTAM Decoder and Route Conflict Check | FlightPlanPro", "Free NOTAM decoder. Paste an ICAO NOTAM, see it decoded and drawn on a map, and check whether your route crosses the restricted area.", open("/home/claude/notam_body.html").read(), _j.loads('{"@context":"https://schema.org","@type":"WebApplication","name":"NOTAM Decoder and Route Check","url":"https://flightplanpro.pages.dev/tools/notam-decoder/","applicationCategory":"UtilitiesApplication","operatingSystem":"Any","offers":{"@type":"Offer","price":"0","priceCurrency":"USD"}}')))

urls += ["/metar/", "/taf/", "/tools/crew-duty-limits/", "/tools/load-sheet-and-balance/", "/tools/aviation-unit-converter/", "/tools/edto-planner/"]
w("tools/load-sheet-and-balance/index.html", page("/tools/load-sheet-and-balance/", "Load Sheet, CG Envelope and Trim Calculator | FlightPlanPro", "Free load sheet calculator: ZFW, TOW and landing weight, CG and %MAC, envelope graph and trim setting. Enter your own aircraft data. For training.", open("/home/claude/wb_body.html").read()))
w("tools/aviation-unit-converter/index.html", page("/tools/aviation-unit-converter/", "Aviation Unit Converter: Knots, NM, hPa, inHg, kg, lb | FlightPlanPro", "Free aviation unit converter: knots, km/h, nautical miles, hPa, inHg, kilograms, pounds, litres, gallons and temperature, with fuel density.", open("/home/claude/conv_body.html").read()))
w("tools/edto-planner/index.html", page("/tools/edto-planner/", "EDTO Flight Planner: Circles, ETPs, Weather | FlightPlanPro", "Free EDTO flight planner: diversion circles, route validation, equal time points and live METAR and TAF checks for en-route alternates.", open("/home/claude/edto_body.html").read()))
w("tools/crew-duty-limits/index.html", page("/tools/crew-duty-limits/", "Crew Duty and Flight Time Limits Calculator | FlightPlanPro", "Check flight time and flight duty period against FAA Part 117 for 2, 3 and 4 pilot crews, rest facility class, segments and deadhead.", open("/home/claude/crew_body.html").read()))
w("assets/wx.js", open("/tmp/wx.js").read())
w("metar/index.html", page("/metar/", "Live METAR by Airport: Decoded Weather | FlightPlanPro", "Latest METAR for any airport, decoded in plain English with flight category. Free, updated every few minutes.", open("/home/claude/metar_page.html").read()))
w("taf/index.html", page("/taf/", "Live TAF Forecast by Airport: Decoded | FlightPlanPro", "Latest TAF airport forecast decoded group by group: FM, BECMG, TEMPO and PROB, with flight category.", open("/home/claude/taf_page.html").read()))

urls += ["/guides/"] + ["/guides/%s/" % g["slug"] for g in G]
w("guides/index.html", page("/guides/", "Aviation Guides: Weather, Flight Plans and Crew Limits | FlightPlanPro", "Plain-English aviation guides: crosswind, METAR, TAF, ICAO flight plans, the wind triangle and FAA Part 117 crew limits.", '<h1>Guides</h1><p class="lead">Plain-English explanations of the calculations and rules behind the tools.</p>'+GL))
for g in G:
    p = "/guides/%s/" % g["slug"]
    rel = "".join('<li><a href="/guides/%s/">%s</a></li>' % (x["slug"], x["title"]) for x in G if x is not g)
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Article", "headline": g["title"], "author": {"@type": "Organization", "name": "FlightPlanPro"}, "datePublished": "2026-10-18", "dateModified": "2026-10-18", "mainEntityOfPage": S + p},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in g["faq"]]}]}
    body = '<nav class="crumb" aria-label="Breadcrumb"><a href="/">Home</a> / <a href="/guides/">Guides</a> / ' + g["title"] + '</nav><article><h1>' + g["title"] + '</h1>' + g["body"] + '<p><a class="btn" href="' + g["tool"][0] + '">Open the ' + g["tool"][1].lower() + '</a></p><h2>FAQ</h2>' + "".join("<h3>%s</h3><p>%s</p>" % qa for qa in g["faq"]) + '<h2>More guides</h2><ul class="links">' + rel + '</ul><p class="note">For training and reference only. Check official sources before any real flight.</p></article>'
    w(p.strip("/") + "/index.html", page(p, g["title"] + " | FlightPlanPro", g["desc"], body, ld))

urls.append("/site-map/")
_mk=lambda items:'<ul class="links">'+"".join('<li><a href="%s">%s</a></li>'%i for i in items)+'</ul>'
_main=[("/flight-planner/","Flight Planner"),("/metar/","Live METAR"),("/taf/","Live TAF"),("/tools/crew-duty-limits/","Crew duty limits"),("/tools/notam-decoder/","NOTAM decoder and route check"),("/tools/load-sheet-and-balance/","Load sheet, CG envelope and trim"),("/edto/","EDTO learning path"),("/oceanic/","Oceanic flying learning path")]
_calc=[("/tools/%s/"%t["slug"],t["name"]) for t in T]+[("/tools/metar-decoder/","METAR decoder"),("/tools/aviation-unit-converter/","Aviation unit converter"),("/tools/edto-planner/","EDTO planner"),("/tools/","All tools")]
_gd=[("/guides/%s/"%g["slug"],g["title"]) for g in G]+[("/guides/","All guides")]
_info=[("/","Home"),("/about/","About"),("/data-sources/","Data sources and disclaimer"),("/privacy/","Privacy policy")]
w("site-map/index.html", page("/site-map/", "Site Map | FlightPlanPro", "Every page on FlightPlanPro: flight planner, weather, crew duty limits, calculators and guides.", '<h1>Site map</h1><h2>Main tools</h2>'+_mk(_main)+'<h2>Calculators</h2>'+_mk(_calc)+'<h2>Guides</h2>'+_mk(_gd)+'<h2>About the site</h2>'+_mk(_info)))

urls += ["/edto/", "/oceanic/"]
_t=lambda s:next(g["title"] for g in G if g["slug"]==s)
_gl=lambda s,d:'<li><a href="/guides/%s/">%s</a>: %s</li>'%(s,_t(s),d)
_rows="".join("<tr><td>%d min</td><td>%d NM</td><td>%d NM</td><td>%d NM</td></tr>"%(m,int(350*m/60+.5),int(400*m/60+.5),int(450*m/60+.5)) for m in (60,90,120,138,180,207,240))
w("edto/index.html", page("/edto/", "EDTO from Scratch: A Learning Path | FlightPlanPro", "Learn EDTO step by step: why it exists, approval and dispatch, adequate and suitable airports, equal time points, diversion circles and polar routes, with free tools.",
 '<style>.tb{width:100%;border-collapse:collapse;font-variant-numeric:tabular-nums;background:var(--card)}.tb th,.tb td{padding:8px 10px;border-bottom:1px solid var(--line);text-align:left}</style><h1>EDTO from Scratch: A Learning Path</h1><p class="lead">Extended Diversion Time Operations (EDTO) is how aeroplanes fly far from airports where they could land. Follow these steps in order, from the basic idea to planning a route with live tools.</p>'
 '<h2>Step by step</h2><ol class="links">'+_gl("edto-explained","what EDTO is, why it exists, threshold time and maximum diversion time")+_gl("adequate-vs-suitable-aerodrome","which airports can be used, and when")+_gl("edto-approval-and-dispatch","approval levels and the checks before every flight")+_gl("equal-time-point-explained","the formula for where to divert, with an example")+'<li><a href="/tools/equal-time-point-calculator/">Equal time point calculator</a>: try the formula with your own numbers</li><li><a href="/tools/edto-planner/">EDTO flight planner</a>: circles, route validation, ETPs and live weather on a map</li>'+_gl("polar-routes-explained","what is special about flying near the poles")+_gl("polar-operations-requirements-checklist","what the FAA requires for polar operations")+'</ol>'
 '<h2>What a diversion circle looks like</h2><p>A diversion circle is drawn around an alternate airport. Its radius is the one-engine-inoperative speed multiplied by the diversion time. The table shows the radius for three example speeds. Your aircraft\'s approved speed is what counts, and it is not the same for every type.</p><div style="overflow-x:auto"><table class="tb"><tr><th>Diversion time</th><th>At 350 kt</th><th>At 400 kt</th><th>At 450 kt</th></tr>'+_rows+'</table></div><p class="note">Still air, for illustration only. Approved diversion times such as 120 and 180 minutes, and the 15 percent extensions (138 and 207), come from the operator\'s approval.</p>'
 '<h2>Key terms</h2><ul><li><b>Threshold time:</b> the range to an en-route alternate, set by the State, beyond which an EDTO approval is needed.</li><li><b>Maximum diversion time:</b> the longest diversion time the operator\'s approval allows.</li><li><b>Adequate aerodrome:</b> can handle the aeroplane. <b>Suitable aerodrome:</b> adequate, with weather and runway conditions good enough at the time of use.</li><li><b>Equal time point (ETP):</b> where continuing and returning take the same time.</li><li><b>EDTO-significant system:</b> a system whose time limit can restrict how far the flight may go, for example cargo fire suppression.</li></ul>'
 '<h2>FAQ</h2><h3>Is EDTO only for twin-engine aeroplanes?</h3><p>It applies to turbine-engine aeroplanes with two or more engines, though the thresholds differ. The older term ETOPS covered twins.</p><h3>Can I use these tools for real planning?</h3><p>No. They are training tools. Use your approved data, your operator\'s procedures and your State\'s rules.</p>'))
w("oceanic/index.html", page("/oceanic/", "Oceanic and North Atlantic Flying: A Learning Path | FlightPlanPro", "Learn North Atlantic flying step by step: the organised track system, the track message and TMI, NAT high level airspace, oceanic clearances and contingency procedures.",
 '<h1>Oceanic and North Atlantic Flying: A Learning Path</h1><p class="lead">The North Atlantic is crossed by a large volume of traffic every day, so it has its own tracks, requirements and procedures. Follow these steps in order.</p><h2>Step by step</h2><ol class="links">'+_gl("north-atlantic-organised-track-system-explained","what the tracks are and how they are built")+_gl("nat-track-message-and-tmi-explained","what the message contains and what the TMI means")+'<li><a href="/tools/nat-tmi-calculator/">NAT TMI calculator</a>: get the day-of-year number for a date</li>'+_gl("nat-hla-requirements-explained","the approvals and equipment needed to enter")+_gl("nat-oceanic-clearance-explained","how to obtain and read back a clearance")+_gl("nat-contingency-and-slop-explained","what to do when a clearance cannot be obtained, and how offsets work")+'<li><a href="/edto/">EDTO learning path</a>: ocean crossings by twin-engine aeroplanes also involve diversion planning</li></ol><p class="note">Procedures in the region change from time to time. Always use the current North Atlantic Operations and Airspace Manual (NAT Doc 007) and the State AIPs. Information checked October 2026.</p>'))
w("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {S}/sitemap.xml\n")
w("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"<url><loc>{S}{u}</loc><lastmod>{D}</lastmod></url>\n" for u in urls) + "</urlset>\n")
w("_headers", "/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n  X-Frame-Options: SAMEORIGIN\n/assets/*\n  Cache-Control: public, max-age=86400\n")
w("README.md", f"""# FlightPlanPro
Static site (plain HTML/CSS/JS, no build step, no paid services).

## Deploy
1. Push this folder to a GitHub repo.
2. Cloudflare dashboard > Workers & Pages > Create > Pages > Connect to Git. Project name `flightplanpro`, framework preset *None*, build command empty, output directory `/`.
3. Site goes live at https://flightplanpro.pages.dev (if the name is free).

## Google Search Console (HTML tag method)
1. Add property > URL prefix > `{S}/` > HTML tag.
2. Replace the placeholder in every page: `grep -rl {GSC} . | xargs sed -i 's/{GSC}/YOUR_CODE/'`
3. Deploy, click Verify, then submit `{S}/sitemap.xml`.
(HTML file method also works: drop the `google*.html` file in the repo root.)

## Add a tool
Tools are defined in `build.py` (list `T`). Edit it, run `python3 build.py`, commit the output.
""")

REL={"tools/crosswind-calculator":["how-to-calculate-crosswind"],"tools/wind-triangle-calculator":["wind-triangle-explained"],"tools/fuel-planning-calculator":["flight-fuel-planning-explained"],"tools/density-altitude-calculator":["density-altitude-explained"],"tools/metar-decoder":["how-to-read-a-metar"],"metar":["how-to-read-a-metar"],"taf":["how-to-read-a-taf"],"tools/notam-decoder":["how-to-read-a-notam"],"tools/crew-duty-limits":["faa-part-117-explained","easa-flight-time-limitations-basics"],"flight-planner":["what-is-in-an-icao-flight-plan","how-to-file-a-flight-plan","flight-fuel-planning-explained"],"tools/mach-tas-calculator":["wind-triangle-explained"],"tools/nat-tmi-calculator":["nat-track-message-and-tmi-explained","north-atlantic-organised-track-system-explained"],"tools/edto-planner":["edto-explained","edto-approval-and-dispatch","adequate-vs-suitable-aerodrome","equal-time-point-explained","polar-routes-explained","polar-operations-requirements-checklist"],"tools/equal-time-point-calculator":["equal-time-point-explained","edto-explained"],"tools/great-circle-distance-calculator":["what-is-in-an-icao-flight-plan"]}
for _p,_sl in REL.items():
    _f=os.path.join(O,_p,"index.html");_h=open(_f,encoding="utf-8").read()
    _b='<h2>Related guides</h2><ul class="links">'+"".join('<li><a href="/guides/%s/">%s</a></li>'%(x,next(g["title"] for g in G if g["slug"]==x)) for x in _sl)+'</ul>'
    assert '</main>' in _h
    open(_f,"w",encoding="utf-8").write(_h.replace('</main>',_b+'</main>',1))
os.system(f"cp /home/claude/build.py {O}/build.py")
print(len(urls), "pages")
