# 원본 대조 — learn-pdm-lite-hdh

| 항목 | 정답 실행 (expected.json) | 원본 | 일치 |
|---|---|---|---|
| 설비A 진동 판정 | 노이즈 (12:40 · 3.5 mm/s 한 점) | 정답 메모: "진동이 한 번 튄 3.5만 이상 후보 — 노이즈형" · 덱 27장 "3.5는 한 번 튀고 곧 정상으로 돌아온 일시적 노이즈" | ✓ |
| 설비B 온도 추세 시작 | 13:00 (상한 57.0℃, 초과 10점) | 보충교재 learn-auto-pdm expected.json `b_temp_trend_start` 13:00 · 실습판 점검표 "추세 시작 13:00" | ✓ |
| 설비B 진동 추세 시작 | 15:00 (상한 1.12 mm/s) | 보충교재 learn-auto-pdm expected.json `b_vib_trend_start` 15:00 | ✓ |
| 설비B 유형 | 추세 | 정답 메모: "추세형" | ✓ |
