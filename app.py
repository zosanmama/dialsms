from flask import Flask, request, render_template, session

import os  # os を先にインポートする

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your_secret_key')  # セッション用の秘密鍵

@app.route('/webhook', methods=['POST'])
def webhook():
    content_type = request.headers.get('Content-Type')

    if content_type == 'application/json':
        data = request.get_json()
    elif content_type == 'application/x-www-form-urlencoded':
        data = request.form.to_dict()
    else:
        return "Unsupported Content-Type", 400

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
    return render_template(
        'display.html',
        caller=session.get('caller', 'No Data'),
        recipient=session.get('recipient', 'No Data'),
        call_time=session.get('call_time', 'No Data')
    )

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
