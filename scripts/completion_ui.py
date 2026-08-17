from pathlib import Path
import re

p=Path('index.html')
s=p.read_text()

if 'v30-today-reference-ui' not in s:
    raise SystemExit('Expected v30 Today UI baseline not found; refusing unsafe patch')

css=r'''<style id="agenda-v31">
.agendaDivider{display:flex;align-items:center;justify-content:space-between;gap:12px;margin:18px 2px 10px;padding:10px 12px;border-radius:12px;font-size:9px;font-weight:900;letter-spacing:.12em}
.agendaDivider small{font-size:9px;font-weight:700;letter-spacing:0;text-transform:none}
.doneDivider{background:#edf2ee;color:#4f685e;border:1px solid #d8e1db}
.aheadDivider{background:#f5eee2;color:#8d6737;border:1px solid #e4d4bc;box-shadow:inset 3px 0 0 #b88447}
.timeline .item.done{background:#f3f5f2;border-color:#d6ded8;opacity:.78}
.timeline .item.done>button{background:#173f36;color:#fff;border-color:#173f36;font-weight:900}
.timeline .item.done>div:nth-child(2),
.timeline .item.done>div:nth-child(3)>h3,
.timeline .item.done>div:nth-child(3)>p{text-decoration:line-through;text-decoration-color:#809188;text-decoration-thickness:1.4px}
.timeline .item.done .bits{opacity:.55}
.timeline .item.done .actions{opacity:.72}
.timeline .item.done .actions a{text-decoration:none}
.allDone{margin:18px 0;background:#edf2ee;border:1px solid #d8e1db;color:#315c4d;border-radius:14px;padding:16px;text-align:center;font-weight:900;font-size:11px;letter-spacing:.05em}
</style>'''

if 'id="agenda-v31"' not in s:
    s=s.replace('</head>',css+'\n</head>',1)

helper=r'''function agendaItemHtml(x,i,isDone){return `<article class="item ${isDone?'done':''}"><button aria-label="${isDone?'Mark incomplete':'Mark complete'}" onclick="toggle('${day}-${i}')">${isDone?'✓':'○'}</button><div><b>${x[1]}</b><br><small>${x[0]}</small></div><div><h3>${x[2]}</h3><p>${x[3]}</p><div class="bits"><div><b>SEE</b>${x[4]}</div><div><b>TRY / TIP</b>${x[5]}</div></div><div class="actions"><a target="_blank" href="${map(x[6])}">↗ Directions</a><a class="uber" href="${uber(x[6])}">Uber</a></div></div></article>`}
function agendaItemsHtml(d){let completed=[],remaining=[];d.items.forEach((x,i)=>(done[day+'-'+i]?completed:remaining).push([x,i]));let html='';if(completed.length){html+=`<div class="agendaDivider doneDivider"><span>✓ COMPLETED</span><small>${completed.length} done</small></div>`+completed.map(v=>agendaItemHtml(v[0],v[1],true)).join('')}if(remaining.length){html+=`<div class="agendaDivider aheadDivider"><span>${completed.length?'UP NEXT':'AGENDA'}</span><small>${remaining.length} remaining</small></div>`+remaining.map(v=>agendaItemHtml(v[0],v[1],false)).join('')}else{html+=`<div class="allDone">✓ DAY COMPLETE · Everything on today’s agenda is checked off</div>`}return html}
'''

if 'function agendaItemsHtml(d)' not in s:
    s=s.replace('function today(){',helper+'function today(){',1)

# Replace exactly the inline itinerary renderer inside Today with the grouped renderer.
pattern=re.compile(r"\$\{d\.items\.map\(\(x,i\)=>`<article class=\"item\">.*?\)\.join\(''\)\}",re.S)
matches=pattern.findall(s)
if len(matches)!=1:
    raise SystemExit(f'Expected exactly one inline Today agenda renderer, found {len(matches)}')
s=pattern.sub(lambda m:'${agendaItemsHtml(d)}',s,count=1)

s=s.replace('content="v30-today-reference-ui"','content="v31-completion-sections"',1)

# Guard the core travel actions from accidental changes.
required=['uber://riderequest?pickup=my_location','↗ Directions','function cruisePage()','function local()','function list()','function agendaItemsHtml(d)','v31-completion-sections']
for marker in required:
    if marker not in s:
        raise SystemExit('Missing required marker: '+marker)

p.write_text(s)
print('Applied v31 completion-state UI')
