from flask import Flask, request, render_template
import json

app = Flask(__name__)

# 本地文件路径
file_path = 'lan-ip.json'

@app.route('/update_ip', methods=['POST'])
def update_ip():
    ip = request.form.get('ip', '')  # 更新的IP
    device = request.form.get('dev', '')  # 设备名称
    with open(file_path, 'r') as f1:
        data = json.load(f1)
    data[device] = ip
    with open(file_path, 'w') as f2:
        json.dump(data, f2, indent=4)
    return 'OK'


@app.route('/')  # 打印机
def show_printer_ip():
    with open(file_path, 'r') as file:
        data = json.load(file)
        ipstring = data['printer']
    return render_template('lan-ip.html', latest_ip=ipstring, device='打印机')


@app.route('/yzh')  # yzh_pc
def show_yzhpc_ip():
    with open(file_path, 'r') as file:
        data = json.load(file)
        ipstring = data['yzh']
    return render_template('lan-ip.html', latest_ip=ipstring, device='yzh_pc')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000, debug=True)