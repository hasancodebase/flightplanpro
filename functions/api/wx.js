const OK=/^[A-Z0-9]{3,4}$/;
export async function onRequestGet({request,waitUntil}){
const u=new URL(request.url),t=u.searchParams.get('t')==='taf'?'taf':'metar';
const ids=(u.searchParams.get('ids')||'').toUpperCase().split(',').filter(x=>OK.test(x)).slice(0,6).sort();
if(!ids.length)return new Response('[]',{status:400,headers:{'Content-Type':'application/json'}});
const key=new Request(u.origin+'/api/wx?t='+t+'&ids='+ids.join(',')),c=caches.default;
let r=await c.match(key);
if(!r){
const up=await fetch('https://aviationweather.gov/api/data/'+t+'?format=json&ids='+ids.join(',')+(t==='metar'?'&hours=3':''),{headers:{'User-Agent':'FlightPlanPro/1.0 (https://flightplanpro.pages.dev)'}});
const body=up.ok?((await up.text())||'[]'):'[]';
r=new Response(body,{status:up.ok?200:502,headers:{'Content-Type':'application/json','Cache-Control':'public, max-age='+(up.ok?300:20),'Access-Control-Allow-Origin':'*'}});
if(up.ok)waitUntil(c.put(key,r.clone()));
}
return r}
