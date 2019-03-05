import requests
import re
import json
import random
import sys


class SignIn:
    s = '012345689ABCDE'
    urlLogin = 'https://csust.edu.chsh8j.com:8088/magus/appuserloginapi/userlogin?'
    urlSignid = 'https://csust.edu.chsh8j.com:8088/dorm/app/dormsign/sign/student/detail?'
    urlSendSignInfo = 'https://csust.edu.chsh8j.com:8088/dorm/app/dormsign/sign/student/edit?'

    def getRandom(self,length):
        a = ''
        for i in range(length):
            a += SignIn.s[random.randint(0, len(SignIn.s) - 1)]
        return a

    def __init__(self, userName, password):
        self.userName = userName
        self.password = password
        self.headers = {
            'Host': 'csust.edu.chsh8j.com:8088',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept-Encoding': 'br, gzip, deflate',
            'Connection': 'keep-alive',
            'Accept': '*/*',
            'User-Agent': 'ScienceAndEngineerOnHand/2.5.4 (iPhone; iOS 12.0; Scale/2.00)',
            'Accept-Language': 'zh-Hans-CN;q=1',
            'token': ''  # 登录后的身份认证
        }
        self.data = {
            'bleId': '1918FC07D996665659',  # 楼层蓝牙地址
            'devUuid':  SignIn.getRandom(self,8)+'-'+SignIn.getRandom(self,4)+'-'+SignIn.getRandom(self,4)+'-'+SignIn.getRandom(self,4)+'-' + SignIn.getRandom(self,12),  # 设备号
            'osName': 'iPhone 6 运营商:中国联通 12.0',  # 设备名称 运营商 系统版本
            'signId': ''  # 每次签到的id
        }
        self.params = {
            'params': '{"password": "' +self.getPassword() + '","userName": "' + self.getUserName() + '"}'
        }

    def getPassword(self):
        return self.password

    def getUserName(self):
        return self.userName

    def setUserName(self):
        self.userName = input("请输入你的学号:")

    def setPassword(self):
        self.password = input("请输入你的密码:")

    def setParams(self):
        self.params = {
            'params': '{"password": "' + self.getPassword() + '","userName": "' + self.getUserName() + '"}'
        }

    def getToken(self):
        responseLogin = requests.get(url=SignIn.urlLogin,params=self.params,headers=self.headers)
        responseLoginJson = json.loads(responseLogin.text)
        print(responseLoginJson['result']['message'])
        if(responseLoginJson['result']['message'] == '账号或密码错误'):
            self.setUserName()
            self.setPassword()
            self.setParams()
            self.getToken()
        else:
            token = re.findall('"token":"(.*?)"', responseLogin.text)
            self.headers['token'] = token[0]

    def getSignid(self):
        self.getToken()
        responseSignid = requests.post(url=SignIn.urlSignid,headers=self.headers)
        responseSignidJson = json.loads(responseSignid.text)
        if responseSignidJson['message'] == '成功' and responseSignidJson['data']['isAvailable'] == '0':
            print('无需签到')
            sys.exit()
        else:
            self.data['signId'] = responseSignidJson['data']['signId']
            self.data['bleId'] = responseSignidJson['data']['bleinfoList'][0]['bleId']

    def sendSignInfo(self):
        self.getSignid()
        responseSignInfo = requests.post(url=SignIn.urlSendSignInfo,data=self.data,headers=self.headers)
        print(responseSignInfo.text)
        print('签到成功')


if __name__ == "__main__":
    try:
        userName = input("请输入你的学号:")
        password = input("请输入你的密码:")
        sign = SignIn(userName, password)
        sign.sendSignInfo()
    except BaseException as e:
        print(e)






