# # from flask import Flask, request, abort

# # app = Flask(__name__)

# # @app.route('/webhook', methods=['POST'])
# # def receive_data():
# #     if request.method != 'POST':
# #         abort(403)  # POST以外を禁止
# #     data = request.form
# #     print("===== 📞 Webhook Data Received! =====")
# #     print(f"Caller: {data.get('caller')}")
# #     print(f"Recipient: {data.get('recipient')}")
# #     print(f"Call Time: {data.get('call_time')}")
# #     print("======================================")
# #     return "Data received!", 200

# # # if __name__ == '__main__':
# # #     app.run(host='127.0.0.1', port=5002, debug=True)

# # if __name__ == '__main__':
# #     app.run(host='0.0.0.0', port=5002, debug=True)

# from flask import Flask, request, render_template_string

# app = Flask(__name__)

# # 受信したデータを保持するグローバル変数（単純なデモ用）
# received_data = {}

# @app.route('/webhook', methods=['POST'])
# def receive_data():
#     global received_data
#     data = request.form
#     received_data = {
#         "caller": data.get('caller'),
#         "recipient": data.get('recipient'),
#         "call_time": data.get('call_time')
#     }
#     print("===== 📞 Webhook Data Received! =====")
#     print(f"Caller: {received_data['caller']}")
#     print(f"Recipient: {received_data['recipient']}")
#     print(f"Call Time: {received_data['call_time']}")
#     print("======================================")
#     return "Data received!", 200

# @app.route('/display', methods=['GET'])
# def display_data():
#     if received_data:
#         return render_template_string("""
#             <h1>Webhook Data</h1>
#             <p><strong>Caller:</strong> {{ caller }}</p>
#             <p><strong>Recipient:</strong> {{ recipient }}</p>
#             <p><strong>Call Time:</strong> {{ call_time }}</p>
#         """, **received_data)
#     else:
#         return "No data received yet."

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5002, debug=True)

# import os
# app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))


from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def receive_data():
    # JSON形式でも form形式でも対応できるように
    data = request.get_json() if request.is_json else request.form

    caller = data.get('caller', 'No Data')
    recipient = data.get('recipient', 'No Data')
    call_time = data.get('call_time', 'No Data')

    print("===== 📞 Webhook Data Received! =====")
    print(f"Caller: {caller}")
    print(f"Recipient: {recipient}")
    print(f"Call Time: {call_time}")
    print("======================================")

    return "Data received!", 200

@app.route('/display')
def display_data():
    return render_template('display.html', caller=caller, recipient=recipient, call_time=call_time)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
