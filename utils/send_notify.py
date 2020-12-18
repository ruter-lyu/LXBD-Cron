import os
import httpx

SCKEY = os.getenv('SCKEY', None)


def sc_notify(title, desp):
    if SCKEY:
        resp = httpx.post(f'https://sc.ftqq.com/{SCKEY}.send', data={
            'text': title,
            'desp': desp
        })
        if resp.status_code != httpx.codes.OK:
            print('\n发送通知调用 API 失败\n')
            print(resp.text())
        else:
            result = resp.json()
            if result['errno'] == 0:
                print('\nServer酱发送通知消息成功\n')
            elif result['errno'] == 1024:
                print('\nSCKEY 错误\n')
    else:
        print('\n您未提供Server酱的 SCKEY，取消微信推送消息通知\n')
