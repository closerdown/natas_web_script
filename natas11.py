import json
import requests
import base64
from bs4 import BeautifulSoup 
from urllib.parse import unquote
from itertools import cycle

url = "http://natas11.natas.labs.overthewire.org/"
enc_cookie = 'EGAgHwQ1IxYYMSQYGSZxTUksPFVHYDEQCC0%2FGBlgaVVIJDURDSQ1VRY%3D'
natas11_cred = "VUMQDmuITOEHzhviLE5V0VG9cPMQkyxd"

sess = requests.Session()
sess.auth = ("natas11", natas11_cred)


text_str = {"showpassword":"no", "bgcolor":"#ffffff"}

# 복호화하여 xor_key값 추출
def dec_value(enc_cookie):
  # 웹 인코딩으로 인한 기호로 인식하는 부분 수정
  clean_cookie = unquote(enc_cookie)      
  
  #base64로 디코딩 
  base_dec_value = base64.b64decode(clean_cookie)
  plain_text = json.dumps(text_str, separators=(",", ":"))
  
  #xor key값을 구하기 위해 xor 연산(xor 연산은 key값을 연산하면 기존 평문으로 돌아오는 성질이 있다)
  xor_dec_char = []
  for p_char, b_byte in zip(plain_text, base_dec_value):
    xor_dec_char.append(ord(p_char) ^ b_byte)
  
  xor_key = "".join(chr(num) for num in xor_dec_char)
  return xor_key

xor_key_value = dec_value(enc_cookie)

# 조건을 통과하기 위한 문자열을 인코딩 
input_text = {"showpassword":"yes", "bgcolor":"#ffffff"}

def enc_value(input_text, xor_key_value):
  json_enc = json.dumps(input_text, separators=(",", ":"))
  
  real_slice_key = xor_key_value[:4]
  
  key_cycle = cycle(real_slice_key)
  
  xor_enc = []
  for char in json_enc:
    key_char = next(key_cycle)
    xor_result = ord(char) ^ ord(key_char)
    xor_enc.append(xor_result)
  
  flag_cookie = base64.b64encode(bytes(xor_enc))
  return flag_cookie

enc_cookie = enc_value(input_text, xor_key_value)

print(f"[*]xor_key값 ==> {xor_key_value}")
print(f"[*]입력할 인코딩 key값 ==> {enc_cookie}")

# 현재 바이트값이라 사전 형태의 쿠키에는 대입이 안되므로 벼환
if isinstance(enc_cookie, bytes):
  enc_cookie = enc_cookie.decode()
  
payload = {"data": enc_cookie}
response = sess.get(url, auth= sess.auth, cookies=payload)

soup = BeautifulSoup(response.text, "html.parser")

page_text = soup.get_text()

for line in page_text.split("\n"):
  if "The password for natas12 is" in line:
    print(f"[+]비밀번호를 찾았습니다: {line.strip()}")
    break
