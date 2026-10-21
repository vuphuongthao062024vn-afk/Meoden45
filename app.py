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
        
