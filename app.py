from flask import Flask, request, render_template
import os
import sys 
import json  # 追加

app = Flask(__name__)

# セッションを使わずにデータを保存する
received_data = {}
 # 追加



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
