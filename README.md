# Natas Web Wargame — Python Writeups

[OverTheWire Natas](https://overthewire.org/wargames/natas/) 워게임을 **수동 진단 → 취약점 분석 → Python 자동화 익스플로잇** 흐름으로 풀어본 기록입니다.

각 레벨의 상세 풀이는 블로그에 정리했고, 이 저장소에는 **취약점을 자동으로 익스플로잇해 결과값까지 출력하는 코드**만 담았습니다. 코드를 직접 해석하며 더 나은 방식으로 다시 짜보는 것도 좋은 연습이 됩니다.

> 블로그 전체 글: https://kisuk0104.tistory.com/

---

## 풀이 목록

| 파일 | 취약점 | 핵심 아이디어 | 블로그 풀이 |
|------|--------|---------------|-------------|
| [`natas08.py`](natas08.py) | 인코딩 역추적 | base64 → reverse → hex 로직을 역연산해 secret 복원 | [natas8](https://kisuk0104.tistory.com/51) |
| [`natas09.py`](natas09.py) | OS Command Injection | `passthru`에 입력값을 검증 없이 연결 → `;`로 명령 분리 후 임의 명령 실행 | [natas9](https://kisuk0104.tistory.com/52) |
| [`natas10.py`](natas10.py) | Command Injection (필터 우회) | `preg_match`로 `;`,`&`,`\|` 필터 → grep 정규식 특성을 이용한 파일 읽기 | [natas10](https://kisuk0104.tistory.com/53) |
| [`natas11.py`](natas11.py) | 쿠키 변조 (XOR) | base64+JSON 쿠키를 XOR 복호화 → 키 복원 후 위조 쿠키 생성 | [natas11](https://kisuk0104.tistory.com/55) |
| [`natas12.py`](natas12.py) | 파일 업로드 (Hidden 필드 조작, 웹셸 이용) | 확장자를 지정하는 hidden 값을 `.php`로 조작해 웹셸 업로드 → 비밀번호 파일 접근 | [natas12](https://kisuk0104.tistory.com/56) |
| [`natas13.py`](natas13/natas13.py) | 파일 업로드 (`exif_imagetype()` 시그니처 검사 우회, 웹셸 이용) | 웹셸 앞에 JPG 매직 바이트(예: `\xFF\xD8\xFF\xE1`)를 붙여 `exif_imagetype()` 검사를 통과시키고, natas12처럼 hidden 확장자를 `.php`로 조작해 업로드 → 웹셸로 비밀번호 접근 (페이로드 생성 보조: [`creat_file.py`](natas13/creat_file.py)) | [natas13](https://kisuk0104.tistory.com/57) |
| [`natas14.py`](natas14.py) | SQL Injection (로그인 우회) | 입력값이 쿼리 문법으로 해석되는 점을 이용. `" or 1=1#`로 WHERE 조건을 참으로 만들어 `num_rows > 0` 통과 → 인증 우회 후 비밀번호 추출 | [natas14](https://kisuk0104.tistory.com/58) |
| [`natas15.py`](natas15.py) | Blind SQL Injection (Boolean 기반) | 응답의 `This user exists.` 유무로만 참/거짓이 노출됨. `LENGTH(password)`로 길이를 확정한 뒤 `substr(password, i, 1) = BINARY "문자"`로 한 글자씩 brute force. `BINARY`로 대소문자까지 구분해 비밀번호 완성 | [natas15](https://kisuk0104.tistory.com/59) |
| [`natas16.py`](natas16.py) | Blind OS Command Injection (명령 치환) | `grep "$key" dictionary.txt`에서 큰따옴표 안 `$(...)` 명령 치환이 동작하는 점을 이용. `$(grep ^<접두사> /etc/natas_webpass/natas17)<사전단어>`를 주입해, 접두사가 맞으면 사전 단어가 결과에서 사라지는 Boolean 신호를 만들어 한 글자씩 비밀번호 추출 | [natas16](https://kisuk0104.tistory.com/) |

---

## 실행 방법

```bash
pip install requests
python natas08.py
```

각 스크립트 상단의 비밀번호 변수에 본인 값을 넣고 실행하세요.
Natas는 직전 레벨을 풀어야 다음 레벨 비밀번호를 얻는 구조라, 값을 고정하지 않고 실행 시 직접 입력하도록 비워두었습니다.

> `natas13`은 폴더로 구성되어 있습니다. `natas13.py`가 실행 중에 업로드 페이로드 파일을 직접 생성하므로, 기본 실행만 할 때는 [`natas13/natas13.py`](natas13/natas13.py)만 돌리면 됩니다. 다만 코드를 수정해 미리 만든 파일을 읽어 올리는 방식으로 바꿀 경우에는, [`natas13/creat_file.py`](natas13/creat_file.py)로 페이로드를 먼저 생성한 뒤 실행하세요.

---

## 참고

- 대상: OverTheWire Natas (공개 학습용 워게임)
- 목적: 웹 취약점 원리 학습 및 익스플로잇 자동화 연습
