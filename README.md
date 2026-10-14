# Natas Web Wargame — Python Writeups

[OverTheWire Natas](https://overthewire.org/wargames/natas/) 워게임을 **수동 진단 → 취약점 분석 → Python 자동화 익스플로잇** 흐름으로 풀어본 기록입니다.

각 레벨마다 "왜 터지는가"는 블로그에, "어떻게 자동화했는가"는 이 레포의 코드에 나눠 정리했습니다.

> 블로그 전체 글: https://kisuk0104.tistory.com/

---

## 풀이 목록

| 파일 | 취약점 | 핵심 아이디어 | 블로그 풀이 |
|------|--------|---------------|-------------|
| [`natas08.py`](natas08.py) | 인코딩 역추적 | base64 → reverse → hex 로직을 역연산해 secret 복원 | [natas8](https://kisuk0104.tistory.com/51) |
| [`natas09.py`](natas09.py) | OS Command Injection | `passthru`에 입력값을 검증 없이 연결 → `;`로 명령 분리 후 임의 명령 실행 | [natas9](https://kisuk0104.tistory.com/52) |
| [`natas10.py`](natas10.py) | Command Injection (필터 우회) | `preg_match`로 `;`,`&`,`\|` 필터 → grep 정규식 특성을 이용한 파일 읽기 | [natas10](https://kisuk0104.tistory.com/53) |
| [`natas11.py`](natas11.py) | 쿠키 변조 (XOR) | base64+JSON 쿠키를 XOR 복호화 → 키 복원 후 위조 쿠키 생성 | _(작성 예정)_ |

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
