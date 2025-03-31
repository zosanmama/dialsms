from flask import Flask, request, render_template
import os
import sys 

app = Flask(__name__)

# セッションを使わずにデータを保存する
received_data = {}
 # 追加

@app.route('/webhook', methods=['POST'])
def webhook():
    global received_data

    if request.is_json:
        data = request.get_json()
        print("📌 JSON データを受信:", data)
    else:
        data = request.form.to_dict()
        print("📌 Form データを受信:", data)

    sys.stdout.flush()  # バッファをクリアして即座にログ出力

    received_data = {
        "caller": data.get('caller', 'Unknown'),
        "recipient": data.get('recipient', 'Unknown'),
        "call_time": data.get('call_time', 'Unknown')
    }

    print("===== 📞 Webhook Data Received! =====")
    print(f"Caller: {received_data['caller']}")
    print(f"Recipient: {received_data['recipient']}")
    print(f"Call Time: {received_data['call_time']}")
    print("======================================")

    sys.stdout.flush()  # これも追加

    return "Data received!", 200


@app.route('/display')
def display_data():
    return render_template(
        'display.html',
        caller=received_data.get('caller', 'No Data'),
        recipient=received_data.get('recipient', 'No Data'),
        call_time=received_data.get('call_time', 'No Data')
    )

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
