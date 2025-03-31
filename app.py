from flask import Flask, request, render_template, session
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your_secret_key')  # 環境変数から取得

# 📧 メール送信関数
def send_email(caller, recipient, call_time):
    sender_email = "junemomohanamaru@gmail.com"  # 送信元のGmailアドレス
    receiver_email = "aiko@xoxzo.com"  # 受信先のメールアドレス
    password = "cmpa trxd hmxe jffy"  # Gmailの「アプリパスワード」を使う

    subject = "📞 新しいWebhook通知"
    body = f"""
    新しい通話データを受信しました！
    
    📌 Caller: {caller}
    📌 Recipient: {recipient}
    📌 Call Time: {call_time}
    
    """

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        print("📧 メール送信成功！")
    except Exception as e:
        print(f"⚠️ メール送信エラー: {e}")

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

    # 📧 メール送信
    send_email(session['caller'], session['recipient'], session['call_time'])

    return "Data received!", 200

@app.route('/display')
def display_data():
    return render_template(
        'display.html',
        caller=session.get('caller', 'No Data'),
        recipient=session.get('recipient', 'No Data'),
        call_time=session.get('call_time', 'No Data')
    )

import os
app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
