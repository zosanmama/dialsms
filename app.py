from flask import Flask, request, render_template, session

app = Flask(__name__)
app.secret_key = "supersecretkey"  # sessionを使うのに必須！

# Webhookデータを受け取る
# @app.route('/webhook', methods=['POST'])
# def webhook():
#     data = request.form  # POSTデータを取得
#     session['caller'] = data.get('caller', 'Unknown')
#     session['recipient'] = data.get('recipient', 'Unknown')
#     session['call_time'] = data.get('call_time', 'Unknown')
#     return "Data received!", 200

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form

    session['caller'] = data.get('caller', 'Unknown')
    session['recipient'] = data.get('recipient', 'Unknown')
    session['call_time'] = data.get('call_time', 'Unknown')

    return "Data received!", 200



# データを表示する
@app.route('/display', methods=['GET'])
def display_data():
    return render_template(
        'display.html',
        caller=session.get('caller'),
        recipient=session.get('recipient'),
        call_time=session.get('call_time')
    )

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5002, debug=True)
