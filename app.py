import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Meo Den Mat Vang Pinkie Pie Ultimate", layout="centered")

st.title("Game Meo Den Mat Vang 2D")
st.write("Meo Den Run: Co Mua uot nguoi (50d), Nang to mat sức & Bát nuoc hoi suc (90d), Tieng Meow tu nhien va Nhac buon khi te!")

game_html = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>Black Cat Pinkie Pie Ultimate</title>
    <style>
        body {
            background-color: #0b0f19;
            color: #f8fafc;
            font-family: Arial, sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            margin: 0;
            padding: 5px;
        }
        #game-container {
            position: relative;
            box-shadow: 0 8px 24px rgba(0,0,0,0.8);
            border: 2px solid #38bdf8;
            border-radius: 8px;
            overflow: hidden;
        }
        canvas {
            display: block;
        }
        #ui-panel {
            margin-top: 6px;
            background: #0f172a;
            padding: 8px 12px;
            border: 1px solid #334155;
            border-radius: 6px;
            font-size: 13px;
            width: 720px;
            display: flex;
            justify-content: space-between;
            font-weight: bold;
        }
        #control-panel {
            margin-top: 8px;
            display: flex;
            gap: 10px;
            justify-content: center;
            width: 720px;
        }
        .btn {
            border: none;
            border-radius: 8px;
            padding: 14px 20px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            user-select: none;
            touch-action: manipulation;
        }
        .jump-btn {
            background-color: #f59e0b;
            color: #0f172a;
            flex-grow: 2;
            box-shadow: 0 4px 12px rgba(245, 158, 11, 0.4);
        }
        .jump-btn:active {
            background-color: #d97706;
            transform: scale(0.96);
        }
        .sound-btn {
            background-color: #38bdf8;
            color: #0f172a;
            flex-grow: 1;
        }
    </style>
</head>
<body>
    <div id="game-container">
        <canvas id="gameCanvas" height="320" width="720"></canvas>
    </div>
    
    <div id="ui-panel">
        <div>DIEM: <span id="score-txt">0</span></div>
        <div>TRANG THAI: <span id="status-txt" style="color: #38bdf8;">SAN SANG</span></div>
        <div>KY LUC: <span id="high-txt">0</span></div>
    </div>

    <div id="control-panel">
        <button class="btn sound-btn" id="audio-toggle" onclick="toggleAudio()">NHAC (PINKIE PIE): OFF</button>
        <button class="btn jump-btn" id="jump-trigger">NHẢY (1 CHAM)</button>
    </div>

    <script>
        const canvas = document.getElementById('gameCanvas');
        const ctx = canvas.getContext('2d');

        let score = 0;
        let highScore = 0;
        let isGameOver = false;
        let baseSpeed = 3.6;
        let speed = 3.6;
        let audioEnabled = false;

        let weatherMode = 'normal';
        let sunTimer = 0;
        let waterBowls = [];
        let raindrops = [];

        const AudioCtx = window.AudioContext || window.webkitAudioContext;
        let audioCtx = null;
        let bgInterval = null;
        let randomMeowTimer = 0;

        const pinkieVocalNotes = [
            1046.50, 1174.66, 1318.51, 1046.50, 1318.51, 1318.51,
            1396.91, 1396.91, 1318.51, 1174.66, 1046.50, 1174.66,
            1318.51, 1567.98, 1396.91, 1318.51, 1174.66, 1046.50
        ];
        let noteIdx = 0;

        const sadNotes = [329.63, 311.13, 293.66, 277.18, 261.63];

        function initAudio() {
            if (!audioCtx) audioCtx = new AudioCtx();
            if (audioCtx.state === 'suspended') audioCtx.resume();
        }

        function toggleAudio() {
            initAudio();
            audioEnabled = !audioEnabled;
            const btn = document.getElementById('audio-toggle');
            if (audioEnabled) {
                btn.innerText = "NHAC (PINKIE PIE): ON";
                btn.style.backgroundColor = "#22c55e";
                startBgMusic();
            } else {
                btn.innerText = "NHAC (PINKIE PIE): OFF";
                btn.style.backgroundColor = "#38bdf8";
                stopBgMusic();
            }
        }

        function playMeowSound() {
            if (!audioEnabled || !audioCtx) return;
            const osc = audioCtx.createOscillator();
            const gain = audioCtx.createGain();
            osc.type = 'sine';
            
            osc.frequency.setValueAtTime(650, audioCtx.currentTime);
            osc.frequency.linearRampToValueAtTime(1000, audioCtx.currentTime + 0.12);
            osc.frequency.linearRampToValueAtTime(500, audioCtx.currentTime + 0.28);

            gain.gain.setValueAtTime(0.35, audioCtx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.28);

            osc.connect(gain);
            gain.connect(audioCtx.destination);
            osc.start();
            osc.stop(audioCtx.currentTime + 0.28);
        }

        function playSadSong() {
            if (!audioEnabled || !audioCtx) return;
            stopBgMusic();
            let idx = 0;
            let sadInt = setInterval(() => {
                if (idx >= sadNotes.length) { clearInterval(sadInt); return; }
                const osc = audioCtx.createOscillator();
                const gain = audioCtx.createGain();
                osc.type = 'sawtooth';
                osc.frequency.setValueAtTime(sadNotes[idx], audioCtx.currentTime);
                
                gain.gain.setValueAtTime(0.12, audioCtx.currentTime);
                gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.4);

                osc.connect(gain);
                gain.connect(audioCtx.destination);
                osc.start();
                osc.stop(audioCtx.currentTime + 0.4);
                idx++;
            }, 350);
        }

        function startBgMusic() {
            if (!audioCtx) return;
            stopBgMusic();
            bgInterval = setInterval(() => {
                if (!audioEnabled || isGameOver) return;
                const osc = audioCtx.createOscillator();
                const gain = audioCtx.createGain();
                
                osc.type = (noteIdx % 2 === 0) ? 'sine' : 'triangle';
                osc.frequency.setValueAtTime(pinkieVocalNotes[noteIdx], audioCtx.currentTime);
                
                gain.gain.setValueAtTime(0.08, audioCtx.currentTime);
                gain.gain.exponentialRampToValueAtTime(0.005, audioCtx.currentTime + 0.16);

                osc.connect(gain);
                gain.connect(audioCtx.destination);
                osc.start();
                osc.stop(audioCtx.currentTime + 0.16);

                noteIdx = (noteIdx + 1) % pinkieVocalNotes.length;
            }, 180);
        }

        function stopBgMusic() {
            if (bgInterval) {
                clearInterval(bgInterval);
                bgInterval = null;
            }
        }

        for (let i = 0; i < 40; i++) {
            raindrops.push({
                x: Math.random() * 720,
                y: Math.random() * 320,
                len: 8 + Math.random() * 8,
                speedY: 7 + Math.random() * 4
            });
        }

        const cat = {
            x: 90,
            y: 140,
            w: 32,
            h: 22,
            vy: 0,
            gravity: 0.68,
            jumpPower: -11.8,
            isGrounded: false,

            draw() {
                ctx.fillStyle = 'rgba(0,0,0,0.4)';
                ctx.beginPath();
                ctx.ellipse(this.x + 16, this.y + this.h + 2, 14, 4, 0, 0, Math.PI * 2);
                ctx.fill();

                ctx.fillStyle = (weatherMode === 'rain') ? '#090d16' : '#020617';
                ctx.fillRect(this.x, this.y, this.w, this.h);

                ctx.fillRect(this.x + 18, this.y - 12, 16, 16);

                ctx.fillStyle = '#020617';
                ctx.beginPath();
                ctx.moveTo(this.x + 18, this.y - 12);
                ctx.lineTo(this.x + 21, this.y - 20);
                ctx.lineTo(this.x + 25, this.y - 12);
                ctx.fill();

                ctx.beginPath();
                ctx.moveTo(this.x + 27, this.y - 12);
                ctx.lineTo(this.x + 30, this.y - 20);
                ctx.lineTo(this.x + 34, this.y - 12);
                ctx.fill();

                ctx.fillStyle = '#f43f5e';
                ctx.fillRect(this.x + 21, this.y - 16, 2, 4);
                ctx.fillRect(this.x + 29, this.y - 16, 2, 4);

                ctx.fillStyle = '#facc15';
                ctx.fillRect(this.x + 25, this.y - 8, 6, 6);

                ctx.fillStyle = '#000000';
                ctx.fillRect(this.x + 28, this.y - 8, 2, 6);

                ctx.fillStyle = '#fda4af';
                ctx.fillRect(this.x + 31, this.y - 3, 2, 2);

                ctx.strokeStyle = '#94a3b8';
                ctx.lineWidth = 1;
                ctx.beginPath();
                ctx.moveTo(this.x + 33, this.y - 2);
                ctx.lineTo(this.x + 39, this.y - 4);
                ctx.moveTo(this.x + 33, this.y - 1);
                ctx.lineTo(this.x + 39, this.y + 1);
                ctx.stroke();

                ctx.strokeStyle = '#020617';
                ctx.lineWidth = 3;
                ctx.beginPath();
                ctx.moveTo(this.x, this.y + 12);
                ctx.quadraticCurveTo(this.x - 12, this.y + 2, this.x - 8, this.y - 8);
                ctx.stroke();

                if (weatherMode === 'rain') {
                    ctx.fillStyle = '#38bdf8';
                    ctx.fillRect(this.x + 6, this.y + 4, 2, 3);
                    ctx.fillRect(this.x + 20, this.y + 8, 2, 3);
                }
            }
        };

        let buildings = [
            { x: 0, w: 220, h: 120 },
            { x: 290, w: 180, h: 140 },
            { x: 540, w: 200, h: 110 },
            { x: 810, w: 220, h: 130 }
        ];

        function triggerJump(e) {
            if (e) e.preventDefault();
            initAudio();
            if (isGameOver) {
                resetGame();
                return;
            }
            if (cat.isGrounded) {
                cat.vy = cat.jumpPower;
                cat.isGrounded = false;
                playMeowSound();
            }
        }

        const jumpBtn = document.getElementById('jump-trigger');
        jumpBtn.addEventListener('touchstart', triggerJump, {passive: false});
        jumpBtn.addEventListener('click', triggerJump);

        window.addEventListener('keydown', (e) => {
            if (e.code === 'Space' || e.key === 'ArrowUp' || e.key === 'w') {
                triggerJump();
            }
        });

        function resetGame() {
            score = 0;
            baseSpeed = 3.6;
            speed = 3.6;
            isGameOver = false;
            weatherMode = 'normal';
            sunTimer = 0;
            waterBowls = [];
            cat.y = 100;
            cat.vy = 0;
            buildings = [
                { x: 0, w: 220, h: 120 },
                { x: 290, w: 180, h: 140 },
                { x: 540, w: 200, h: 110 },
                { x: 810, w: 220, h: 130 }
            ];
            document.getElementById('status-txt').innerText = "DANG CHAY";
            document.getElementById('status-txt').style.color = "#38bdf8";
            if (audioEnabled) startBgMusic();
        }

        function update() {
            if (isGameOver) return;

            randomMeowTimer++;
            if (randomMeowTimer > 320) {
                if (Math.random() < 0.4) playMeowSound();
                randomMeowTimer = 0;
            }

            if (score >= 50 && score < 90) {
                weatherMode = 'rain';
            } else if (score >= 90) {
                if (sunTimer < 600) {
                    weatherMode = 'sunny';
                    sunTimer++;
                    speed = 2.2;
                } else {
                    weatherMode = 'normal';
                    speed = baseSpeed;
                }
            } else {
                weatherMode = 'normal';
                speed = baseSpeed;
            }
