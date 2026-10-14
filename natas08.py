import base64
import requests
import re


url = "http://natas8.natas.labs.overthewire.org"


# 디코딩하기 위한 함수
def analy_str(incode_string):
  hex_decode = bytes.fromhex(incode_string)
  rev_str = hex_decode[::-1]
  base64_decoded = base64.b64decode(rev_str)
  return base64_decoded.decode("utf-8")


# 디코딩할 문자열 및 함수 적용
incoding_str="3d3d516343746d4d6d6c315669563362"
anly_secret = analy_str(incoding_str)


# 디코딩값 중간 확인
print(f"[+] 함수로 구한 Secret 값: {anly_secret}")

# 로그인을 해서 요청하는 것이 기본이므로 계정정보 
# natas8 로그인 정보 (natas7을 풀면 얻는 비밀번호)
# 직접 풀어서 본인 값으로 교체하세요
natas8_password = "여기에_본인_비밀번호"

auth_input = ("natas8", natas8_password)

# 해당 페이지에서 해야되는 요청
data = { "secret": anly_secret, "submit":"Submit"}

# 실제 요청
response = requests.post(url, auth=auth_input, data=data)

# 정규 표현식 패턴을 통한 원하는 값 찾기 
pattern = r"Access granted. The password for natas9 is [a-zA-Z0-9]{32}"
match = re.search(pattern, response.text)

# 패턴 일치시, 일치하는 부분만 출력
if match:
  print(f"성공 => {match.group(0)}" )
#안되면 그냥 해당 전체적인 응답 나오게하기
else:
  print("못 찾았음, 수동확인")
  print(response.text)
  
  
