from flask import Flask, request, render_template

app = Flask(__name__)

# 存储最新的IP地址
latest_ip = ""

@app.route('/update_ip', methods=['POST'])
def update_ip():
    global latest_ip
    ip = request.form.get('ip', '')
    latest_ip = ip
    return 'OK'

@app.route('/')
def show_latest_ip():
    return render_template('lan-ip.html', latest_ip=latest_ip)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000)
