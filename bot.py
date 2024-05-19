import os
import sys
import json
import time
import requests
from colorama import *

init(autoreset=True)

merah = Fore.LIGHTRED_EX
putih = Fore.LIGHTWHITE_EX
hijau = Fore.LIGHTGREEN_EX
kuning = Fore.LIGHTYELLOW_EX
biru = Fore.LIGHTBLUE_EX
reset = Style.RESET_ALL


class CubeTod:
    def __init__(self):
        self.headers = {
            'content-length': '0',
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; Redmi 4A / 5A Build/QQ3A.200805.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.185 Mobile Safari/537.36',
            'content-type': 'application/json',
            'accept': '*/*',
            'origin': 'https://www.thecubes.xyz',
            'x-requested-with': 'org.telegram.messenger',
            'sec-fetch-site': 'cross-site',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://www.thecubes.xyz/',
            'accept-language': 'en,en-US;q=0.9',
        }
    
    def main(self):
        banner = f"""
    
    {putih}AUTO MINE {hijau}CUBE {putih}/ {hijau}@cubesonthewater_bot
    
    {putih}By: {hijau}t.me/AkasakaID
    {putih}Github: {hijau}@AkasakaID
    
    {hijau}Message: {putih}don't forget to 'git pull' maybe i update the bot !
        """
        
        if len(sys.argv) <= 1:
            os.system('cls' if os.name == 'nt' else 'clear')
        print(banner)
        print('~' * 50)
        if not os.path.exists('data'):
            open('data','a')
        
        data = open('data','r').read().splitlines()
        
        if len(data) <= 0:
            self.log(f"{merah}data file is empty,please fill data file !")
            sys.exit()
            
        data = data[0]
        if not os.path.exists('user-agent'):
            open('user-agent','a')
        
        ua = open('user-agent','r').read().splitlines()
        if len(ua) <= 0:
            self.log(f"{merah}please fill user-agent file with your user-agent !")
            sys.exit()

        self.headers['user-agent'] = ua[0]
        token = self.login(data)
        config = json.loads(open('config.json','r').read())
        self.min_energy = int(config['min_energy'])
        interval = int(config['interval'])
        sleep = int(config['sleep'])
        while True:
            print('~' * 50)
            res = self.mine(token)
            if isinstance(res,str):
                if res == 'limit':
                    self.countdown(sleep)
                    continue
            
            self.countdown(interval)

    def log(self, message):
        year, mon, day, hour, minute, second, a, b, c = time.localtime()
        mon = str(mon).zfill(2)
        hour = str(hour).zfill(2)
        minute = str(minute).zfill(2)
        second = str(second).zfill(2)
        print(f"{biru}[{year}-{mon}-{day} {hour}:{minute}:{second}] {message}")

    def countdown(self, t):
        while t:
            menit, detik = divmod(t, 60)
            jam, menit = divmod(menit, 60)
            jam = str(jam).zfill(2)
            menit = str(menit).zfill(2)
            detik = str(detik).zfill(2)
            print(f"waiting until {jam}:{menit}:{detik} ", flush=True, end="\r")
            t -= 1
            time.sleep(1)
        print("                          ", flush=True, end="\r")
    
    def mine(self,token):
        headers = self.headers
        data = {
            "token": token
        }
        headers['content-length'] = str(len(json.dumps(data)))
        res = self.http('https://server.questioncube.xyz/game/mined',headers,json.dumps(data))
        if res.status_code == 200:
            if '"mined_count"' in res.text:
                self.log(f"{hijau}mined successfully")
                drop = res.json()['drops_amount']
                energy = res.json()['energy']
                mined = res.json()['mined_count']
                boxes = res.json()['boxes_amount']
                self.log(f"{hijau}drop amount : {putih}{drop}")
                self.log(f"{hijau}boxes amount : {putih}{boxes}")
                self.log(f"{hijau}mined count : {putih}{mined}")
                self.log(f"{hijau}remaining energy : {putih}{energy}")
                if int(energy) <= self.min_energy:
                    return 'limit'
                
                return True
        
        self.log(f"{merah}failed to mine, http status code : {kuning}{res.status_code}")
        return False

    def login(self,data):
        url = "https://server.questioncube.xyz/auth"
        data = {
            "initData": data
        }
        headers = self.headers
        headers['content-length'] = str(len(json.dumps(data)))
        res = self.http(url,headers,json.dumps(data))
        if res.status_code == 200:
            if '"token"' in res.text:
                token = res.json()['token']
                name = res.json()['username']
                energy = res.json()['energy']
                drop = res.json()['drops_amount']
                mined = res.json()['mined_count']
                self.log(f'{hijau}success login as {putih}{name}')
                self.log(f'{hijau}drop amount : {putih}{drop}')
                self.log(f'{hijau}mined count : {putih}{mined}')
                self.log(f'{hijau}energy : {putih}{energy}')
                return token
        
        self.log(f'{merah}failed to login, http status code : {kuning}{res.status_code}')
        sys.exit()
                
    def http(self, url, headers, data=None):
        while True:
            try:
                if data is None:
                    res = requests.get(url, headers=headers)
                    return res

                res = requests.post(url, headers=headers, data=data)
                return res
            except (
                requests.exceptions.ConnectionError,
                requests.exceptions.ConnectTimeout,
                requests.exceptions.ReadTimeout,
                requests.exceptions.SSLError,
            ):
                self.log(f"{merah}connection error/ timeout !")

if __name__ == "__main__":
    try:
        app = CubeTod()
        app.main()
    except KeyboardInterrupt:
        sys.exit()