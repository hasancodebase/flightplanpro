const W={MI:'shallow',BC:'patches of',PR:'partial',DR:'drifting',BL:'blowing',SH:'showers of',TS:'thunderstorm with',FZ:'freezing',DZ:'drizzle',RA:'rain',SN:'snow',SG:'snow grains',IC:'ice crystals',PL:'ice pellets',GR:'hail',GS:'small hail',UP:'unknown precipitation',BR:'mist',FG:'fog',FU:'smoke',VA:'volcanic ash',DU:'dust',SA:'sand',HZ:'haze',PY:'spray',PO:'dust whirls',SQ:'squalls',FC:'funnel cloud',SS:'sandstorm',DS:'duststorm'},CL={FEW:'few',SCT:'scattered',BKN:'broken',OVC:'overcast',VV:'vertical visibility'};
function dec(s){const t=s.trim().toUpperCase().split(/\s+/),o=[],add=(a,b)=>o.push([a,b]);let ceil=1e9,vis=99;
for(let i=0;i<t.length;i++){const x=t[i];let m;
if(/^(METAR|SPECI|AUTO|COR)$/.test(x))continue;
if(!o.length&&/^[A-Z]{4}$/.test(x)){add('Station',x);continue}
if(m=x.match(/^(\d\d)(\d\d)(\d\d)Z$/)){add('Observed','day '+m[1]+', '+m[2]+':'+m[3]+' UTC');continue}
if(m=x.match(/^(VRB|\d{3})(P?\d{2,3})(?:G(\d{2,3}))?(KT|MPS)$/)){add('Wind',(m[1]=='VRB'?'variable':'from '+m[1]+'°')+' at '+(+m[2].replace('P',''))+(m[3]?', gusting '+m[3]:'')+(m[4]=='KT'?' kt':' m/s'));continue}
if(/^\d{3}V\d{3}$/.test(x)){add('Wind varying',x.replace('V','° to ')+'°');continue}
if(x=='CAVOK'){add('Visibility and cloud','10 km or more, no significant cloud (CAVOK)');vis=10;continue}
if(/^\d{4}$/.test(x)){const v=+x;add('Visibility',v>=9999?'10 km or more':v+' m');vis=v/1609;continue}
if(m=x.match(/^(P?)(\d+(?:\/\d+)?)SM$/)){let n=m[2].includes('/')?m[2].split('/').reduce((a,b)=>a/b):+m[2];if(i&&/^\d+$/.test(t[i-1]))n+=+t[i-1];add('Visibility',(m[1]?'more than ':'')+n.toFixed(1)+' SM');vis=n;continue}
if(m=x.match(/^(FEW|SCT|BKN|OVC|VV)(\d{3})(CB|TCU)?$/)){const h=m[2]*100;add('Cloud',CL[m[1]]+' at '+h+' ft'+(m[3]?(m[3]=='CB'?' (cumulonimbus)':' (towering cumulus)'):''));if(m[1]!='FEW'&&m[1]!='SCT')ceil=Math.min(ceil,h);continue}
if(/^(SKC|CLR|NSC|NCD)$/.test(x)){add('Cloud','no significant cloud');continue}
if(m=x.match(/^(M?\d\d)\/(M?\d\d)?$/)){const f=v=>v?+v.replace('M','-'):null;add('Temperature / dew point',f(m[1])+' °C / '+(f(m[2])===null?'n/a':f(m[2])+' °C'));continue}
if(m=x.match(/^Q(\d{4})$/)){add('Pressure (QNH)',+m[1]+' hPa');continue}
if(m=x.match(/^A(\d{4})$/)){add('Altimeter',(m[1]/100).toFixed(2)+' inHg');continue}
if(/^(RMK|TEMPO|BECMG|NOSIG)$/.test(x)){add(x=='NOSIG'?'Trend':x,x=='NOSIG'?'no significant change':t.slice(i+1).join(' ')||'none');break}
if(m=x.match(/^([-+]|VC)?((?:MI|BC|PR|DR|BL|SH|TS|FZ|DZ|RA|SN|SG|IC|PL|GR|GS|UP|BR|FG|FU|VA|DU|SA|HZ|PY|PO|SQ|FC|SS|DS)+)$/)){add('Weather',({'-':'light ','+':'heavy ',VC:'nearby '}[m[1]]||'')+m[2].match(/../g).map(c=>W[c]).join(' '));continue}
if(/^R\d/.test(x))add('Runway visual range',x)}
add('Flight category',ceil<500||vis<1?'LIFR':ceil<1000||vis<3?'IFR':ceil<=3000||vis<=5?'MVFR':'VFR');return o}
function taf(s){const P=s.replace(/\s+/g,' ').trim().split(/ (?=FM\d{6}|PROB\d\d|(?<!PROB\d\d )(?:BECMG|TEMPO) )/);return P.map((p,i)=>{let h='Base forecast',r=p;if(i){const k=p.match(/^(FM\d{6}|(?:PROB\d\d )?(?:BECMG|TEMPO) \d{4}\/\d{4}|PROB\d\d \d{4}\/\d{4})/);if(k){h=k[1];r=p.slice(h.length)}}else{const v=p.match(/\d{4}\/\d{4}/);if(v)h='Base forecast, valid '+v[0]}return[h,(R=>R.filter(x=>x[0]!='Flight category'||R.some(y=>/^(Visib|Cloud)/.test(y[0]))))(dec(r).map(x=>x[0]=='Observed'?['Issued',x[1]]:x))]})}
