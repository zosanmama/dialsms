from flask import Flask, request, render_template, session

app = Flask(__name__)
# app.secret_key = 'your_secret_key'  # セッション用の秘密鍵（適当に変えてOK）

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form

    session['caller'] = data.get('caller', 'Unknown')
    session['recipient'] = data.get('recipient', 'Unknown')
    session['call_time'] = data.get('call_time', 'Unknown')

    print("===== 📞 Webhook Data Received! =====")
    print(f"Caller: {session['caller']}")
    print(f"Recipient: {session['recipient']}")
    print(f"Call Time: {session['call_time']}")
    print("======================================")

    return "Data received!", 200

@app.route('/display')
def display_data():
    # セッションからデータを取り出して表示
    return render_template(
        'display.html',
        caller=session.get('caller', 'No Data'),
        recipient=session.get('recipient', 'No Data'),
        call_time=session.get('call_time', 'No Data')
    )

import os
app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
