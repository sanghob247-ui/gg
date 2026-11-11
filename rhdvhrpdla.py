"""AFTER BELL — 1인칭 학교 탈출 게임.

배포: GitHub 저장소에 app.py와 requirements.txt를 올린 뒤
Streamlit Community Cloud에서 app.py를 메인 파일로 선택합니다.
실행: streamlit run app.py

게임 화면/그래픽/오디오는 이 파일 안에 포함되며 외부 자산이 필요 없습니다.
게임 로직은 방문자의 브라우저에서 실행되어 사용자별 플레이가 분리됩니다.
"""

from io import BytesIO
from urllib.parse import urlsplit

import qrcode
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="AFTER BELL | 학교 탈출",
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
<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no"><style>
*{box-sizing:border-box}html,body{margin:0;background:#080c12;color:#edf3fa;font-family:system-ui,'Apple SD Gothic Neo',sans-serif;overscroll-behavior:none}#game{position:relative;width:100%;height:min(760px,94vh);min-height:520px;overflow:hidden;background:#080c12;border:1px solid #273445;border-radius:18px;touch-action:none}canvas{width:100%;height:100%;display:block}.top{position:absolute;top:15px;left:16px;right:16px;display:flex;gap:8px;align-items:center;pointer-events:none}.tag{padding:8px 11px;border:1px solid #364352;border-radius:12px;background:#0a1224dc;font-size:12px}.brand{letter-spacing:2px;font-weight:850;color:#78f5d3}.grow{flex:1}#hint{position:absolute;top:62px;left:16px;right:16px;font-size:13px;text-align:center;text-shadow:0 2px 5px #000;pointer-events:none}#notice{position:absolute;top:115px;left:50%;transform:translateX(-50%);width:min(90%,520px);text-align:center;background:#111e2bea;padding:12px;border:1px solid #68d9bb;border-radius:10px;display:none;font-size:14px}#cross{position:absolute;left:50%;top:48%;transform:translate(-50%,-50%);color:#ffffff88;pointer-events:none}#danger{position:absolute;inset:0;box-shadow:inset 0 0 90px #ef334c;opacity:0;pointer-events:none}#keys{position:absolute;bottom:156px;left:16px;right:16px;display:flex;justify-content:center;gap:5px;flex-wrap:wrap;pointer-events:none}.key{background:#152031df;border:1px solid #647080;color:#c5cddd;padding:5px 8px;border-radius:7px;font-size:11px}.key.have{border-color:#eabf5c;color:#ffdb80}.key.bad{text-decoration:line-through;opacity:.45}#status{position:absolute;bottom:132px;left:16px;right:16px;text-align:center;font-size:12px;color:#d0dbe7;pointer-events:none}.controls{position:absolute;bottom:16px;left:16px;right:16px;display:flex;justify-content:space-between;align-items:end;gap:12px}.pad{display:grid;grid-template-columns:50px 50px 50px;grid-template-rows:48px 48px;gap:5px}.btn{border:1px solid #6b7d96;background:#152131dd;color:#fff;border-radius:12px;font-weight:800;cursor:pointer;touch-action:none;user-select:none;-webkit-user-select:none;font-size:17px}.btn:active{background:#387465}.blank{visibility:hidden}.actions{display:flex;gap:8px;align-items:end}.action{height:60px;padding:0 16px;font-size:13px;border-color:#7be3c2}.run{height:48px;padding:0 12px;font-size:12px}.overlay{position:absolute;inset:0;background:linear-gradient(135deg,#071019ed,#142031ef);display:flex;align-items:center;justify-content:center;padding:22px;z-index:10}.panel{width:min(560px,100%);max-height:100%;overflow:auto}.eyebrow{color:#6cf1c7;letter-spacing:4px;font-size:11px}h1{font-size:clamp(30px,6vw,48px);line-height:1.15;margin:15px 0}p{color:#bfccdb;font-size:14px;line-height:1.8}.rules{display:grid;grid-template-columns:1fr 1fr;gap:9px;margin:18px 0}.rule{padding:12px;border:1px solid #344256;border-radius:12px;color:#dce5ee;font-size:12px;line-height:1.6}.start{width:100%;padding:16px;background:#7af0c7;color:#07201a;border:0;border-radius:12px;font-size:16px;font-weight:900;cursor:pointer}.opts{display:flex;gap:15px;flex-wrap:wrap;margin:14px 0;font-size:13px;color:#cdd9e8}.tiny{font-size:11px;color:#a9b8c9}.hidden{display:none!important}#pauseBtn{pointer-events:auto;cursor:pointer}#jumpscare{position:absolute;inset:0;background:#230b10;display:none;z-index:8;align-items:center;justify-content:center;flex-direction:column}#face{font-size:clamp(130px,32vw,290px);filter:drop-shadow(0 0 40px #e13539);animation:shake .08s infinite alternate}#caughtText{font-size:32px;font-weight:900;z-index:1;text-shadow:0 2px 5px #000}@keyframes shake{from{transform:translate(-7px,2px) scale(1.8)}to{transform:translate(7px,-2px) scale(1.9)}}@media(max-width:520px){.top{left:10px;right:10px;gap:4px}.tag{font-size:10px;padding:7px}.controls{left:10px;right:10px}.actions{gap:5px}.action{padding:0 11px}.rules{gap:6px}.rule{font-size:11px}.run{padding:0 8px}}
</style></head><body><div id="game">
<canvas id="cv" aria-label="1인칭 학교 탈출 게임 화면"></canvas><div id="danger"></div><div class="top"><span class="tag brand">AFTER BELL</span><span class="tag" id="timer">00:00</span><span class="tag" id="count">열쇠 0/10</span><span class="grow"></span><button class="tag" id="pauseBtn" style="color:#fff">일시정지</button></div><div id="hint">학교에서 탈출하세요</div><div id="notice" role="status" aria-live="polite"></div><div id="cross">＋</div><div id="keys"></div><div id="status"></div>
<div class="controls"><div class="pad"><span class="blank"></span><button class="btn" data-hold="forward" aria-label="앞으로">▲</button><span class="blank"></span><button class="btn" data-hold="left" aria-label="왼쪽 회전">↶</button><button class="btn" data-hold="back" aria-label="뒤로">▼</button><button class="btn" data-hold="right" aria-label="오른쪽 회전">↷</button></div><div class="actions"><button class="btn run" data-hold="run">달리기</button><button class="btn action" id="act">조사 / 숨기</button></div></div>
<div id="jumpscare"><div id="face">😡</div><div id="caughtText">거기, 멈춰!</div></div>
<div class="overlay" id="menu"><div class="panel"><div class="eyebrow">FIRST PERSON · SCHOOL ESCAPE</div><h1>종이 울린 뒤,<br>학교에 갇혔다.</h1><p>출입문은 잠겼고 복도 끝에서 쌤의 발소리가 들린다.<br><b>10개 중 진짜 열쇠는 하나.</b> 찾아서 출입문에 직접 맞춰보자.</p><div class="rules"><div class="rule">🔑 교실의 열쇠 수집<br>문 앞에서 조사 → 자동으로 시험</div><div class="rule">🚪 초록색 청소기구함<br>가까이에서 조사 → 숨기 / 나오기</div><div class="rule">👣 발소리가 빨라지면 주의<br>숨으면 쌤은 다른 곳을 수색</div><div class="rule">🎮 PC: W/S 이동 · A/D 회전<br>Shift 달리기 · E 조사 · P 정지</div></div><div class="opts"><label><input id="soundOpt" type="checkbox" checked> 소리 사용</label><label><input id="scareOpt" type="checkbox" checked> 깜짝 연출 사용</label><label><input id="easyOpt" type="checkbox"> 쉬운 모드</label></div><p class="tiny">모바일: 아래 버튼으로 이동·회전, 화면을 좌우로 드래그해 시점 조절. 발소리는 자막으로도 표시됩니다. 놀람·고함 연출이 있으므로 음량을 낮추고 시작하세요. 실제 음성 대신 합성 고함 효과음을 사용합니다.</p><button class="start" id="start">학교에 들어가기</button><p class="tiny">초록색 = 숨을 곳 · 금색 = 열쇠 · 파란색 = 출입문<br>열쇠 위치와 정답은 매번 바뀝니다. 저장 없이 한 판씩 플레이합니다.</p></div></div>
<div class="overlay hidden" id="result"><div class="panel"><div class="eyebrow" id="resultTag"></div><h1 id="resultTitle"></h1><p id="resultBody"></p><button class="start" id="restart">다시 도전하기</button></div></div>
<div class="overlay hidden" id="paused"><div class="panel"><div class="eyebrow">PAUSED</div><h1>잠깐, 숨 고르기.</h1><p>게임과 추격이 모두 멈췄습니다.</p><button class="start" id="resume">계속하기</button><p class="tiny">키보드 P / Esc로도 계속할 수 있습니다.</p></div></div>
</div><script>
'use strict';
const $=id=>document.getElementById(id),cv=$('cv'),ctx=cv.getContext('2d'),TAU=Math.PI*2;
// 1=wall. Broad horizontal corridors connect ten rooms and every hiding place.
const ROWS=[
'1111111111111111111111111',
'1000001000001000001000001',
'1000001000001000001000001',
'1000001000001000001000001',
'1110111110111110111110111',
'1000000000000000000000001',
'1000000000000000000000001',
'1110111110111110111110111',
'1000001000001000001000001',
'1000001000001000001000001',
'1000001000001000001000001',
'1111111111111111111111111',
'1000001000001000001000001',
'1000001000001000001000001',
'1110111110111110111110111',
'1000000000000000000000001',
'1000000000000000000000001',
'1111111111111111111111111'];
// Link both corridors at the west end, and add two connected east classrooms.
const map=ROWS.map(r=>r.split('').map(Number));for(let y=7;y<=15;y++)map[y][1]=0;
const W=25,H=18,exit={x:2.5,y:6.5};
const rooms=[{x:3.5,y:2.5},{x:9.5,y:2.5},{x:15.5,y:2.5},{x:21.5,y:2.5},{x:3.5,y:9.5},{x:9.5,y:9.5},{x:15.5,y:9.5},{x:21.5,y:9.5},{x:9.5,y:12.5},{x:21.5,y:12.5}];
const closets=[{x:5.2,y:5.45},{x:11.4,y:6.5},{x:18.5,y:5.45},{x:23.3,y:6.5},{x:3.4,y:15.5},{x:11.5,y:16.5},{x:19.5,y:15.5}];
let p,t,keys,correct,held,tried,state='menu',hidden=false,hideSpot=null,elapsed=0,stamina=100,searchLeft=0,grace=0,noticeUntil=0,stepClock=0,playerStep=0,aiClock=0,route=[],frame=0,last=0,scare=true,easy=false,audio=null,sound=false,noise=null,lastSee=0;
const inputs={forward:false,back:false,left:false,right:false,run:false};
const dist=(a,b)=>Math.hypot(a.x-b.x,a.y-b.y);const wall=(x,y)=>!map[Math.floor(y)]||map[Math.floor(y)][Math.floor(x)]!==0;
function canStand(x,y){const r=.20;return !wall(x-r,y-r)&&!wall(x+r,y-r)&&!wall(x-r,y+r)&&!wall(x+r,y+r)}
function move(o,dx,dy){if(canStand(o.x+dx,o.y))o.x+=dx;if(canStand(o.x,o.y+dy))o.y+=dy;}
function clearInputs(){Object.keys(inputs).forEach(k=>inputs[k]=false)}
function toast(text){$('notice').textContent=text;$('notice').style.display='block';noticeUntil=performance.now()+3400;}
function setupAudio(){try{audio=audio||new(window.AudioContext||window.webkitAudioContext)();audio.resume();if(!noise){noise=audio.createBuffer(1,audio.sampleRate*.24,audio.sampleRate);const a=noise.getChannelData(0);for(let i=0;i<a.length;i++)a[i]=(Math.random()*2-1)*(1-i/a.length);}}catch(e){sound=false;}}
function tone(freq,duration,volume,type='sine',end=null){if(!sound||!audio||audio.state!=='running')return;const o=audio.createOscillator(),g=audio.createGain(),at=audio.currentTime;o.type=type;o.frequency.setValueAtTime(freq,at);if(end)o.frequency.exponentialRampToValueAtTime(end,at+duration);g.gain.setValueAtTime(.001,at);g.gain.linearRampToValueAtTime(volume,at+.01);g.gain.exponentialRampToValueAtTime(.001,at+duration);o.connect(g);g.connect(audio.destination);o.start(at);o.stop(at+duration+.02);}
function foot(d,teacher){if(!sound||!audio||!noise||audio.state!=='running')return;const src=audio.createBufferSource(),g=audio.createGain(),f=audio.createBiquadFilter();src.buffer=noise;f.type='lowpass';f.frequency.value=teacher?330:190;g.gain.value=teacher?Math.min(.28,.9/(d+1)):.04;src.connect(f);f.connect(g);g.connect(audio.destination);src.start();tone(teacher?65:47,.12,teacher?Math.min(.15,.5/(d+1)):.025);}
function scream(){tone(240,.8,.09,'sawtooth',650);tone(360,.75,.065,'sawtooth',150);tone(780,.65,.035,'triangle',320);}
function reset(){p={x:3.5,y:5.7,a:0};t={x:22.5,y:15.5,mode:'patrol',target:null};correct=1+Math.floor(Math.random()*10);const numbers=Array.from({length:10},(_,i)=>i+1);for(let i=9;i>0;i--){let j=Math.floor(Math.random()*(i+1));[numbers[i],numbers[j]]=[numbers[j],numbers[i]];}keys=rooms.map((v,i)=>({...v,id:numbers[i],taken:false}));held=new Set();tried=new Set();hidden=false;hideSpot=null;elapsed=0;stamina=100;searchLeft=0;grace=3;lastSee=0;stepClock=0;playerStep=0;aiClock=0;route=[];clearInputs();updateKeys();$('jumpscare').style.display='none';$('result').classList.add('hidden');$('menu').classList.add('hidden');$('paused').classList.add('hidden');state='playing';toast('교실에서 금색 열쇠를 찾으세요. 초록색 함은 숨을 곳입니다.');}
function updateKeys(){$('keys').innerHTML=Array.from({length:10},(_,i)=>`<span class="key ${held.has(i+1)?'have':''} ${tried.has(i+1)?'bad':''}">${String(i+1).padStart(2,'0')}</span>`).join('');$('count').textContent=`열쇠 ${held.size}/10`;}
function line(a,b){let d=dist(a,b);for(let q=.12;q<d;q+=.10)if(wall(a.x+(b.x-a.x)*q/d,a.y+(b.y-a.y)*q/d))return false;return true;}
function path(a,b){const sx=Math.floor(a.x),sy=Math.floor(a.y),tx=Math.floor(b.x),ty=Math.floor(b.y),start=sy*W+sx,goal=ty*W+tx;let queue=[start],head=0;const prev=new Map([[start,null]]);while(head<queue.length){const v=queue[head++];if(v===goal)break;const x=v%W,y=Math.floor(v/W);for(const [dx,dy]of [[1,0],[-1,0],[0,1],[0,-1]]){const nx=x+dx,ny=y+dy,n=ny*W+nx;if(nx<0||nx>=W||ny<0||ny>=H||map[ny][nx]!==0||prev.has(n))continue;prev.set(n,v);queue.push(n);}}if(!prev.has(goal))return [];let arr=[],v=goal;while(v!==start){arr.push({x:v%W+.5,y:Math.floor(v/W)+.5});v=prev.get(v);}return arr.reverse();}
function patrolTarget(away=false){let cells=[];for(let y=1;y<H-1;y++)for(let x=1;x<W-1;x++)if(map[y][x]===0&&(!away||Math.hypot(x+.5-p.x,y+.5-p.y)>9))cells.push({x:x+.5,y:y+.5});return cells[Math.floor(Math.random()*cells.length)]||{x:22.5,y:15.5};}
function interact(){if(state!=='playing')return;if(hidden){hidden=false;hideSpot=null;grace=1.5;toast('함에서 나왔습니다. 발소리를 듣고 움직이세요.');return;}
const nearCloset=closets.filter(c=>dist(p,c)<1.55&&line(p,c)).sort((a,b)=>dist(p,a)-dist(p,b))[0];if(nearCloset){hidden=true;hideSpot=nearCloset;t.mode='search';searchLeft=7;t.target=patrolTarget(true);route=path(t,t.target);aiClock=0;clearInputs();tone(110,.2,.08,'triangle');toast('청소기구함에 숨었습니다. 쌤이 다른 곳을 수색합니다.');return;}
if(dist(p,exit)<1.9&&line(p,exit)){const pending=[...held].filter(k=>!tried.has(k));if(!pending.length){toast(held.size?'가진 열쇠는 모두 맞지 않습니다. 다른 교실을 찾아보세요.':'출입문이 잠겼습니다. 교실에서 열쇠를 찾으세요.');return;}if(pending.includes(correct)){win();return;}pending.forEach(k=>tried.add(k));updateKeys();tone(140,.2,.07,'square',80);toast(`${pending.map(k=>k+'번').join(', ')} 열쇠는 맞지 않습니다. 다른 열쇠를 찾으세요.`);return;}
const key=keys.filter(k=>!k.taken&&dist(p,k)<1.55&&line(p,k)).sort((a,b)=>dist(p,a)-dist(p,b))[0];if(key){key.taken=true;held.add(key.id);updateKeys();tone(660,.13,.06);setTimeout(()=>tone(990,.15,.05),100);toast(`${key.id}번 열쇠를 찾았습니다! 출입문에 가서 맞춰보세요.`);return;}toast('조금 더 가까이 가세요. 열쇠·청소기구함·출입문을 조사할 수 있습니다.');}
function finish(ok){state=ok?'won':'lost';clearInputs();$('resultTag').textContent=ok?'ESCAPED · 생존 성공':'CAUGHT · 다음 기회를 노려봐';$('resultTitle').textContent=ok?'드디어, 학교 밖으로.':'쌤에게 잡혔다!';$('resultBody').textContent=ok?`${formatTime(elapsed)} 만에 탈출! 정답은 ${correct}번 열쇠였습니다. 발견한 열쇠 ${held.size}/10개.`:'다음에는 발소리가 빨라질 때 초록색 청소기구함 근처에서 E 또는 조사 버튼을 눌러 숨으세요.';$('result').classList.remove('hidden');}
function win(){tone(523,.3,.07);setTimeout(()=>tone(659,.3,.07),130);setTimeout(()=>tone(784,.5,.07),260);finish(true);}
function caught(){if(state!=='playing')return;state='caught';clearInputs();if(scare){$('jumpscare').style.display='flex';scream();setTimeout(()=>{$('jumpscare').style.display='none';finish(false);},1500);}else finish(false);}
function pause(){if(state==='playing'){state='paused';clearInputs();$('paused').classList.remove('hidden');}else if(state==='paused'){state='playing';$('paused').classList.add('hidden');if(sound)setupAudio();}}
function formatTime(s){return String(Math.floor(s/60)).padStart(2,'0')+':'+String(Math.floor(s%60)).padStart(2,'0')}
function update(dt){elapsed+=dt;grace=Math.max(0,grace-dt);const d=dist(p,t);if(!hidden){p.a+=(Number(inputs.right)-Number(inputs.left))*dt*2.1;const moving=Number(inputs.forward)-Number(inputs.back);const running=inputs.run&&stamina>2&&moving!==0;const speed=running?3.2:1.85;move(p,Math.cos(p.a)*moving*speed*dt,Math.sin(p.a)*moving*speed*dt);stamina=Math.min(100,Math.max(0,stamina+(running?-22:13)*dt));if(moving){playerStep+=dt;if(playerStep>(running?.25:.45)){foot(0,false);playerStep=0;}}if(running&&d<7)t.target={x:p.x,y:p.y};}
const sees=!hidden&&line(t,p)&&d<(easy?7.5:10.5);if(sees){t.mode='chase';t.target={x:p.x,y:p.y};lastSee=elapsed;searchLeft=0;}else if(t.mode==='chase'&&elapsed-lastSee>2){t.mode='search';searchLeft=5;t.target=hidden?patrolTarget(true):{x:p.x,y:p.y};}
if(t.mode==='search'){searchLeft-=dt;if(searchLeft<=0){t.mode='patrol';t.target=null;}}
if(!t.target||dist(t,t.target)<.4)t.target=patrolTarget(hidden);
aiClock-=dt;if(aiClock<=0){route=path(t,t.target);aiClock=t.mode==='chase'?.3:1.2;}
const next=route[0];if(next){const delta=dist(t,next),speed=t.mode==='chase'?(easy?1.25:1.70):(easy?.75:1.0),step=Math.min(delta,speed*dt);if(delta>.01)move(t,(next.x-t.x)/delta*step,(next.y-t.y)/delta*step);if(delta<.12)route.shift();}
if(!hidden&&grace===0&&dist(p,t)<.65&&line(t,p))caught();stepClock+=dt;if(d<12&&stepClock>(t.mode==='chase'?.26:.58)){foot(d,true);stepClock=0;}
$('timer').textContent=formatTime(elapsed);$('status').textContent=hidden?'숨는 중 · 조사 버튼으로 나오기 · 발소리가 멀어질 때까지 기다리세요':`체력 ${Math.round(stamina)}% · ${inputs.run?'달리는 소리는 쌤의 주의를 끕니다':'조사는 가까이에서 E 또는 버튼'}`;
$('danger').style.opacity=hidden?'0':String(t.mode==='chase'?Math.max(.15,1-d/11)*.65:0);
$('hint').textContent=hidden?'쌤이 다른 곳을 찾고 있습니다.':t.mode==='chase'?'🏃 쌤이 쫓아옵니다! 초록색 청소기구함으로 숨으세요!':d<5?'👣 가까운 곳에서 무거운 발소리…':d<10?'👣 복도 어딘가에서 발소리가 들립니다.':'교실을 조사해 열쇠를 찾고, 파란 출입문으로 돌아가세요.';
}
function resize(){const r=cv.getBoundingClientRect();cv.width=Math.min(1000,Math.round(r.width*(window.devicePixelRatio>1?1.25:1)));cv.height=Math.round(cv.width*r.height/r.width)}window.addEventListener('resize',resize);resize();
function render(){const w=cv.width,h=cv.height;ctx.fillStyle='#141c28';ctx.fillRect(0,0,w,h/2);const floor=ctx.createLinearGradient(0,h/2,0,h);floor.addColorStop(0,'#111820');floor.addColorStop(1,'#394047');ctx.fillStyle=floor;ctx.fillRect(0,h/2,w,h/2);if(!p)return;const fov=Math.PI/2.8,focal=w/(2*Math.tan(fov/2)),cols=Math.ceil(w/3),depth=new Float32Array(cols),bob=state==='playing'&&!hidden&&(inputs.forward||inputs.back)?Math.sin(elapsed*11)*h*.004:0;
for(let c=0;c<cols;c++){const screenX=(c*3-w/2)/focal,ang=p.a+Math.atan(screenX),rx=Math.cos(ang),ry=Math.sin(ang);let mx=Math.floor(p.x),my=Math.floor(p.y),ddx=Math.abs(1/rx),ddy=Math.abs(1/ry),sx=rx<0?-1:1,sy=ry<0?-1:1,sideX=(rx<0?p.x-mx:mx+1-p.x)*ddx,sideY=(ry<0?p.y-my:my+1-p.y)*ddy,side=0,steps=0;while(steps++<80){if(sideX<sideY){sideX+=ddx;mx+=sx;side=0;}else{sideY+=ddy;my+=sy;side=1;}if(mx<0||my<0||mx>=W||my>=H||map[my][mx])break;}const raw=side===0?sideX-ddx:sideY-ddy,d=Math.max(.05,raw*Math.cos(ang-p.a));depth[c]=d;const wh=focal/d,top=h/2-wh/2+bob,wallU=side===0?p.y+raw*ry:p.x+raw*rx,shade=Math.max(.15,1/(1+d*.17))*(side?.72:1);let base=my===4||my===7||my===14?[131,145,146]:[151,157,155];ctx.fillStyle=`rgb(${base.map(v=>Math.round(v*shade)).join(',')})`;ctx.fillRect(c*3,top,3,wh);ctx.fillStyle=`rgba(24,65,69,${Math.max(.3,shade)})`;ctx.fillRect(c*3,top+wh*.58,3,wh*.27);ctx.fillStyle=`rgba(8,15,20,${.3+(.5-shade*.4)})`;ctx.fillRect(c*3,top+wh*.91,3,wh*.09);if((wallU%1)<.025){ctx.fillStyle='#14202a88';ctx.fillRect(c*3,top,3,wh);}ctx.fillStyle=`rgba(217,231,211,${shade*.6})`;ctx.fillRect(c*3,top,3,Math.max(1,wh*.025));}
const objects=[...keys.filter(k=>!k.taken).map(k=>({...k,type:'key'})),...closets.map(c=>({...c,type:'closet'})),{...exit,type:'exit'},{...t,type:'teacher'}].sort((a,b)=>dist(p,b)-dist(p,a));
for(const o of objects){const dx=o.x-p.x,dy=o.y-p.y;let angle=Math.atan2(dy,dx)-p.a;angle=Math.atan2(Math.sin(angle),Math.cos(angle));if(Math.abs(angle)>fov*.85)continue;const z=Math.hypot(dx,dy)*Math.cos(angle);if(z<.12)continue;const x=w/2+Math.tan(angle)*focal,sz=focal/z,y=h/2+bob,sw=sz*(o.type==='key'?.35:.58),sh=sz*(o.type==='key'?.25:.92),top=o.type==='key'?y+sz*.15:y-sz*.43;ctx.save();ctx.beginPath();for(let c=Math.max(0,Math.floor((x-sw/2)/3));c<Math.min(cols,Math.ceil((x+sw/2)/3));c++)if(z<depth[c]+.08)ctx.rect(c*3,0,3,h);ctx.clip();const shade=Math.max(.3,1/(1+z*.12));ctx.globalAlpha=shade;
if(o.type==='key'){ctx.strokeStyle='#ffcc55';ctx.lineWidth=Math.max(2,sz*.04);ctx.beginPath();ctx.arc(x-sw*.25,top+sh*.35,sw*.21,0,TAU);ctx.moveTo(x-sw*.06,top+sh*.35);ctx.lineTo(x+sw*.45,top+sh*.35);ctx.lineTo(x+sw*.45,top+sh*.63);ctx.moveTo(x+sw*.25,top+sh*.35);ctx.lineTo(x+sw*.25,top+sh*.60);ctx.stroke();if(z<4){ctx.fillStyle='#ffdf8b';ctx.font=`bold ${Math.max(12,sz*.10)}px sans-serif`;ctx.textAlign='center';ctx.fillText(`${o.id}번`,x,top-sh*.15);}}
else if(o.type==='closet'||o.type==='exit'){ctx.fillStyle=o.type==='closet'?'#28685c':'#315f89';ctx.fillRect(x-sw/2,top,sw,sh);ctx.strokeStyle=o.type==='closet'?'#73c3a6':'#84c5ed';ctx.lineWidth=Math.max(1,sz*.018);ctx.strokeRect(x-sw/2,top,sw,sh);ctx.fillStyle='#0e2528';for(let i=0;i<3;i++)ctx.fillRect(x-sw*.32,top+sh*(.2+i*.065),sw*.64,sh*.022);ctx.fillStyle='#f2dca1';ctx.fillRect(x+sw*.30,top+sh*.56,sw*.06,sh*.07);if(z<6){ctx.fillStyle='#f3ffef';ctx.textAlign='center';ctx.font=`bold ${Math.max(10,sz*.085)}px sans-serif`;ctx.fillText(o.type==='closet'?'청소기구함':'출입문',x,top+sh*.47);}}
else{const stride=Math.sin(elapsed*(t.mode==='chase'?19:10))*sz*.045;ctx.fillStyle='#1b202e';ctx.fillRect(x-sw*.28,top+sh*.60,sw*.21,sh*.4+stride);ctx.fillRect(x+sw*.05,top+sh*.60,sw*.21,sh*.4-stride);ctx.fillStyle=t.mode==='chase'?'#a34a4a':'#777fa3';ctx.fillRect(x-sw*.38,top+sh*.29,sw*.76,sh*.42);ctx.fillStyle='#e6b79c';ctx.fillRect(x-sw*.53,top+sh*.33,sw*.15,sh*.36-stride);ctx.fillRect(x+sw*.38,top+sh*.33,sw*.15,sh*.36+stride);ctx.beginPath();ctx.ellipse(x,top+sh*.17,sw*.27,sh*.16,0,0,TAU);ctx.fill();ctx.fillStyle='#20212b';ctx.fillRect(x-sw*.27,top,sw*.54,sh*.09);ctx.fillStyle='#242332';ctx.fillRect(x-sw*.18,top+sh*.14,sw*.12,sh*.035);ctx.fillRect(x+sw*.06,top+sh*.14,sw*.12,sh*.035);ctx.fillStyle='#6a2226';ctx.fillRect(x-sw*.09,top+sh*.23,sw*.18,sh*.045);ctx.fillStyle='#eee';ctx.beginPath();ctx.moveTo(x-sw*.16,top+sh*.30);ctx.lineTo(x,top+sh*.42);ctx.lineTo(x+sw*.16,top+sh*.30);ctx.fill();}
ctx.restore();}
// Deliberate soft vignette, no flashing.
const vignette=ctx.createRadialGradient(w/2,h/2,h*.15,w/2,h/2,w*.65);vignette.addColorStop(0,'#0000');vignette.addColorStop(1,'#000b');ctx.fillStyle=vignette;ctx.fillRect(0,0,w,h);
if(hidden){ctx.fillStyle='#07100f';ctx.fillRect(0,0,w,h*.35);ctx.fillRect(0,h*.65,w,h*.35);ctx.fillRect(0,0,w*.09,h);ctx.fillRect(w*.91,0,w*.09,h);for(let i=0;i<4;i++)ctx.fillRect(0,h*(.37+i*.07),w,h*.035);ctx.strokeStyle='#3e5d52';ctx.lineWidth=6;ctx.strokeRect(w*.09,h*.35,w*.82,h*.3);}
// A compact floorplan helps phone users orient themselves without revealing teacher/key positions.
if(easy&&!hidden){const cell=Math.min(5,w/85),ox=w-W*cell-14,oy=78;ctx.fillStyle='#050c14d9';ctx.fillRect(ox-4,oy-4,W*cell+8,H*cell+8);for(let y=0;y<H;y++)for(let x=0;x<W;x++){ctx.fillStyle=map[y][x]?'#536374':'#16232d';ctx.fillRect(ox+x*cell,oy+y*cell,cell-.3,cell-.3);}ctx.fillStyle='#74f2cf';ctx.beginPath();ctx.arc(ox+p.x*cell,oy+p.y*cell,3,0,TAU);ctx.fill();ctx.strokeStyle='#74f2cf';ctx.beginPath();ctx.moveTo(ox+p.x*cell,oy+p.y*cell);ctx.lineTo(ox+(p.x+Math.cos(p.a)*1.5)*cell,oy+(p.y+Math.sin(p.a)*1.5)*cell);ctx.stroke();ctx.fillStyle='#6db9ff';ctx.fillRect(ox+exit.x*cell-2,oy+exit.y*cell-2,4,4);}
}
function loop(now){const dt=Math.min(.05,(now-last)/1000||.016);last=now;if(state==='playing')update(dt);if(now>noticeUntil)$('notice').style.display='none';render();requestAnimationFrame(loop)}
const keymap={KeyW:'forward',ArrowUp:'forward',KeyS:'back',ArrowDown:'back',KeyA:'left',ArrowLeft:'left',KeyD:'right',ArrowRight:'right',ShiftLeft:'run',ShiftRight:'run'};
window.addEventListener('keydown',e=>{if(keymap[e.code]){e.preventDefault();if(state==='playing')inputs[keymap[e.code]]=true;}if(e.repeat)return;if(e.code==='KeyE'||e.code==='Space'){e.preventDefault();interact();}if(e.code==='KeyP'||e.code==='Escape')pause();});window.addEventListener('keyup',e=>{if(keymap[e.code])inputs[keymap[e.code]]=false});
document.querySelectorAll('[data-hold]').forEach(btn=>{const k=btn.dataset.hold;btn.addEventListener('pointerdown',e=>{e.preventDefault();if(state!=='playing')return;btn.setPointerCapture(e.pointerId);inputs[k]=true;});for(const name of ['pointerup','pointercancel','lostpointercapture'])btn.addEventListener(name,()=>inputs[k]=false);});
let drag=null;cv.addEventListener('pointerdown',e=>{if(state==='playing'){drag={id:e.pointerId,x:e.clientX};cv.setPointerCapture(e.pointerId);}});cv.addEventListener('pointermove',e=>{if(drag&&drag.id===e.pointerId&&state==='playing'&&!hidden){p.a+=(e.clientX-drag.x)*.006;drag.x=e.clientX;}});for(const name of ['pointerup','pointercancel'])cv.addEventListener(name,()=>drag=null);
window.addEventListener('blur',()=>{clearInputs();if(state==='playing')pause();});document.addEventListener('visibilitychange',()=>{if(document.hidden&&state==='playing')pause();});
$('start').onclick=()=>{sound=$('soundOpt').checked;scare=$('scareOpt').checked;easy=$('easyOpt').checked;if(sound)setupAudio();reset();};$('restart').onclick=()=>{$('result').classList.add('hidden');$('menu').classList.remove('hidden');state='menu';$('danger').style.opacity='0';};$('act').onclick=interact;$('pauseBtn').onclick=pause;$('resume').onclick=pause;
requestAnimationFrame(loop);
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
        "- **PC:** W/S 또는 ↑/↓ 이동, A/D 또는 ←/→ 회전, Shift 달리기, "
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
        "- **잡힘 연출:** 쌤이 다가와 잡는 순간 큰 얼굴과 합성 고함 효과음이 나옵니다. "
        "시작 화면에서 깜짝 연출을 끄면 즉시 결과 화면으로 넘어갑니다.\n"
        "- **개인별 플레이:** 저장·로그인·멀티플레이 기능은 없습니다. 새로고침하면 한 판이 초기화됩니다. "
        "QR 생성 등 앱 바깥의 설정을 바꾸면 게임이 초기화될 수 있으므로 시작 전에 QR을 준비하세요."
    )
