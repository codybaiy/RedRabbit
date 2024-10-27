import sys
import time
import requests
import qrcode
import subprocess
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0"
}
def login_with_qr():
    qrcode_url = 'https://passport.bilibili.com/x/passport-login/web/qrcode/generate?source=main-fe-header'
    res = requests.get(qrcode_url,headers=headers).json()
    qr_result = {'url': res['data']['url'], 'qrcode_key': res['data']['qrcode_key']}
    img = qrcode.make(qr_result['url'])
    img.show()
    login_url = f"https://passport.bilibili.com/x/passport-login/web/qrcode/poll?qrcode_key={qr_result['qrcode_key']}&source=main-fe-header"
    while True:
        req = requests.get(login_url,headers=headers)
        rj = req.json()
        if rj['data']['code'] == 0:
            command = ["taskkill", "/IM", "360AlbumViewer64.exe", "/F"]
            subprocess.run(command, capture_output=True, text=True)
            print('login success.',end='\n\n')
            return req.cookies.get_dict()
        time.sleep(2)

# ****************************

def get_target_info(s_user,c):
    search_url = f'https://search.bilibili.com/upuser?keyword={s_user}'
    r = requests.get(search_url,headers=headers,cookies=c)
    soup = BeautifulSoup(r.text,'lxml')
    a_tag = soup.find('a', title = search_user)
    if a_tag:
        href = a_tag.get('href')
        uid = href.split('/')[3]
        print(f" {s_user} 的uid是 {uid}",end='\n\n')
        return uid
    else:
        print("找不到对象.")
        sys.exit()

# *****************************

def follow_action(f_id,csrf_t,c):
    f_url = 'https://api.bilibili.com/x/relation/modify'
    data = {
        'fid' : f_id,
        'act' : '1',
        're_src' : '11',
        'csrf' : csrf_t,
        'gaia_source' : "web_main",
    }
    res = requests.post(f_url,headers=headers,data=data,cookies=c)
    if res.json()['code'] == 0:
        print('关注成功.')
    else:
        print(res.json()['message'])

# *********************************

def get_id(target_id,c):
    ids_list = []
    for i in range(1,3):
        following_api = f'https://api.bilibili.com/x/relation/followings?vmid={target_id}&pn={i}&ps=50&order=desc&jsonp=jsonp'
        res = requests.get(following_api,headers=headers,cookies=c)
        res = res.json()['data']['list']
        for d in res:
            r_id = d['mid']
            ids_list.append(r_id)
    return ids_list

# *****************************

if __name__ == "__main__":
    cookie = login_with_qr()
    csrf_token = cookie['bili_jct']
    search_user = input('你想copy哪位up的关注列表？ ：')
    user_id = get_target_info(search_user,cookie)
    id_list = get_id(user_id,cookie)
    for u_id in id_list:
        follow_action(u_id,csrf_token,cookie)