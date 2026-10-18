# Natas Web Wargame — Python Writeups

[OverTheWire Natas](https://overthewire.org/wargames/natas/) 워게임을 **수동 진단 → 취약점 분석 → Python 자동화 익스플로잇** 흐름으로 풀어본 기록입니다.

각 레벨마다 풀이에 대한 자세한 부분은 블로그에 작성했습니다. 여긴 익스플로잇 코드만해서 결과값까지 출력하는 로직만을 포함하고 있습니다.
직접 해석해서 좋은 코드를 짜도 좋을 것 같습니다

> 블로그 전체 글: https://kisuk0104.tistory.com/

---

## 풀이 목록

| 파일 | 취약점 | 핵심 아이디어 | 블로그 풀이 |
|------|--------|---------------|-------------|
| [`natas08.py`](natas08.py) | 인코딩 역추적 | base64 → reverse → hex 로직을 역연산해 secret 복원 | [natas8](https://kisuk0104.tistory.com/51) |
| [`natas09.py`](natas09.py) | OS Command Injection | `passthru`에 입력값을 검증 없이 연결 → `;`로 명령 분리 후 임의 명령 실행 | [natas9](https://kisuk0104.tistory.com/52) |
| [`natas10.py`](natas10.py) | Command Injection (필터 우회) | `preg_match`로 `;`,`&`,`\|` 필터 → grep 정규식 특성을 이용한 파일 읽기 | [natas10](https://kisuk0104.tistory.com/53) |
| [`natas11.py`](natas11.py) | 쿠키 변조 (XOR) | base64+JSON 쿠키를 XOR 복호화 → 키 복원 후 위조 쿠키 생성 | [natas11](https://kisuk0104.tistory.com/55)|
| [`natas12.py`](natas12.py) | HTML에서 사용자 입력값 검증 부재로 인한, Hidden 값을 통한 파일 업로드 확장자 우회 취약점 (웹셸 이용)| 파일 확장자를 참조하는 hidden값 조작 및 php환경에 사용되는 웹셸을 이용하여 비밀번호 데이터에 접근| [natas12](https://kisuk0104.tistory.com/56)|
| [`natas13.py`](natas13.py) | 파일 업로드 (`exif_imagetype()` 이미지 시그니처 검사 우회, 웹셸 이용)| 웹셸 앞에 이미지(jpg) 매직 바이트(예:`\xFF\xD8\xFF\xE1`)를 붙여 `exif_imagetype()` 검사를 통과시킨 뒤, natas12와 동일하게 hidden 확장자를 php로 조작해 업로드 → 웹셸로 비밀번호 접근| [natas13](https://kisuk0104.tistory.com/57) |

---

## 실행 방법

```bash
pip install requests
python natas08.py
```

각 스크립트 상단의 비밀번호 변수에 본인 값을 넣고 실행하세요.
Natas는 직전 레벨을 풀어야 다음 레벨 비밀번호를 얻는 구조라, 값을 고정하지 않고 실행 시 직접 입력하도록 비워두었습니다.

---

## 참고

- 대상: OverTheWire Natas (공개 학습용 워게임)
- 목적: 웹 취약점 원리 학습 및 익스플로잇 자동화 연습
