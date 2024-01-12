import socket
import requests
import time
import logging
from logging.handlers import RotatingFileHandler
import argparse

# 创建 ArgumentParser 对象
parser = argparse.ArgumentParser(description='Get local IP and send it to remote API.')

parser.add_argument('-u', '--url', default='',help='The remote url, such as "http(s)://domain or IP(:port)/path".')
parser.add_argument('-i', '--interval', default=300, type=int, help='The interval of reporting local IP, in seconds. Default is 300(5 minutes).')

# 解析命令行参数
args = parser.parse_args()

# 配置日志格式
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# 创建RotatingFileHandler，设置日志文件名、最大文件大小和备份文件数
log_file = "lan-ip.log"
max_file_size_bytes = 1024 * 1024  # 1 MB
backup_count = 3

handler = RotatingFileHandler(log_file, maxBytes=max_file_size_bytes, backupCount=backup_count)
handler.setLevel(logging.INFO)

# 创建日志对象并将handler添加到日志对象
logger = logging.getLogger(__name__)
logger.addHandler(handler)

def get_local_ip():
    try:
        # 创建一个socket连接
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        # 连接到一个不存在的目标地址和端口
        s.connect(("10.0.0.1", 80))
        
        # 获取本地IP地址
        local_ip = s.getsockname()[0]
        
        # 关闭socket连接
        s.close()
        logger.info(f"Get Local IP is: {local_ip}")
        return local_ip
    except Exception as e:
        logger.error(f"Failed to get local IP: {e}")
        return None

def send_ip_to_remote_api(ip):
    try:
        # 替换下面的URL为你的远端web函数接口的URL
        url = args.url
        
        # 发送POST请求，将IP数据发送到远端接口
        # 根据发型版本不同，确定 device 参数
        response = requests.post(url, data={"ip": ip, "dev": 'printer'})
        
        # 打印响应结果
        logger.info(f"response: {response.text}")
    except Exception as e:
        logger.error(f"Failed to send IP to remote API: {e}")


# 主循环，每隔 interval 执行一次
while True:
    # 获取本地IP地址
    local_ip = get_local_ip()

    # 发送IP到远端接口
    send_ip_to_remote_api(local_ip)

    # 等待5分钟
    time.sleep(args.interval)

