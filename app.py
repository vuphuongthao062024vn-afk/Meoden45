import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Meo Den Mat Vang 2D Deluxe", layout="centered")

st.title("Game Meo Den Mat Vang 2D")
st.write("Meo den nhay qua cac toa nha - Co tieng Meow, nhac nen to hon va hieu ung sang dan theo diem so!")

game_html = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>Black Cat Deluxe Jump</title>
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
            box-shadow: 0 8px 20px rgba(0,0,0,0.8);
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

        // Audio API cho nhac nen to hon va tieng Meow
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

        // Tieng Meow vui nhộn khi nhay
        function playMeowSound() {
            if (!audioEnabled || !audioCtx) return;
            const osc = audioCtx.createOscillator();
            const gain = audioCtx.createGain();
            osc.type = 'sine';
            osc.frequency.setValueAtTime(400, audioCtx.currentTime);
            osc.frequency.exponentialRampToValueAtTime(700, audioCtx.currentTime + 0.1);
            osc.frequency.exponentialRampToValueAtTime(300, audioCtx.currentTime + 0.3);
            
            gain.gain.setValueAtTime(0.25, audioCtx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.3);

            osc.connect(gain);
            gain.connect(audioCtx.destination);
            osc.start();
            osc.stop(audioCtx.currentTime + 0.3);
        }

        function startBgMusic() {
            if (!audioCtx) return;
            stopBgMusic();
            bgOsc = audioCtx.createOscillator();
            bgGain = audioCtx.createGain();
            bgOsc.type = 'triangle';
            bgOsc.frequency.setValueAtTime(130, audioCtx.currentTime);
            
            // Tang am luong nhac nen to hon
            bgGain.gain.setValueAtTime(0.12, audioCtx.currentTime);
            
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

        // Meo den mat vang to ro, sac net
        const cat = {
            x: 90,
            y: 140,
            w: 30,
            h: 22,
            vy: 0,
            gravity: 0.65,
            jumpPower: -11.5,
            isGrounded: false,

            draw() {
                // Bong meo
                ctx.fillStyle = 'rgba(0,0,0,0.4)';
                ctx.beginPath();
                ctx.ellipse(this.x + 15, this.y + this.h + 2, 12, 4, 0, 0, Math.PI * 2);
                ctx.fill();

                // Than meo den
                ctx.fillStyle = '#020617';
                ctx.fillRect(this.x, this.y, this.w, this.h);

                // Dau meo den
                ctx.fillRect(this.x + 16, this.y - 10, 14, 14);

                // Tai meo sac nhon
                ctx.beginPath();
                ctx.moveTo(this.x + 16, this.y - 10);
                ctx.lineTo(this.x + 19, this.y - 18);
                ctx.lineTo(this.x + 22, this.y - 10);
                ctx.fillStyle = '#020617';
                ctx.fill();

                ctx.beginPath();
                ctx.moveTo(this.x + 23, this.y - 10);
                ctx.lineTo(this.x + 26, this.y - 18);
                ctx.lineTo(this.x + 29, this.y - 10);
                ctx.fill();

                // Mat vang choi sang dac trung
                ctx.fillStyle = '#facc15';
                ctx.fillRect(this.x + 23, this.y - 6, 5, 5);

                // Con ngươi den trong mat
                ctx.fillStyle = '#000000';
                ctx.fillRect(this.x + 25, this.y - 6, 2, 5);

                // Mui hong nho
                ctx.fillStyle = '#fda4af';
                ctx.fillRect(this.x + 27, this.y - 2, 2, 2);

                // Duoi meo den cong vuot cong
                ctx.strokeStyle = '#020617';
                ctx.lineWidth = 3;
                ctx.beginPath();
                ctx.moveTo(this.x, this.y + 12);
                ctx.quadraticCurveTo(this.x - 10, this.y + 2, this.x - 6, this.y - 6);
                ctx.stroke();
            }
        };

        // Danh sach cac toa nha
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
                playMeowSound();
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

                // Tang toc do moi khi vuot qua toa nha
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
                document.getElementById('status-txt').innerText = "THUA - NHAN NHAY DE CHOI LAI";
                document.getElementById('status-txt').style.color = "#ef4444";
            }
        }

        function render() {
            // Hieu ung troi sang dan theo diem so (Mỗi 10 điểm trời sáng lên một chút)
            let brightnessFactor = Math.min(score * 0.015, 0.7);
            
            let skyR = Math.floor(15 + brightnessFactor * 120);
            let skyG = Math.floor(23 + brightnessFactor * 140);
            let skyB = Math.floor(42 + brightnessFactor * 160);
            
            ctx.fillStyle = `rgb(${skyR}, ${skyG}, ${skyB})`;
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            // Ve sao lung linh ban dem (mo dan khi troi sang)
            if (brightnessFactor < 0.4) {
                ctx.fillStyle = '#ffffff';
                ctx.fillRect(110, 40, 2, 2);
                ctx.fillRect(270, 60, 2, 2);
                ctx.fillRect(450, 30, 2, 2);
                ctx.fillRect(600, 50, 2, 2);
            }

            // Ve Mat Trang sang ruc ro
            ctx.fillStyle = '#fef08a';
            ctx.beginPath();
            ctx.arc(630, 50, 20, 0, Math.PI * 2);
            ctx.fill();

            // Ve cac toa nha ro net va chi tiet hon
            buildings.forEach(b => {
                const roofY = canvas.height - b.h;

                // Than toa nha
                ctx.fillStyle = '#090d16';
                ctx.fillRect(b.x, roofY, b.w, b.h);

                // Vien noc sang ro
                ctx.fillStyle = '#64748b';
                ctx.fillRect(b.x, roofY, b.w, 6);

                // Cua so vang sang ruc ro
                ctx.fillStyle = '#fde047';
                for (let wx = b.x + 14; wx < b.x + b.w - 14; wx += 22) {
                    for (let wy = roofY + 16; wy < canvas.height - 10; wy += 24) {
                        ctx.fillRect(wx, wy, 9, 12);
                    }
                }
            });

            // Ve chu meo den ro net
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
