/* Siembra 70 dias de datos de prueba para el usuario activo (peso, pasos, agua, creatina,
   movilidad, entrenos segun S.week, comida de los ultimos 21 dias, check-ins, medidas y Hyrox).
   Correr en el Chrome de pruebas (perfil propio, nunca el telefono de nadie) con Runtime.evaluate,
   una vez por usuario: ACTIONS._doSwitch('andres') y luego ACTIONS._doSwitch('cami'). Usado en el
   analisis UX del 14/10/2026. */
(()=>{
  const t=TODAY(), N=70, r0=addDays(t,-(N-1)), A=UID==='andres';
  let seed=A?7:13; const rnd=(a,b)=>{ seed=(seed*9301+49297)%233280; return a+(seed/233280)*(b-a); };
  // peso: baja con ruido, saltando dias
  S.weights=[]; let kg=A?94.4:59.6;
  for(let i=0;i<N;i++){ if(rnd(0,1)<0.72 || i===N-1){ S.weights.push({d:addDays(r0,i), kg:Math.round((kg+rnd(-.35,.35))*10)/10}); } kg-= A?rnd(0.02,0.12):rnd(-0.01,0.04); }
  S.steps={}; S.water={}; S.creat={}; S.mobil={};
  for(let i=0;i<N-1;i++){ const d=addDays(r0,i); S.steps[d]=Math.round(rnd(4200,13500)); S.water[d]=Math.round(rnd(6,15))*250; if(rnd(0,1)<.85) S.creat[d]=1; if(rnd(0,1)<.3) S.mobil[d]=1; }
  S.steps[t]=3870; S.water[t]=1000;
  // entrenos segun la semana del usuario
  S.sessions=[]; S.logs={};
  const rs=ROUTINES_VIS();
  for(let i=0;i<N-1;i++){
    const d=addDays(r0,i), dow=new Date(d+'T12:00:00').getDay(), rid=S.week[dow];
    const r=rs.find(x=>x.id===rid); if(!r) continue;
    if(rnd(0,1)<.18) continue; // se salto el dia
    S.sessions.push({d, rid:r.id});
    const wk=Math.floor(i/7);
    r.ex.forEach(e=>{
      const reps=Array.isArray(e.reps)?e.reps:[8,12];
      const base=A?({bench:60,shpress:45,row:65,pullup:5,hack:90,lpress:160,dip:10,incmach:50,pullup2:0,rowuni:25,rdl:80,hip:100}[e.id]||22):({hipthrust_bb:60,rdl_bb:40}[e.id]||14);
      const w=Math.round((base+wk*(e.inc||1.25)*(wk>6?0.3:1))*2)/2;
      (S.logs[e.id]=S.logs[e.id]||[]).push({d, sets:Array.from({length:e.sets||3},()=>({w, r:Math.round(rnd(reps[0],reps[1]))}))});
    });
  }
  // comida loggeada (catalogo real NFOODS)
  const F=id=>NFOODS.find(f=>f[0]===id);
  const pick=(ids)=>ids.map(([id,q])=>{ const f=NFOODS.find(x=>x[0]===id)||NFOODS[0]; const kc=Math.round((f[4]*4+f[5]*4+f[6]*9)*q); return {n:f[1], q, u:f[3], id:f[0], pg:Math.round(f[4]*q), cg:Math.round(f[5]*q), fg:Math.round(f[6]*q), kc}; });
  const ids=NFOODS.map(f=>f[0]);
  const prot=NFOODS.filter(f=>f[4]>=15).map(f=>f[0]);
  const carb=NFOODS.filter(f=>f[5]>=20 && f[4]<10).map(f=>f[0]);
  S.nlog={};
  for(let i=N-21;i<N;i++){
    const d=addDays(r0,i), isT=(d===t);
    const day=[];
    day.push({s:'m', ts:Date.parse(d+'T08:10:00'), items:pick([['cafele',1],[prot[Math.floor(rnd(0,prot.length))],1],[carb[Math.floor(rnd(0,carb.length))],1]])});
    if(!isT){
      day.push({s:'t', ts:Date.parse(d+'T13:20:00'), items:pick([[prot[Math.floor(rnd(0,prot.length))],A?2:1.5],[carb[Math.floor(rnd(0,carb.length))],1.5]])});
      if(rnd(0,1)<.8) day.push({s:'n', ts:Date.parse(d+'T19:40:00'), items:pick([[prot[Math.floor(rnd(0,prot.length))],A?1.8:1.2],[carb[Math.floor(rnd(0,carb.length))],1]])});
    }
    S.nlog[d]=day;
  }
  // check-ins semanales
  S.checkins=[];
  for(let w=8;w>=1;w--){ const d=addDays(t,-w*7+1); const wkg=(S.weights.filter(x=>x.d<=d).slice(-1)[0]||{kg:kg}).kg; S.checkins.push({d, kg:wkg, cint:A?(96-(8-w)*0.5):(72-(8-w)*0.15), cad:A?104:101, adh:Math.round(rnd(70,95)), ene:Math.round(rnd(3,5)), sue:Math.round(rnd(2,5)), notas:''}); }
  // medidas cada 3 semanas
  const base=Object.values(S.medidas)[0];
  [21,42,63].forEach((off,j)=>{ const d=addDays(base.fecha,off); if(d>t) return; const m={...base, fecha:d}; m.peso=(S.weights.filter(x=>x.d<=d).slice(-1)[0]||{kg:base.peso}).kg; m.cintura=+(base.cintura-(j+1)*(A?0.9:0.3)).toFixed(1); m.cuello=+(base.cuello-(j+1)*0.1).toFixed(1); m.pecho=+(base.pecho-(j+1)*(A?0.6:0.1)).toFixed(1); S.medidas[d]=m; });
  // hyrox: algunas marcas
  S.hyrox=[{d:addDays(t,-30),est:'ski',seg:A?282:318},{d:addDays(t,-9),est:'ski',seg:A?271:309},{d:addDays(t,-16),est:'row',seg:A?268:301},{d:addDays(t,-12),est:'sledpush',seg:A?150:170}];
  ['weights','steps','water','creat','mobil','sessions','logs','nlog','checkins','medidas','hyrox'].forEach(k=>save(k));
  return JSON.stringify({uid:UID, w:S.weights.length, ses:S.sessions.length, logs:Object.keys(S.logs).length, nlog:Object.keys(S.nlog).length, med:Object.keys(S.medidas).length});
})()
