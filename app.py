import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Meo Den Mat Vang Chimi Changa", layout="centered")

st.title("Game Meo Den Mat Vang 2D")
st.write("Song: Chimi Chimi Changa (TikTok Trend) | Co nui phia sau, den duong va meo nhay 1 cham!")

game_html = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>Black Cat Chimi Changa Run</title>
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
        <button class="btn sound-btn" id="audio-toggle" onclick="toggleAudio()">NHAC (CHIMI CHANGA): OFF</button>
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

        // Web Audio API - Melody Chimi Chimi Changa (TikTok)
        const AudioCtx = window.AudioContext || window.webkitAudioContext;
        let audioCtx = null;
        let bgInterval = null;

        // Giai điệu Chimi Chimi Changa TikTok
        const chimiNotes = [
            587.33, 659.25, 659.25, 587.33, 659.25, 659.25, // Chi-mi chi-mi chan-ga
            783.99, 783.99, 659.25, 587.33,               // Chi-mi chi-mi
            587.33, 659.25, 659.25, 587.33, 659.25, 659.25, // Chi-mi chi-mi chan-ga
            880.00, 783.99, 659.25, 523.25                // Changa lalala
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
                btn.innerText = "NHAC (CHIMI CHANGA): ON";
                btn.style.backgroundColor = "#22c55e";
                startBgMusic();
            } else {
                btn.innerText = "NHAC (CHIMI CHANGA): OFF";
                btn.style.backgroundColor = "#38bdf8";
                stopBgMusic();
            }
        }

        // Tieng Meow ngot ngat khi nhay
        function playMeowSound() {
            if (!audioEnabled || !audioCtx) return;
            const osc = audioCtx.createOscillator();
            const gain = audioCtx.createGain();
            osc.type = 'triangle';
            
            osc.frequency.setValueAtTime(450, audioCtx.currentTime);
            osc.frequency.linearRampToValueAtTime(780, audioCtx.currentTime + 0.12);
            osc.frequency.linearRampToValueAtTime(360, audioCtx.currentTime + 0.28);

            gain.gain.setValueAtTime(0.35, audioCtx.currentTime);
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
                osc.frequency.setValueAtTime(chimiNotes[noteIdx], audioCtx.currentTime);
                
                gain.gain.setValueAtTime(0.09, audioCtx.currentTime);
                gain.gain.exponentialRampToValueAtTime(0.005, audioCtx.currentTime + 0.18);

                osc.connect(gain);
                gain.connect(audioCtx.destination);
                osc.start();
                osc.stop(audioCtx.currentTime + 0.18);

                noteIdx = (noteIdx + 1) % chimiNotes.length;
            }, 200);
        }

        function stopBgMusic() {
            if (bgInterval) {
                clearInterval(bgInterval);
                bgInterval = null;
            }
        }

        // Meo Den Mat Vang
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

                // Than meo den
                ctx.fillStyle = '#020617';
                ctx.fillRect(this.x, this.y, this.w, this.h);

                // Dau meo den
                ctx.fillRect(this.x + 18, this.y - 12, 16, 16);

                // Tai meo sac nhon
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

                // Vien hong trong tai
                ctx.fillStyle = '#f43f5e';
                ctx.fillRect(this.x + 21, this.y - 16, 2, 4);
                ctx.fillRect(this.x + 29, this.y - 16, 2, 4);

                // MAT VANG LONG LANH
                ctx.fillStyle = '#facc15';
                ctx.fillRect(this.x + 25, this.y - 8, 6, 6);

                // Con ngươi mau den
                ctx.fillStyle = '#000000';
                ctx.fillRect(this.x + 28, this.y - 8, 2, 6);

                // Mui hong va rau meo
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

                // Duoi meo uon cong
                ctx.strokeStyle = '#020617';
                ctx.lineWidth = 3;
                ctx.beginPath();
                ctx.moveTo(this.x, this.y + 12);
                ctx.quadraticCurveTo(this.x - 12, this.y + 2, this.x - 8, this.y - 8);
                ctx.stroke();
            }
        };

        // Danh sach toa nha - Khoang cach xa hon xieu
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
            speed = 4.2;
            isGameOver = false;
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
        }

        function update() {
            if (isGameOver) return;

            cat.vy += cat.gravity;
            cat.y += cat.vy;

            buildings.forEach(b => b.x -= speed);

            if (buildings[0].x + buildings[0].w < 0) {
                buildings.shift();
                const last = buildings[buildings.length - 1];
                const gap = 70 + Math.random() * 60;
                const newW = 160 + Math.random() * 100;
                const newH = 90 + Math.random() * 60;
                buildings.push({
                    x: last.x + last.w + gap,
                    w: newW,
                    h: newH
                });

                score += 10;
                if (score > highScore) highScore = score;
                document.getElementById('score-txt').innerText = score;
                document.getElementById('high-txt').innerText = highScore;

                speed += 0.35;
            }

            cat.isGrounded = false;
            buildings.forEach(b => {
                const roofY = canvas.height - b.h;
                if (
                    cat.x + cat.w > b.x &&
                    cat.x < b.x + b.w &&
                    cat.y + cat.h >= roofY &&
                    cat.y + cat.h <= roofY + 12 &&
                    cat.vy >= 0
                ) {
                    cat.y = roofY - cat.h;
                    cat.vy = 0;
                    cat.isGrounded = true;
                }
            });

            if (cat.y > canvas.height) {
                isGameOver = true;
                document.getElementById('status-txt').innerText = "THUA - BAM NHAY DE CHOI LAI";
                document.getElementById('status-txt').style.color = "#ef4444";
            }
        }

        function render() {
            let brightnessFactor = Math.min(score * 0.015, 0.7);
            
            let skyR = Math.floor(11 + brightnessFactor * 120);
            let skyG = Math.floor(15 + brightnessFactor * 140);
            let skyB = Math.floor(25 + brightnessFactor * 160);
            
            ctx.fillStyle = "rgb(" + skyR + ", " + skyG + ", " + skyB + ")";
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            // NUI PHIA SAU
            let mR = Math.floor(skyR * 0.5);
            let mG = Math.floor(skyG * 0.5);
            let mB = Math.floor(skyB * 0.7);
            ctx.fillStyle = "rgb(" + mR + ", " + mG + ", " + mB + ")";
            ctx.beginPath();
            ctx.moveTo(0, canvas.height - 40);
            ctx.lineTo(120, canvas.height - 130);
            ctx.lineTo(260, canvas.height - 50);
            ctx.lineTo(410, canvas.height - 150);
            ctx.lineTo(580, canvas.height - 60);
            ctx.lineTo(720, canvas.height - 140);
            ctx.lineTo(720, canvas.height);
            ctx.lineTo(0, canvas.height);
            ctx.fill();

            // MAT TRANG
            ctx.fillStyle = '#fef08a';
            ctx.beginPath();
            ctx.arc(620, 50, 22, 0, Math.PI * 2);
            ctx.fill();

            // TOA NHA 2D
            buildings.forEach(b => {
                const roofY = canvas.height - b.h;

                ctx.fillStyle = '#0f172a';
                ctx.fillRect(b.x, roofY, b.w, b.h);

                ctx.fillStyle = '#475569';
                ctx.fillRect(b.x, roofY, b.w, 6);

                ctx.fillStyle = '#fde047';
                for (let wx = b.x + 14; wx < b.x + b.w - 14; wx += 22) {
                    for (let wy = roofY + 16; wy < canvas.height - 10; wy += 24) {
                        ctx.fillRect(wx, wy, 9, 12);
                    }
                }

                // DEN DUONG
                ctx.fillStyle = '#94a3b8';
                ctx.fillRect(b.x + b.w + 15, canvas.height - 40, 3, 40);
                ctx.fillStyle = '#fef08a';
                ctx.beginPath();
                ctx.arc(b.x + b.w + 16, canvas.height - 42, 5, 0, Math.PI * 2);
                ctx.fill();
            });

            // MEO DEN
            cat.draw();

            update();
            requestAnimationFrame(render);
        }

        render();
    </script>
</body>
</html>
"""

components.html(game_html, height=440)
