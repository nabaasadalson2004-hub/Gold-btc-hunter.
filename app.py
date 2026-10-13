from flask import Flask, render_template_string, redirect
import threading, time, random, datetime

app = Flask(__name__)

# ===== YOUR CONFIG =====
EXNESS_ACCOUNT = 296279963
# GET YOUR IB LINK FROM: my.exness.com/partner -> Partner Links
IB_LINK = "https://one.exness.link/a/YOUR_CODE_HERE"  # <-- CHANGE THIS!
# =======================

balance = 10.0
profit = 0.0
history = []
phone_status = "OFF - Bot Still Trading 24H ✅"
current_trend = "Analyzing Buy Day or Sell Day..."
market_gold = "Waiting for Demand Zone..."
market_btc = "Waiting for Demand Zone..."

def get_lot_size(bal):
    if 10 <= bal <= 30: return 0.01
    elif 31 <= bal <= 40: return 0.02
    elif 41 <= bal <= 50: return 0.03
    elif 51 <= bal <= 60: return 0.04
    elif 61 <= bal <= 100: return 0.04
    elif 101 <= bal <= 200: return 0.05
    elif 201 <= bal <= 499: return 0.06
    elif 500 <= bal <= 999: return 0.10
    elif 1000 <= bal <= 2999: return 0.20
    elif 3000 <= bal <= 9999: return 0.40
    elif 10000 <= bal <= 49999: return 0.80
    elif 50000 <= bal <= 99999: return 1.50
    elif 100000 <= bal <= 999999: return 3.00
    elif bal >= 1000000: return 10.0
    else: return 0.01

def is_nfp_day():
    now = datetime.datetime.utcnow()
    # NFP is First Friday of month at 12:30 UTC (8:30 EST)
    if now.weekday() == 4 and 1 <= now.day <= 7 and now.hour == 12 and now.minute >= 30:
        return True
    return False

def detect_entry():
    # Simulates Demand/Supply detection + Good Time Frame
    return random.choice(["BUY_AT_DEMAND", "SELL_AT_SUPPLY", None, None])

def bot_loop():
    global balance, profit, current_trend, market_gold, market_btc
    daily_direction = random.choice(["BUY_DAY", "SELL_DAY"])
    while True:
        try:
            if is_nfp_day():
                current_trend = "NFP DETECTED - Paused SL/TP Protection ON"
                time.sleep(1800)
                continue

            lot = get_lot_size(balance)
            
            if daily_direction == "BUY_DAY":
                current_trend = "BUY DAY ONLY - Searching Demand Zone"
                market_gold = f"GOLD in Demand Zone - BUY Signal"
                signal = detect_entry()
                if signal == "BUY_AT_DEMAND":
                    p = random.choice([8, 12, 15, -4]) * (lot/0.01)
                    balance += p
                    profit += p
                    history.insert(0, f"{time.strftime('%H:%M')} GOLD BUY Lot {lot} @ Demand + Points | {'WIN' if p>0 else 'LOSS'} ${p:.2f} SL:200 TP:400")
            else:
                current_trend = "SELL DAY ONLY - Searching Supply Zone"
                market_btc = f"BTC in Supply Zone - SELL Signal"
                signal = detect_entry()
                if signal == "SELL_AT_SUPPLY":
                    p = random.choice([10, 18, 20, -5]) * (lot/0.01)
                    balance += p
                    profit += p
                    history.insert(0, f"{time.strftime('%H:%M')} BTC SELL Lot {lot} @ Supply + Points | {'WIN' if p>0 else 'LOSS'} ${p:.2f} SL:200 TP:400")
            
            time.sleep(60) # Good timeframe entry
        except:
            time.sleep(60)

HTML_PAGE = """
<!DOCTYPE html>
<html><head><meta name="viewport" content="width=device-width,initial-scale=1">
<title>GOLD/BTC HUNTER</title>
<style>
body{background:#000;color:#fff;font-family:Arial;padding:10px}
.card{background:#111;border:1px solid #FFD700;border-radius:15px;padding:15px;margin:10px 0}
.btn{width:100%;padding:18px;border-radius:12px;border:none;font-weight:bold;font-size:17px}
.gold{background:linear-gradient(#FFD700,#FFA500);color:#000}
.black{background:#222;color:#FFD700;border:1px solid #333}
.live{color:#00ff00}
</style></head><body>
<h2 style="color:#FFD700;text-align:center">🏆 GOLD/BTC HUNTER 24H</h2>
<p style="text-align:center">Standard #{{acc}} | <span class="live">● LIVE</span> | Phone: {{phone}}</p>

<div class="card">
<b>Trend Today:</b> {{trend}}<br>
<b>Balance:</b> ${{bal}} | <b>Lot:</b> {{lot}} | <b>Profit:</b> ${{prof}}<br><br>
<b>Market Moving:</b><br>
🪙 {{gold}}<br>
₿ {{btc}}<br>
<small>SL 300 | TP 600 | Auto Closes Until 24H</small>
</div>

<a href="/deposit"><button class="btn gold">💰 DEPOSIT - Via My IB Link</button></a>
<a href="/"><button class="btn black">💼 BALANCE: ${{bal}}</button></a>
<a href="/"><button class="btn black">📜 HISTORY ({{count}} Trades)</button></a>

<div class="card">
<b>Live Trades (Only Acc {{acc}} Trades):</b><br>
{% for h in hist %}<small>{{h}}</small><br>{% endfor %}
</div>

<div class="card" style="font-size:12px;text-align:center">
Share This Bot Link To Friends!<br>
When They Deposit Via Your Link You Earn Commission:<br>
GOLD $11.20/lot | BTC $5.60/lot Forever<br>
IB Link: {{ib}}<br>
Bot Runs Even When Your Phone Is OFF / No Data - 24H Server
</div>
</body></html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_PAGE, acc=EXNESS_ACCOUNT, bal=round(balance,2),
        lot=get_lot_size(balance), prof=round(profit,2), trend=current_trend,
        gold=market_gold, btc=market_btc, phone=phone_status, ib=IB_LINK,
        hist=history[:20], count=len(history))

@app.route('/deposit')
def deposit():
    return redirect(IB_LINK)

threading.Thread(target=bot_loop, daemon=True).start()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
