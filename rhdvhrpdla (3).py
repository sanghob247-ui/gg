"""AFTER BELL — 1인칭 학교 탈출 게임.

배포: GitHub 저장소에 app.py와 requirements.txt를 올린 뒤
Streamlit Community Cloud에서 app.py를 메인 파일로 선택합니다.
실행: streamlit run app.py

맵/입체 캐릭터/효과음은 이 파일에 포함됩니다.
3D 라이브러리(Three.js)는 게임 시작 시 공개 CDN에서 불러오므로 인터넷이 필요합니다.
게임 로직은 방문자의 브라우저에서 실행되어 사용자별 플레이가 분리됩니다.
"""

from io import BytesIO
from urllib.parse import urlsplit

try:
    import qrcode
    from PIL import Image as _PillowImage
except ImportError:
    qrcode = None
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="AFTER BELL 3D | 학교 탈출",
    page_icon="🔑",
    layout="wide",
    initial_sidebar_state="collapsed",
)
st.markdown(
    """<style>
    .stApp { background: #080c12; color: #edf3fa; }
    .block-container { padding-top: 1rem; padding-bottom: 1rem; max-width: 1200px; }
    header[data-testid="stHeader"] { background: transparent; }
    </style>""",
    unsafe_allow_html=True,
)

GAME_HTML = r'''
<!DOCTYPE html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,user-scalable=no"><style>
*{box-sizing:border-box}html,body{margin:0;background:#090f18;color:#f0f5fc;font-family:system-ui,'Apple SD Gothic Neo',sans-serif}button{font-family:inherit;cursor:pointer}#app{height:780px;position:relative;overflow:hidden;border:1px solid #314256;border-radius:18px;background:#0b1624;touch-action:none}#view{position:absolute;inset:0}canvas{display:block;width:100%;height:100%}.overlay{position:absolute;inset:0;background:radial-gradient(ellipse at 80% 15%,#254350,#0b1524 65%);z-index:10;overflow:auto;padding:32px 24px}.panel{max-width:740px;margin:0 auto}.label{font-size:11px;letter-spacing:4px;color:#84f3ca;margin-bottom:16px}h1{font-size:clamp(32px,6vw,58px);line-height:1.15;margin:12px 0 20px}h2{font-size:23px}p{font-size:14px;line-height:1.85;color:#c5d2e1}.accent{color:#86f3ce}.cards{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin:22px 0}.card{border:1px solid #3e5065;background:#152539bb;padding:16px;border-radius:14px;font-size:13px;line-height:1.8}.card b{display:block;color:#f4f7fc;margin-bottom:4px}.main{border:0;background:#89edcb;color:#09281f;padding:17px 22px;border-radius:12px;font-size:15px;font-weight:900}.secondary{border:1px solid #53687f;background:#1b2c41;color:#edf4ff;padding:13px 18px;border-radius:12px}.row{display:flex;gap:12px;align-items:center;flex-wrap:wrap}.small{font-size:11px;color:#adbed1}.hide{display:none!important}#hud{position:absolute;inset:0;pointer-events:none}.top{display:flex;gap:7px;align-items:center;padding:13px}.badge{background:#0b1829dd;border:1px solid #526277;padding:8px 10px;border-radius:10px;font-size:12px}.brand{color:#88efca;letter-spacing:2px;font-weight:850}.grow{flex:1}.click{pointer-events:auto;color:#fff;cursor:pointer}#hint{text-align:center;padding:0 18px;font-size:13px;text-shadow:0 2px 6px black}#toast{position:absolute;top:100px;left:50%;transform:translateX(-50%);width:min(90%,560px);padding:12px 16px;border:1px solid #82d6bb;background:#0a172aef;border-radius:12px;text-align:center;font-size:13px;display:none}#cross{position:absolute;top:48%;left:50%;color:#ffffff88}#inventory{position:absolute;bottom:160px;left:12px;right:12px;display:flex;justify-content:center;gap:5px;flex-wrap:wrap}.key{font-size:11px;border:1px solid #657388;border-radius:7px;padding:5px 8px;background:#0b1629d9;color:#acb9cc}.have{border-color:#ffd36f;color:#ffe09d}.bad{opacity:.45;text-decoration:line-through}#status{position:absolute;bottom:137px;width:100%;text-align:center;font-size:11px;color:#e0eafa}.controls{position:absolute;bottom:17px;left:14px;right:14px;display:flex;justify-content:space-between;align-items:flex-end;gap:8px;pointer-events:none}.pad{display:grid;grid-template-columns:49px 49px 49px;grid-template-rows:48px 48px;gap:5px}.control{pointer-events:auto;touch-action:none;user-select:none;-webkit-user-select:none;background:#14263be8;border:1px solid #94a6bf;border-radius:12px;color:white;font-size:18px;font-weight:800}.control:active{background:#3b806f}.actions{display:flex;gap:7px;align-items:flex-end}.action{height:61px;font-size:13px;padding:0 15px;border-color:#88efca}.run{height:48px;font-size:12px;padding:0 12px}#edge{position:absolute;inset:0;pointer-events:none;box-shadow:inset 0 0 95px #d93640;opacity:0}#cabinet{position:absolute;inset:0;pointer-events:none;display:none;background:repeating-linear-gradient(90deg,#17221c 0,#17221c 27%,#101911 27.3%,#1e2c22 28%,#17221c 29%);box-shadow:inset 0 0 150px #000}#cabinet:before{content:'';position:absolute;left:18%;right:18%;top:27%;height:22%;background:repeating-linear-gradient(#09130d 0px,#09130d 10px,#293b2d 11px,#293b2d 24px);border:8px solid #202e24;box-shadow:0 4px 15px #000}#cabinetText{position:absolute;top:55%;left:15%;right:15%;text-align:center;line-height:1.9;color:#c1cbbb;font-size:14px}#grab{display:none;position:absolute;bottom:25%;width:100%;text-align:center;font-size:clamp(26px,6vw,48px);font-weight:900;color:#fff;text-shadow:0 3px 10px #611;pointer-events:none}#map{position:absolute;right:15px;top:105px;width:170px;height:108px;border:1px solid #7b91aa;border-radius:8px;background:#061321cf;display:none}.options{display:flex;gap:15px;flex-wrap:wrap;margin:18px 0;font-size:13px}.alert{padding:12px;border:1px solid #ba8b59;border-radius:10px;color:#e8d1ad;font-size:12px;line-height:1.7}@media(max-width:520px){.overlay{padding:25px 18px}.cards{gap:8px}.card{padding:12px;font-size:12px}.badge{font-size:10px;padding:7px}.top{gap:4px;padding:10px}.brand{letter-spacing:1px}.action{padding:0 10px}.run{padding:0 8px}.pad{grid-template-columns:45px 45px 45px}.controls{left:10px;right:10px}#map{width:130px;height:82px}}
#cabinet{background:linear-gradient(to bottom,#18251d 0%,#18251d 38%,transparent 38%,transparent 45%,#18251d 45%,#18251d 100%);box-shadow:inset 0 0 65px #000}#cabinet:before{left:0;right:0;top:38%;height:7%;background:linear-gradient(to right,#18251d 0%,#18251d 20%,transparent 20%,transparent 80%,#18251d 80%,#18251d 100%);border:0;box-shadow:inset 0 4px 5px #000,inset 0 -4px 5px #000}#cabinetText{top:61%}#grab{background:#26050ab8;padding:18px 0} </style></head><body><div id="app"><div id="view"></div><div id="edge"></div><div id="cabinet"><div id="cabinetText">청소도구함 안에 숨었습니다.<br>문은 닫혔습니다. 환기 구멍으로 복도를 살펴보세요.<br><span class="small">발소리가 멀어진 뒤 조사 버튼으로 나오세요.</span></div></div><div id="grab">거기! 딱 걸렸어!</div>
<div id="hud" class="hide"><div class="top"><span class="badge brand">AFTER BELL 3D</span><span class="badge" id="time">00:00</span><span class="badge" id="keyCount">열쇠 0/10</span><span class="grow"></span><button id="pause" class="badge click">일시정지</button></div><div id="hint"></div><div id="toast" role="status" aria-live="polite"></div><div id="cross">＋</div><canvas id="map" width="390" height="230"></canvas><div id="inventory"></div><div id="status"></div><div class="controls"><div class="pad"><span></span><button class="control" data-hold="forward" aria-label="전진">▲</button><span></span><button class="control" data-hold="left" aria-label="왼쪽 회전">↶</button><button class="control" data-hold="back" aria-label="후진">▼</button><button class="control" data-hold="right" aria-label="오른쪽 회전">↷</button></div><div class="actions"><button class="control run" id="runToggle" aria-pressed="false">🏃 달리기 OFF</button><button class="control action" id="interact">조사 / 숨기</button></div></div></div>
<section id="intro" class="overlay"><div class="panel"><div class="label">AFTER BELL · 3D ESCAPE</div><h1>쌤이 온다.<br><span class="accent">들키기 전에 탈출해.</span></h1><p>🔑 열쇠를 찾고　🚪 출입문을 열어라.<br>👣 가까워지는 소리? 청소도구함에 숨어!</p><div class="row"><button class="main" id="toGuide">준비하기 →</button></div><p class="small">이어폰 권장 · 놀람 연출 있음</p></div></section>
<section id="guide" class="overlay hide"><div class="panel"><div class="label">READY?</div><h1>소리를 듣고,<br>뛰거나 숨어.</h1><p><b>PC</b> W/S 이동 · A/D 회전 · Shift 달리기 · E 조사<br><b>폰</b> 방향 버튼 이동 · 달리기 버튼을 켠 뒤 이동<br>🟩 청소도구함에서 조사 → 숨기 / 나오기</p><div class="options"><label><input type="checkbox" id="soundOpt" checked> 오싹한 소리</label><label><input type="checkbox" id="scareOpt" checked> 깜짝 연출</label><label><input type="checkbox" id="easyOpt"> 쉬운 모드 + 지도</label></div><div class="row"><button class="main" id="start">게임 시작</button><button class="secondary" id="backIntro">← 돌아가기</button></div><p class="small" id="loadState"></p></div></section>
<section id="paused" class="overlay hide"><div class="panel"><div class="label">PAUSED</div><h1>잠깐, 숨 고르기.</h1><p>이동·추격·시간이 모두 멈췄습니다.</p><div class="row"><button class="main" id="resume">계속하기</button><button class="secondary" id="returnIntro">소개 화면으로</button></div></div></section>
<section id="result" class="overlay hide"><div class="panel"><div class="label" id="resultLabel"></div><h1 id="resultTitle"></h1><p id="resultText"></p><div class="row"><button class="main" id="again">다시 준비하기</button><button class="secondary" id="resultIntro">게임 소개</button></div></div></section></div>
<script>
'use strict';
const $=id=>document.getElementById(id),inputs={forward:false,back:false,left:false,right:false,run:false};
let T,renderer,scene,camera,teacher,teacherParts,clockLast=0,state='intro',elapsed=0,p,t,keys=[],held=new Set(),tried=new Set(),correct=1,hidden=false,stamina=100,grace=0,aiTimer=0,route=[],searchTime=0,lastSight=0,stepTime=0,playerStep=0,toastUntil=0,sound=false,scare=true,easy=false,audio=null,noise=null,loading=null,catchTimer=0;
let hideTransition=0,activeCloset=null,hideFacing=0,hideStart=null,aiMood=0,aiMoodTime=0,lastKnown=null;
let runLatched=false,exhausted=false,spawnWarmup=0,horrorClock=0,horrorNodes=null;
const WIDTH=39,HEIGHT=23,grid=Array.from({length:HEIGHT},()=>Array(WIDTH).fill(1));
function carve(x1,z1,x2,z2){for(let z=z1;z<=z2;z++)for(let x=x1;x<=x2;x++)grid[z][x]=0;}
carve(1,10,37,13); // broad, straight central school corridor
const rooms=[];
for(let i=0;i<4;i++){let x=2+i*8;carve(x,2,x+5,8);carve(x+2,9,x+3,9);rooms.push({x:x+2.5,z:5.5,name:`${i+1}학년 ${i+1}반`,kind:'class',side:'north',left:x});}
for(let i=0;i<4;i++){let x=2+i*8;carve(x,15,x+5,21);carve(x+2,14,x+3,14);rooms.push({x:x+2.5,z:18.5,name:i===0?'교무실':i===1?'음악실':`${i+1}학년 ${i+1}반`,kind:i===0?'office':i===1?'music':'class',side:'south',left:x});}
carve(34,2,37,8);carve(35,9,36,9);rooms.push({x:35.8,z:5.5,name:'남자 화장실',kind:'toilet',side:'north',left:34});
carve(34,15,37,21);carve(35,14,36,14);rooms.push({x:35.8,z:18.5,name:'여자 화장실',kind:'toilet',side:'south',left:34});
const exit={x:1.45,z:11.5},closets=[{x:8.5,z:10.55},{x:16.5,z:13.40},{x:24.5,z:10.55},{x:32.5,z:13.40}],obstacles=[];
const distance=(a,b)=>Math.hypot(a.x-b.x,a.z-b.z);
function wall(x,z){return !grid[Math.floor(z)]||grid[Math.floor(z)][Math.floor(x)]!==0;}
function free(x,z){let r=.23;if(wall(x-r,z-r)||wall(x+r,z-r)||wall(x-r,z+r)||wall(x+r,z+r))return false;return !obstacles.some(o=>x>o.x-o.w/2-r&&x<o.x+o.w/2+r&&z>o.z-o.d/2-r&&z<o.z+o.d/2+r);}
function move(o,dx,dz){if(free(o.x+dx,o.z))o.x+=dx;if(free(o.x,o.z+dz))o.z+=dz;}
function sight(a,b){const d=distance(a,b);for(let k=.12;k<d;k+=.12)if(wall(a.x+(b.x-a.x)*k/d,a.z+(b.z-a.z)*k/d))return false;return true;}
function bfs(a,b){const sx=Math.floor(a.x),sz=Math.floor(a.z),tx=Math.floor(b.x),tz=Math.floor(b.z),s=sz*WIDTH+sx,g=tz*WIDTH+tx,queue=[s],prev=new Map([[s,null]]);let head=0;while(head<queue.length){const v=queue[head++];if(v===g)break;for(const [dx,dz]of [[1,0],[-1,0],[0,1],[0,-1]]){const x=v%WIDTH+dx,z=Math.floor(v/WIDTH)+dz,n=z*WIDTH+x;if(x<0||z<0||x>=WIDTH||z>=HEIGHT||grid[z][x]||prev.has(n)||!free(x+.5,z+.5))continue;prev.set(n,v);queue.push(n);}}if(!prev.has(g))return [];let result=[],v=g;while(v!==s){result.push({x:v%WIDTH+.5,z:Math.floor(v/WIDTH)+.5});v=prev.get(v);}return result.reverse();}
function chooseTarget(away=false){const candidates=[];for(let z=10;z<=13;z++)for(let x=3;x<37;x++)if(free(x+.5,z+.5)&&(!away||distance(p,{x:x+.5,z:z+.5})>14))candidates.push({x:x+.5,z:z+.5});return candidates[Math.floor(Math.random()*candidates.length)]||{x:35.5,z:11.5};}
function notify(text){$('toast').textContent=text;$('toast').style.display='block';toastUntil=performance.now()+3500;}
function clearInputs(){Object.keys(inputs).forEach(k=>inputs[k]=false);runLatched=false;syncRun();}
function syncRun(){const b=$('runToggle');b.textContent=runLatched?'🏃 달리기 ON':'🏃 달리기 OFF';b.setAttribute('aria-pressed',String(runLatched));b.style.background=runLatched?'#347c66':'';}
function loadThree(){if(window.THREE)return Promise.resolve(window.THREE);if(loading)return loading;loading=new Promise((resolve,reject)=>{const urls=['https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.min.js','https://unpkg.com/three@0.160.0/build/three.min.js'];function attempt(i){if(i>=urls.length){loading=null;reject(Error('3D 화면을 불러오지 못했습니다. 인터넷 연결을 확인하고 다시 시작해 주세요.'));return;}const script=document.createElement('script');script.src=urls[i];let done=false;const timer=setTimeout(()=>{if(!done){done=true;attempt(i+1);}},15000);script.onload=()=>{if(done)return;done=true;clearTimeout(timer);if(window.THREE)resolve(window.THREE);else attempt(i+1);};script.onerror=()=>{if(done)return;done=true;clearTimeout(timer);attempt(i+1);};document.head.appendChild(script);}attempt(0);});return loading;}
function mat(color,extra={}){return new T.MeshLambertMaterial({color,...extra});}
function box(w,h,d,color,x,y,z,parent=scene,extra={}){const mesh=new T.Mesh(new T.BoxGeometry(w,h,d),mat(color,extra));mesh.position.set(x,y,z);parent.add(mesh);return mesh;}
function ball(rx,ry,rz,color,x,y,z,parent){const m=new T.Mesh(new T.SphereGeometry(1,20,14),mat(color));m.scale.set(rx,ry,rz);m.position.set(x,y,z);parent.add(m);return m;}
function label(text,bg='#eef1e8',fg='#17342b',w=2,h=.42){const c=document.createElement('canvas');c.width=768;c.height=128;const q=c.getContext('2d');q.fillStyle=bg;q.fillRect(0,0,c.width,c.height);q.fillStyle=fg;q.textAlign='center';q.textBaseline='middle';q.font='bold 67px sans-serif';q.fillText(text,384,67,735);const tex=new T.CanvasTexture(c);tex.colorSpace=T.SRGBColorSpace;return new T.Mesh(new T.PlaneGeometry(w,h),new T.MeshBasicMaterial({map:tex,side:T.DoubleSide}));}
function addSign(text,x,y,z,north=true,w=2){const s=label(text,undefined,undefined,w);s.position.set(x,y,z);if(!north)s.rotation.y=Math.PI;scene.add(s);return s;}
function floorTexture(){const c=document.createElement('canvas');c.width=c.height=256;const q=c.getContext('2d');q.fillStyle='#bcc5bf';q.fillRect(0,0,256,256);q.strokeStyle='#9ca9a5';q.lineWidth=3;q.strokeRect(0,0,256,256);q.beginPath();q.moveTo(128,0);q.lineTo(128,256);q.moveTo(0,128);q.lineTo(256,128);q.stroke();const tex=new T.CanvasTexture(c);tex.wrapS=tex.wrapT=T.RepeatWrapping;tex.repeat.set(WIDTH/2,HEIGHT/2);tex.colorSpace=T.SRGBColorSpace;return tex;}
function makeDesk(x,z,office=false){box(.94,.10,.68,office?0x76624b:0xb78b57,x,.78,z);for(const dx of [-.36,.36])for(const dz of [-.23,.23])box(.045,.73,.045,0x5d6870,x+dx,.36,z+dz);box(.52,.08,.45,0x99734d,x,.46,z+.58);box(.52,.46,.07,0x99734d,x,.73,z+.80); // furniture is solid and shares navigation collision
obstacles.push({x,z:z+.15,w:1.03,d:1.48});}
function makeToilet(room){const north=room.side==='north',back=north?2.5:20.5;for(let i=0;i<2;i++){let x=34.85+i*1.65;box(.07,2.1,2.3,0x809ba3,x-.72,1.05,back+(north?.7:-.7));box(1.35,1.75,.08,0xa4bec3,x,.95,back+(north?1.85:-1.85));ball(.27,.19,.37,0xf0f4f1,x,.42,back+(north?.5:-.5),scene);box(.52,.62,.20,0xe5ecec,x,.62,back+(north?-.03:.03));obstacles.push({x,z:back+(north?.5:-.5),w:1.45,d:2.5});}for(let i=0;i<2;i++){const x=37.48,z=(north?6.65:15.8)+i*1.35;box(.56,.14,.85,0xe1ebec,x,.92,z);box(.07,.6,.55,0x8bc4cf,37.80,1.65,z);box(.04,.23,.04,0x707d84,x,1.08,z);obstacles.push({x,z,w:.65,d:.9});}}
function makeCloset(c){const g=new T.Group();g.position.set(c.x,0,c.z);if(c.z>12)g.rotation.y=Math.PI;scene.add(g);const color=0x3d6352;box(1.12,2.55,.07,color,0,1.275,-.29,g);box(.07,2.55,.64,color,-.525,1.275,0,g);box(.07,2.55,.64,color,.525,1.275,0,g);box(1.12,.07,.64,color,0,.035,0,g);box(1.12,.07,.64,color,0,2.515,0,g);box(.035,2.05,.035,0x9c7747,-.25,1.1,-.10,g);box(.36,.18,.13,0x6d785b,-.25,.20,-.10,g);box(.035,2.20,.035,0xac9766,.23,1.18,-.12,g);const hinge=new T.Group();hinge.position.set(-.51,0,.35);g.add(hinge);c.hinge=hinge;box(.99,2.36,.06,0x496c55,.51,1.28,0,hinge);c.group=g;box(.035,2.25,.04,0x263b2d,0,1.28,.39,g);for(let i=0;i<5;i++)box(.31,.025,.025,0x233b2c,-.24,1.95-i*.08,.395,g);for(let i=0;i<5;i++)box(.31,.025,.025,0x233b2c,.24,1.95-i*.08,.395,g);box(.035,.21,.05,0xcac2a5,.09,1.15,.42,g);box(.035,.21,.05,0xcac2a5,-.09,1.15,.42,g);const s=label('청소도구함','#dddcc8','#263d2d',.83,.18);s.position.set(0,1.50,.393);g.add(s);box(1.20,.09,.77,0x263a2e,0,2.59,0,g);obstacles.push({x:c.x,z:c.z,w:1.2,d:.8});}
function makeTeacher(){const root=new T.Group();scene.add(root);const skin=0xcda58b,cream=0xc6c3a5,blue=0x205c80,hair=0x382b25,brown=0x614634;const body=box(.77,.78,.37,cream,0,1.20,0,root);box(.20,.78,.40,blue,-.30,1.20,.015,root);box(.20,.78,.40,blue,.30,1.20,.015,root);box(.76,.10,.41,0x3b2923,0,.79,.0,root);box(.13,.095,.025,0xc3a64d,0,.79,.225,root);
for(let i=0;i<3;i++)ball(.022,.022,.015,0x5c5c50,0,1.36-i*.16,.203,root);
const bowL=ball(.105,.075,.04,0xb73529,-.09,1.51,.255,root);bowL.rotation.z=-.35;const bowR=ball(.105,.075,.04,0xb73529,.09,1.51,.255,root);bowR.rotation.z=.35;ball(.045,.06,.045,0xb73529,0,1.51,.27,root);
const head=new T.Group();head.position.y=1.90;root.add(head);ball(.305,.395,.285,skin,0,0,.015,head);ball(.075,.115,.05,skin,-.315,-.025,0,head);ball(.075,.115,.05,skin,.315,-.025,0,head);ball(.065,.23,.19,hair,-.26,.12,-.055,head);ball(.065,.23,.19,hair,.26,.12,-.055,head);
for(const x of [-.12,.12]){ball(.085,.055,.038,0xece8df,x,.035,.272,head);ball(.026,.032,.020,0x37291f,x,.025,.310,head);ball(.010,.012,.008,0xffffff,x-.008,.04,.328,head);const brow=box(.19,.045,.045,hair,x,.145,.265,head);brow.rotation.z=x<0?-.20:.20;}
ball(.065,.12,.105,skin,0,-.045,.29,head);ball(.18,.17,.038,hair,0,-.23,.235,head);ball(.10,.09,.045,skin,0,-.18,.269,head);ball(.085,.038,.028,0x652c28,0,-.19,.31,head);ball(.10,.037,.038,hair,-.075,-.11,.29,head);ball(.10,.037,.038,hair,.075,-.11,.29,head);
const arms=[],legs=[];for(const side of [-1,1]){const a=new T.Group();a.position.set(side*.46,1.50,0);a.rotation.z=side*.25;root.add(a);box(.23,.35,.29,cream,0,-.12,0,a);box(.15,.43,.17,skin,0,-.48,0,a);ball(.11,.14,.075,skin,0,-.75,.02,a);arms.push(a);const leg=new T.Group();leg.position.set(side*.19,.78,0);root.add(leg);box(.28,.65,.30,brown,0,-.29,0,leg);ball(.17,.12,.27,0x342e2b,0,-.68,.09,leg);legs.push(leg);}return {root,head,arms,legs};}
function buildScene(){T=window.THREE;scene=new T.Scene();scene.background=new T.Color(0x91a8ac);scene.fog=new T.Fog(0x91a8ac,22,55);camera=new T.PerspectiveCamera(72,1,.055,75);camera.rotation.order='YXZ';renderer=new T.WebGLRenderer({antialias:true,powerPreference:'high-performance'});renderer.setPixelRatio(Math.min(window.devicePixelRatio||1,1.5));renderer.outputColorSpace=T.SRGBColorSpace;renderer.setClearColor(0x91a8ac);$('view').appendChild(renderer.domElement);scene.add(new T.HemisphereLight(0xe8f4ff,0x6b6653,2.1));const sun=new T.DirectionalLight(0xfff1d8,2.0);sun.position.set(-8,16,-7);scene.add(sun);
box(WIDTH,.12,HEIGHT,0xffffff,WIDTH/2,-.08,HEIGHT/2,scene,{map:floorTexture()});box(WIDTH,.12,HEIGHT,0xe2e9e5,WIDTH/2,3.25,HEIGHT/2);
// Merge adjacent wall cells into horizontal runs to reduce phone draw calls.
for(let z=0;z<HEIGHT;z++){let x=0;while(x<WIDTH){if(!grid[z][x]){x++;continue;}const start=x;while(x<WIDTH&&grid[z][x])x++;const n=x-start;box(n,3.2,1,0xdce1d5,start+n/2,1.6,z+.5);box(n,1.0,1.018,0x87a69b,start+n/2,.51,z+.5);box(n,.10,1.03,0x4f7568,start+n/2,1.05,z+.5);box(n,.09,1.04,0x637469,start+n/2,.045,z+.5);}}
// Ceiling fixtures and school noticeboards along an ordinary straight corridor.
for(let x=4;x<38;x+=6){box(1.8,.06,.55,0xffffff,x,3.14,11.5,scene,{emissive:0xaebfaf,emissiveIntensity:.6});}
addSign('← 출입문 / EXIT',3.5,2.55,10.03,true,3.0);
for(const r of rooms){const north=r.side==='north',doorX=r.kind==='toilet'?36:r.left+3;addSign(r.name,doorX,2.58,north?9.97:14.03,north,r.kind==='toilet'?2.3:2.1);box(.10,2.35,.15,0x8b6946,doorX-1.04,1.17,north?9.5:14.5);box(.10,2.35,.15,0x8b6946,doorX+1.04,1.17,north?9.5:14.5);if(r.kind==='toilet'){makeToilet(r);continue;}
const boardZ=north?2.035:21.965;box(3.9,1.25,.07,0x285445,r.left+2.9,1.88,boardZ);addSign(r.kind==='music'?'음악과 함께하는 하루':'오늘도 즐거운 학교',r.left+2.9,2.0,boardZ+(north?.05:-.05),north,3.0);
// Desks leave a broad center aisle from the door to the key.
for(const x of [r.left+1.0,r.left+4.7])for(const z of (north?[4.4,6.6]:[17.2,19.4]))makeDesk(x,z,r.kind==='office');
if(r.kind==='music'){box(1.7,.9,.65,0x302b28,r.left+2.7,.45,20.8);box(1.55,.08,.37,0xeee8d9,r.left+2.7,.82,20.39);obstacles.push({x:r.left+2.7,z:20.8,w:1.7,d:.7});}
// Opaque framed blue window panels — no invisible room walls.
const winZ=north?1.985:22.015;for(const x of [r.left+1.3,r.left+4.3]){box(1.5,1.12,.035,0x8fbed0,x,1.95,winZ,scene,{emissive:0x3f6576,emissiveIntensity:.22});box(.055,1.15,.07,0xeeeeea,x,1.95,winZ);box(1.55,.055,.07,0xeeeeea,x,1.95,winZ);}}
closets.forEach(makeCloset);
// Locked school exit on the western end wall, facing into the corridor.
const door=box(.12,2.65,2.25,0x245d81,.99,1.325,11.5);box(.17,.13,.34,0xd8bd69,1.10,1.12,11.7);const exitSign=label('출입문 · EXIT','#dbece6','#205b48',2.0,.38);exitSign.rotation.y=Math.PI/2;exitSign.position.set(1.08,2.9,11.5);scene.add(exitSign);
teacherParts=makeTeacher();teacher=teacherParts.root;
window.addEventListener('resize',resize);resize();setupPointer(renderer.domElement);}
function resize(){if(!renderer)return;const r=$('app').getBoundingClientRect();renderer.setSize(r.width,r.height);camera.aspect=r.width/r.height;camera.updateProjectionMatrix();}
function makeKey(id,pos){const g=new T.Group();const gold=new T.MeshStandardMaterial({color:0xffcb42,metalness:.6,roughness:.3,emissive:0x8b5100,emissiveIntensity:.30});const ring=new T.Mesh(new T.TorusGeometry(.14,.04,7,18),gold);ring.position.x=-.12;g.add(ring);const shaft=new T.Mesh(new T.BoxGeometry(.35,.065,.065),gold);shaft.position.x=.15;g.add(shaft);for(const x of [.18,.29]){const tooth=new T.Mesh(new T.BoxGeometry(.055,.13,.06),gold);tooth.position.set(x,-.06,0);g.add(tooth);}g.position.set(pos.x,.72,pos.z);const tag=label(String(id).padStart(2,'0'),'#f2e5be','#624214',.32,.16);tag.position.set(0,.34,0);g.add(tag);scene.add(g);return {...pos,id,mesh:g,taken:false};}
function disposeKey(k){scene.remove(k.mesh);k.mesh.traverse(o=>{if(o.geometry)o.geometry.dispose();if(o.material){if(o.material.map)o.material.map.dispose();o.material.dispose();}});}
function reset(){keys.forEach(disposeKey);const nums=Array.from({length:10},(_,i)=>i+1);for(let i=9;i>0;i--){const j=Math.floor(Math.random()*(i+1));[nums[i],nums[j]]=[nums[j],nums[i]];}keys=rooms.map((r,i)=>makeKey(nums[i],{x:r.x,z:r.kind==='toilet'?(r.side==='north'?6.2:17.8):r.z}));correct=1+Math.floor(Math.random()*10);held=new Set();tried=new Set();p={x:3.2,z:11.5,a:Math.PI/2};t={x:28.5,z:5.5,mode:'patrol',target:null};elapsed=0;stamina=100;exhausted=false;spawnWarmup=10;horrorClock=0;grace=3;aiTimer=0;route=[];searchTime=0;lastSight=0;hidden=false;hideTransition=0;activeCloset=null;aiMoodTime=0;aiMood=0;lastKnown=null;closets.forEach(c=>{if(c.hinge)c.hinge.rotation.y=0;});stepTime=0;playerStep=0;catchTimer=0;clearInputs();$('cabinet').style.display='none';$('grab').style.display='none';$('edge').style.opacity='0';for(const id of ['intro','guide','paused','result'])$(id).classList.add('hide');$('hud').classList.remove('hide');$('map').style.display=easy?'block':'none';state='playing';refreshKeys();notify('Shift 또는 🏃 버튼으로 달리기 · 쌤은 먼 교실에서 출발합니다.');}
function refreshKeys(){$('inventory').innerHTML=Array.from({length:10},(_,i)=>`<span class="key ${held.has(i+1)?'have':''} ${tried.has(i+1)?'bad':''}">${String(i+1).padStart(2,'0')}</span>`).join('');$('keyCount').textContent=`열쇠 ${held.size}/10`;}
function interact(){if(state!=='playing'||hideTransition>0)return;if(hidden){hidden=false;if(activeCloset&&activeCloset.hinge)activeCloset.hinge.rotation.y=0;activeCloset=null;grace=1.5;$('cabinet').style.display='none';notify('함에서 나왔습니다. 쌤의 발소리를 확인하세요.');return;}
const closet=closets.filter(c=>distance(p,c)<1.65&&sight(p,c)).sort((a,b)=>distance(p,a)-distance(p,b))[0];if(closet){hidden=true;hideTransition=1.5;activeCloset=closet;hideStart={x:p.x,z:p.z,a:p.a};hideFacing=closet.z<12?Math.PI:0;runLatched=false;syncRun();t.mode='search';searchTime=10;t.target=chooseTarget(true);route=bfs(t,t.target);aiTimer=1;clearInputs();tone(155,.55,.06,'triangle',62);notify('문을 열고 들어가는 중… 닫힌 뒤 환기 구멍으로 살펴보세요.');return;}
if(distance(p,exit)<1.85){const pending=[...held].filter(k=>!tried.has(k));if(!pending.length){notify(held.size?'시험하지 않은 열쇠가 없습니다. 다른 방을 찾아보세요.':'문이 잠겼습니다. 방에서 열쇠를 찾아오세요.');return;}if(pending.includes(correct)){tone(660,.4,.07);finish(true);return;}pending.forEach(k=>tried.add(k));refreshKeys();tone(125,.2,.05,'square');notify(pending.map(k=>k+'번').join(', ')+' 열쇠는 맞지 않습니다. 다른 열쇠를 찾아보세요.');return;}
const k=keys.filter(k=>!k.taken&&distance(p,k)<1.5&&sight(p,k)).sort((a,b)=>distance(p,a)-distance(p,b))[0];if(k){k.taken=true;k.mesh.visible=false;held.add(k.id);refreshKeys();tone(800,.18,.06);notify(k.id+'번 열쇠 획득! 출입문에서 맞춰보세요.');return;}notify('대상 가까이 다가가세요. 열쇠·청소도구함·출입문을 조사할 수 있습니다.');}
function setupAudio(){try{audio=audio||new(window.AudioContext||window.webkitAudioContext)();audio.resume();if(!noise){noise=audio.createBuffer(1,Math.floor(audio.sampleRate*.2),audio.sampleRate);const data=noise.getChannelData(0);for(let i=0;i<data.length;i++)data[i]=(Math.random()*2-1)*(1-i/data.length);}}catch(e){sound=false;}}
function tone(freq,duration,vol,type='sine',end=null){if(!sound||!audio||audio.state!=='running')return;const o=audio.createOscillator(),g=audio.createGain(),at=audio.currentTime;o.type=type;o.frequency.setValueAtTime(freq,at);if(end)o.frequency.exponentialRampToValueAtTime(end,at+duration);g.gain.setValueAtTime(.001,at);g.gain.linearRampToValueAtTime(vol,at+.012);g.gain.exponentialRampToValueAtTime(.001,at+duration);o.connect(g);g.connect(audio.destination);o.start();o.stop(at+duration+.03);}
function scareSound(){if(!sound||!audio||audio.state!=='running')return;const at=audio.currentTime;const count=Math.floor(audio.sampleRate*1.25),buf=audio.createBuffer(1,count,audio.sampleRate),data=buf.getChannelData(0);for(let i=0;i<count;i++){const tm=i/audio.sampleRate,envelope=Math.exp(-tm*3.2);data[i]=((Math.random()*2-1)*.6+Math.sin(tm*1700+Math.sin(tm*65)*7)*.4)*envelope;}const src=audio.createBufferSource(),filter=audio.createBiquadFilter(),g=audio.createGain();src.buffer=buf;filter.type='bandpass';filter.frequency.setValueAtTime(1700,at);filter.frequency.exponentialRampToValueAtTime(330,at+1.15);filter.Q.value=.85;g.gain.value=.17;src.connect(filter);filter.connect(g);g.connect(audio.destination);src.start();tone(65,.9,.15,'sine',26);tone(460,1.1,.05,'sawtooth',115);}
function setupHorror(){if(!sound||!audio||horrorNodes)return;const gain=audio.createGain(),filter=audio.createBiquadFilter();gain.gain.value=0;filter.type='lowpass';filter.frequency.value=420;filter.connect(gain);gain.connect(audio.destination);const oscillators=[];for(const f of [47,50.7,94.8]){const o=audio.createOscillator();o.type='triangle';o.frequency.value=f;o.connect(filter);o.start();oscillators.push(o);}horrorNodes={gain,filter,oscillators};}
function silenceHorror(){if(horrorNodes&&audio)horrorNodes.gain.gain.setTargetAtTime(0,audio.currentTime,.07);}
function updateHorror(dt,d){if(!sound||!audio||audio.state!=='running')return;setupHorror();const near=Math.max(0,Math.min(1,(14-d)/12)),v=near*(hidden?.28:1);horrorNodes.gain.gain.setTargetAtTime(v*.065,audio.currentTime,.18);horrorNodes.filter.frequency.setTargetAtTime(150+near*400,audio.currentTime,.2);horrorClock-=dt;if(near>0&&horrorClock<=0){horrorClock=1.55-near*.98;tone(56,.16,v*.10,'sine',35);setTimeout(()=>{if(state==='playing')tone(49,.13,v*.07,'sine',32);},150);if(d<8&&!hidden){tone(184+near*35,.65,v*.014,'sine',160);tone(196+near*35,.7,v*.012,'triangle',172);}}}
function foot(d,isTeacher){if(!sound||!audio||!noise||audio.state!=='running')return;const src=audio.createBufferSource(),f=audio.createBiquadFilter(),g=audio.createGain();src.buffer=noise;f.type='lowpass';f.frequency.value=isTeacher?420:170;g.gain.value=isTeacher?Math.min(.23,.8/(d+1)):.035;src.connect(f);f.connect(g);g.connect(audio.destination);src.start();tone(isTeacher?70:48,.1,isTeacher?Math.min(.12,.45/(d+1)):.025);}
function finish(ok){state=ok?'won':'lost';clearInputs();$('grab').style.display='none';$('resultLabel').textContent=ok?'ESCAPED / 탈출 성공':'CAUGHT / 쌤에게 잡혔다';$('resultTitle').textContent=ok?'드디어, 학교 밖으로.':'다음에는 숨을 곳을 기억하자.';$('resultText').textContent=ok?`${fmt(elapsed)} 만에 탈출! 정답은 ${correct}번 열쇠. 찾은 열쇠는 ${held.size}/10개입니다.`:'발소리가 빨라지면 가까운 초록색 청소도구함으로 이동해서 조사하세요. 쉬운 모드를 켜면 쌤이 느려지고 안내 지도가 표시됩니다.';$('result').classList.remove('hide');}
function caught(){if(state!=='playing')return;clearInputs();if(!scare){finish(false);return;}state='caught';catchTimer=0;$('grab').style.display='block';tone(250,.8,.085,'sawtooth',580);tone(450,.8,.045,'sawtooth',160);tone(780,.6,.025,'triangle',340);scareSound();}
function pause(){if(state==='playing'){state='paused';clearInputs();$('paused').classList.remove('hide');}else if(state==='paused'){state='playing';$('paused').classList.add('hide');if(sound)setupAudio();}}
function fmt(s){return String(Math.floor(s/60)).padStart(2,'0')+':'+String(Math.floor(s%60)).padStart(2,'0');}
function update(dt){elapsed+=dt;grace=Math.max(0,grace-dt);const d=distance(p,t);aiMoodTime-=dt;if(aiMoodTime<=0){aiMood=Math.random();aiMoodTime=.8+Math.random()*1.5;}if(hideTransition>0){hideTransition=Math.max(0,hideTransition-dt);const progress=1-hideTransition/1.5;if(activeCloset&&activeCloset.hinge)activeCloset.hinge.rotation.y=-Math.sin(progress*Math.PI)*1.65;if(progress<.45){p.a=Math.atan2(activeCloset.x-p.x,-(activeCloset.z-p.z));}else{p.a=hideFacing;}if(progress>.85)$('cabinet').style.display='block';if(hideTransition===0)tone(85,.18,.08,'triangle');}if(!hidden){p.a+=(Number(inputs.right)-Number(inputs.left))*dt*1.8;const moving=Number(inputs.forward)-Number(inputs.back),run=(inputs.run||runLatched)&&moving!==0&&!exhausted&&stamina>0,speed=run?4.7:2.35;move(p,Math.sin(p.a)*moving*speed*dt,-Math.cos(p.a)*moving*speed*dt);stamina=Math.max(0,Math.min(100,stamina+(run?-19:15)*dt));if(stamina<=0)exhausted=true;if(exhausted&&stamina>=28)exhausted=false;if(moving){playerStep+=dt;if(playerStep>(run?.26:.46)){foot(0,false);playerStep=0;}}if(run&&spawnWarmup===0&&d<12&&t.mode!=='chase'){t.mode='search';searchTime=5;t.target={x:p.x,z:p.z};lastKnown={...t.target};aiTimer=0;}}
spawnWarmup=Math.max(0,spawnWarmup-dt);const sees=spawnWarmup===0&&!hidden&&d<(easy?10:15)&&sight(t,p);if(sees){t.mode='chase';const lead=aiMood>.40&&(inputs.forward||inputs.back)?1.8:0,sign=inputs.back?-1:1;const predicted={x:p.x+Math.sin(p.a)*lead*sign,z:p.z-Math.cos(p.a)*lead*sign};t.target=free(predicted.x,predicted.z)&&sight(t,predicted)?predicted:{x:p.x,z:p.z};lastSight=elapsed;lastKnown={x:p.x,z:p.z};searchTime=0;}else if(t.mode==='chase'&&elapsed-lastSight>1.2){t.mode='search';searchTime=7;t.target=lastKnown?{...lastKnown}:chooseTarget();aiTimer=0;}
if(t.mode==='search'){searchTime-=dt;if(searchTime<=0){t.mode='patrol';t.target=null;}}
if(spawnWarmup>0){t.target={x:28.5,z:5.5};route=[];}else if(!t.target||distance(t,t.target)<.4){if(t.mode==='search'&&!hidden&&lastKnown){const spots=[];for(let z=-3;z<=3;z++)for(let x=-3;x<=3;x++){const q={x:Math.floor(lastKnown.x)+x+.5,z:Math.floor(lastKnown.z)+z+.5};if(free(q.x,q.z)&&distance(t,q)>1)spots.push(q);}t.target=spots[Math.floor(Math.random()*spots.length)]||chooseTarget();}else t.target=chooseTarget(hidden);}aiTimer-=dt;if(aiTimer<=0){route=spawnWarmup>0?[]:bfs(t,t.target);aiTimer=t.mode==='chase'?.32:1.1;}
const next=route[0];if(next){const d=distance(t,next),speed=t.mode==='chase'?(easy?2.15:(aiMood>.72?3.85:aiMood<.20?2.4:3.05)):(easy?1.0:(aiMood<.12?.25:1.5)),step=Math.min(d,speed*dt);if(d>.001){move(t,(next.x-t.x)/d*step,(next.z-t.z)/d*step);teacher.rotation.y=Math.atan2(next.x-t.x,next.z-t.z);}if(d<.13)route.shift();}
if(!hidden&&grace===0&&distance(p,t)<.8&&sight(p,t))caught();stepTime+=dt;if(d<14&&stepTime>(t.mode==='chase'?.26:.59)){foot(d,true);stepTime=0;}
updateHorror(dt,d);$('time').textContent=fmt(elapsed);$('hint').textContent=hidden?'숨는 중 · 환기 구멍으로 쌤이 멀어지는지 확인하세요.':t.mode==='chase'?'🏃 쌤이 달려옵니다! 초록색 청소도구함으로 숨으세요!':d<7?'👣 가까운 곳에서 무거운 발소리…':d<15?'👣 복도에서 쌤의 발소리가 들립니다.':'교실·교무실·음악실·화장실에서 열쇠를 찾으세요.';
$('status').textContent=hidden?'문틈으로 복도를 확인 · 조사 버튼으로 나오기':`체력 ${Math.round(stamina)}% · ${exhausted?'숨 고르기… 체력 회복 중':(inputs.run||runLatched)?'🏃 달리기 준비 / 이동하면 질주':'Shift 또는 🏃 버튼으로 달리기'}`;$('edge').style.opacity=!hidden&&t.mode==='chase'?String(Math.max(.12,1-d/16)*.6):'0';
if(easy)drawMap();}
function drawMap(){const c=$('map').getContext('2d');c.clearRect(0,0,390,230);for(let z=0;z<HEIGHT;z++)for(let x=0;x<WIDTH;x++){c.fillStyle=grid[z][x]?'#516474':'#142838';c.fillRect(x*10,z*10,10,10);}for(const r of rooms){c.fillStyle='#e1ede9';c.font='9px sans-serif';c.textAlign='center';c.fillText(r.kind==='toilet'?'WC':r.kind==='office'?'교무실':r.kind==='music'?'음악실':r.name,r.x*10,r.z*10);}c.fillStyle='#f8da74';for(const k of keys)if(!k.taken)c.fillRect(k.x*10-2,k.z*10-2,4,4);c.fillStyle='#6bbfe9';c.fillRect(exit.x*10-3,exit.z*10-5,6,10);c.fillStyle='#80f5cc';c.beginPath();c.arc(p.x*10,p.z*10,4,0,Math.PI*2);c.fill();c.strokeStyle='#80f5cc';c.beginPath();c.moveTo(p.x*10,p.z*10);c.lineTo((p.x+Math.sin(p.a))*10,(p.z-Math.cos(p.a))*10);c.stroke();}
function render(dt){if(!renderer||!p)return;if(state==='caught'){catchTimer+=dt;teacher.position.set(t.x,0,t.z);teacher.rotation.y=Math.atan2(p.x-t.x,p.z-t.z);const dx=Math.sin(teacher.rotation.y),dz=Math.cos(teacher.rotation.y),d=1.5-Math.min(1,catchTimer*2)*.72;camera.position.set(t.x+dx*d,1.98,t.z+dz*d);camera.lookAt(t.x,1.95,t.z);teacherParts.arms[0].rotation.x=-1.15;teacherParts.arms[1].rotation.x=-1.15;if(catchTimer>1.6)finish(false);}else{camera.position.set(p.x,1.65+(!hidden&&state==='playing'&&(inputs.forward||inputs.back)?Math.sin(elapsed*11)*.025:0),p.z);camera.rotation.set(0,-p.a,0);if(hidden&&hideTransition===0&&activeCloset){camera.position.set(activeCloset.x,1.65,activeCloset.z+(activeCloset.z<12?.53:-.53));camera.rotation.set(0,-hideFacing,0);}teacher.position.set(t.x,0,t.z);const stride=state==='playing'?Math.sin(elapsed*(t.mode==='chase'?14:8))*.5:0;teacherParts.legs[0].rotation.x=stride;teacherParts.legs[1].rotation.x=-stride;teacherParts.arms[0].rotation.x=-stride*.8;teacherParts.arms[1].rotation.x=stride*.8;}
for(const k of keys)if(!k.taken){k.mesh.rotation.y=elapsed*.85;k.mesh.position.y=.78+Math.sin(elapsed*2+k.id)*.08;}
renderer.render(scene,camera);}
function loop(now){if(state!=='playing')silenceHorror();const dt=Math.min(.05,(now-clockLast)/1000||.016);clockLast=now;if(state==='playing')update(dt);if(now>toastUntil)$('toast').style.display='none';render(dt);requestAnimationFrame(loop);}requestAnimationFrame(loop);
function setupPointer(canvas){let drag=null;canvas.addEventListener('pointerdown',e=>{if(state==='playing'){drag={id:e.pointerId,x:e.clientX};canvas.setPointerCapture(e.pointerId);}});canvas.addEventListener('pointermove',e=>{if(drag&&drag.id===e.pointerId&&state==='playing'&&!hidden){p.a+=(e.clientX-drag.x)*.005;drag.x=e.clientX;}});for(const name of ['pointerup','pointercancel'])canvas.addEventListener(name,()=>drag=null);}
const keymap={KeyW:'forward',ArrowUp:'forward',KeyS:'back',ArrowDown:'back',KeyA:'left',ArrowLeft:'left',KeyD:'right',ArrowRight:'right',ShiftLeft:'run',ShiftRight:'run'};
window.addEventListener('keydown',e=>{if(keymap[e.code]){e.preventDefault();if(state==='playing')inputs[keymap[e.code]]=true;}if(e.repeat)return;if(e.code==='KeyE'||e.code==='Space'){e.preventDefault();interact();}if(e.code==='KeyP'||e.code==='Escape')pause();});window.addEventListener('keyup',e=>{if(keymap[e.code])inputs[keymap[e.code]]=false;});
document.querySelectorAll('[data-hold]').forEach(btn=>{const k=btn.dataset.hold;btn.addEventListener('pointerdown',e=>{e.preventDefault();if(state!=='playing')return;btn.setPointerCapture(e.pointerId);inputs[k]=true;});for(const name of ['pointerup','pointercancel','lostpointercapture'])btn.addEventListener(name,()=>inputs[k]=false);});
window.addEventListener('blur',()=>{clearInputs();if(state==='playing')pause();});document.addEventListener('visibilitychange',()=>{if(document.hidden&&state==='playing')pause();});
function showIntro(){clearInputs();state='intro';for(const id of ['guide','paused','result','hud'])$(id).classList.add('hide');$('intro').classList.remove('hide');$('cabinet').style.display='none';$('edge').style.opacity='0';$('grab').style.display='none';}
$('toGuide').onclick=()=>{$('intro').classList.add('hide');$('guide').classList.remove('hide');state='guide';};$('backIntro').onclick=showIntro;$('returnIntro').onclick=showIntro;$('resultIntro').onclick=showIntro;
$('start').onclick=async()=>{const b=$('start');b.disabled=true;b.textContent='3D 학교 준비 중…';sound=$('soundOpt').checked;scare=$('scareOpt').checked;easy=$('easyOpt').checked;if(sound)setupAudio();try{await loadThree();if(!renderer)buildScene();reset();$('loadState').textContent='';}catch(e){$('loadState').textContent='화면 준비 실패: '+e.message+' WebGL 지원 브라우저(최신 Chrome/Safari)를 사용해 주세요.';}finally{b.disabled=false;b.textContent='게임 시작';}};
$('runToggle').onclick=()=>{if(state!=='playing'||hidden)return;runLatched=!runLatched;syncRun();};$('interact').onclick=interact;$('pause').onclick=pause;$('resume').onclick=pause;$('again').onclick=()=>{$('result').classList.add('hide');$('guide').classList.remove('hide');$('hud').classList.add('hide');$('edge').style.opacity='0';state='guide';};
</script></body></html>
'''

components.html(GAME_HTML, height=800, scrolling=False)

with st.expander("📱 QR로 친구 초대 / 배포 안내"):
    st.markdown(
        "**QR은 배포된 게임 주소를 여는 링크입니다.** 별도 앱 설치 없이 "
        "휴대폰 브라우저에서 플레이할 수 있습니다.\n\n"
        "1. GitHub 저장소에 `app.py`, `requirements.txt` 두 파일을 업로드합니다.\n"
        "2. [Streamlit Community Cloud](https://share.streamlit.io/)에서 "
        "GitHub 저장소를 연결하고 메인 파일을 `app.py`로 지정해 배포합니다.\n"
        "3. 배포 완료 후 나온 **공개 HTTPS 주소**를 아래에 붙여 넣습니다.\n"
        "4. 생성된 QR 이미지를 다운로드해 게시하거나 공유합니다."
    )
    public_url = st.text_input(
        "배포된 앱의 공개 주소",
        placeholder="https://your-game.streamlit.app",
        help="예시 주소가 아니라 실제 배포 완료된 주소를 입력하세요. localhost 주소는 휴대폰에서 접속할 수 없습니다.",
        max_chars=2048,
    ).strip()
    if public_url:
        try:
            parts = urlsplit(public_url)
            host = (parts.hostname or "").lower()
            valid = (
                parts.scheme == "https"
                and bool(host)
                and "." in host
                and host not in {"localhost", "127.0.0.1", "0.0.0.0"}
                and not host.endswith(".localhost")
                and not parts.username
                and not parts.password
                and not any(ch.isspace() for ch in public_url)
            )
        except ValueError:
            valid = False
        if not valid:
            st.warning("실제 배포된 공개 HTTPS 주소를 입력해 주세요.")
        elif qrcode is None:
            st.warning(
                "QR 생성 패키지가 아직 설치되지 않았습니다. "
                "requirements.txt를 실행 파일과 같은 폴더에 올린 후 앱을 재부팅하세요. "
                "게임은 QR 없이도 정상적으로 플레이할 수 있습니다."
            )
            st.code(public_url, language=None)
        else:
            qr = qrcode.QRCode(
                version=None,
                error_correction=qrcode.constants.ERROR_CORRECT_M,
                box_size=10,
                border=4,
            )
            qr.add_data(public_url)
            qr.make(fit=True)
            image = qr.make_image(fill_color="black", back_color="white")
            buffer = BytesIO()
            image.save(buffer, format="PNG")
            qr_bytes = buffer.getvalue()
            st.image(qr_bytes, caption="스캔하면 배포된 게임이 열립니다.", width=260)
            st.download_button(
                "QR 이미지 다운로드",
                data=qr_bytes,
                file_name="after_bell_qr.png",
                mime="image/png",
            )
            st.caption("주소의 실제 접속 가능 여부는 QR 생성과 별개입니다. 휴대폰에서 한 번 접속해 확인하세요.")

with st.expander("🎮 조작법 · 게임 규칙 · 소리 문제 해결"):
    st.markdown(
        "- **PC:** W/S 또는 ↑/↓ 이동, A/D 또는 ←/→ 회전, Shift 달리기(휴대폰은 달리기 ON/OFF 버튼), "
        "E 또는 스페이스 조사, P/Esc 일시정지. 먼저 게임 화면을 클릭하면 키보드 입력이 전달됩니다.\n"
        "- **휴대폰:** 하단 방향 버튼을 길게 눌러 이동·회전합니다. "
        "화면 드래그로도 회전할 수 있고, 달리기와 이동을 동시에 누를 수 있습니다.\n"
        "- **열쇠:** 열쇠 근처에서 조사해 줍습니다. 출입문 근처에서 조사하면 "
        "아직 시험하지 않은 보유 열쇠를 한 번에 맞춰봅니다. 10개 중 정확히 하나만 정답입니다.\n"
        "- **청소기구함:** 초록색 함 가까이에서 조사하면 숨습니다. "
        "숨은 동안 쌤은 다른 곳으로 수색하러 갑니다. 다시 조사하면 나옵니다.\n"
        "- **쌤:** 벽 너머로는 볼 수 없지만, 가까운 달리기 소리에 주의를 기울입니다. "
        "청소기구함에 숨은 동안에는 잡히지 않습니다.\n"
        "- **쉬운 모드:** 느린 추격과 출입문 위치가 표시된 미니맵이 제공됩니다.\n"
        "- **소리:** 시작 화면에서 소리를 켠 뒤 시작 버튼을 직접 눌러 주세요. "
        "휴대폰 음소거·브라우저 오디오 차단 설정도 확인하세요. 발소리 경고는 자막으로도 표시됩니다.\n"
        "- **쌤 디자인:** 참고 이미지의 대머리, 눈썹과 수염, 파란 조끼, 빨간 나비넥타이를 반영한 입체 캐릭터입니다.\n"
        "- **잡힘 연출:** 쌤이 다가와 잡는 순간 얼굴이 가까워지고 합성 고함 효과음이 나옵니다. "
        "시작 화면에서 깜짝 연출을 끄면 즉시 결과 화면으로 넘어갑니다.\n"
        "- **개인별 플레이:** 저장·로그인·멀티플레이 기능은 없습니다. 새로고침하면 한 판이 초기화됩니다. "
        "QR 생성 등 앱 바깥의 설정을 바꾸면 게임이 초기화될 수 있으므로 시작 전에 QR을 준비하세요."
    )
