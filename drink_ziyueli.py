import os
import sys

import requests

from tools import notify as notify

ZIYUELI_TOKENS = os.getenv('ZIYUELI_TOKENS')  # {token1,token2,...}
ZIYUELI_NAMES = os.getenv('ZIYUELI_NAMES')  # {name1,name2,...}
appid = 'wx0efa6f01d6869646'
appname = '子曰礼'


def get_headers(token_):
    headers_ = {
        "Qm-From": "wechat",
        "Qm-User-Token": token_,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a13) XWEB/9129",
        "Qm-From-Type": "mealmate",
        "Referer": "https://servicewechat.com/wx0efa6f01d6869646/8/page-frame.html",
        "xweb_xhr": "1"
    }
    return headers_


def check_score(headers_, name_):
    url1 = 'https://webapi.qmai.cn/web/mall-apiserver/integral/user/points-info'
    data = {"appid": appid}
    try:
        response = requests.post(url=url1, headers=headers_, data=data).json()
        notify.print(response)
        if not response['status']:
            print("{} check score failed: {}".format(name_, response['message']))
            return False
        score = int(response["data"]["totalPoints"])
        title = "{} {}签到".format(name_, appname)
        content = "总积分: {}".format(score)
        notify.wecom_bot(title, content)
        return True
    except requests.exceptions.RequestException as e:
        print("{} check score error: {}".format(name_, e))
        return False


def daily_sign(headers_, name_):
    activity_id = '988140066214645761'
    url1 = 'https://webapi.qmai.cn/web/cmk-center/sign/takePartInSign'
    data = {"activityId": activity_id, "appid": appid}
    try:
        response = requests.post(url=url1, headers=headers, data=data).json()
        notify.print(response)
        if not response['status']:
            print("{} daily sign failed: {}".format(name_, response['message']))
            title = "{} {}签到".format(name_, appname)
            content = "错误信息: {}".format(response['message'])
            notify.wecom_bot(title, content)
            return False
        return check_score(headers_, name_)
    except requests.exceptions.RequestException as e:
        print("{} daily sign error: {}".format(name_, e))
        return False


if __name__ == '__main__':
    if not ZIYUELI_TOKENS:
        notify.print("请先配置环境变量 ZIYUELI_TOKENS ")
        sys.exit()
    tokens = ZIYUELI_TOKENS.split()
    names = ZIYUELI_NAMES.split()
    for i, token in enumerate(tokens):
        headers = get_headers(token)
        name = names[i] if names[i] else "#{}用户".format(i + 1)
        daily_sign(headers, name)
