import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Meo Den Pro Max", layout="centered")
st.title("Game Meo Den Mat Vang 2D")

game_html = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>Cat Game</title>
    <style>
        body { background: #0b0f19; color: #f8fafc; font-family: Arial; display: flex; flex-direction: column; align-items: center; justify-content: center; margin: 0; padding: 5px; }
        #game-container { position: relative; border: 2px solid #38bdf8; border-radius: 8px; overflow: hidden; box-shadow: 0 8px 24px rgba(0,0,0,0.8); }
        canvas { display: block; }
        #ui { margin-top: 6px; background: #0f172a; padding: 8px 12px; border: 1px solid #334155; border-radius: 6px; font-size: 13px; width: 720px; display: flex; justify-content: space-between; font-weight: bold; }
        #ctrl { margin-top: 8px; display: flex; gap: 10px; justify-content: center; width: 720px; }
        .btn { border: none; border-radius: 8px; padding: 14px 20px; font-size: 16px; font-weight: bold; cursor: pointer; user-select: none; }
        .jump { background: #f59e0b; color: #0f172a; flex-grow: 2; }
        .sound { background: #38bdf8; color: #0f172a; flex-grow: 1; }
    </style>
</head>
<body>
    <div id="game-container"><canvas id="gameCanvas" height="320" width="720"></canvas></div>
    <div id="ui">
        <div>DIEM: <span id="score">0</span></div>
        <div>TRANG THAI: <span id="status" style="color:#38bdf8;">SAN SANG</span></div>
        <div>KY LUC: <span id="high">0</span></div>
    </div>
    <div id="ctrl">
        <button class="btn sound" id="audio-toggle" onclick="toggleAudio()">NHAC: OFF</button>
        <button class="btn jump" id="jump-trigger">NHẢY (1 CHAM)</button>
    </div>
<script>
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
let score = 0, high = 0, over = false, baseSpeed = 3.6, speed = 3.6, audioOn = false;
let weather = 'normal', sunT = 0, bowls = [], rain = [];
let audioCtx = null, bgTimer = null, meowT = 0;
const notes = [1046, 1174, 1318, 1046, 1318, 1318, 1396, 1396, 1318, 1174, 1046, 1174, 1318, 1567, 1396, 1318, 1174, 1046];
let noteIdx = 0;
const sad = [329, 311, 293, 277, 261];

function initAudio() { if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)(); if (audioCtx.state === 'suspended') audioCtx.resume(); }
function toggleAudio() {
    initAudio(); audioOn = !audioOn;
    let btn = document.getElementById('audio-toggle');
    if (audioOn) { btn.innerText = 'NHAC: ON'; btn.style.background = '#22c55e'; startMusic(); }
    else { btn.innerText = 'NHAC: OFF'; btn.style.background = '#38bdf8'; stopMusic(); }
}
function playMeow() {
    if (!audioOn || !audioCtx) return;
    let o = audioCtx.createOscillator(), g = audioCtx.createGain();
    o.type = 'sine'; o.frequency.setValueAtTime(700, audioCtx.currentTime);
    o.frequency.linearRampToValueAtTime(1100, audioCtx.currentTime + 0.12);
    g.gain.setValueAtTime(0.4, audioCtx.currentTime);
    g.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.28);
    o.connect(g); g.connect(audioCtx.destination); o.start(); o.stop(audioCtx.currentTime + 0.28);
}
function playSad() {
    if (!audioOn || !audioCtx) return;
    stopMusic(); let i = 0;
    let t = setInterval(() => {
        if (i >= sad.length) { clearInterval(t); return; }
        let o = audioCtx.createOscillator(), g = audioCtx.createGain();
        o.type = 'sawtooth'; o.frequency.setValueAtTime(sad[i], audioCtx.currentTime);
        g.gain.setValueAtTime(0.15, audioCtx.currentTime); g.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.4);
        o.connect(g); g.connect(audioCtx.destination); o.start(); o.stop(audioCtx.currentTime + 0.4); i++;
    }, 350);
}
function startMusic() {
    if (!audioCtx) return; stopMusic();
    bgTimer = setInterval(() => {
        if (!audioOn || over) return;
        let o = audioCtx.createOscillator(), g = audioCtx.createGain();
        o.type = (noteIdx % 2 === 0) ? 'sine' : 'triangle';
        o.frequency.setValueAtTime(notes[noteIdx], audioCtx.currentTime);
        g.gain.setValueAtTime(0.12, audioCtx.currentTime); g.gain.exponentialRampToValueAtTime(0.005, audioCtx.currentTime + 0.16);
        o.connect(g); g.connect(audioCtx.destination); o.start(); o.stop(audioCtx.currentTime + 0.16);
        noteIdx = (noteIdx + 1) % notes.length;
    }, 180);
}
function stopMusic() { if (bgTimer) { clearInterval(bgTimer); bgTimer = null; } }

for (let i = 0; i < 35; i++) rain.push({x: Math.random()*720, y: Math.random()*320, len: 8+Math.random()*6, sy: 7+Math.random()*3});

const cat = {
    x: 90, y: 140, w: 32, h: 22, vy: 0, gravity: 0.68, ground: false,
    draw() {
        ctx.fillStyle = 'rgba(0,0,0,0.4)'; ctx.beginPath(); ctx.ellipse(this.x+16, this.y+this.h+2, 14, 4, 0, 0, Math.PI*2); ctx.fill();
        ctx.fillStyle = (weather === 'rain') ? '#090d16' : '#020617'; ctx.fillRect(this.x, this.y, this.w, this.h);
        ctx.fillRect(this.x+18, this.y-12, 16, 16);
        ctx.fillStyle = '#020617';
        ctx.beginPath(); ctx.moveTo(this.x+18, this.y-12); ctx.lineTo(this.x+21, this.y-20); ctx.lineTo(this.x+25, this.y-12); ctx.fill();
        ctx.beginPath(); ctx.moveTo(this.x+27, this.y-12); ctx.lineTo(this.x+30, this.y-20); ctx.lineTo(this.x+34, this.y-12); ctx.fill();
        ctx.fillStyle = '#f43f5e'; ctx.fillRect(this.x+21, this.y-16, 2, 4); ctx.fillRect(this.x+29, this.y-16, 2, 4);
        ctx.fillStyle = '#facc15'; ctx.fillRect(this.x+25, this.y-8, 6, 6);
        ctx.fillStyle = '#000000'; ctx.fillRect(this.x+28, this.y-8, 2, 6);
        if (score >= 200) { ctx.fillStyle = '#f43f5e'; ctx.fillRect(this.x+10, this.y-18, 12, 3); }
    }
};

let bld = [{x:0, w:220, h:120}, {x:290, w:180, h:140}, {x:540, w:200, h:110}, {x:810, w:220, h:130}];

function jump(e) {
    if (e) e.preventDefault();
    initAudio();
    if (over) { reset(); return; }
    if (cat.ground) { cat.vy = (score >= 200) ? -13.2 : -11.8; cat.ground = false; playMeow(); }
}

let jBtn = document.getElementById('jump-trigger');
jBtn.addEventListener('touchstart', jump, {passive: false});
jBtn.addEventListener('click', jump);
window.addEventListener('keydown', e => { if (e.code === 'Space' || e.key === 'ArrowUp') jump(); });

function reset() {
    score = 0; baseSpeed = 3.6; speed = 3.6; over = false; weather = 'normal'; sunT = 0; bowls = [];
    cat.y = 100; cat.vy = 0;
    bld = [{x:0, w:220, h:120}, {x:290, w:180, h:140}, {x:540, w:200, h:110}, {x:810, w:220, h:130}];
    document.getElementById('status').innerText = "SAN SANG"; document.getElementById('status').style.color = "#38bdf8";
    if (audioOn) startMusic();
}

function update() {
    if (over) return;
    meowT++; if (meowT > 320) { if (Math.random() < 0.4) playMeow(); meowT = 0; }
    if (score >= 50 && score < 90) { weather = 'rain'; }
    else if (score >= 90) {
        if (sunT < 600) { weather = 'sunny'; sunT++; speed = 1.8; }
        else { weather = 'normal'; speed = baseSpeed; }
    } else { weather = 'normal'; speed = baseSpeed; }

    cat.vy += cat.gravity; cat.y += cat.vy;
    bld.forEach(b => b.x -= speed);

    if (bld[0].x + bld[0].w < 0) {
        bld.shift();
        let last = bld[bld.length - 1];
        let gap = (weather === 'sunny') ? 55 + Math.random()*20 : 80 + speed*4 + Math.random()*40;
        let nw = 160 + Math.random()*100, nh = 90 + Math.random()*60;
        let nb = {x: last.x + last.w + gap, w: nw, h: nh};
        bld.push(nb);
        if (weather === 'sunny' || (score >= 90 && Math.random() < 0.7)) {
            bowls.push({x: nb.x + nw/2 - 10, y: 320 - nh - 12, w: 20, h: 12});
        }
        score += 10; if (score > high) high = score;
        document.getElementById('score').innerText = score; document.getElementById('high').innerText = high;
        baseSpeed += 0.18;
    }

    for (let i = bowls.length - 1; i >= 0; i--) {
        let bw = bowls[i]; bw.x -= speed;
        if (cat.x < bw.x + bw.w && cat.x + cat.w > bw.x && cat.y < bw.y + bw.h && cat.y + cat.h > bw.y) {
            bowls.splice(i, 1); sunT = 600; speed = baseSpeed + 0.5; playMeow();
        }
        if (bw.x < -30) bowls.splice(i, 1);
    }

    cat.ground = false;
    bld.forEach(b => {
        let roof = 320 - b.h;
        if (cat.x + cat.w > b.x && cat.x < b.x + b.w && cat.y + cat.h >= roof && cat.y + cat.h <= roof + 12 && cat.vy >= 0) {
            cat.y = roof - cat.h; cat.vy = 0; cat.ground = true;
        }
    });

    if (cat.y > 320) {
        over = true; playSad();
        document.getElementById('status').innerText = "OI KHONG MEO TE ROI ( ´-｀)";
        document.getElementById('status').style.color = "#ef4444";
    }
}

function render() {
    ctx.fillStyle = (weather === 'rain') ? '#0f172a' : (weather ===
