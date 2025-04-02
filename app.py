from flask import Flask, request, render_template, session
from datetime import datetime
import os
import pytz
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your_secret_key')

def format_timestamp(timestamp):
    try:
        dt_utc = datetime.utcfromtimestamp(float(timestamp))
        dt_jst = dt_utc.replace(tzinfo=pytz.utc).astimezone(pytz.timezone("Asia/Tokyo"))
        return dt_jst.strftime('%Y-%m-%d %H:%M:%S')
    except Exception as e:
        print(f"⚠️ タイムスタンプ変換エラー: {e}")
        return "Unknown"

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form

    session['caller'] = data.get('caller', 'Unknown')
    session['recipient'] = data.get('recipient', 'Unknown')
    session['call_time'] = format_timestamp(data.get('call_time', 'Unknown'))

    print("===== 📞 Webhook Data Received! =====")
    print(f"Caller: {session['caller']}")
    print(f"Recipient: {session['recipient']}")
    print(f"Call Time: {session['call_time']}")
    print("======================================")

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

def send_email(caller, recipient, call_time):
    sender_email = "your_email@example.com"
    receiver_email = "notify@example.com"
    subject = "📞 New Call Notification"
    body = f"Caller: {caller}\nRecipient: {recipient}\nCall Time: {call_time}"

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP('smtp.example.com', 587) as server:
            server.starttls()
            server.login("your_email@example.com", "your_password")
            server.sendmail(sender_email, receiver_email, msg.as_string())
            print("📧 メール送信成功！")
    except Exception as e:
        print(f"⚠️ メール送信エラー: {e}")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
