# -*- coding: utf-8 -*-
"""pool_six.py — 六肖先定·双池可重复 原型 (task200 最终定版, 2026-10-23)

用户最终点选: (1) 两池合起来去重恰好6个不同生肖, 其中上期重肖2个+新肖4个;
              (2) 先定这六个不同生肖(Universe U), 再按各自排名分进池1/池2,
                  同一生肖可同时进两池, 池位可为4+4/4+5/3+6等 (看数据).
概念分清: 重肖 = 肖 in PREV (上期7球 distinct); 重复肖 = 同一生肖同时在池1与池2. 两者不同.

Universe 选择 (分层 _pick: PREV最优2 + 非PREV最优4, 层不足顺延, 返回按原序):
  v4.0 (承 v2.5, 100期窗): Universe序 = 名次和 merged; 不读 BAN.
  v4.1 (承 v3.0, 30/60窗): Universe序 = 组合序 (在order30的位置 + 在order60的位置 升序, 并列生肖序小者); 读 BAN.
  v4.2 (2026-10-23 task202 深复盘调整, 承 v4.1): 组合序/窗口/BAN 不变; 分层改为
       重肖取 R[0]+R[-1], 新肖取 F[0..2]+F[-1] (每层最后一席为尾部对冲);
       仍恰好2重4新, 不足时沿组合序兜底。调整只分散排名门槛暴露, 不主张预测力。
  单期人工定案: 目标2026299以[鷄、馬、虎、蛇、龍、狗]覆盖自动 Universe;
       目标2026300按《300期网站人工选肖_复盘闸门版》以[虎、兔、龍、蛇、馬、鷄]覆盖;
       目标2026301按《301期网站人工选肖_300深度复盘后》以[虎、蛇、鼠、兔、龍、鷄]覆盖;
       目标2026302按《302期网站人工选肖_301深度复盘后》以[虎、蛇、兔、馬、鷄、狗]覆盖;
       目标2026303按《303期网站人工选肖_302深度复盘后》以[蛇、鷄、虎、鼠、龍、兔]覆盖;
       目标2026304按《304期网站人工选肖_303深度复盘后》以[蛇、虎、鼠、羊、猴、鷄]覆盖；
       目标2026305按《305期网站人工选肖_304深度复盘后》以[鷄、馬、虎、蛇、兔、豬]覆盖；
       目标2026306按《306期网站人工选肖_305深度复盘后》以[虎、蛇、鷄、猴、羊、龍]覆盖；
       目标2026307先按长窗报告覆盖，后经用户在开奖前明确授权改用35—45期主窗口，
       现按《307期网站人工选肖_35-45主窗口修订》以[蛇、兔、虎、鼠、鷄、羊]覆盖；
       目标2026308按《308期网站人工选肖_35-45主窗口》以[蛇、馬、虎、兔、豬、鼠]覆盖。
       _alloc 与4000步摇号保持网站框架。若目标另有 PERIOD_BAN, 为守BAN不变量不启用
       覆盖并回自动 v4.2。其他目标期不受影响。
  v5.0 (2026-11-04, 308深复盘后): pools_v50/ent_v50 只读取
       data/manual_site_decisions.json 中目标期的人工六肖与 top/A/B/C/D,
       重肖数不设配额, cands/pool仅为派生归类, 不调用 _alloc/LCG;
       无人工记录时 fail-closed。v4.x函数保留作历史冻结盘复算。
双池分配 _alloc (两线共用; o1=池1排名序, o2=池2排名序):
  1) 初始入池: 池1 = U 中在 o1 前4名(前1/3)者; 池2 = U 中在 o2 前6名(前1/2)者.
  2) 最小池长: 池1<2 时按 o1 从 U 顺延补至2; 池2<4 时按 o2 从 U 顺延补至4.
  3) 全覆盖: U 中未入任何池者, 入其排名位置更靠前的一池 (同位入池2).
  4) 各按本池排名序排列; 任一池无 PREV 重肖时, 按该池排名序补入 U 中最靠前的重肖.
  优先级: U=6 distinct(2重4新) > 两池并集=U > 池2>=4/池1>=2 > 每池>=1重肖 > 入池门槛 > 排名.
  结果: 两池大小与重叠数随数据变化 (池内仍不重复), 并集恒为 U 的6个不同生肖.
摇号不变: v4.0 = LCG 1步取top + splice4步; v4.1/v4.2 = 单一LCG 4000步 (池1x1000取最多, 池2x3000降序取前4).
仅结构审计, 不做命中回测 (遵196). 与 JS (gen_trend.py poolTop6_v40/v41/v42) 互为独立复算.
"""
import csv, collections, statistics, json, sys
from pathlib import Path
_CSV = Path(__file__).resolve().parents[1] / 'data' / 'macau_mark_six_full.csv'

ORDER = ['鼠','牛','虎','兔','龍','蛇','馬','羊','猴','鷄','狗','豬']
rows = list(csv.DictReader(open(_CSV, encoding='utf-8-sig')))
rows.sort(key=lambda r: int(r['period']))
ALL = [[int(r['period']), r['date'][5:10].replace('-','/'),
        [int(r[f'n{j}']) for j in range(1,7)],
        [ORDER.index(r[f'z{j}']) for j in range(1,7)],
        int(r['special']), ORDER.index(r['special_zodiac'])] for r in rows]
N2Z = {}
for r in rows:
    if int(r['period']) >= 2026048:
        for j in range(1,7): N2Z[int(r[f'n{j}'])] = ORDER.index(r[f'z{j}'])
        N2Z[int(r['special'])] = ORDER.index(r['special_zodiac'])
assert len(N2Z) == 49 and all(N2Z[n] == (7-n) % 12 for n in range(1,50))
Z2N = {z: sorted(n for n in range(1,50) if N2Z[n] == z) for z in range(12)}
PERIOD_BAN = {2026289: {11}}
# 单期人工 Universe (报告顺序); 每项只对键名目标期生效。
MANUAL_UNIVERSES = {
    2026299: [ORDER.index(z) for z in ['鷄', '馬', '虎', '蛇', '龍', '狗']],
    2026300: [ORDER.index(z) for z in ['虎', '兔', '龍', '蛇', '馬', '鷄']],
    2026301: [ORDER.index(z) for z in ['虎', '蛇', '鼠', '兔', '龍', '鷄']],
    2026302: [ORDER.index(z) for z in ['虎', '蛇', '兔', '馬', '鷄', '狗']],
    2026303: [ORDER.index(z) for z in ['蛇', '鷄', '虎', '鼠', '龍', '兔']],
    2026304: [ORDER.index(z) for z in ['蛇', '虎', '鼠', '羊', '猴', '鷄']],
    2026305: [ORDER.index(z) for z in ['鷄', '馬', '虎', '蛇', '兔', '豬']],
    2026306: [ORDER.index(z) for z in ['虎', '蛇', '鷄', '猴', '羊', '龍']],
    2026307: [ORDER.index(z) for z in ['蛇', '兔', '虎', '鼠', '鷄', '羊']],
    2026308: [ORDER.index(z) for z in ['蛇', '馬', '虎', '兔', '豬', '鼠']],
}

# v5.0 (2026-11-04, 308深复盘后用户定案): 六肖与 top/A/B/C/D 全部人工决定,
# 重肖数不设配额, 不调用 _alloc/LCG。人工记录的唯一来源是
# data/manual_site_decisions.json; 没有目标期记录时 fail-closed, 绝不回退摇号。
MANUAL_DECISIONS_PATH = Path(__file__).resolve().parents[1] / 'data' / 'manual_site_decisions.json'


class ManualDecisionMissing(ValueError):
    pass


def _zidx(value):
    if isinstance(value, bool):
        raise ValueError(f'非法生肖值: {value!r}')
    if isinstance(value, int):
        if 0 <= value < 12:
            return value
        raise ValueError(f'生肖索引越界: {value!r}')
    if isinstance(value, str) and value in ORDER:
        return ORDER.index(value)
    raise ValueError(f'非法生肖值: {value!r}')


def _load_manual_site_decision(target):
    if not MANUAL_DECISIONS_PATH.exists():
        return None
    doc = json.loads(MANUAL_DECISIONS_PATH.read_text(encoding='utf-8'))
    decisions = doc.get('decisions', {}) if isinstance(doc, dict) else {}
    if not isinstance(decisions, dict):
        raise ValueError('manual_site_decisions.json: decisions 必须是对象')
    return decisions.get(str(target), decisions.get(target))


def _normalize_manual_site_decision(raw, target, PREV, BAN):
    if not isinstance(raw, dict):
        raise ValueError('v5.0人工定案必须是对象')
    rec_target = raw.get('target', target)
    if int(rec_target) != target:
        raise ValueError(f'v5.0人工定案目标期不符: record={rec_target}, expected={target}')
    source_report = raw.get('source_report')
    if not isinstance(source_report, str) or not source_report.strip():
        raise ValueError('v5.0人工定案必须写明 source_report')
    universe_raw = raw.get('universe_zodiac', raw.get('U', raw.get('universe')))
    if not isinstance(universe_raw, list):
        raise ValueError('v5.0人工定案缺少 universe_zodiac 数组')
    U = [_zidx(z) for z in universe_raw]
    if len(U) != 6 or len(set(U)) != 6:
        raise ValueError('v5.0人工Universe必须恰好6个不同生肖')
    roles = {
        'top': _zidx(raw.get('top_zodiac', raw.get('top'))),
        'A': _zidx(raw.get('a_zodiac', raw.get('A'))),
        'B': _zidx(raw.get('b_zodiac', raw.get('B'))),
        'C': _zidx(raw.get('c_zodiac', raw.get('C'))),
        'D': _zidx(raw.get('d_zodiac', raw.get('D'))),
    }
    abcd = [roles['A'], roles['B'], roles['C'], roles['D']]
    if len(set(abcd)) != 4:
        raise ValueError('v5.0 A/B/C/D必须互不相同')
    if roles['top'] not in U or not set(abcd) <= set(U):
        raise ValueError('v5.0 top/A/B/C/D必须都在人工Universe内')
    if BAN and (set(U) & set(BAN)):
        banned = [ORDER[z] for z in sorted(set(U) & set(BAN))]
        raise ValueError(f'v5.0人工定案与PERIOD_BAN冲突: {banned}')
    overlap_mode = 'concentrated' if roles['top'] in abcd else 'coverage'
    declared_mode = raw.get('top_overlap_mode', overlap_mode)
    if declared_mode != overlap_mode:
        raise ValueError(
            f'v5.0 top_overlap_mode不符: declared={declared_mode}, derived={overlap_mode}'
        )
    display = []
    for z in [roles['top'], *abcd]:
        if z not in display:
            display.append(z)
    reserves = [z for z in U if z not in display]
    return {
        'target': target,
        'U': U,
        'universe_zodiac': [ORDER[z] for z in U],
        'roles': roles,
        'roles_zodiac': {k: ORDER[v] for k, v in roles.items()},
        'display': display,
        'display_zodiac': [ORDER[z] for z in display],
        'reserves': reserves,
        'reserve_zodiac': [ORDER[z] for z in reserves],
        'repeat_count': sum(1 for z in U if z in PREV),
        'top_overlap_mode': overlap_mode,
        'source_report': source_report,
        'universe_rationale': raw.get('universe_rationale', ''),
        'slot_rationale': raw.get('slot_rationale', {}),
        'reserve_rationale': raw.get('reserve_rationale', ''),
        'selection_mode': 'manual_universe_and_slots_no_shake',
    }


def _manual_site_v50_result(hist, decision=None):
    if not hist:
        raise ValueError('v5.0需要至少一期历史数据')
    target = hist[-1][0] + 1
    PREV = set(hist[-1][3] + [hist[-1][5]])
    BAN = PERIOD_BAN.get(target, set())
    raw = _load_manual_site_decision(target) if decision is None else decision
    if raw is None:
        raise ManualDecisionMissing(
            f'v5.0目标{target}尚无人工定案记录; 已拒绝回退自动选肖/摇号'
        )
    dec = _normalize_manual_site_decision(raw, target, PREV, BAN)
    roles = dec['roles']
    # 两池仅为兼容字段的结果归类: cands=展示组, pool=组合四员+非展示替补。
    cands = list(dec['display'])
    pool = [roles['A'], roles['B'], roles['C'], roles['D'], *dec['reserves']]
    return {
        'top': roles['top'],
        't2': [roles['A'], roles['B']],
        't3': [roles['A'], roles['C'], roles['D']],
        'pool': pool,
        'cands': cands,
        'PREV': PREV,
        'U': list(dec['U']),
        'decision': dec,
        'target': target,
        'BAN': BAN,
    }


def pools_v50(hist, decision=None, debug=False):
    ent = _manual_site_v50_result(hist, decision=decision)
    dbg = ({'target': ent['target'], 'BAN': ent['BAN'], 'decision': ent['decision'],
            'pool_semantics': 'cands=display group; pool=A/B/C/D plus nondisplay reserves'}
           if debug else None)
    return ent['pool'], ent['cands'], ent['PREV'], ent['U'], dbg


def ent_v50(hist, decision=None):
    return _manual_site_v50_result(hist, decision=decision)

def _ranks(W):
    cnt = [0]*50
    for r in W:
        for n in r[2]: cnt[n] += 1
    E = 6*len(W)/49; zs = [0]*12; ks = [0]*12
    for n in range(1,50):
        z = N2Z[n]; zs[z] += cnt[n]; ks[z] += 1
    rec = sorted([[z, zs[z]/(ks[z]*E)] for z in range(12)], key=lambda a: (-a[1], a[0]))
    rA = [0]*12
    for i,(z,v) in enumerate(rec): rA[z] = i+1
    zb = [0]*12
    for r in W:
        for z in set(r[3]): zb[z] += 1
    oB = sorted(range(12), key=lambda z: (-zb[z], z)); rB = [0]*12
    for i,z in enumerate(oB): rB[z] = i+1
    S = [rA[z]+rB[z] for z in range(12)]
    return {'order': sorted(range(12), key=lambda z: (S[z], z)), 'S': S,
            'rec': rec, 'oB': oB, 'rA': rA, 'rB': rB, 'zb': zb}

def _pick(order, PREV, BAN, exclude, n_rep, n_fresh):
    size = n_rep + n_fresh
    elig = [z for z in order if z not in BAN and z not in exclude]
    picks = []
    def add(z):
        if z not in picks: picks.append(z)
    for z in [z for z in elig if z in PREV][:n_rep]: add(z)
    for z in [z for z in elig if z not in PREV][:n_fresh]: add(z)
    for z in elig:
        if len(picks) >= size: break
        add(z)
    for z in order:
        if len(picks) >= size: break
        if z not in exclude: add(z)
    for z in order:
        if len(picks) >= size: break
        add(z)
    pos = {z: i for i, z in enumerate(order)}
    return sorted(picks[:size], key=lambda z: pos[z])

def _pick_hedge(order, PREV, BAN, n_rep=2, n_fresh=4):
    """v4.2 分层尾部对冲: 每层前 k-1 席沿原序, 最后一席取该层原序末位。
    BAN 在分层前剔除; 层不足/席位重合时按原序补满, 再不足才放行 BAN (与 _pick 兜底一致)。"""
    size = n_rep + n_fresh
    elig = [z for z in order if z not in BAN]
    reps = [z for z in elig if z in PREV]
    fresh = [z for z in elig if z not in PREV]
    def choose(xs, k):
        if k <= 0: return []
        if len(xs) <= k: return list(xs)
        out = list(xs[:k-1])
        if xs[-1] not in out: out.append(xs[-1])
        for z in xs:
            if len(out) >= k: break
            if z not in out: out.append(z)
        return out
    picks = choose(reps, n_rep) + choose(fresh, n_fresh)
    for z in elig:
        if len(picks) >= size: break
        if z not in picks: picks.append(z)
    for z in order:
        if len(picks) >= size: break
        if z not in picks: picks.append(z)
    pos = {z: i for i, z in enumerate(order)}
    return sorted(picks[:size], key=lambda z: pos[z])

def _alloc(U, PREV, o1, o2):
    """Universe U -> (cands, pool, diag). 门槛: 池1前4 / 池2前6; 最小2/4; 全覆盖; 每池>=1重肖."""
    Uset = set(U)
    pos1 = {z: i for i, z in enumerate(o1)}; pos2 = {z: i for i, z in enumerate(o2)}
    cands = [z for z in o1 if z in Uset and pos1[z] < 4]
    pool = [z for z in o2 if z in Uset and pos2[z] < 6]
    diag = {'init1': list(cands), 'init2': list(pool), 'min_ext1': 0, 'min_ext2': 0,
            'coverage': [], 'rep_add1': False, 'rep_add2': False}
    def extend(p, order, minimum, key):
        for z in order:
            if len(p) >= minimum: break
            if z in Uset and z not in p: p.append(z); diag[key] += 1
        return sorted(p, key=lambda z: {x: i for i, x in enumerate(order)}[z])
    cands = extend(cands, o1, 2, 'min_ext1')
    pool = extend(pool, o2, 4, 'min_ext2')
    for z in U:
        if z not in cands and z not in pool:
            if pos1[z] < pos2[z]: cands.append(z); diag['coverage'].append((z, 1))
            else: pool.append(z); diag['coverage'].append((z, 2))
    cands = sorted(cands, key=lambda z: pos1[z]); pool = sorted(pool, key=lambda z: pos2[z])
    reps = [z for z in U if z in PREV]
    if reps and not any(z in PREV for z in cands):
        z = min(reps, key=lambda zz: pos1[zz]); cands.append(z)
        cands = sorted(cands, key=lambda zz: pos1[zz]); diag['rep_add1'] = True
    if reps and not any(z in PREV for z in pool):
        z = min(reps, key=lambda zz: pos2[zz]); pool.append(z)
        pool = sorted(pool, key=lambda zz: pos2[zz]); diag['rep_add2'] = True
    return cands, pool, diag

class LCG:
    def __init__(s, seed): s.x = seed & 0xFFFFFFFF
    def step(s): s.x = (1664525*s.x + 1013904223) & 0xFFFFFFFF; return s.x

def pools_v40(hist, debug=False):
    R = _ranks(hist[-100:]); rec, oB, merged = R['rec'], R['oB'], R['order']
    PREV = set(hist[-1][3] + [hist[-1][5]])
    champs = [rec[0][0], oB[0]]
    if champs[1] == champs[0]: champs.pop()
    warm = [z for z in oB[4:8] if z not in champs]
    C = []
    for z in champs + warm:
        if z not in C: C.append(z)
    P = C + [z for z in merged if z not in C]
    EMPTY = set()
    U = _pick(merged, PREV, EMPTY, EMPTY, 2, 4)
    cands, pool, diag = _alloc(U, PREV, P, merged)
    dbg = ({'rec': rec, 'oB': oB, 'merged': merged, 'champs': champs, 'warm': warm, 'C': C, 'P': P,
            'S': R['S'], 'rA': R['rA'], 'rB': R['rB'], 'zb': R['zb'], 'diag': diag} if debug else None)
    return pool, cands, PREV, U, dbg

def pools_v41(hist, debug=False):
    target = hist[-1][0] + 1
    PREV = set(hist[-1][3] + [hist[-1][5]]); BAN = PERIOD_BAN.get(target, set())
    r1 = _ranks(hist[-30:]); r2 = _ranks(hist[-60:])
    o30, o60 = r1['order'], r2['order']
    pos30 = {z: i for i, z in enumerate(o30)}; pos60 = {z: i for i, z in enumerate(o60)}
    comb = sorted(range(12), key=lambda z: (pos30[z] + pos60[z], z))
    U = _pick(comb, PREV, BAN, set(), 2, 4)
    cands, pool, diag = _alloc(U, PREV, o30, o60)
    dbg = ({'order30': o30, 'order60': o60, 'comb': comb, 'pos30': pos30, 'pos60': pos60,
            'S30': r1['S'], 'S60': r2['S'], 'BAN': BAN, 'target': target, 'diag': diag} if debug else None)
    return pool, cands, PREV, U, dbg

def pools_v42(hist, debug=False):
    target = hist[-1][0] + 1
    PREV = set(hist[-1][3] + [hist[-1][5]]); BAN = PERIOD_BAN.get(target, set())
    r1 = _ranks(hist[-30:]); r2 = _ranks(hist[-60:])
    o30, o60 = r1['order'], r2['order']
    pos30 = {z: i for i, z in enumerate(o30)}; pos60 = {z: i for i, z in enumerate(o60)}
    comb = sorted(range(12), key=lambda z: (pos30[z] + pos60[z], z))
    auto_U = _pick_hedge(comb, PREV, BAN, 2, 4)
    manual_U = MANUAL_UNIVERSES.get(target)
    manual_override = bool(manual_U and hist[-1][0] == target - 1 and not BAN)
    if manual_override:
        assert len(manual_U) == 6 and len(set(manual_U)) == 6, '人工Universe须6个different生肖'
        assert sum(1 for z in manual_U if z in PREV) == 2, '人工Universe须2重4新'
        U = list(manual_U)
    else:
        U = auto_U
    cands, pool, diag = _alloc(U, PREV, o30, o60)
    dbg = ({'order30': o30, 'order60': o60, 'comb': comb, 'pos30': pos30, 'pos60': pos60,
            'S30': r1['S'], 'S60': r2['S'], 'BAN': BAN, 'target': target, 'diag': diag,
            'auto_U': auto_U, 'manual_override': manual_override,
            'manual_U': list(manual_U) if manual_U else None} if debug else None)
    return pool, cands, PREV, U, dbg

def ent_v40(hist):
    pool, cands, PREV, U, _ = pools_v40(hist); g = LCG(hist[-1][0]+1)
    g.step(); top = cands[(g.x >> 16) % len(cands)]
    rest = list(pool); abcd = []
    for _ in range(4):
        g.step(); abcd.append(rest.pop((g.x >> 16) % len(rest)))
    a,b,c,d = abcd
    return {'top': top, 't2': [a,b], 't3': [a,c,d], 'pool': pool, 'cands': cands, 'PREV': PREV, 'U': U}

def ent_v41(hist):
    pool, cands, PREV, U, _ = pools_v41(hist); g = LCG(hist[-1][0]+1)
    c1 = [0]*12; c2 = [0]*12
    for _ in range(1000): g.step(); c1[cands[(g.x >> 16) % len(cands)]] += 1
    for _ in range(3000): g.step(); c2[pool[(g.x >> 16) % len(pool)]] += 1
    by = lambda arr,cnt: sorted(arr, key=lambda z: (-cnt[z], z))
    r = by(pool, c2)
    return {'top': by(cands,c1)[0], 't2': [r[0],r[1]], 't3': [r[0],r[2],r[3]],
            'pool': pool, 'cands': cands, 'PREV': PREV, 'U': U, 'c1': c1, 'c2': c2}

def ent_v42(hist):
    pool, cands, PREV, U, _ = pools_v42(hist); g = LCG(hist[-1][0]+1)
    c1 = [0]*12; c2 = [0]*12
    for _ in range(1000): g.step(); c1[cands[(g.x >> 16) % len(cands)]] += 1
    for _ in range(3000): g.step(); c2[pool[(g.x >> 16) % len(pool)]] += 1
    by = lambda arr,cnt: sorted(arr, key=lambda z: (-cnt[z], z))
    r = by(pool, c2)
    return {'top': by(cands,c1)[0], 't2': [r[0],r[1]], 't3': [r[0],r[2],r[3]],
            'pool': pool, 'cands': cands, 'PREV': PREV, 'U': U, 'c1': c1, 'c2': c2}

def nm(z): return ORDER[z]
def mark(z, PREV): return ORDER[z] + ('*' if z in PREV else '')
def nums(z): return ' '.join(f'{n:02d}' for n in Z2N[z])

if __name__ == '__main__':
    T = ALL[-1][0] + 1
    print(f'== 六肖先定·双池可重复原型(最终定版) @目标{T} (数据至{ALL[-1][0]}, * =重肖∈PREV) ==')
    last = ALL[-1]
    PREV0 = set(last[3] + [last[5]])
    print(f'上期{last[0]}: 平码 {[f"{n:02d}" for n in last[2]]} 生肖 {[nm(z) for z in last[3]]} + 特 {last[4]:02d}{nm(last[5])}')
    print(f'PREV({len(PREV0)}肖) = {[nm(z) for z in sorted(PREV0)]} | 新肖域 = {[nm(z) for z in range(12) if z not in PREV0]}')

    pool, cands, PREV, U, dbg = pools_v40(ALL, debug=True)
    e = ent_v40(ALL)
    print('\n--- v4.0 (100期窗) 逐步 ---')
    print('A榜rec序:', [(nm(z), round(v,3)) for z,v in dbg['rec']])
    print('B榜oB序:', [(nm(z), dbg['zb'][z]) for z in dbg['oB']])
    print('名次和merged(Universe序):', [(mark(z,PREV), dbg['S'][z]) for z in dbg['merged']])
    print(f"Universe U(2重4新, merged分层) = {[mark(z,PREV) for z in U]}")
    print(f"两冠 champs={[nm(z) for z in dbg['champs']]} 温号 warm={[nm(z) for z in dbg['warm']]} C={[mark(z,PREV) for z in dbg['C']]} 池1序P={[mark(z,PREV) for z in dbg['P']]}")
    dg = dbg['diag']
    print(f"分配: 初始池1(U在P前4)={[mark(z,PREV) for z in dg['init1']]} 初始池2(U在merged前6)={[mark(z,PREV) for z in dg['init2']]} "
          f"最小补位({dg['min_ext1']}/{dg['min_ext2']}) 全覆盖补={[(mark(z,PREV), w) for z,w in dg['coverage']]} 重肖补池=({dg['rep_add1']},{dg['rep_add2']})")
    print(f"池1({len(cands)}肖) = {[mark(z,PREV) for z in cands]} | 池2({len(pool)}肖) = {[mark(z,PREV) for z in pool]} | 重复肖(两池同肖)={[mark(z,PREV) for z in sorted(set(cands)&set(pool))]}")
    print(f"摇号(seed={T}, 1+4步): 最大可能={mark(e['top'],PREV)} 二中二={[mark(z,PREV) for z in e['t2']]} 三中三={[mark(z,PREV) for z in e['t3']]}")
    union = sorted(set(cands)|set(pool)); disp = sorted({e['top']}|set(e['t2'])|set(e['t3']))
    print(f"两池并集={[mark(z,PREV) for z in union]}({len(union)}个不同生肖) 号码{sum(len(Z2N[z]) for z in union)}个 | 展示去重={[mark(z,PREV) for z in disp]}({len(disp)}肖) 号码{sum(len(Z2N[z]) for z in disp)}个")
    for z in union: print(f'   {mark(z,PREV)}: {nums(z)}')

    pool1, cands1, PREV1, U1, dbg1 = pools_v41(ALL, debug=True)
    e1 = ent_v41(ALL)
    print('\n--- v4.1 (30/60期窗) 逐步 ---')
    print('order30:', [(mark(z,PREV1), dbg1['S30'][z]) for z in dbg1['order30']])
    print('order60:', [(mark(z,PREV1), dbg1['S60'][z]) for z in dbg1['order60']])
    print('组合序(pos30+pos60):', [(mark(z,PREV1), dbg1['pos30'][z]+dbg1['pos60'][z]) for z in dbg1['comb']])
    print(f"BAN({T}) = {[nm(z) for z in sorted(dbg1['BAN'])] if dbg1['BAN'] else '无'} | Universe U(2重4新, 组合序分层) = {[mark(z,PREV1) for z in U1]}")
    dg1 = dbg1['diag']
    print(f"分配: 初始池1(U在30序前4)={[mark(z,PREV1) for z in dg1['init1']]} 初始池2(U在60序前6)={[mark(z,PREV1) for z in dg1['init2']]} "
          f"最小补位({dg1['min_ext1']}/{dg1['min_ext2']}) 全覆盖补={[(mark(z,PREV1), w) for z,w in dg1['coverage']]} 重肖补池=({dg1['rep_add1']},{dg1['rep_add2']})")
    print(f"池1({len(cands1)}肖) = {[mark(z,PREV1) for z in cands1]} | 池2({len(pool1)}肖) = {[mark(z,PREV1) for z in pool1]} | 重复肖={[mark(z,PREV1) for z in sorted(set(cands1)&set(pool1))]}")
    print(f"摇号(4000步): 池1计数={ {nm(z): e1['c1'][z] for z in cands1} } 最大可能={mark(e1['top'],PREV1)}")
    print(f"              池2计数={ {nm(z): e1['c2'][z] for z in pool1} } 二中二={[mark(z,PREV1) for z in e1['t2']]} 三中三={[mark(z,PREV1) for z in e1['t3']]}")
    union1 = sorted(set(cands1)|set(pool1)); disp1 = sorted({e1['top']}|set(e1['t2'])|set(e1['t3']))
    print(f"两池并集={[mark(z,PREV1) for z in union1]}({len(union1)}个不同生肖) 号码{sum(len(Z2N[z]) for z in union1)}个 | 展示去重={[mark(z,PREV1) for z in disp1]}({len(disp1)}肖) 号码{sum(len(Z2N[z]) for z in disp1)}个")
    pool2, cands2, PREV2, U2, dbg2 = pools_v42(ALL, debug=True)
    e2 = ent_v42(ALL)
    u2_mode = f'{T}人工定案U + 30/60分池' if dbg2.get('manual_override') else '30/60期窗 + 分层尾部对冲'
    print(f'\n--- v4.2 ({u2_mode}) 逐步 ---')
    print('order30:', [(mark(z,PREV2), dbg2['S30'][z]) for z in dbg2['order30']])
    print('order60:', [(mark(z,PREV2), dbg2['S60'][z]) for z in dbg2['order60']])
    print('组合序(pos30+pos60):', [(mark(z,PREV2), dbg2['pos30'][z]+dbg2['pos60'][z]) for z in dbg2['comb']])
    u2_desc = '人工多维定案覆盖自动U' if dbg2.get('manual_override') else '每层最后一席尾部对冲'
    print(f"BAN({T}) = {[nm(z) for z in sorted(dbg2['BAN'])] if dbg2['BAN'] else '无'} | Universe U(2重4新, {u2_desc}) = {[mark(z,PREV2) for z in U2]}")
    if dbg2.get('manual_override'):
        print(f"自动v4.2 Universe(未采用, 仅留痕) = {[mark(z,PREV2) for z in dbg2['auto_U']]}")
    dg2 = dbg2['diag']
    print(f"分配: 初始池1(U在30序前4)={[mark(z,PREV2) for z in dg2['init1']]} 初始池2(U在60序前6)={[mark(z,PREV2) for z in dg2['init2']]} "
          f"最小补位({dg2['min_ext1']}/{dg2['min_ext2']}) 全覆盖补={[(mark(z,PREV2), w) for z,w in dg2['coverage']]} 重肖补池=({dg2['rep_add1']},{dg2['rep_add2']})")
    print(f"池1({len(cands2)}肖) = {[mark(z,PREV2) for z in cands2]} | 池2({len(pool2)}肖) = {[mark(z,PREV2) for z in pool2]} | 重复肖={[mark(z,PREV2) for z in sorted(set(cands2)&set(pool2))]}")
    print(f"摇号(4000步): 池1计数={ {nm(z): e2['c1'][z] for z in cands2} } 最大可能={mark(e2['top'],PREV2)}")
    print(f"              池2计数={ {nm(z): e2['c2'][z] for z in pool2} } 二中二={[mark(z,PREV2) for z in e2['t2']]} 三中三={[mark(z,PREV2) for z in e2['t3']]}")
    union2 = sorted(set(cands2)|set(pool2)); disp2 = sorted({e2['top']}|set(e2['t2'])|set(e2['t3']))
    print(f"两池并集={[mark(z,PREV2) for z in union2]}({len(union2)}个不同生肖) 号码{sum(len(Z2N[z]) for z in union2)}个 | 展示去重={[mark(z,PREV2) for z in disp2]}({len(disp2)}肖) 号码{sum(len(Z2N[z]) for z in disp2)}个")
    bothU = sorted(set(union)|set(union1)); bothD = sorted(set(disp)|set(disp1))
    print(f"v4.0/v4.1两线合并: 池并集={[nm(z) for z in bothU]}({len(bothU)}肖,{sum(len(Z2N[z]) for z in bothU)}号码) 展示并集={[nm(z) for z in bothD]}({len(bothD)}肖,{sum(len(Z2N[z]) for z in bothD)}号码)")

    p2i = {r[0]: i for i,r in enumerate(ALL)}
    targets = [t for t in range(2026148, T+1) if t-1 in p2i]
    print(f'\n== 结构审计: 目标 {targets[0]}..{targets[-1]} n={len(targets)} (只验结构不验命中) ==')
    for ver, fn, pfn in [('v4.0', ent_v40, pools_v40), ('v4.1', ent_v41, pools_v41), ('v4.2', ent_v42, pools_v42)]:
        viol = []; s1d=[]; s2d=[]; ovd=[]; r1d=[]; r2d=[]; drd=[]; dsd=[]
        u_repd = []; quota_bad = 0; stage = collections.Counter()
        for t in targets:
            hist = ALL[:p2i[t-1]+1]; assert hist[-1][0] == t-1
            ee = fn(hist); PV_ = ee['PREV']; UU = ee['U']; ca, po = ee['cands'], ee['pool']
            dispS = {ee['top']}|set(ee['t2'])|set(ee['t3'])
            ur = sum(1 for z in UU if z in PV_); r1 = sum(1 for z in ca if z in PV_); r2 = sum(1 for z in po if z in PV_)
            u_repd.append(ur); s1d.append(len(ca)); s2d.append(len(po)); ovd.append(len(set(ca)&set(po)))
            r1d.append(r1); r2d.append(r2); drd.append(len(dispS & PV_)); dsd.append(len(dispS))
            if ur != 2: quota_bad += 1
            _,_,_,_,dd = pfn(hist, debug=True); dgt = dd['diag']
            if dgt['min_ext1']: stage['min1'] += 1
            if dgt['min_ext2']: stage['min2'] += 1
            if dgt['coverage']: stage['cover'] += 1
            if dgt['rep_add1']: stage['rep1'] += 1
            if dgt['rep_add2']: stage['rep2'] += 1
            checks = [
                (len(UU) == 6 and len(set(UU)) == 6 and ur == 2, 'U=6distinct且2重'),
                (set(ca) <= set(UU) and set(po) <= set(UU) and (set(ca)|set(po)) == set(UU), '两池并集=U'),
                (len(ca) == len(set(ca)) and len(po) == len(set(po)), '池内distinct'),
                (2 <= len(ca) <= 6 and 4 <= len(po) <= 6, '池长池1>=2池2>=4且<=6'),
                (r1 >= 1 and r2 >= 1, '每池>=1重肖'),
                (ee['top'] in ca, 'top in池1'),
                (set(ee['t2']) <= set(po) and set(ee['t3']) <= set(po), 't2/t3 subset池2'),
                (len(set(ee['t2'])&set(ee['t3'])) == 1, 't2 cap t3=1'),
                (4 <= len(dispS) <= 5, '展示去重4-5'),
            ]
            for okc, lab in checks:
                if not okc: viol.append((t, lab))
        def dist(v): return dict(sorted(collections.Counter(v).items()))
        print(f"{ver}: U重肖{dist(u_repd)} 池1大小{dist(s1d)} 池2大小{dist(s2d)} 重复肖(交集){dist(ovd)} 池1重肖{dist(r1d)} 池2重肖{dist(r2d)} "
              f"展示去重{dist(dsd)} 展示重肖{dist(drd)} | mean池长={statistics.mean(s1d):.2f}/{statistics.mean(s2d):.2f} mean重复={statistics.mean(ovd):.2f} "
              f"U配额降级{quota_bad}期 违例{len(viol)} 分配阶段触发{dict(stage)}")
        if viol: print('  VIOLATIONS:', viol[:20])
    print('AUDIT_DONE')
    out = {'target': T,
           'v4.0': {'top': e['top'], 't2': e['t2'], 't3': e['t3'], 'cands': e['cands'], 'pool': e['pool'], 'U': e['U']},
           'v4.1': {'top': e1['top'], 't2': e1['t2'], 't3': e1['t3'], 'cands': e1['cands'], 'pool': e1['pool'], 'U': e1['U']},
           'v4.2': {'top': e2['top'], 't2': e2['t2'], 't3': e2['t3'], 'cands': e2['cands'], 'pool': e2['pool'], 'U': e2['U']}}
    print('SIX_JSON ' + json.dumps(out, ensure_ascii=False))
