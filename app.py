import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Meo Den Mat Vang 2D Jump", layout="centered")

st.title("Game Meo Den Mat Vang 2D")
st.write("Dieu khien meo den mat vang nhay qua cac toa nha 2D!")

game_html = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>Black Cat 2D Jump</title>
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
            background-color: #1e293b;
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
            justify-content: center;
            width: 720px;
        }
        .jump-btn {
            background-color: #f59e0b;
            color: #0f172a;
            border: none;
            border-radius: 8px;
            padding: 14px 40px;
            font-size: 18px;
            font-weight: bold;
            cursor: pointer;
            box-shadow: 0 4px 10px rgba(245, 158, 11, 0.4);
            user-select: none;
            width: 100%;
            max-width: 320px;
        }
        .jump-btn:active {
            background-color: #d97706;
            transform: scale(0.96);
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
        <button class="jump-btn" onclick="triggerJump()">NHẢY (JUMP)</button>
    </div>

    <script>
        const canvas = document.getElementById('gameCanvas');
        const ctx = canvas.getContext('2d');

        let score = 0;
        let highScore = 0;
        let isGameOver = false;
        let speed = 4;

        // Meo den 2D
        const cat = {
            x: 80,
            y: 150,
            w: 24,
            h: 18,
            vy: 0,
            gravity: 0.65,
            jumpPower: -11.5,
            isGrounded: false,

            draw() {
                // Than meo den
                ctx.fillStyle = '#090d16';
                ctx.fillRect(this.x, this.y, this.w, this.h);

                // Dau meo den
                ctx.fillRect(this.x + 12, this.y - 8, 12, 12);

                // Tai meo den
                ctx.beginPath();
                ctx.moveTo(this.x + 13, this.y - 8);
                ctx.lineTo(this.x + 16, this.y - 14);
                ctx.lineTo(this.x + 18, this.y - 8);
                ctx.fillStyle = '#090d16';
                ctx.fill();

                ctx.beginPath();
                ctx.moveTo(this.x + 19, this.y - 8);
                ctx.lineTo(this.x + 22, this.y - 14);
                ctx.lineTo(this.x + 24, this.y - 8);
                ctx.fill();

                // MAT VANG CHOI SANG
                ctx.fillStyle = '#facc15';
                ctx.fillRect(this.x + 19, this.y - 5, 3, 3);

                // Duoi meo
                ctx.strokeStyle = '#090d16';
                ctx.lineWidth = 2;
                ctx.beginPath();
                ctx.moveTo(this.x, this.y + 10);
                ctx.lineTo(this.x - 6, this.y - 2);
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
            if (isGameOver) {
                resetGame();
                return;
            }
            if (cat.isGrounded) {
                cat.vy = cat.jumpPower;
                cat.isGrounded = false;
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

            // Di chuyen toa nha sang trai
            buildings.forEach(b => b.x -= speed);

            // Sinh toa nha moi 2D
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

            // Kiem tra va cham dap noc 2D
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

            // Thua cuoc khi rơi xuong
            if (cat.y > canvas.height) {
                isGameOver = true;
                document.getElementById('status-txt').innerText = "THUA - NHAN NHAY DE CHOI LAI";
                document.getElementById('status-txt').style.color = "#ef4444";
            }
        }

        function render() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // Ve mat trang 2D
            ctx.fillStyle = '#fef08a';
            ctx.beginPath();
            ctx.arc(650, 45, 16, 0, Math.PI * 2);
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

                // Cua so 2D
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
