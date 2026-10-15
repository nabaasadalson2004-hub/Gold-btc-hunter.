
from flask import Flask, render_template_string

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
<title>BTC Gold Hunter - Build Your Future</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body { font-family: Arial; background: #f5f5f5; padding: 15px; text-align: center; }
.title { color: #0066ff; font-size: 32px; font-weight: bold; }
.status { color: green; font-size: 22px; font-weight: bold; margin: 10px; }
.btns { display: flex; justify-content: center; gap: 10px; margin: 15px; }
.btn { padding: 15px 25px; border-radius: 10px; font-size: 18px; font-weight: bold; border: none; cursor: pointer; }
.balance { background: #d0e1ff; color: #001a66; }
.deposit { background: #ffcc00; color: #000; }
.graph-box { background: white; border-radius: 15px; padding: 15px; margin-top: 15px; text-align: left; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
.supply { background: #ffcccc; padding: 8px; border-left: 5px solid red; }
.demand { background: #ccffcc; padding: 8px; border-left: 5px solid green; }
a { text-decoration: none; }
</style>
</head>
<body>
<div class="title">Build your future</div>
<div class="status">The bot is buying - BUY DAY</div>

<div class="btns">
<button class="btn balance">Balance: $20.00</button>
<a href="https://one.exness.link/a/296279963" target="_blank">
<button class="btn deposit">Deposit -> Exness</button>
</a>
</div>

<div class="graph-box">
<h3>Market Moving + Entry Graph:</h3>
<div class="supply">Supply Zone -> SELL entry (Top) - Bot will SELL here</div>
<p style="text-align:center;">📈 Chart: BTC/USD M5 Live - Candlesticks moving...</p>
<p>Entry: <b>BOT ACTIVE -> BUY</b> at Demand Zone</p>
<div class="demand">Demand Zone -> BUY entry (Bottom) - Bot will BUY here</div>
<br>
<p><b>Graph showing where the bot will sell or buy and showing the entry</b></p>
<hr>
<p>Lot Table: $10-30 = 0.01 | $31-40 = 0.02 ... $1M = 10.0</p>
<p>SL 30 pips | TP 60 pips | NFP Detector | 24Hrs Auto - Phone OFF Works</p>
<p>Exness Standard #296279963</p>
<br>
<a href="https://github.com" target="_blank">
<button style="padding:12px; background:#000; color:#fff; border-radius:8px; width:100%;">Download Bot .mq5 for MT5 VPS</button>
</a>
</div>

<p style="color:gray; font-size:12px;">BTC Gold Hunter - Trades Gold + BTC 24Hrs | Buys whole day / Sells whole day</p>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
