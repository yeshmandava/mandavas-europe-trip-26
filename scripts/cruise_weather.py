from pathlib import Path
import re

p=Path('index.html')
s=p.read_text()

if 'v31-completion-sections' not in s:
    raise SystemExit('Expected v31 baseline not found; refusing unsafe cruise weather patch')

css=r'''<style id="cruise-weather-v32">
.portWeatherWrap{margin:12px 0 14px}
.portWeatherLabel{display:flex;align-items:center;justify-content:space-between;margin:0 2px 7px}
.portWeatherLabel small{font-size:8px;letter-spacing:.12em;color:#b88447;font-weight:900}
.portWeatherLabel span{font-size:8px;color:#7a8881}
.portWeatherCard{background:#fff;border:1px solid #deddd5;border-radius:16px;padding:13px 14px;display:grid;grid-template-columns:minmax(0,1fr) auto;gap:12px;align-items:center;box-shadow:0 1px 0 rgba(23,63,54,.02)}
.portWxPlace{font-size:12px;font-weight:900;color:#173f36;margin-bottom:6px}.portWxTemp{font:600 27px Georgia,serif;color:#173f36;line-height:1}.portWxTemp small{font:400 10px -apple-system,BlinkMacSystemFont,sans-serif;color:#718078}.portWxDesc{font-size:9.5px;color:#718078;margin-top:5px}.portWxMeta{display:flex;gap:6px;flex-wrap:wrap;margin-top:9px}.portWxPill{display:inline-flex;align-items:center;border:1px solid #e5e1d7;border-radius:999px;padding:5px 7px;font-size:8.5px;color:#6f7e76;background:#fbfaf6}.portWxRight{text-align:center;min-width:54px}.portWxEmoji{font-size:30px;line-height:1}.portWxTip{font-size:8px;color:#906d3d;font-weight:800;line-height:1.25;margin-top:7px;max-width:70px}.portWxLoading{color:#7a8881;font-size:9px;padding:3px 0}.portWxUnavailable{color:#7a8881;font-size:9px;line-height:1.4}
@media(max-width:390px){.portWeatherCard{padding:12px}.portWxTemp{font-size:25px}.portWxEmoji{font-size:28px}}
</style>'''
s=s.replace('</head>',css+'\n</head>',1)

helpers=r'''const cruiseWxMeta=[
 {date:'2026-08-22',name:'Casablanca',lat:33.5731,lon:-7.5898},
 {date:'2026-08-23',name:'Tangier',lat:35.7595,lon:-5.8340},
 {date:'2026-08-24',name:'Cádiz',lat:36.5271,lon:-6.2886},
 {date:'2026-08-25',name:'Gibraltar',lat:36.1408,lon:-5.3536},
 {date:'2026-08-26',name:'Málaga',lat:36.7213,lon:-4.4214},
 {date:'2026-08-27',name:'Cartagena',lat:37.6257,lon:-0.9966},
 {date:'2026-08-28',name:'Palma',lat:39.5696,lon:2.6502}
];
function cruiseWeatherShell(i){let m=cruiseWxMeta[i];return `<div class="portWeatherWrap"><div class="portWeatherLabel"><small>PORT-DAY WEATHER</small><span>${m.date.slice(5).replace('-','/')}</span></div><div id="portwx-${i}" class="portWeatherCard"><div class="portWxLoading">Loading ${m.name} forecast…</div><div class="portWxRight"><div class="portWxEmoji">🌤️</div></div></div></div>`}
function cruiseWxText(c){if(c===0)return'Clear';if(c<=2)return'Partly cloudy';if(c===3)return'Cloudy';if(c===45||c===48)return'Fog';if(c>=51&&c<=57)return'Drizzle';if(c>=61&&c<=67)return'Rain';if(c>=71&&c<=77)return'Snow';if(c>=80&&c<=82)return'Showers';if(c>=95)return'Thunderstorms';return'Mixed'}
function cruiseWxTip(c,r,hi){if(r>=40)return'☂️ Pack rain protection';if(hi>=86)return'🧴 Sunscreen + water';if(c===45||c===48)return'👟 Allow extra visibility time';return'👟 Good walking conditions'}
async function loadCruiseWeather(i){let el=document.getElementById('portwx-'+i),m=cruiseWxMeta[i];if(!el||!m||el.dataset.loaded==='1')return;try{let u=`https://api.open-meteo.com/v1/forecast?latitude=${m.lat}&longitude=${m.lon}&daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max&temperature_unit=fahrenheit&timezone=auto&start_date=${m.date}&end_date=${m.date}`;let r=await fetch(u);if(!r.ok)throw new Error('weather');let j=await r.json();if(!j.daily||!j.daily.time||!j.daily.time.length)throw new Error('forecast');let hi=Math.round(j.daily.temperature_2m_max[0]),lo=Math.round(j.daily.temperature_2m_min[0]),code=j.daily.weather_code[0],rain=j.daily.precipitation_probability_max[0]||0;el.dataset.loaded='1';el.innerHTML=`<div><div class="portWxPlace">${m.name}</div><div class="portWxTemp">${hi}° <small>/ ${lo}°F</small></div><div class="portWxDesc">${cruiseWxText(code)}</div><div class="portWxMeta"><span class="portWxPill">💧 ${rain}% rain</span><span class="portWxPill">📅 ${m.date.slice(5).replace('-','/')}</span></div></div><div class="portWxRight"><div class="portWxEmoji">${wxIcon(code)}</div><div class="portWxTip">${cruiseWxTip(code,rain,hi)}</div></div>`}catch(e){el.dataset.loaded='1';el.innerHTML=`<div class="portWxUnavailable"><b>${m.name}</b><br>Forecast unavailable right now. The rest of your port guide is still ready.</div><div class="portWxRight"><div class="portWxEmoji">🌤️</div></div>`}}
function loadAllCruiseWeather(){cruiseWxMeta.forEach((_,i)=>loadCruiseWeather(i))}
'''

# Add weather helper block immediately before cruisePage.
if 'const cruiseWxMeta=' not in s:
    s=s.replace('function cruisePage(){',helpers+'function cruisePage(){',1)

# Insert the port weather shell directly below each port summary in the expanded section.
old='<p class="portSummary">${d.summary}</p>${d.booked?'
new='<p class="portSummary">${d.summary}</p>${cruiseWeatherShell(i)}${d.booked?'
if old not in s:
    raise SystemExit('Cruise summary insertion point not found')
s=s.replace(old,new,1)

# Load forecasts after rendering Cruise view; Today behavior remains unchanged.
old_render="function render(){tabs();nav();document.getElementById('app').innerHTML=view==='today'?today():view==='cruise'?cruisePage():view==='local'?local():list();if(view==='today')weather()}"
new_render="function render(){tabs();nav();document.getElementById('app').innerHTML=view==='today'?today():view==='cruise'?cruisePage():view==='local'?local():list();if(view==='today')weather();if(view==='cruise')loadAllCruiseWeather()}"
if old_render not in s:
    raise SystemExit('Render function insertion point not found')
s=s.replace(old_render,new_render,1)

s=s.replace('content="v31-completion-sections"','content="v32-cruise-port-weather"',1)
p.write_text(s)
print('Cruise weather tiles added to 7 ports')
