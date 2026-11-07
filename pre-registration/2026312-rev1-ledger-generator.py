#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Task241: target 2026312 twelve-zodiac recent-fluctuation raw ledgers.

This is an evidence ledger only.  It does not select six zodiac signs or any
slot.  The main windows are W35/W40/W45, shown separately and never averaged
or converted into a total score.  W10/W20 describe the newest segment;
W60/W100/W250 provide medium/long context used to characterise the recent
movement.  Only the six normal numbers enter any frequency, occurrence, gap,
or route statistic.  The special zodiac is used only to form the PREV label.
"""
import csv
from collections import Counter
from math import comb
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "data" / "task242_1042_reconciled_history.csv"
OUT_PATH = ROOT / "data" / "task242_target312_reconciled_fluctuation_ledgers.txt"

ORDER = ["鼠", "牛", "虎", "兔", "龍", "蛇", "馬", "羊", "猴", "鷄", "狗", "豬"]
Z2N = {
    "鼠": [7, 19, 31, 43], "牛": [6, 18, 30, 42], "虎": [5, 17, 29, 41],
    "兔": [4, 16, 28, 40], "龍": [3, 15, 27, 39], "蛇": [2, 14, 26, 38],
    "馬": [1, 13, 25, 37, 49], "羊": [12, 24, 36, 48], "猴": [11, 23, 35, 47],
    "鷄": [10, 22, 34, 46], "狗": [9, 21, 33, 45], "豬": [8, 20, 32, 44],
}
N2Z = {n: z for z, ns in Z2N.items() for n in ns}
RED = {1, 2, 7, 8, 12, 13, 18, 19, 23, 24, 29, 30, 34, 35, 40, 45, 46}
BLUE = {3, 4, 9, 10, 14, 15, 20, 25, 26, 31, 36, 37, 41, 42, 47, 48}
WINDOWS = (10, 20, 35, 40, 45, 60, 100, 250)


def wave(n):
    return "红" if n in RED else "蓝" if n in BLUE else "绿"


rows_desc = list(csv.DictReader(CSV_PATH.open(encoding="utf-8-sig", newline="")))
rows = sorted(rows_desc, key=lambda r: int(r["period"]))
assert len(rows) == 1042, len(rows)
assert int(rows[-1]["period"]) == 2026311
assert len({r["period"] for r in rows}) == len(rows)
assert all(int(a["period"]) < int(b["period"]) for a, b in zip(rows, rows[1:]))
TARGET = int(rows[-1]["period"]) + 1
assert TARGET == 2026312

PERIODS = [int(r["period"]) for r in rows]
DRAW_NUMS = [[int(r[f"n{j}"]) for j in range(1, 7)] for r in rows]
DRAW_ZS = [[r[f"z{j}"] for j in range(1, 7)] for r in rows]
for nums, zs in zip(DRAW_NUMS, DRAW_ZS):
    assert len(nums) == len(set(nums)) == 6
    assert all(1 <= n <= 49 for n in nums)
    assert len(zs) == 6 and all(z in ORDER for z in zs)
# Current number->zodiac map is asserted only over the latest 250 draws;
# every statistic below is inside that era.  Earlier CSV zodiac fields are not
# reinterpreted through this fixed map.
for nums, zs in list(zip(DRAW_NUMS, DRAW_ZS))[-250:]:
    assert all(N2Z[n] == z for n, z in zip(nums, zs))

assert DRAW_NUMS[-1] == [32, 40, 49, 14, 19, 16]
assert DRAW_ZS[-1] == ["豬", "兔", "馬", "蛇", "鼠", "兔"]
assert int(rows[-1]["special"]) == 34 and rows[-1]["special_zodiac"] == "鷄"

PREV = set(DRAW_ZS[-1]) | {rows[-1]["special_zodiac"]}
PREV_ORDER = [z for z in ORDER if z in PREV]
FRESH_ORDER = [z for z in ORDER if z not in PREV]
assert PREV_ORDER == ["鼠", "兔", "蛇", "馬", "鷄", "豬"], PREV_ORDER
assert FRESH_ORDER == ["牛", "虎", "龍", "羊", "猴", "狗"], FRESH_ORDER
PRIOR_FROZEN_311 = ["蛇", "馬", "兔", "豬", "龍", "鷄"]


def summarize_indices(idxs):
    balls = Counter()
    occ = Counter()
    nums = Counter()
    for i in idxs:
        balls.update(DRAW_ZS[i])
        occ.update(set(DRAW_ZS[i]))
        nums.update(DRAW_NUMS[i])
    w = len(idxs)
    out = {}
    for z in ORDER:
        k = len(Z2N[z])
        eb = w * 6 * k / 49
        eo = w * (1 - comb(49 - k, 6) / comb(49, 6))
        routes = [nums[n] for n in Z2N[z]]
        out[z] = {
            "balls": balls[z], "occ": occ[z], "eb": eb, "eo": eo,
            "bd": balls[z] - eb, "od": occ[z] - eo, "routes": routes,
        }
    assert sum(balls.values()) == 6 * w
    assert sum(nums.values()) == 6 * w
    assert all(sum(out[z]["routes"]) == out[z]["balls"] for z in ORDER)
    return out, nums


def window_stats(w):
    return summarize_indices(list(range(len(rows) - w, len(rows))))


def age_segment_stats(age_start, age_end):
    """Ages are draws back from the latest row: age0=latest, [start,end)."""
    return summarize_indices(list(range(len(rows) - age_end, len(rows) - age_start)))


def number_gap(n):
    for age, nums in enumerate(reversed(DRAW_NUMS)):
        if n in nums:
            return age
    raise AssertionError(n)


def zodiac_flat_age(z):
    for age, zs in enumerate(reversed(DRAW_ZS)):
        if z in zs:
            return age
    raise AssertionError(z)


def recent_identity_events(z, limit=12):
    events = []
    for age in range(len(rows)):
        i = len(rows) - 1 - age
        c = DRAW_ZS[i].count(z)
        if c:
            nums = [DRAW_NUMS[i][j] for j in range(6) if DRAW_ZS[i][j] == z]
            events.append((age, PERIODS[i], c, nums))
            if len(events) >= limit:
                break
    return events


GAPS = {n: number_gap(n) for n in range(1, 50)}
Z_GAPS = {z: zodiac_flat_age(z) for z in ORDER}
WSTATS = {}
WNUMS = {}
for w in WINDOWS:
    WSTATS[w], WNUMS[w] = window_stats(w)

lines = []
add = lines.append
add("TASK242 RECONCILED TARGET2026312 十二肖近期波动原始账本")
add("method=人工无摇号v5.0账本；35/40/45主窗口并列；10/20看近端；60/100/250给近期波动定性；不平均、不合成总分、不定席")
add("data_rows=1042 latest=2026311 target=2026312 normal_numbers_only=6 special_frequency_excluded=yes")
add(
    f"latest_draw=2026311 numbers={DRAW_NUMS[-1]} zodiacs={DRAW_ZS[-1]} "
    f"special=34鷄(frequency excluded; identity included only in PREV label)"
)
add(f"PREV_label_ORDER={PREV_ORDER} count=6 (label only; no repeat quota)")
add(f"NON_PREV_ORDER={FRESH_ORDER} count=6 (no fresh quota)")
add(f"prior_frozen311={PRIOR_FROZEN_311} (comparator only; no carry-over entitlement)")

add("\n## 最近45期逐期平码（正序）")
for r, ns, zs in list(zip(rows, DRAW_NUMS, DRAW_ZS))[-45:]:
    add(f"{r['period']} {' '.join(f'{n:02d}{z}' for n, z in zip(ns, zs))}")

add("\n## 十二肖跨窗口总览（每格=球/出现期；括号=校准球差/出现差）")
add("zodiac label last_flat_age W10 W20 W35 W40 W45 W60 W100 W250")
for z in ORDER:
    vals = []
    for w in WINDOWS:
        s = WSTATS[w][z]
        vals.append(f"W{w}={s['balls']}/{s['occ']}({s['bd']:+.2f}/{s['od']:+.2f})")
    add(f"{z} {'PREV' if z in PREV else 'NON_PREV'} age={Z_GAPS[z]} " + " ".join(vals))

for w in WINDOWS:
    st = WSTATS[w]
    role = "近端观察" if w in (10, 20) else "主窗口" if w in (35, 40, 45) else "中长期背景"
    add(f"\n## {role} W={w}: {rows[-w]['period']}..{rows[-1]['period']}")
    add("zodiac label balls occ ball_exp ball_diff occ_exp occ_diff route_counts route_gaps top1share top2share stale_routes>=10 prior311")
    for z in ORDER:
        s = st[z]
        rg = [GAPS[n] for n in Z2N[z]]
        ordered_routes = sorted(s["routes"], reverse=True)
        top1 = ordered_routes[0] / s["balls"] if s["balls"] else 0
        top2 = sum(ordered_routes[:2]) / s["balls"] if s["balls"] else 0
        add(
            f"{z} {'PREV' if z in PREV else 'NON_PREV'} {s['balls']:2d} {s['occ']:2d} "
            f"{s['eb']:.2f} {s['bd']:+.2f} {s['eo']:.2f} {s['od']:+.2f} "
            f"routes={s['routes']} gaps={rg} top1={top1:.1%} top2={top2:.1%} "
            f"stale={sum(g >= 10 for g in rg)} {'P311' if z in PRIOR_FROZEN_311 else '-'}"
        )

add("\n## 35..45逐一窗口敏感度（每格=原始球/出现期；校准球差/出现差）")
for z in ORDER:
    seq = []
    for w in range(35, 46):
        s = window_stats(w)[0][z]
        seq.append(f"W{w}:{s['balls']}/{s['occ']}({s['bd']:+.1f}/{s['od']:+.1f})")
    add(f"{z} {'PREV' if z in PREV else 'NON_PREV'} " + " ".join(seq))

add("\n## 嵌套窗口的增量壳（互不重叠；每格=球/出现期）")
shells = [(0, 10), (10, 20), (20, 35), (35, 40), (40, 45), (45, 60), (60, 100), (100, 250)]
shell_stats = []
shell_labels = []
for age_start, age_end in shells:
    periods = [PERIODS[len(rows) - 1 - age] for age in range(age_end - 1, age_start - 1, -1)]
    shell_labels.append(f"age{age_start}-{age_end-1}({periods[0]}..{periods[-1]},n={len(periods)})")
    shell_stats.append(age_segment_stats(age_start, age_end)[0])
add("shells=" + " | ".join(shell_labels))
for z in ORDER:
    vals = [f"{s[z]['balls']}/{s[z]['occ']}({s[z]['bd']:+.1f}/{s[z]['od']:+.1f})" for s in shell_stats]
    add(f"{z} {'PREV' if z in PREV else 'NON_PREV'} shells={vals}")

add("\n## W45内部年龄块（新到旧；每格=球/出现期，附逐号路线）")
block_bounds = [(0, 10), (10, 20), (20, 30), (30, 35), (35, 40), (40, 45)]
block_labels = []
for age_start, age_end in block_bounds:
    periods = [rows[-1 - age]["period"] for age in range(age_end - 1, age_start - 1, -1)]
    block_labels.append(f"age{age_start}-{age_end-1}({periods[0]}..{periods[-1]},n={len(periods)})")
add("blocks=" + " | ".join(block_labels))
for z in ORDER:
    vals = []
    route_vals = []
    for age_start, age_end in block_bounds:
        idxs = list(range(len(rows) - age_end, len(rows) - age_start))
        b = sum(DRAW_ZS[i].count(z) for i in idxs)
        o = sum(z in set(DRAW_ZS[i]) for i in idxs)
        vals.append(f"{b}/{o}")
        route_vals.append(str([sum(DRAW_NUMS[i].count(n) for i in idxs) for n in Z2N[z]]))
    add(f"{z} {'PREV' if z in PREV else 'NON_PREV'} blocks={vals} route_blocks={route_vals}")

add("\n## 最近20期逐期出现轨迹（正序数字=每期该肖平码球数）")
add(f"periods={[p for p in PERIODS[-20:]]}")
for z in ORDER:
    trace = [DRAW_ZS[i].count(z) for i in range(len(rows) - 20, len(rows))]
    events = [(age, per, c, nums) for age, per, c, nums in recent_identity_events(z, 10)]
    add(f"{z} {'PREV' if z in PREV else 'NON_PREV'} trace20={trace} last10_events(age,period,balls,nums)={events}")

add("\n## 逐号码跨窗口频次与结构")
add("number zodiac label wave head tail parity road012 size gap W10 W20 W35 W40 W45 W60 W100 W250")
for n in range(1, 50):
    z = N2Z[n]
    add(
        f"{n:02d} {z} {'PREV' if z in PREV else 'NON_PREV'} wave={wave(n)} head={n//10} tail={n%10} "
        f"parity={'odd' if n%2 else 'even'} road={n%3} size={'big' if n>=25 else 'small'} gap={GAPS[n]} "
        + " ".join(f"W{w}={WNUMS[w][n]}" for w in WINDOWS)
    )

add("\n## 每肖路线矩阵（号码顺序与Z2N相同；每路列W10/W20/W35/W40/W45）")
for z in ORDER:
    route_lines = []
    for n in Z2N[z]:
        route_lines.append(
            f"{n:02d}:{'/'.join(str(WNUMS[w][n]) for w in (10,20,35,40,45))}@gap{GAPS[n]}"
        )
    add(f"{z} {'PREV' if z in PREV else 'NON_PREV'} routes=" + "; ".join(route_lines))

add("\n## 多窗维度原始汇总（结构观察，不作分数）")
for w in (10, 20, 35, 40, 45, 60, 100, 250):
    ns = [n for draw in DRAW_NUMS[-w:] for n in draw]
    add(f"W{w} wave(red/blue/green)={[sum(wave(n)==c for n in ns) for c in ('红','蓝','绿')]}")
    add(f"W{w} head0-4={[sum(n//10 == h for n in ns) for h in range(5)]}")
    add(f"W{w} tail0-9={[sum(n % 10 == t for n in ns) for t in range(10)]}")
    add(
        f"W{w} odd/even={sum(n%2 for n in ns)}/{sum(1-n%2 for n in ns)} "
        f"small/big={sum(n<25 for n in ns)}/{sum(n>=25 for n in ns)} "
        f"road0/1/2={[sum(n % 3 == r for n in ns) for r in range(3)]}"
    )

add("\n## 上期311身份在新账本中的位置（只作衔接，不自动保留/剔除）")
for z in ORDER:
    flat311 = DRAW_ZS[-1].count(z)
    special_label = "special_label_only" if z == rows[-1]["special_zodiac"] else "-"
    add(
        f"{z} prev_label={'yes' if z in PREV else 'no'} flat311_balls={flat311} {special_label} "
        f"W35={WSTATS[35][z]['balls']}/{WSTATS[35][z]['occ']} W40={WSTATS[40][z]['balls']}/{WSTATS[40][z]['occ']} "
        f"W45={WSTATS[45][z]['balls']}/{WSTATS[45][z]['occ']}"
    )

assert len(PREV_ORDER) == 6 and len(FRESH_ORDER) == 6
assert all(sum(WSTATS[w][z]["routes"]) == WSTATS[w][z]["balls"] for w in WINDOWS for z in ORDER)
assert all(sum(s[z]["balls"] for s in shell_stats[:6]) == WSTATS[60][z]["balls"] for z in ORDER)
add("\nTASK242_RECONCILED_FLUCTUATION_LEDGERS PASS")

assert not OUT_PATH.exists(), 'ledger exists; refuse overwrite'
OUT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"written {OUT_PATH} lines={len(lines)} target=2026312 rows=1042")
