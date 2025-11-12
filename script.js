
const API_BASE = "https://persona-backend-4ru3.onrender.com";


function setActive(navId){
  document.querySelectorAll("nav a").forEach(a=>a.classList.remove("active"));
  const el = document.getElementById(navId); if(el) el.classList.add("active");
}

async function askLLM(message, persona="Producer", rpm=null){
  const res = await fetch(`${API_BASE}/ask`, {
    method: "POST",
    headers: {"Content-Type":"application/json"},
    body: JSON.stringify({message, persona, rpm})
  });
  return res.json();
}

function useVoiceInput(targetInputId, onText){
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  if(!SpeechRecognition){ alert("Voice recognition not supported in this browser."); return; }
  const rec = new SpeechRecognition();
  rec.lang = "en-US"; rec.interimResults = false; rec.maxAlternatives = 1;
  rec.onresult = (e)=>{
    const text = e.results[0][0].transcript;
    const input = document.getElementById(targetInputId);
    if(input){ input.value = text; }
    if(onText){ onText(text); }
  };
  rec.start();
}

function getTasks(){ return JSON.parse(localStorage.getItem("tasks")||"[]"); }
function saveTasks(tasks){ localStorage.setItem("tasks", JSON.stringify(tasks)); }
function getXP(){ return JSON.parse(localStorage.getItem("xp")||'{"Producer":0,"Administrator":0,"Entrepreneur":0,"Integrator":0}'); }
function saveXP(xp){ localStorage.setItem("xp", JSON.stringify(xp)); }

function addTask(obj){
  const tasks = getTasks();
  tasks.push({...obj, id: Date.now(), done:false});
  saveTasks(tasks);
}

function completeTask(id){
  const tasks = getTasks();
  const idx = tasks.findIndex(t=>t.id===id);
  if(idx>-1){
    tasks[idx].done = true;
    saveTasks(tasks);
    const xp = getXP();
    const avatar = tasks[idx].avatar || "Producer";
    const base = 10;
    xp[avatar] = (xp[avatar]||0) + base;
    saveXP(xp);
  }
}

function renderXPBars(){
  const xp = getXP();
  for(const k of ["Producer","Administrator","Entrepreneur","Integrator"]){
    const val = xp[k] || 0;
    const pct = Math.min(100, Math.round(val/2));
    const bar = document.querySelector(`.bar[data-avatar='${k}']`);
    const label = document.getElementById(`xp-${k}`);
    if(bar){ bar.style.width = pct + "%"; }
    if(label){ label.innerText = val + " XP"; }
  }
}

async function draftEmail(thread){
  const res = await fetch(`${API_BASE}/draft-email`, {
    method: "POST",
    headers: {"Content-Type":"application/json"},
    body: JSON.stringify({thread})
  });
  return res.json();
}

function fmtDateTimeLocal(dt){
  const pad = n=> String(n).padStart(2,'0');
  return `${dt.getFullYear()}-${pad(dt.getMonth()+1)}-${pad(dt.getDate())}T${pad(dt.getHours())}:${pad(dt.getMinutes())}`;
}
