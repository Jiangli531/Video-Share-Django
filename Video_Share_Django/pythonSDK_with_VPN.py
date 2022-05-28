#通过 COS 默认域名和代理初始化


# -*- coding=utf-8
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
import sys
import logging

# 正常情况日志级别使用INFO，需要定位时可以修改为DEBUG，此时SDK会打印和服务端的通信信息
logging.basicConfig(level=logging.INFO, stream=sys.stdout)

# 1. 设置用户属性, 包括 secret_id, secret_key, region等。Appid 已在CosConfig中移除，请在参数 Bucket 中带上 Appid。Bucket 由 BucketName-Appid 组成
secret_id = 'AKIDEVn1ADAKWp9VpzvqiWG8xlQvIZmmZ8UW'     # 替换为用户的 SecretId，请登录访问管理控制台进行查看和管理，https://console.cloud.tencent.com/cam/capi
secret_key = 'tsjPvHSSH1fHrPtQxRr6GMclxANURFwV'   # 替换为用户的 SecretKey，请登录访问管理控制台进行查看和管理，https://console.cloud.tencent.com/cam/capi
region = 'ap-beijing'      # 替换为用户的 region，已创建桶归属的region可以在控制台查看，https://console.cloud.tencent.com/cos5/bucket
                           # COS支持的所有region列表参见https://cloud.tencent.com/document/product/436/6224
token = None               # 如果使用永久密钥不需要填入token，如果使用临时密钥需要填入，临时密钥生成和使用指引参见https://cloud.tencent.com/document/product/436/14048
proxies = {
    'http': '127.0.0.1:10809',  # 替换为用户的 HTTP代理地址
    'https': '127.0.0.1:10808' # 替换为用户的 HTTPS代理地址
}

config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token, Proxies=proxies)
client = CosS3Client(config)