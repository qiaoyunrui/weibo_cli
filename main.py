# coding=utf-8
from weibo import APIClient
import os.path
import json
import datetime

app_key = ''
app_secret = ''
callback_url = ''
domain = ''

access_token = ''
expires_in = ''

key_file_name = "key.json"
token_file_name = "token.json"


def get_access_token(app_key, app_secret, callback_url):
    client = APIClient(app_key=app_key, app_secret=app_secret, redirect_uri=callback_url)
    # 获取授权页面网址
    auth_url = client.get_authorize_url()
    print auth_url
    code = raw_input("Input code:")
    r = client.request_access_token(code)
    local_access_token = r.access_token
    # token 过期的 UNIX 时间
    local_expires_in = r.expires_in

    return local_access_token, local_expires_in


def load_key():
    if os.path.exists(key_file_name):
        with open(key_file_name, 'r') as f:
            content = f.read()
            dict_key = json.loads(content)
            return dict_key


def load_token():
    if os.path.exists(token_file_name):
        with open(token_file_name, 'r') as f:
            content = f.read()
            dict_token = json.loads(content)
            return dict_token


def save_token(token_dict):
    json_content = json.dumps(token_dict)
    with open(token_file_name, 'w') as f:
        f.write(json_content)


def init_login():
    client = APIClient(app_key=app_key, app_secret=app_secret, redirect_uri=callback_url)
    client.set_access_token(access_token, expires_in)
    return client


def send_message(client, message):
    u_text = unicode(message, "UTF-8")
    client.statuses.share.post(status=u_text + " " + domain)
    # post('statuses/share', status=)
    print u"发送成功！"


def get_remain_days():
    start_time = datetime.datetime.now()
    end_time = datetime.datetime(2018, 12, 22)
    return (end_time - start_time).days


if __name__ == '__main__':
    key_dict = load_key()
    if key_dict is None:
        raise Exception("Some key is empty")
    app_key = key_dict['app_key']
    app_secret = key_dict['app_secret']
    callback_url = key_dict['callback_url']
    domain = key_dict['domain']
    if app_key == "" or app_secret == "" or callback_url == "" or domain == "":
        raise Exception("Some key is empty")
    token_dict = load_token()
    if token_dict is None:
        access_token, expires_in = get_access_token(app_key, app_secret, callback_url)
        token_dict = {"access_token": access_token, "expires_in": expires_in}
        save_token(token_dict)
    access_token = token_dict['access_token']
    expires_in = token_dict['expires_in']

    client = init_login()
    message = "[%s天] 今天你学习了嘛？" % get_remain_days()
    send_message(client, message)
