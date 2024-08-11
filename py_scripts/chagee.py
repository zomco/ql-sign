import json
import sys

import requests
import os
import py_tools.notify as notify

CHAGEE_TOKENS = os.getenv('CHAGEE_TOKENS')  # {token1,token2,...}
CHAGEE_NAMES = os.getenv('CHAGEE_NAMES')    # {name1,name2,...}
appid = 'wxafec6f8422cb357b'


def get_headers(token_):
    headers_ = {
        "Qm-From": "wechat",
        "Qm-User-Token": token_,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a13) XWEB/9129",
        "Qm-From-Type": "catering",
        "Referer": "https://servicewechat.com/wxafec6f8422cb357b/167/page-frame.html",
        "xweb_xhr": "1"
    }
    return headers_


def check_score(headers_, name_):
    url1 = 'https://webapi2.qmai.cn/web/catering2-apiserver/crm/points-info'
    data = {"appid": appid}
    try:
        response = requests.post(url=url1, headers=headers_, data=data).json()
        notify.print(response)
        if not response['status']:
            print("{} check score failed: {}".format(name_, response['message']))
            return False
        score = int(response["data"]["totalPoints"])
        title = "{} 霸王茶姬签到".format(name_)
        content = "总积分: {}".format(score)
        notify.wecom_bot(title, content)
        return True
    except requests.exceptions.RequestException as e:
        print("{} check score error: {}".format(name_, e))
        return False


def daily_sign(headers_, name_):
    activity_id = '947079313798000641'
    url1 = 'https://webapi2.qmai.cn/web/cmk-center/sign/takePartInSign'
    data = {"activityId": activity_id, "appid": appid}
    try:
        response = requests.post(url=url1, headers=headers, data=data).json()
        notify.print(response)
        if not response['status']:
            print("{} daily sign failed: {}".format(name_, response['message']))
            return False
        return check_score(headers_, name_)
    except requests.exceptions.RequestException as e:
        print("{} daily sign error: {}".format(name_, e))
        return False


if __name__ == '__main__':
    APP_NAME = '霸王茶姬'
    if not CHAGEE_TOKENS:
        notify.print("请先配置环境变量 CHAGEE_TOKENS ")
        sys.exit()
    tokens = CHAGEE_TOKENS.split(',')
    names = CHAGEE_NAMES.split(',')
    for i, token in enumerate(tokens):
        headers = get_headers(token)
        name = names[i] if not names[i] else "#{}用户".format(i + 1)
        daily_sign(headers, name)
