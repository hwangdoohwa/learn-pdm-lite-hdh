"""learn-pdm-lite-hdh 정답 예시 — 노이즈 vs 추세 그래프 한 장(index.html)을 만든다.

실행: python build_chart.py   (작업 폴더 안에서 — data/Day5_설비센서_50건_가상.csv 가 있어야 한다)
출력: 현재 폴더에 index.html (GitHub Pages 첫 화면) 과 expected.json (course-forge 검증용)

원본 강의: keerhee/kma-auto-genai-3-1 · Day5_예지보전 본 강의 ④ 분석 1
추세 규칙: 같은 저장소 보충교재 learn-auto-pdm 과 같다 (처음 12점 기준선 + 3σ, 3번 연속)
"""
import csv
import json
import statistics
from pathlib import Path

DATA = Path("data") / "Day5_설비센서_50건_가상.csv"
BASE_N = 12   # 기준선: 처음 12점(08:00~11:40) — 정상 운전 구간
K_SIGMA = 3   # 기준선 상한 = 평균 + 3σ
RUN = 3       # 3번 연속 넘으면 추세
REPO = "https://github.com/keerhee/kma-auto-genai-3-1"


def read():
    with open(DATA, encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    eq = {}
    for r in rows:
        eq.setdefault(r["설비"][:3], []).append(r)   # "설비A" / "설비B"
    return eq


def judge(rows, col):
    """기준선 상한, 상한 초과 점, 추세 시작 시각을 돌려준다."""
    v = [float(r[col]) for r in rows]
    t = [r["시간"][-5:] for r in rows]
    base = v[:BASE_N]
    ul = statistics.mean(base) + K_SIGMA * statistics.stdev(base)
    over = [x > ul for x in v]
    start, streak = None, 0
    for i, o in enumerate(over):
        streak = streak + 1 if o else 0
        if streak == RUN:
            start = i - RUN + 1
            break
    return {"t": t, "v": v, "ul": ul, "over": over, "start": start,
            "kind": "추세" if start is not None else ("노이즈" if any(over) else "정상")}


# ── 그래프(SVG) ────────────────────────────────────────────────────
W, H, L, R, T, B = 720, 380, 48, 52, 20, 40
VMAX = 4.0              # 왼쪽 축: 진동 0~4 mm/s
TMIN, TMAX = 50.0, 66.0  # 오른쪽 축: 온도 50~66 ℃


def x(i, n):
    return L + (W - L - R) * i / (n - 1)


def yv(v):
    return T + (H - T - B) * (1 - v / VMAX)


def yt(v):
    return T + (H - T - B) * (1 - (v - TMIN) / (TMAX - TMIN))


def line(pts, color, dash=""):
    d = " ".join(f"{px:.1f},{py:.1f}" for px, py in pts)
    da = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<polyline points="{d}" fill="none" stroke="{color}" stroke-width="2"{da}/>'


def svg(a_vib, b_vib, b_tmp):
    n = len(a_vib["t"])
    s = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="설비A·B 진동과 설비B 온도 선 그래프">']
    for k in range(5):  # 가로 눈금
        yy = yv(k)
        s.append(f'<line x1="{L}" x2="{W-R}" y1="{yy:.1f}" y2="{yy:.1f}" class="grid"/>')
        s.append(f'<text x="{L-6}" y="{yy+4:.1f}" text-anchor="end" class="ax">{k}</text>')
        s.append(f'<text x="{W-R+6}" y="{yt(TMIN + 4*k)+4:.1f}" class="ax">{TMIN + 4*k:.0f}</text>')
    for i, tt in enumerate(a_vib["t"]):
        if tt.endswith(":00"):
            s.append(f'<text x="{x(i, n):.1f}" y="{H-B+18}" text-anchor="middle" class="ax">{tt[:2]}시</text>')
    s.append(f'<text x="{L-6}" y="{T-6}" text-anchor="end" class="ax">mm/s</text>')
    s.append(f'<text x="{W-R+6}" y="{T-6}" class="ax">℃</text>')
    # 추세 시작 세로선
    for j, color, label in [(b_tmp, "var(--c3)", "B 온도 추세 시작"), (b_vib, "var(--c2)", "B 진동 추세 시작")]:
        xi = x(j["start"], n)
        s.append(f'<line x1="{xi:.1f}" x2="{xi:.1f}" y1="{T}" y2="{H-B}" stroke="{color}" stroke-width="1.5" stroke-dasharray="2 3"/>')
        s.append(f'<text x="{xi-4:.1f}" y="{T+12}" text-anchor="end" class="lb" fill="{color}">{label} {j["t"][j["start"]]}</text>')
    # 기준선 상한(점선)
    s.append(line([(L, yv(a_vib["ul"])), (W - R, yv(a_vib["ul"]))], "var(--c1)", "6 4"))
    s.append(line([(L, yv(b_vib["ul"])), (W - R, yv(b_vib["ul"]))], "var(--c2)", "6 4"))
    s.append(line([(L, yt(b_tmp["ul"])), (W - R, yt(b_tmp["ul"]))], "var(--c3)", "6 4"))
    # 값
    s.append(line([(x(i, n), yv(v)) for i, v in enumerate(a_vib["v"])], "var(--c1)"))
    s.append(line([(x(i, n), yv(v)) for i, v in enumerate(b_vib["v"])], "var(--c2)"))
    s.append(line([(x(i, n), yt(v)) for i, v in enumerate(b_tmp["v"])], "var(--c3)"))
    # 노이즈 표시: 설비A 진동이 상한을 넘은 점
    for i, o in enumerate(a_vib["over"]):
        if o:
            s.append(f'<circle cx="{x(i, n):.1f}" cy="{yv(a_vib["v"][i]):.1f}" r="6" fill="none" stroke="var(--c1)" stroke-width="2"/>')
            s.append(f'<text x="{x(i, n)+10:.1f}" y="{yv(a_vib["v"][i])+4:.1f}" class="lb" fill="var(--c1)">A 노이즈 {a_vib["t"][i]} · {a_vib["v"][i]}</text>')
    s.append("</svg>")
    return "\n".join(s)


PAGE = """<!doctype html>
<html lang="ko"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>노이즈 vs 추세</title>
<style>
:root {{ --bg:#fff; --fg:#1f2328; --mute:#656d76; --line:#d0d7de; --c1:#2f6fb3; --c2:#d9822b; --c3:#c0392b; }}
@media (prefers-color-scheme: dark) {{ :root {{ --bg:#0d1117; --fg:#e6edf3; --mute:#9198a1; --line:#30363d; --c1:#6ea8fe; --c2:#f0a050; --c3:#ff7b72; }} }}
* {{ box-sizing:border-box; }}
body {{ margin:0; background:var(--bg); color:var(--fg); font:16px/1.6 system-ui, "Malgun Gothic", sans-serif; }}
main {{ max-width:860px; margin:0 auto; padding:24px 16px; }}
h1 {{ font-size:1.4rem; margin:0 0 4px; }}
.sum {{ margin:0 0 16px; }}
.sum b {{ color:var(--c3); }}
svg {{ width:100%; height:auto; display:block; }}
.grid {{ stroke:var(--line); }}
.ax {{ fill:var(--mute); font-size:12px; }}
.lb {{ font-size:12px; font-weight:600; }}
.key {{ display:flex; flex-wrap:wrap; gap:4px 16px; margin:8px 0 0; padding:0; list-style:none; font-size:.9rem; }}
.key i {{ display:inline-block; width:16px; height:3px; vertical-align:middle; margin-right:6px; }}
footer {{ margin-top:20px; color:var(--mute); font-size:.85rem; }}
a {{ color:var(--c1); }}
</style></head>
<body><main>
<h1>노이즈 vs 추세 — 설비A·B 센서</h1>
<p class="sum">설비B 온도가 <b>{b_tmp_start}</b>부터, 설비B 진동이 <b>{b_vib_start}</b>부터 기준선 상한을 연속으로 넘으며 오른다(추세 → 정비 신호).
설비A 진동은 {a_t} 한 번 {a_v} mm/s로 튀고 돌아왔다(노이즈).</p>
{svg}
<ul class="key">
<li><i style="background:var(--c1)"></i>설비A 진동 (왼쪽 축)</li>
<li><i style="background:var(--c2)"></i>설비B 진동 (왼쪽 축)</li>
<li><i style="background:var(--c3)"></i>설비B 온도 (오른쪽 축)</li>
<li>점선 = 기준선 상한 (처음 12점 평균 + 3σ · A 진동 {a_ul:.2f} · B 진동 {b_vul:.2f} · B 온도 {b_tul:.1f}℃)</li>
</ul>
<footer>센서 값은 <b>실습용 가상 데이터</b>다 (2026-09-15 08:00~16:00, 20분 간격).
원본 강의: <a href="{repo}">keerhee/kma-auto-genai-3-1</a> · Day5 예지보전 ④ 분석 1</footer>
</main></body></html>
"""


def main():
    eq = read()
    a_vib = judge(eq["설비A"], "진동(mm/s)")
    b_vib = judge(eq["설비B"], "진동(mm/s)")
    b_tmp = judge(eq["설비B"], "온도(℃)")
    ai = a_vib["over"].index(True)
    html = PAGE.format(svg=svg(a_vib, b_vib, b_tmp), repo=REPO,
                       b_tmp_start=b_tmp["t"][b_tmp["start"]], b_vib_start=b_vib["t"][b_vib["start"]],
                       a_t=a_vib["t"][ai], a_v=a_vib["v"][ai],
                       a_ul=a_vib["ul"], b_vul=b_vib["ul"], b_tul=b_tmp["ul"])
    Path("index.html").write_text(html, encoding="utf-8")

    exp = {"values": {
        "a_vib_kind": {"value": a_vib["kind"], "decimals": None, "block": 1},
        "a_noise_time": {"value": a_vib["t"][ai], "decimals": None, "block": 1},
        "a_noise_value": {"value": a_vib["v"][ai], "decimals": 1, "block": 1},
        "b_temp_trend_start": {"value": b_tmp["t"][b_tmp["start"]], "decimals": None, "block": 1},
        "b_temp_upper": {"value": round(b_tmp["ul"], 1), "decimals": 1, "block": 1},
        "b_temp_over_points": {"value": sum(b_tmp["over"]), "decimals": 0, "block": 1},
        "b_vib_trend_start": {"value": b_vib["t"][b_vib["start"]], "decimals": None, "block": 1},
        "b_vib_upper": {"value": round(b_vib["ul"], 2), "decimals": 2, "block": 1},
    }}
    Path("expected.json").write_text(json.dumps(exp, ensure_ascii=False, indent=1), encoding="utf-8")
    for k, v in exp["values"].items():
        print(f"{k}: {v['value']}")


if __name__ == "__main__":
    main()
