"""One-off: turn the reviewed design (source_v1.html, a snapshot with hard-coded specifics) into
template.html, where every snapshot-specific value is read from the embedded data (D).
Each replacement asserts it matched exactly once, so a silent miss is impossible."""
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
src = (HERE / "source_v1.html").read_text()
lines = src.split("\n")
assert lines[456].startswith('<script type="application/json" id="data">')
lines[456] = '<script type="application/json" id="data">__DATA__</script>'
s = "\n".join(lines)


def rep(a, b, count=1):
    global s
    n = s.count(a)
    assert n == count, (n, a[:90])
    s = s.replace(a, b)


def repfn(start, end, new):
    global s
    i = s.index(start)
    j = s.index(end, i)
    s = s[:i] + new + s[j:]


rep("var DEF={wallWatch:30,wallSevere:50,y1:30,relWatch:15,relSevere:25,actF:3,jointF:2,jointM:2};",
    "var DEF=Object.assign({},D.thresholds);")
rep("""/* overlay rule, reconstructed from the file: config.toml [overlay] was not supplied.
   Triggers seen in the file: covenant headroom below 10%, own facility maturing within 12 months of as_of.
   The file says an overlay can only escalate. Step size is assumed: one bucket per run, any trigger. */
var AS_OF=Date.UTC(2026,10,9),STEP={'ROUTINE':'WATCH','WATCH':'ACT NOW'};""",
    """/* overlay rule: config.toml [overlay] (assumptions), passed in D.overlay_cfg. It can only escalate, one bucket. */
var AS_OF=Date.parse(D.as_of+'T00:00:00Z'),STEP={'ROUTINE':'WATCH','WATCH':'ACT NOW'},OC=D.overlay_cfg;""")
rep("if(row.headroom!=null&&row.headroom<10)trig.push('covenant headroom '+row.headroom.toFixed(1)+'% < 10%');",
    "if(row.headroom!=null&&row.headroom<OC.headroom_min)trig.push('covenant headroom '+row.headroom.toFixed(1)+'% < '+OC.headroom_min.toFixed(0)+'%');")
rep("""  else if(mo<=12)trig.push('own facility matures '+row.mat+' ('+mo.toFixed(1)+' months after as_of, within 12)')}""",
    """  else if(mo<=OC.months)trig.push('own facility matures '+row.mat+' ('+mo.toFixed(1)+' months after as_of, within '+OC.months+')')}""")
rep("function mkOv(src,name,rows,notes)",
    "var OVBY={};D.overrides.forEach(function(o){OVBY[o.ticker]=o});\nfunction mkOv(src,name,rows,notes)")
rep(""" if(t==='OPI') tl='<span class="tagline test">pipeline test, not live distress</span>';
 if(L.ov) tl+='<span class="tagline syn">'+ovLabel()+', from '+esc(L.ov.from)+'</span>';
 else if(t==='CBL') tl+='<span class="tagline">override proposed: ROUTINE (pending)</span>';
 else if(t==='SLG') tl+='<span class="tagline">override: WATCH, reason changed (pending)</span>';""",
    """ if(t===D.pipeline_test) tl='<span class="tagline test">pipeline test, not live distress</span>';
 if(L.ov) tl+='<span class="tagline syn">'+ovLabel()+', from '+esc(L.ov.from)+'</span>';
 else if(OVBY[t]&&t!==D.pipeline_test) tl+='<span class="tagline">override: '+esc(OVBY[t].short)+' ('+(hr(t+'.override')?'human reviewed':'pending')+')</span>';""")

repfn("function renderHero(){", "function laneName(", r"""function renderHero(){
 var H=D.hero; if(!H){$('#hero').hidden=true;return}
 $('#hero').setAttribute('aria-label',H.aria);
 var lad=H.ladder,q=H.q10.map(function(d){return {label:d.label,claim:d.claim,v:d.total==null?null:d.total/1000,note:d.total==null?'the 10-Q row shows a dash in the total column, no consolidated principal listed':''}});
 var max=Math.max(Math.max.apply(0,lad.map(function(d){return d.v||0})),Math.max.apply(0,q.map(function(d){return d.v||0})));
 var a=lad[H.hot].v,b=q[H.qhot].v,k=C[H.pcid];
 var N=function(v){return Math.round(v).toLocaleString('en-US')};
 var rev=hr(H.tk+'.override');
 var h='<div class="herocard"><div class="heroco"><div class="co"><span class="n">'+N(a)+'</span><span class="to">to</span><span class="n b">'+N(b)+'</span><span class="u">($M)</span></div>'+
  '<p class="cl">'+esc(H.caption)+'</p>'+
  '<p class="ex">Exact figures: $'+fmt1(a)+'M '+chip(lad[H.hot].claim)+' and '+'$'+fmt1(H.q10[H.qhot].total/1000)+'M '+chip(H.q10[H.qhot].claim)+'. Both are consolidated principal by calendar year, converted to $M. The highlighted bar is '+esc(H.year)+'.</p></div>'+
  '<div class="herochart"><figure><figcaption>'+esc(H.k_caption)+'</figcaption>'+ladderSVG(lad,max,{hot:H.hot,aria:H.tk+' 10-K debt maturity ladder',cap:H.k_cap})+'</figure>'+
  '<figure><figcaption>'+esc(H.q_caption)+'</figcaption>'+ladderSVG(q,max,{hot:H.qhot,aria:H.tk+' 10-Q debt maturity ladder, same scale',cap:H.q_cap})+'</figure></div>'+
  '<div class="heroq"><blockquote class="q"><div class="qm">Verbatim, '+esc(H.q_period)+' '+chip(H.pcid)+(/^https?:/.test(k.src)?' <a href="'+esc(k.src)+'" target="_blank" rel="noopener noreferrer">filing</a>':'')+'</div><p>“'+esc(H.head)+'”</p></blockquote>'+
  (H.rest?'<details><summary>Rest of the same paragraph</summary><blockquote class="q"><p>'+esc(H.rest)+'</p></blockquote></details>':'')+'</div>'+
  '<p class="herocap">'+rt(H.note)+' The reading that the filing explains the smaller figure is tagged inferred and '+(rev?'human reviewed':'pending human sign-off')+(C[H.tk+'.override']?' '+chip(H.tk+'.override'):'')+'. The screen still scores the older 10-K ladder.</p></div>';
 $('#heroBody').innerHTML=h;
}
""")

repfn("var T0=Date.UTC(2026,10,1)", "/* ---------- screen table ---------- */", r"""var CW=D.clock_window,T0=Date.parse(CW.start+'T00:00:00Z'),T1=Date.parse(CW.end+'T00:00:00Z'),SPAN=(T1-T0)/864e5+1;
function pos(iso){var p=iso.split('-');return ((Date.UTC(+p[0],+p[1]-1,+p[2])-T0)/864e5)/SPAN*100}
function qhtml(text,cid,period,extra,label){
 var c=C[cid];
 return '<blockquote class="q"><div class="qm">'+esc(label||'Verbatim,')+' '+esc(period)+' '+chip(cid)+(extra||'')+(c&&/^https?:/.test(c.src)?' <a href="'+esc(c.src)+'" target="_blank" rel="noopener noreferrer">filing</a>':'')+'</div><p>'+(label?esc(text):'“'+esc(text)+'”')+'</p></blockquote>';
}
function renderClocks(){
 var asof=pos(D.as_of),tks=D.clock_tickers;
 if(!tks.length){$('#clockBody').innerHTML='<p class="muted">No dated maturity is named in the latest 10-Q text of the case-file names inside this window.</p>';$('#clockOff').innerHTML='';return}
 var h='<div class="tl"><div class="tlhead"><span></span><div class="m" aria-hidden="true">'+CW.labels.map(function(m){return '<div>'+esc(m)+'</div>'}).join('')+'</div></div>';
 tks.forEach(function(tk){
  h+='<div class="tlrow"><span class="lab">'+esc(tk)+'</span><div class="tr"><div class="tlbands" aria-hidden="true">'+CW.labels.map(function(){return '<div></div>'}).join('')+'</div>';
  D.clocks.filter(function(e){return e.tk===tk}).forEach(function(e){
   if(e.exact) h+='<span class="dot2" style="left:'+pos(e.exact).toFixed(2)+'%">'+esc(e.amt.replace(' thousand','K'))+'<i></i></span>';
   else h+='<span class="bar2" style="left:'+pos(e.m0).toFixed(2)+'%;width:'+(pos(e.m1)-pos(e.m0)+100/SPAN).toFixed(2)+'%">'+esc(e.amt)+'</span>';
  });
  var hasDot=D.clocks.some(function(e){return e.tk===tk&&e.exact});
  D.clocks_off.filter(function(e){return e.tk===tk}).slice(0,1).forEach(function(e){h+='<span class="offm"'+(hasDot?' style="right:auto;left:6px"':'')+'>'+esc(e.amt)+' '+esc(e.when)+' <span aria-hidden="true">→</span></span>'});
  h+='</div></div>';
 });
 h+='<div class="today" style="left:calc(54px + (100% - 54px) * '+(asof/100).toFixed(4)+');top:22px"><span>as of '+esc(D.as_of)+'</span></div></div>';
 h+='<p class="cap" style="margin-top:8px">Bars span the month the filing names. The dot is an exact date. The dashed box shows the next maturity after this window.</p>';
 $('#clockBody').innerHTML=h;
 var q='<div class="qcards">';
 D.clocks.forEach(function(e){
  q+='<div class="qc"><div class="big">'+esc(e.amt)+'</div><div class="sub"><b>'+esc(e.tk)+'</b> · '+esc(e.what)+' · '+esc(e.when)+'</div>'+qhtml(e.quote,e.cid,e.period,'',e.label)+'</div>';
 });
 D.clocks_off.forEach(function(e){
  q+='<div class="qc off"><div class="big">'+esc(e.amt)+'</div><div class="sub"><b>'+esc(e.tk)+'</b> · '+esc(e.what)+' · '+esc(e.when)+' (after this window)</div>'+qhtml(e.quote,e.cid,e.period,'',e.label)+'</div>';
 });
 q+='</div>';
 $('#clockOff').innerHTML=q;
}

""")

rep("""  if(x.share27==null) h+=gapCell('gap',D.gapreason['BXP.ladder_y2_2027'],'2027 share',chip(t+'.ladder_y2_2027'));""",
    """  if(x.share27==null) h+=gapCell('gap',r.wall_gap,'2027 share',chip(t+'.ladder_y2_2027'));""")
rep("""(x.share26==null?'<span class="g"><b>gap</b></span> <span class="why">'+esc(D.gapreason['BXP.ladder_y2_2027'])+'</span>'""",
    """(x.share26==null?'<span class="g"><b>gap</b></span> <span class="why">'+esc(r.wall_gap)+'</span>'""")
rep("""  if(x.dd==null) h+=gapCell('gap',D.gapreason['OPI.drawdown_52w'],'Drawdown vs sector',chip(t+'.drawdown_52w'));""",
    """  if(x.dd==null) h+=gapCell('gap',r.dd_gap,'Drawdown vs sector',chip(t+'.drawdown_52w'));""")
rep("""  if(t==='OPI') gn='<span class="gn">market data gap: partial window, 99 closes since 2026-06-18</span>';\n""", "")
rep("""  var test=t==='OPI'?'<span class="pill">pipeline test, not live distress</span>':'';""",
    """  var test=t===D.pipeline_test?'<span class="pill">pipeline test, not live distress</span>':'';""")

rep("""var OVEV={OPI:['OPI.ev10.1.03'],SLG:['SLG.10q_2027_p0','SLG.10q_table_r2'],CBL:['CBL.ev15.2.03','CBL.ev10.2.03']};
var OVSUP={SLG:['SLG.mapping_check'],CBL:['CBL.y1_2026_share','CBL.latest_debt','CBL.latest_cash','CBL.printed_total'],OPI:[]};
var OVNAME={'Office Properties Income Trust':'OPI','SL Green':'SLG','CBL & Associates':'CBL'};
""", "")
rep("""  var t=OVNAME[o.name],x=ROW[t],rev=hr(o.claim_id)||hr(t+'.override');""",
    """  var t=o.ticker,x=ROW[t],rev=hr(t+'.override');""")
rep("""  (OVSUP[t].length?'<p class="small"><b>Supporting evidence:</b> '+OVSUP[t].map(chip).join('')+'</p>':'')+
  '<details><summary>Filing text behind it</summary>'+OVEV[t].map(function(id)""",
    """  (o.sup.length?'<p class="small"><b>Supporting evidence:</b> '+o.sup.map(chip).join('')+'</p>':'')+
  '<details><summary>Filing text behind it</summary>'+o.ev.filter(function(id){return C[id]}).map(function(id)""")

rep(""" if(tk==='ESRT'&&/^Latest 10-Q/.test(b.h)){
  h+='<blockquote class="q"><div class="qm">Debt table row mentioning 2027, $ thousands '+chip('ESRT.10q_debtrow0')+' <a href="'+esc(C['ESRT.10q_debtrow0'].src)+'" target="_blank" rel="noopener noreferrer">filing</a></div><p>'+esc(C['ESRT.10q_debtrow0'].claim.replace(/^\\s*/,''))+'</p></blockquote>';
 }
""", "")

rep(""" ['SLG','JBGS','ESRT'].forEach(function(tk){
  var c=D.cases[tk],x=ROW[tk],lad=D.ladders[tk];""",
    """ D.case_order.forEach(function(tk){
  var c=D.cases[tk],x=ROW[tk],lad=D.ladders[tk],HT=D.hero&&D.hero.tk===tk;""")
rep("""  if(tk==='SLG'){
   var q=D.q10.map(function(d){return {label:d.label.replace('2026 (remaining)','2026 rest').replace('Thereafter','Later'),claim:d.claim,v:d.total==null?null:d.total/1000,note:d.total==null?'the 10-Q row shows a dash in the total column, no consolidated principal listed':''}});
   max=Math.max(max,Math.max.apply(0,q.map(function(d){return d.v})));
   charts='<div class="grid2"><div><h4 style="margin-top:0">FY2025 10-K ladder (what the screen scores)</h4>'+ladderSVG(lad,max,{hot:1,aria:'SL Green 10-K debt maturity ladder',cap:'$M, 10-K filed 2026-02-17, as of 2025-12-31'})+'</div>'+
    '<div><h4 style="margin-top:0">Q3-2026 10-Q ladder (stale-ladder problem)</h4>'+ladderSVG(q,max,{hot:1,aria:'SL Green 10-Q debt maturity ladder, same scale',cap:'$M, 10-Q filed 2026-11-05, same scale, consolidated total column'})+
    '<p class="cap">2027 falls from $'+fmt1(lad[1].v)+'M to $'+fmt1(q[1].v)+'M after the March 2026 facility amendment. SLG\\'s share of joint-venture debt due 2027 is $'+fmt1(D.q10[1].jv/1000)+'M, outside the wall '+chip('SLG.10q_table_r2')+' '+chip('SLG.jv_debt_2027')+'</p></div></div>';""",
    """  if(HT){
   var H=D.hero,q=H.q10.map(function(d){return {label:d.label,claim:d.claim,v:d.total==null?null:d.total/1000,note:d.total==null?'the 10-Q row shows a dash in the total column, no consolidated principal listed':''}});
   max=Math.max(max,Math.max.apply(0,q.map(function(d){return d.v||0})));
   charts='<div class="grid2"><div><h4 style="margin-top:0">FY2025 10-K ladder (what the screen scores)</h4>'+ladderSVG(lad,max,{hot:1,aria:x.name+' 10-K debt maturity ladder',cap:H.k_cap})+'</div>'+
    '<div><h4 style="margin-top:0">Latest 10-Q ladder (same scale)</h4>'+ladderSVG(q,max,{hot:H.qhot,aria:x.name+' 10-Q debt maturity ladder, same scale',cap:H.q_cap})+
    '<p class="cap">'+rt(H.note)+'</p></div></div>';""")
rep("""  var price=tk==='SLG'?""", """  var price=HT?""")
rep("""  var pricenote=tk!=='SLG'?'':'';\n""", "")
rep("""+(tk==='SLG'?'':' hidden')+'><article""", """+(tk===D.case_order[0]?'':' hidden')+'><article""")
rep("""+(x.r.override?' <span class="pill ov">override: '+esc(x.r.override)+'</span><span class="pill pend">pending sign-off</span>':'')+(tk==='SLG'?' <span class="disag">disagreement: filings say risk, market calm</span>':'')+'</h3>'+""",
    """+(x.r.override?' <span class="pill ov">override: '+esc(x.r.override)+'</span><span class="pill pend">'+(hr(tk+'.override')?'human reviewed':'pending sign-off')+'</span>':'')+(x.r.disagreement?' <span class="disag">disagreement: '+esc(x.r.disagreement)+'</span>':'')+'</h3>'+""")
rep("""  if(tk==='SLG') h+='<details class="det" style="margin-top:6px">""", """  if(HT) h+='<details class="det" style="margin-top:6px">""")
rep("""  if(tk!=='SLG'){h+='<div class="small muted" """, """  if(!HT){h+='<div class="small muted" """)
rep(""" var tabs='<div class="tabs" role="tablist" aria-label="Case files">'+['SLG','JBGS','ESRT'].map(""",
    """ var tabs='<div class="tabs" role="tablist" aria-label="Case files">'+D.case_order.map(""")
rep("""['SLG','JBGS','ESRT'].forEach(function(t){document.getElementById('pane-'+t).hidden=t!==k})""",
    """D.case_order.forEach(function(t){document.getElementById('pane-'+t).hidden=t!==k})""")
rep(""" ['JBGS','ESRT'].forEach(function(tk){var el=document.getElementById('px-'+tk)""",
    """ D.case_order.forEach(function(tk){var el=document.getElementById('px-'+tk)""")

rep("""<b>5 of 12</b>""", """<b>'+D.checked_n+' of '+ROWS.length+'</b>""")
rep("""'<div class="stat pass"><span class="cap">Pipeline control</span><b>PASS</b>""",
    """'<div class="stat '+(D.control_pass?'pass':'')+'"><span class="cap">Pipeline control</span><b>'+(D.control_pass?'PASS':'FAIL')+'</b>""")
rep("""<li>Trigger 1: covenant headroom below 10%.</li><li>Trigger 2: the lender\\'s own facility matures within 12 months of the run date, 2026-11-09 (a date already past also counts).</li>""",
    """<li>Trigger 1: covenant headroom below '+OC.headroom_min+'%.</li><li>Trigger 2: the lender\\'s own facility matures within '+OC.months+' months of the run date, '+esc(D.as_of)+' (a date already past also counts).</li>""")
rep("""<li>These are assumptions. The thresholds come from the report\\'s overlay table, and config.toml [overlay] was not supplied, so the step size is not confirmed by a file.</li>""",
    """<li>These are assumptions, set in config.toml [overlay].</li>""")
rep("""$('#miniBody').innerHTML='<span><b>SLG 2027 principal</b> '+N(D.ladders.SLG[1].v)+' to '+N(D.q10[1].total/1000)+' ($M), 10-K to 10-Q</span><span class="sep hide-s" aria-hidden="true">|</span>'+""",
    """$('#miniBody').innerHTML=(D.hero?'<span><b>'+esc(D.hero.tk)+' '+esc(D.hero.year)+' principal</b> '+N(D.hero.ladder[D.hero.hot].v)+' to '+N(D.hero.q10[D.hero.qhot].total/1000)+' ($M), 10-K to 10-Q</span><span class="sep hide-s" aria-hidden="true">|</span>':'')+""")
repfn(""" var T={""", """ Object.keys(T)""", """ var T=D.takeaways;
""")
rep("""renderBanner();renderAnswer();renderClocks();""",
    """$('#hB').textContent=D.clock_title;$('#hD').textContent=D.case_title;
renderBanner();renderAnswer();renderClocks();""")
rep("""<h2 id="hB">Dated maturities, November 2026 to March 2027</h2>""", """<h2 id="hB"></h2>""")
rep("""<h2 id="hD">SL Green, JBG Smith, Empire State Realty Trust</h2>""", """<h2 id="hD"></h2>""")
rep("""<section class="hero" id="hero" aria-label="SL Green 2027 maturities, FY2025 10-K against Q3-2026 10-Q">""",
    """<section class="hero" id="hero" aria-label="Lead finding">""")
rep("""<title>REIT borrower screen, as of 2026-11-09</title>""", """<title>REIT Borrower Screen</title>""")
rep("""$('#screenFoot').textContent='Ladder as of 2025-12-31 (FY2025 10-K). 2027 share is the share of the six-bucket ladder. Prices are unofficial.';""",
    """$('#screenFoot').textContent=D.screen_foot;""")
rep("""It adds no analysis, makes no network calls and sends nothing anywhere.""",
    """It adds no analysis, makes no network calls and sends nothing anywhere. Data refreshed '+esc(D.refreshed)+'.""")

rep("""tipBtn('Drawdown vs sector','Close on 2026-11-06 against the 52-week high""", """tipBtn('Drawdown vs sector','Close on '+D.price_as_of+' against the 52-week high""")

# ---- quadrant chart: full width under the table, larger, no label collisions (review feedback)
rep("@media(min-width:1200px){.screenwrap{grid-template-columns:minmax(0,1fr) 330px}}",
    "#quad{max-width:980px}.quadchart text{font-size:13px}.quadchart .ax{font-size:12.5px}.quadchart .qlab{font-size:12.5px}.quadchart .pt text{font-weight:600}")
rep(" var L=live(),W=330,H=380,ml=46,mr=12,mt=14,mb=50,xmin=-16,xmax=26,ymin=0,ymax=70;",
    " var L=live(),W=900,H=470,ml=60,mr=16,mt=16,mb=58,xmin=-16,xmax=26,ymin=0,ymax=70;")
rep("""var s='<svg class="chart" viewBox="0 0 '+W+' '+H+'" role="group" aria-label="Chart of 2027""",
    """var s='<svg class="chart quadchart" viewBox="0 0 '+W+' '+H+'" role="group" aria-label="Chart of 2027""")
rep("""s+='<text class="qlab" x="'+(W-mr-6)+'" y="'+(yt+14)+'" text-anchor="end">Market singles out,</text><text class="qlab" x="'+(W-mr-6)+'" y="'+(yt+26)+'" text-anchor="end">filings below watch</text>';""",
    """s+='<text class="qlab" x="'+(W-mr-8)+'" y="'+(H-mb-24)+'" text-anchor="end">Market singles out,</text><text class="qlab" x="'+(W-mr-8)+'" y="'+(H-mb-9)+'" text-anchor="end">filings below watch</text>';""")
rep("shape(b,cx,cy,5)+'<circle class=\"ring\" cx=\"'+cx+'\" cy=\"'+cy+'\" r=\"10\"/>'",
    "shape(b,cx,cy,7)+'<circle class=\"ring\" cx=\"'+cx+'\" cy=\"'+cy+'\" r=\"13\"/>'")
rep("var LABPOS={SLG:[9,4,'start'],JBGS:[-9,4,'end'],ESRT:[9,4,'start'],CBL:[0,-10,'middle'],KRG:[9,4,'start'],AKR:[-9,4,'end'],PDM:[0,-10,'middle'],SPG:[9,4,'start'],CUZ:[9,4,'start'],BRX:[9,4,'start']};",
    "var LABPOS={SLG:[12,5,'start'],JBGS:[-13,5,'end'],ESRT:[12,5,'start'],CBL:[0,-13,'middle'],KRG:[12,5,'start'],AKR:[-12,5,'end'],PDM:[0,-13,'middle'],SPG:[12,5,'start'],CUZ:[12,5,'start'],BRX:[12,5,'start']};")

rep("(x.ub?'<path d=\"M'+cx+' '+(cy+8)+' v9 m-3 -3 l3 3 l3 -3\"", "(x.ub?'<path d=\"M'+cx+' '+(cy+11)+' v11 m-4 -4 l4 4 l4 -4\"")
# ---- honest human-review line, derived from signoff.csv counts (D.review)
rep(""" if(!D.signoff.length) b.innerHTML=warn+'<span>Overrides pending human sign-off.</span>';
 else b.innerHTML=warn+'<span>'+D.signoff.length+' claim(s) human reviewed. Other overrides remain pending human sign-off.</span>';""",
    """ var R=D.review,pend=D.overrides.filter(function(o){return !hr(o.ticker+'.override')}).length;
 b.innerHTML=warn+'<span>Human review: '+R.n+' of '+R.m+' claims human reviewed'+(R.n?'':' (none yet)')+'. '+(pend?pend+' of '+D.overrides.length+' overrides pending human sign-off.':'All overrides human reviewed.')+'</span>';""")
rep("""'<div class="stat"><span class="cap">Human sign-off (signoff.csv)</span><b>'+D.signoff.length+' claims</b><span class="small">'+(D.signoff.length?'Listed claims show human reviewed.':'No rows yet. Nothing is shown as human reviewed.')+'</span></div></div>';""",
    """'<div class="stat"><span class="cap">Human review (signoff.csv)</span><b>'+D.review.n+' of '+D.review.m+'</b><span class="small">claims human reviewed'+(D.review.n?'':' (none yet)')+'. Only ids listed in signoff.csv are shown as human reviewed.</span></div></div>';""")
# ---- claim panel: show the raw filing row when the displayed text was normalised
rep("""  '<dt>Source</dt><dd>'+srcLink(c.src)+'</dd>'+""",
    """  (c.raw?'<dt>Raw filing row</dt><dd><code>'+esc(c.raw)+'</code><br><span class="muted small">Empty cells are shown as n/a above.</span></dd>':'')+
  '<dt>Source</dt><dd>'+srcLink(c.src)+'</dd>'+""")

# ---- more names, 10-Q ladder and secured split (display only)
rep("""<h2 id="hC">All 12 names, ranked</h2>""", """<h2 id="hC"></h2>""")
rep("""is not one of the 12 screened names, so it was ignored.""", """is not one of the '+ROWS.length+' screened names, so it was ignored.""")
rep("""$('#hB').textContent=D.clock_title;""", """$('#hB').textContent=D.clock_title;$('#hC').textContent='All '+D.screen.length+' names, ranked';""")
rep("""+'<br><span class="muted small">$'+esc(x.wallM)+'M</span>'+chip(t+'.ladder_y2_2027')+'</td>';""",
    """+'<br><span class="muted small">$'+esc(x.wallM)+'M</span>'+chip(t+'.ladder_y2_2027')+(r.wallq?'<br><span class="muted small">'+esc(r.wallq)+'</span>'+(r.wallq_cid?chip(r.wallq_cid):''):'')+'</td>';""")
rep("""  h+='<td data-label="Flags and gaps">'+fl+""", """  if(r.secured) fl+='<span class="flag">'+esc(r.secured)+'</span>'+chip(t+'.secured_split');
  h+='<td data-label="Flags and gaps">'+fl+""")

# ---- quadrant labels: greedy non-overlapping placement (24 names crowd the fixed offsets)
rep("""  var cx=X(x.rel),cy=Y(x.share27),b=L[x.t].pub,lp=LABPOS[x.t]||[9,4,'start'];""",
    """  var cx=X(x.rel),cy=Y(x.share27),b=L[x.t].pub,lp=placeLabel(cx,cy,x.t);""")
rep(""" var np=[];
 ROWS.forEach(function(x){""", """ var np=[],placed=[];
 ROWS.forEach(function(x){if(x.share27!=null&&x.rel!=null)placed.push({x0:X(x.rel)-9,x1:X(x.rel)+9,y0:Y(x.share27)-9,y1:Y(x.share27)+9})});
 function placeLabel(cx,cy,t){
  var w=t.length*8.2+2,h=14,C2=[[12,5,'start'],[-12,5,'end'],[0,-13,'middle'],[0,24,'middle'],[12,-9,'start'],[-12,-9,'end'],[12,19,'start'],[-12,19,'end']];
  for(var i=0;i<C2.length;i++){var c=C2[i],x0=c[2]==='start'?cx+c[0]:c[2]==='end'?cx+c[0]-w:cx-w/2,y0=cy+c[1]-11,r={x0:x0,x1:x0+w,y0:y0,y1:y0+h};
   if(r.x0<ml||r.x1>W-mr||r.y0<mt||r.y1>H-mb)continue;
   if(!placed.some(function(p){return r.x0<p.x1&&r.x1>p.x0&&r.y0<p.y1&&r.y1>p.y0})){placed.push(r);return c}}
  return [12,5,'start'];
 }
 ROWS.forEach(function(x){""")

# ---- ladder-check stat split into 10-K and 10-Q (review feedback: 10-Q ladders are not 10-K text)
rep("""'<div class="stat"><span class="cap">Ladders checked against 10-K text</span><b>'+D.checked_n+' of '+ROWS.length+'</b><span class="small">'+esc(D.checked_names)+'</span></div>'+""",
    """'<div class="stat"><span class="cap">10-K ladders checked against 10-K text</span><b>'+D.ladder_counts.k_checked+' of '+D.ladder_counts.k_total+'</b><span class="small">'+D.ladder_counts.no_k+' of '+ROWS.length+' names file no 10-K ladder tags. Checked: '+esc(D.checked_names)+'</span></div>'+
 '<div class="stat"><span class="cap">10-Q ladders checked against 10-Q text</span><b>'+D.ladder_counts.q_checked+' of '+D.ladder_counts.q_total+'</b><span class="small">Display only, never scored. Year mapping confirmed against the 10-K for '+D.ladder_counts.q_confirmed+' of '+D.ladder_counts.q_total+'.</span></div>'+""")

(HERE / "template.html").write_text(s)
left = re.findall(r"'(?:SLG|JBGS|ESRT|CBL|OPI|BXP)'|2026-11-09|2026,10|2026-11-0[56]", s.split("__DATA__")[1])
print("template written; hard-coded specifics left in the script:", left)
