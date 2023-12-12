from flask import Flask, request, render_template
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
import os
import configparser

app = Flask(__name__)
config = configparser.ConfigParser()
config.read('.env')

# 本地文件路径
file_path = '/tmp/lan-ip.txt'
# 上传路径
key = '/lan-ip.txt'
# 从环境变量获取cos配置信息
region = config.get('cos', 'region')
target_bucket = config.get('cos', 'target_bucket')
secret_id = config.get('cos', 'secret_id')
secret_key = config.get('cos','secret_key')

client = CosS3Client(CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key))

def upload_cos():
    try:
        # 上传
        with open(file_path, 'rb', encoding='utf-8') as fp:
            client.put_object(
                Bucket=target_bucket,  # Bucket 由 BucketName-APPID 组成
                Body=fp,  # 文件流/字节流
                Key=key,
                StorageClass='STANDARD',
                ContentType='text/html; charset=utf-8'
            )
    except Exception as e:
        print(f'upload error:\n{e}')

@app.route('/update_ip', methods=['POST'])
def update_ip():
    ip = request.form.get('ip', '')
    os.makedirs('/tmp', exist_ok=True)
    with open(file_path, 'w') as fw:
        fw.write(ip)
    upload_cos()
    return 'OK'

@app.route('/')
def show_latest_ip():
    # 获取文件流
    response = client.get_object(
        Bucket=target_bucket,
        Key=key
    )
    file_stream = response['Body'].get_raw_stream()
    ipstring = file_stream.read().decode('utf-8')

    return render_template('lan-ip.html', latest_ip=ipstring)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000)
