@app.route('/webhook', methods=['POST'])
def webhook():
    # リクエストの Content-Type を確認
    content_type = request.headers.get('Content-Type')

    if content_type == 'application/json':
        data = request.get_json()
    elif content_type == 'application/x-www-form-urlencoded':
        data = request.form.to_dict()
    else:
        return "Unsupported Content-Type", 400

    # 受け取ったデータをセッションに保存
    session['caller'] = data.get('caller', 'Unknown')
    session['recipient'] = data.get('recipient', 'Unknown')
    session['call_time'] = data.get('call_time', 'Unknown')

    print("===== 📞 Webhook Data Received! =====")
    print(f"Caller: {session['caller']}")
    print(f"Recipient: {session['recipient']}")
    print(f"Call Time: {session['call_time']}")
    print("======================================")

    return "Data received!", 200
