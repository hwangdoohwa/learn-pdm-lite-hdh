# Block 2: 공개 — GitHub Pages와 공유

> **Phase A 시작 시 그대로 출력한다:**
> ```
> 📖 GitHub Pages 사이트 만들기: https://docs.github.com/ko/pages/getting-started-with-github-pages/creating-a-github-pages-site
> 📖 GitHub CLI 로그인: https://cli.github.com/manual/gh_auth_login
> ```

## EXPLAIN

### 1. 용어

| 용어 | 뜻 |
|---|---|
| **GitHub Pages** | GitHub 저장소의 `index.html`을 `https://<아이디>.github.io/<저장소>/` 주소로 보여 주는 무료 웹 공개 기능 |
| **일회용 코드** | GitHub 로그인 때 브라우저에 입력하는 8자리 코드. 비밀번호처럼 다룬다 |

### 2. 왜 주소로 공개하는가

| 기준 | 파일로 보내기 | 주소로 공개 |
|---|---|---|
| 받는 사람 | 내려받아 열어야 보인다 | 휴대폰·회의실 화면에서 바로 열린다 |
| 고친 뒤 | 다시 보내야 한다 | 같은 주소가 최신으로 바뀐다 |

### 3. 공개 전 약속

- GitHub 비밀번호와 일회용 코드는 github.com 공식 사이트(브라우저)에만 입력한다. 대화창·메신저에 쓰지 않는다.
- 공개 저장소는 누구나 본다. '실습용 가상 데이터' 표기가 없으면 실제 공장 데이터로 오해받는다.
- 우리 회사 실제 설비 데이터는 공개 저장소에 올리지 않는다.

## EXECUTE

아래 프롬프트를 붙여 넣으라고 안내한다.

```
kma-pdm-lite 의 그래프를 GitHub Pages로 공개하자.
1. 올라갈 파일 목록을 보여 주고, 개인정보·비밀번호가 없는지 점검해 줘.
   env_check.txt 는 .gitignore 로 빼 줘.
2. gh auth status 로 GitHub 연결을 확인해 줘. 안 되어 있으면 로그인을 시작해서
   일회용 코드와 접속 주소만 보여 줘. 코드는 내가 브라우저에만 입력할 거야.
3. git init 하고 커밋한 뒤 kma-pdm-lite 공개 저장소를 만들어 푸시하고,
   GitHub Pages(main, /)를 켜 줘.
4. 배포 상태가 built 가 될 때까지 확인하고 사이트 주소를 크게 보여 줘.
```

### 확인할 것 (Phase B)

- `gh repo view kma-pdm-lite`로 저장소가 public이고 `index.html`이 있다
- 올라간 파일에 `env_check.txt`가 없다
- `https://<아이디>.github.io/kma-pdm-lite/`가 열리고 추세 시작 13:00이 보인다 (켠 뒤 1~3분은 404가 정상)

404가 3분 넘게 이어지면 "Pages가 404인데 원인을 찾아 줘"를 붙여 넣게 한다.

## QUIZ

Block 2는 퀴즈가 없다. 확인이 끝나면 아래 과제를 안내하고 수업을 마친다.

## 과제와 다음

1. **짝에게 공유** — 내 Pages 주소와 이 강의 설치 한 줄(`npx skills add <만든 사람 아이디>/learn-pdm-lite-hdh --agent claude-code --global --yes`)을 짝에게 보낸다. 제출물: 보낸 메시지 캡처.
2. **점검표 받기** — 짝이 이 수업을 들은 뒤 "블록 3개 진행 · 퀴즈가 판단형 · 추세 시작 13:00 · 헷갈린 문장"을 예/아니오로 적어 보내게 한다. 제출물: 받은 점검표.
3. **내 강의 하나 더** — 다른 Day나 내 업무 주제로 `/course-forge`를 다시 돌려 내 강의를 하나 더 만든다. 제출물: 새 learn- 저장소 주소.
