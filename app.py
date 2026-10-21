import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Meo Den Mat Vang 2D Jump", layout="centered")

st.title("Game Meo Den Mat Vang 2D")
st.write("Dieu khien meo den mat vang nhay qua cac toa nha 2D - Co nhac nen va hieu ung am thanh!")

game_html = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>Black Cat 2D Jump Audio</title>
    <style>
        body {
            background-color: #0f172a;
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
            box-shadow: 0 8px 20px rgba(0,0,0,0.6);
            border: 2px solid #38bdf8;
            border-radius: 8px;
            overflow: hidden;
        }
        canvas {
            display: block;
            background-color: #0b1329;
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
            padding: 12px 20px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            user-select: none;
        }
        .jump-btn {
            background-color: #f59e0b;
            color: #0f172a;
            flex-grow: 2;
            box-shadow: 0 4px 10px rgba(245, 158, 11, 0.4);
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
        <canvas id="gameCanvas" height="300" width="720"></canvas>
    </div>
    
    <div id="ui-panel">
        <div>DIEM: <span id="score-txt">0</span></div>
        <div>TRANG THAI: <span id="status-txt" style="color: #38bdf8;">SAN SANG</span></div>
        <div>KY LUC: <span id="high-txt">0</span></div>
    </div>

    <div id="control-panel">
        <button class="btn sound-btn" id="audio-toggle" onclick="toggleAudio()">AM THANH: OFF</button>
        <button class="btn jump-btn" onclick="triggerJump()">NHẢY (JUMP)</button>
    </div>

    <script>
        const canvas = document.getElementById('gameCanvas');
        const ctx = canvas.getContext('2d');

        let score = 0;
        let highScore = 0;
        let isGameOver = false;
        let speed = 4;
        let audioEnabled = false;

        // Sound System dung Web Audio API
        const AudioCtx = window.AudioContext || window.webkitAudioContext;
        let audioCtx = null;
        let bgOsc = null;
        let bgGain = null;

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
                btn.innerText = "AM THANH: ON";
                btn.style.backgroundColor = "#22c55e";
                startBgMusic();
            } else {
                btn.innerText = "AM THANH: OFF";
                btn.style.backgroundColor = "#38bdf8";
                stopBgMusic();
            }
        }

        function playJumpSound() {
            if (!audioEnabled || !audioCtx) return;
            const osc = audioCtx.createOscillator();
            const gain = audioCtx.createGain();
            osc.type = 'sine';
            osc.frequency.setValueAtTime(150, audioCtx.currentTime);
            osc.frequency.exponentialRampToValueAtTime(400, audioCtx.currentTime + 0.15);
            gain.gain.setValueAtTime(0.2, audioCtx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.15);
            osc.connect(gain);
            gain.connect(audioCtx.destination);
            osc.start();
            osc.stop(audioCtx.currentTime + 0.15);
        }

        function startBgMusic() {
            if (!audioCtx) return;
            stopBgMusic();
            bgOsc = audioCtx.createOscillator();
            bgGain = audioCtx.createGain();
            bgOsc.type = 'triangle';
            bgOsc.frequency.setValueAtTime(110, audioCtx.currentTime);
            bgGain.gain.setValueAtTime(0.05, audioCtx.currentTime);
            bgOsc.connect(bgGain);
            bgGain.connect(audioCtx.destination);
            bgOsc.start();
        }

        function stopBgMusic() {
            if (bgOsc) {
                bgOsc.stop();
                bgOsc = null;
            }
        }

        // Chú Mèo Đen Mắt Vàng
        const cat = {
            x: 80,
            y: 150,
            w: 26,
            h: 18,
            vy: 0,
            gravity: 0.65,
            jumpPower: -11.5,
            isGrounded: false,

            draw() {
                // Than meo den
                ctx.fillStyle = '#050811';
                ctx.fillRect(this.x, this.y, this.w, this.h);

                // Dau meo den
                ctx.fillRect(this.x + 14, this.y - 8, 12, 12);

                // Tai meo den (2 hinh tam giac)
                ctx.beginPath();
                ctx.moveTo(this.x + 14, this.y - 8);
                ctx.lineTo(this.x + 17, this.y - 14);
                ctx.lineTo(this.x + 19, this.y - 8);
                ctx.fillStyle = '#050811';
                ctx.fill();

                ctx.beginPath();
                ctx.moveTo(this.x + 20, this.y - 8);
                ctx.lineTo(this.x + 23, this.y - 14);
                ctx.lineTo(this.x + 25, this.y - 8);
                ctx.fill();

                // MAT VANG CHOI SANG (Yellow Eyes)
                ctx.fillStyle = '#facc15';
                ctx.fillRect(this.x + 20, this.y - 5, 4, 4);

                // Con ngươi mau den trong mat
                ctx.fillStyle = '#000000';
                ctx.fillRect(this.x + 21, this.y - 5, 2, 4);

                // Duoi meo den cong len
                ctx.strokeStyle = '#050811';
                ctx.lineWidth = 3;
                ctx.beginPath();
                ctx.moveTo(this.x, this.y + 10);
                ctx.quadraticCurveTo(this.x - 8, this.y + 2, this.x - 6, this.y - 6);
                ctx.stroke();
            }
        };

        // Danh sach cac toa nha 2D
        let buildings = [
            { x: 0, w: 220, h: 120 },
            { x: 260, w: 180, h: 140 },
            { x: 480, w: 200, h: 110 },
            { x: 720, w: 220, h: 130 }
        ];

        function triggerJump() {
            initAudio();
            if (isGameOver) {
                resetGame();
                return;
            }
            if (cat.isGrounded) {
                cat.vy = cat.jumpPower;
                cat.isGrounded = false;
                playJumpSound();
            }
        }

        window.addEventListener('keydown', (e) => {
            if (e.code === 'Space' || e.key === 'ArrowUp' || e.key === 'w') {
                triggerJump();
            }
        });

        function resetGame() {
            score = 0;
            speed = 4;
            isGameOver = false;
            cat.y = 100;
            cat.vy = 0;
            buildings = [
                { x: 0, w: 220, h: 120 },
                { x: 260, w: 180, h: 140 },
                { x: 480, w: 200, h: 110 },
                { x: 720, w: 220, h: 130 }
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
                const gap = 50 + Math.random() * 55;
                const newW = 150 + Math.random() * 100;
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

                if (score % 40 === 0) speed += 0.3;
            }

            cat.isGrounded = false;
            buildings.forEach(b => {
                const roofY = canvas.height - b.h;
                if (
                    cat.x + cat.w > b.x &&
                    cat.x < b.x + b.w &&
                    cat.y + cat.h >= roofY &&
                    cat.y + cat.h <= roofY + 10 &&
                    cat.vy >= 0
                ) {
                    cat.y = roofY - cat.h;
                    cat.vy = 0;
                    cat.isGrounded = true;
                }
            });

            if (cat.y > canvas.height) {
                isGameOver = true;
                document.getElementById('status-txt').innerText = "THUA - NHAN NHAY DE CHOI LAI";
                document.getElementById('status-txt').style.color = "#ef4444";
            }
        }

        function render() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // Ve ngoi sao lung linh tren bau troi
            ctx.fillStyle = '#ffffff';
            ctx.fillRect(100, 30, 2, 2);
            ctx.fillRect(250, 50, 2, 2);
            ctx.fillRect(420, 20, 2, 2);
            ctx.fillRect(580, 40, 2, 2);

            // Ve MAT TRANG VANG DONG 2D (Moon)
            ctx.fillStyle = '#fef08a';
            ctx.beginPath();
            ctx.arc(640, 45, 18, 0, Math.PI * 2);
            ctx.fill();

            ctx.fillStyle = '#fde047';
            ctx.beginPath();
            ctx.arc(636, 42, 14, 0, Math.PI * 2);
            ctx.fill();

            // Ve cac toa nha 2D phang
            buildings.forEach(b => {
                const roofY = canvas.height - b.h;

                // Khoi toa nha 2D
                ctx.fillStyle = '#0f172a';
                ctx.fillRect(b.x, roofY, b.w, b.h);

                // Vien noc
                ctx.fillStyle = '#475569';
                ctx.fillRect(b.x, roofY, b.w, 4);

                // Cua so 2D sang den
                ctx.fillStyle = '#fbbf24';
                for (let wx = b.x + 12; wx < b.x + b.w - 12; wx += 20) {
                    for (let wy = roofY + 15; wy < canvas.height - 8; wy += 22) {
                        ctx.fillRect(wx, wy, 8, 10);
                    }
                }
            });

            // Ve meo den mat vang
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

