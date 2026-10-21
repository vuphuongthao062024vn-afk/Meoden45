import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Meo Den Jump", layout="centered")

st.title("Game Meo Den Mat Vang")

game_html = '''
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>Cat Jump</title>
    <style>
        body { background: #0f172a; color: white; text-align: center; font-family: Arial; margin: 0; padding: 5px; }
        canvas { background: #1e293b; border: 2px solid #38bdf8; border-radius: 8px; display: block; margin: 0 auto; }
        #ui { margin-top: 6px; font-size: 14px; font-weight: bold; }
        .btn { margin-top: 8px; background: #f59e0b; color: #0f172a; border: none; padding: 12px 30px; font-size: 16px; font-weight: bold; border-radius: 8px; cursor: pointer; }
    </style>
</head>
<body>
    <canvas id="gameCanvas" height="280" width="700"></canvas>
    <div id="ui">DIEM: <span id="score">0</span></div>
    <button class="btn" onclick="jumpCat()">NHAY</button>

    <script>
        const canvas = document.getElementById('gameCanvas');
        const ctx = canvas.getContext('2d');

        let score = 0;
        let isOver = false;
        let speed = 4;

        const cat = { x: 80, y: 140, w: 28, h: 20, vy: 0, gravity: 0.6, jump: -10, grounded: false };
        let buildings = [{ x: 0, w: 200, h: 100 }, { x: 250, w: 180, h: 130 }, { x: 470, w: 220, h: 110 }, { x: 730, w: 200, h: 120 }];

        function jumpCat() {
            if (isOver) { resetGame(); return; }
            if (cat.grounded) { cat.vy = cat.jump; cat.grounded = false; }
        }

        window.addEventListener('keydown', (e) => { if (e.key === ' ' || e.key === 'ArrowUp') jumpCat(); });

        function resetGame() {
            score = 0; speed = 4; isOver = false; cat.y = 100; cat.vy = 0;
            buildings = [{ x: 0, w: 200, h: 100 }, { x: 250, w: 180, h: 130 }, { x: 470, w: 220, h: 110 }, { x: 730, w: 200, h: 120 }];
        }

        function update() {
            if (isOver) return;
            cat.vy += cat.gravity; cat.y += cat.vy;
            buildings.forEach(b => b.x -= speed);

            if (buildings[0].x + buildings[0].w < 0) {
                buildings.shift();
                let last = buildings[buildings.length - 1];
                buildings.push({ x: last.x + last.w + 60 + Math.random() * 50, w: 160 + Math.random() * 80, h: 80 + Math.random() * 60 });
                score += 10;
                document.getElementById('score').innerText = score;
                speed += 0.2;
            }

            cat.grounded = false;
            buildings.forEach(b => {
                let roofY = canvas.height - b.h;
                if (cat.x + cat.w > b.x && cat.x < b.x + b.w && cat.y + cat.h >= roofY && cat.y + cat.h <= roofY + 10 && cat.vy >= 0) {
                    cat.y = roofY - cat.h; cat.vy = 0; cat.grounded = true;
                }
            });

            if (cat.y > canvas.height) isOver = true;
        }

        function render() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            
            // Mat trang
            ctx.fillStyle = '#fef08a'; ctx.beginPath(); ctx.arc(620, 40, 16, 0, Math.PI * 2); ctx.fill();

            // Toa nha
            buildings.forEach(b => {
                let roofY = canvas.height - b.h;
                ctx.fillStyle = '#0f172a'; ctx.fillRect(b.x, roofY, b.w, b.h);
                ctx.fillStyle = '#fde047';
                for (let wx = b.x + 12; wx < b.x + b.w - 12; wx += 20) {
                    for (let wy = roofY + 12; wy < canvas.height - 8; wy += 20) {
                        ctx.fillRect(wx, wy, 8, 10);
                    }
                }
            });

            // Meo den mat vang
            ctx.fillStyle = '#020617'; ctx.fillRect(cat.x, cat.y, cat.w, cat.h);
            ctx.fillStyle = '#facc15'; ctx.fillRect(cat.x + 20, cat.y - 5, 4, 4);

            update();
            requestAnimationFrame(render);
        }
        render();
    </script>
</body>
</html>
'''

components.html(game_html, height=400)
