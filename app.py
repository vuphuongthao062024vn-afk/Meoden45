import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Meo Den Mat Vang TikTok Jump", layout="centered")

st.title("Game Meo Den Mat Vang 2D")
st.write("Song: Sophie/Sophia is my kitty | Co nui phia sau, den duong va meo nhay sieu nhay!")

game_html = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>Black Cat Rooftop Run</title>
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
        <button class="btn sound-btn" id="audio-toggle" onclick="toggleAudio()">NHAC (SOPHIA KITTY): OFF</button>
        <button class="btn jump-btn" id="jump-trigger">NHẢY (1 CHAM)</button>
    </div>

    <script>
        const canvas = document.getElementById('gameCanvas');
        const ctx = canvas.getContext('2d');

        let score = 0;
        let highScore = 0;
        let isGameOver = false;
        let speed = 4.2;
        let audioEnabled = false;

        // Web Audio API - Melodic "Sophia is my kitty" TikTok Song Theme
        const AudioCtx = window.AudioContext || window.webkitAudioContext;
        let audioCtx = null;
        let bgInterval = null;

        const melodyNotes = [
            523.25, 587.33, 659.25, 523.25, // C5, D5, E5, C5 (So-phie/So-phi-a)
            659.25, 659.25, 587.33, 523.25, // E5, E5, D5, C5 (is my kit-ty)
            659.25, 698.46, 783.99, 659.25, // E5, F5, G5, E5
            783.99, 783.99, 698.46, 659.25  // G5, G5, F5, E5
        ];
        let noteIdx = 0;

        function initAudio() {
            if (!audioCtx) {
                audioCtx = new AudioCtx();
            }
            if (audioCtx.state === 'suspended') {
                audioCtx.resume();
            }
        }

        function toggleAudio() {
            initAudio();
            audioEnabled = !audioEnabled;
            const btn = document.getElementById('audio-toggle');
            if (audioEnabled) {
                btn.innerText = "NHAC (SOPHIA KITTY): ON";
                btn.style.backgroundColor = "#22c55e";
                startBgMusic();
            } else {
                btn.innerText = "NHAC (SOPHIA KITTY): OFF";
                btn.style.backgroundColor = "#38bdf8";
                stopBgMusic();
            }
        }

        function playMeowSound() {
            if (!audioEnabled || !audioCtx) return;
            const osc = audioCtx.createOscillator();
            const gain = audioCtx.createGain();
            osc.type = 'triangle';
            
            // Hieu ung am thanh tieng Meow ngot ngat
            osc.frequency.setValueAtTime(450, audioCtx.currentTime);
            osc.frequency.linearRampToValueAtTime(750, audioCtx.currentTime + 0.12);
            osc.frequency.linearRampToValueAtTime(350, audioCtx.currentTime + 0.28);

            gain.gain.setValueAtTime(0.3, audioCtx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.28);

            osc.connect(gain);
            gain.connect(audioCtx.destination);
            osc.start();
            osc.stop(audioCtx.currentTime + 0.28);
        }

        function startBgMusic() {
            if (!audioCtx) return;
            stopBgMusic();
            bgInterval = setInterval(() => {
                if (!audioEnabled) return;
                const osc = audioCtx.createOscillator();
                const gain = audioCtx.createGain();
                osc.type = 'square';
                osc.frequency.setValueAtTime(melodyNotes[noteIdx], audioCtx.currentTime);
                
                gain.gain.setValueAtTime(0.06, audioCtx.currentTime);
                gain.gain.exponentialRampToValueAtTime(0.005, audioCtx.currentTime + 0.22);

                osc.connect(gain);
                gain.connect(audioCtx.destination);
                osc.start();
                osc.stop(audioCtx.currentTime + 0.22);

                noteIdx = (noteIdx + 1) % melodyNotes.length;
            }, 250);
        }

        function stopBgMusic() {
            if (bgInterval) {
                clearInterval(bgInterval);
                bgInterval = null;
            }
        }

        // Mèo Đen Mắt Vàng - Thiết kế đẹp hơn
        const cat = {
            x: 90,
            y: 140,
            w: 32,
            h: 22,
            vy: 0,
            gravity: 0.68,
            jumpPower: -12.0,
            isGrounded: false,

            draw() {
                // Bong meo
                ctx.fillStyle = 'rgba(0,0,0,0.4)';
                ctx.beginPath();
                ctx.ellipse(this.x + 16, this.y + this.h + 2, 14, 4, 0, 0, Math.PI * 2);
                ctx.fill();

                // Than meo den hinh khoi
                ctx.fillStyle = '#020617';
                ctx.fillRect(this.x, this.y, this.w, this.h);

                // Dau meo den
                ctx.fillRect(this.x + 18, this.y - 12, 16, 16);

                // Tai meo sac nhon co vien hong
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

                // Trong tai
                ctx.fillStyle = '#f43f5e';
                ctx.fillRect(this.x + 21, this.y - 16, 2, 4);
                ctx.fillRect(29 + this.x, this.y - 16, 2, 4);

                // MAT VANG LONG LANH
                ctx.fillStyle = '#facc15';
                ctx.fillRect(this.x + 25, this.y - 8, 6, 6);

                // Con ngươi mau den trong mat
                ctx.fillStyle = '#000000';
                ctx.fillRect(this.x + 28, this.y - 8, 2, 6);

                // Mui hong va râu meo
                ctx.fillStyle = '#fda4af';
                ctx.fillRect(this.x + 3
