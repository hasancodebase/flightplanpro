// Usage: node scripts/make-nasr.js <folder containing AWY_BASE.csv, FIX_BASE.csv, NAV_BASE.csv, DP_BASE.csv, STAR_BASE.csv>
const fs=require('fs');
function csv(f){const t=fs.readFileSync(f,'utf8'),rows=[];let r=[],c='',q=false;for(let i=0;i<t.length;i++){const ch=t[i];if(q){if(ch=='"'){if(t[i+1]=='"'){c+='"';i++}else q=false}else c+=ch}else if(ch=='"')q=true;else if(ch==','){r.push(c);c=''}else if(ch=='\n'||ch=='\r'){if(ch=='\r'&&t[i+1]=='\n')i++;r.push(c);c='';if(r.length>1||r[0])rows.push(r);r=[]}else c+=ch}if(c||r.length){r.push(c);rows.push(r)}const h=rows.shift();return rows.map(x=>Object.fromEntries(h.map((k,i)=>[k,x[i]])))}
const d=process.argv[2]||'.',pf=f=>d+'/'+f;
for(const f of ['FIX_BASE.csv','NAV_BASE.csv','AWY_BASE.csv']){if(!fs.existsSync(pf(f))){console.log('Missing '+f+' in '+d);process.exit(1)}}
const pts={};let cyc='';const add=(id,la,lo)=>{la=parseFloat(la);lo=parseFloat(lo);if(!id||isNaN(la)||isNaN(lo))return;(pts[id]=pts[id]||[]).push([la,lo])};
for(const r of csv(pf('FIX_BASE.csv'))){add(r.FIX_ID,r.LAT_DECIMAL,r.LONG_DECIMAL);cyc=cyc||r.EFF_DATE}
for(const r of csv(pf('NAV_BASE.csv')))add(r.NAV_ID,r.LAT_DECIMAL,r.LONG_DECIMAL);
const dd=(a,b)=>Math.hypot(a[0]-b[0],(a[1]-b[1])*Math.cos(a[0]*Math.PI/180)),aw=[];let miss=0;
for(const r of csv(pf('AWY_BASE.csv'))){let seg=[],prev=null;const flush=()=>{if(seg.length>1)aw.push([r.AWY_ID,seg]);seg=[]};
for(const n of(r.AIRWAY_STRING||'').trim().split(/\s+/)){const c=pts[n];if(!c){miss++;flush();prev=null;continue}let b=c[0];if(prev)b=c.reduce((m,x)=>dd(prev,x)<dd(prev,m)?x:m,c[0]);prev=b;seg.push([n,+b[0].toFixed(3),+b[1].toFixed(3)])}flush()}
const pr={};function proc(file,col,k,pick){if(!fs.existsSync(pf(file)))return;for(const r of csv(pf(file))){const nm=pick((r[col]||'').split('.'));if(!nm)continue;for(const a of(r.SERVED_ARPT||'').trim().split(/\s+/)){if(!a)continue;const o=pr[a]=pr[a]||{d:[],s:[]};if(!o[k].includes(nm))o[k].push(nm)}}}
proc('DP_BASE.csv','DP_COMPUTER_CODE','d',c=>c[0]);proc('STAR_BASE.csv','STAR_COMPUTER_CODE','s',c=>c[1]||c[0]);for(const a in pr){pr[a].d.sort();pr[a].s.sort()}
fs.mkdirSync('data',{recursive:true});fs.writeFileSync('data/airways.json',JSON.stringify({cycle:cyc,a:aw}));fs.writeFileSync('data/procs.json',JSON.stringify(pr));
console.log(aw.length+' airway segments written to data/airways.json ('+Math.round(fs.statSync('data/airways.json').size/1024)+' KB), cycle '+cyc+'; '+miss+' points not found');
console.log(Object.keys(pr).length+' airports with procedures written to data/procs.json');
