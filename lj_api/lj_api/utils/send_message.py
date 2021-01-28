import requests


class Message(object):
    def __init__(self, api_key):
        self.api_key = api_key
        self.single_send_url = "https://sms.yunpian.com/v2/sms/single_send.json"

    def send_message(self, phone, code):
        params = {
            "apikey": self.api_key,
            "mobile": phone,
            "text": "【李静test】您的验证码是{code}。如非本人操作，请忽略本短信".format(code=code)
        }
        req = requests.post(self.single_send_url, data=params)
        print(req)
