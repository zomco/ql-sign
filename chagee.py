import os
import requests
import urllib3
import time
import json
from urllib.parse import urlparse, parse_qs
import sys
import notify

CHAGEE_TOKENS = os.getenv('CHAGEE_TOKENS')  # {token1,token2,...}


def daily_sign(token):
    activityId='947079313798000641'
    appid='wxafec6f8422cb357b'

    url1='https://webapi2.qmai.cn/web/cmk-center/sign/takePartInSign'
    headers={
            "Qm-From": "wechat",
            "Qm-User-Token": token,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a13) XWEB/9129",
            "Qm-From-Type": "catering",
            "Referer": "https://servicewechat.com/wxafec6f8422cb357b/167/page-frame.html",
            "xweb_xhr" : "1"
    }
    data={"activityId":activityId,"appid":appid}
    response = requests.post(url=url1,headers=headers,data=data)  # 三个参数
    notify.print(response.text)

    url2='https://webapi2.qmai.cn/web/catering2-apiserver/crm/points-info'
    data2={"appid":appid}
    response2 = requests.post(url=url2,headers=headers,data=data2)
    xiaoku=json.loads(response2.text)
    score = int(xiaoku["data"]["totalPoints"])
    notify.wecom_bot("霸王茶姬签到", "总积分: {}".format(score))


if __name__ == '__main__':
    APP_NAME = '霸王茶姬'
    if not CHAGEE_TOKENS:
        notify.print("请先配置环境变量 CHAGEE_TOKENS ")
        sys.exit()
    tokens = str.split(',')
    for i, token in enumerate(tokens):
        daily_sign(token)