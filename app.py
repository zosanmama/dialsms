from flask import Flask, request, render_template
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import json
from datetime import datetime
import pytz

def format_timestamp_jst(timestamp):
    try:
        dt_utc = datetime.utcfromtimestamp(float(timestamp))
        dt_jst = dt_utc.replace(tzinfo=pytz.utc).astimezone(pytz.timezone("Asia/Tokyo"))
        return dt_jst.strftime('%Y-%m-%d %H:%M:%S')
    except Exception as e:
        print(f"⚠️ タイムスタンプ変換エラー: {e}")
        return "Unknown"

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your_secret_key')

def format_timestamp(timestamp):
    try:
        dt = datetime.utcfromtimestamp(float(timestamp))  # UTC時間に変換
        return dt.strftime('%Y-%m-%d %H:%M:%S')  # 人間が読める形式
    except Exception as e:
        print(f"⚠️ タイムスタンプ変換エラー: {e}")
        return "Unknown"

# 📧 メール送信関数
def send_email(caller, recipient, call_time):
    sender_email = "junemomohanamaru@gmail.com"  # 送信元のGmailアドレス
    receiver_email = "aikoy31@hotmail.com"  # 受信先のメールアドレス
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
    # 📌 受信したデータの形式をログに記録
    print("📌 受信したデータ (リクエストボディ):", request.data)

    try:
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form.to_dict()  # form データを辞書に変換

        print("📌 パースしたデータ:", data)  # データ構造を確認

        # JSON形式の場合、ネストされているかチェック
        if "results" in data:
            parsed_data = json.loads(data["results"])
            caller = parsed_data.get("caller", "Unknown")
            recipient = parsed_data.get("recipient", "Unknown")
            call_time = parsed_data.get("call_time", "Unknown")
        else:
            caller = data.get("caller", "Unknown")
            recipient = data.get("recipient", "Unknown")
            call_time = data.get("call_time", "Unknown")

    except Exception as e:
        print(f"⚠️ データ取得エラー: {e}")
        return "Invalid Data Format", 400

    # 🔹 タイムスタンプを変換
    formatted_time = format_timestamp(call_time)

    print("===== 📞 Webhook Data Received! =====")
    print(f"Caller: {caller}")
    print(f"Recipient: {recipient}")
    print(f"Call Time: {formatted_time}")
    print("======================================")

    # 📧 メール送信（データを直接渡す）
    send_email(caller, recipient, formatted_time)

    return "Data received!", 200

@app.route('/display')
def display_data():
    return render_template(
        'display.html',
        caller=request.args.get('caller', 'No Data'),
        recipient=request.args.get('recipient', 'No Data'),
        call_time=request.args.get('call_time', 'No Data')
    )

import os
app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
