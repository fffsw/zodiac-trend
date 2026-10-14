#!/usr/bin/env bash
# 一键部署到 GitHub Pages(分支直出模式,无需 Actions/workflow scope)
# 用法: GITHUB_TOKEN=ghp_xxxx REPO=用户名/仓库名 ./deploy.sh
set -euo pipefail
TOKEN="${GITHUB_TOKEN:?请设置 GITHUB_TOKEN}"
REPO="${REPO:?请设置 REPO=用户名/仓库名}"
BRANCH="${BRANCH:-main}"
API=https://api.github.com
AUTH=(-H "Authorization: Bearer ${TOKEN}" -H "Accept: application/vnd.github+json")

echo "==> 1/3 检查仓库 $REPO"
curl -sf "${AUTH[@]}" "$API/repos/$REPO" >/dev/null && echo "仓库存在" || {
  echo "仓库不存在,尝试创建(需要 Administration 权限)…"
  curl -sf -X POST "${AUTH[@]}" "$API/user/repos" \
    -d "{\"name\":\"${REPO##*/}\",\"public\":true,\"auto_init\":false}" >/dev/null && echo "已创建" || {
      echo "ERROR: 仓库不存在且无权创建,请到 github.com/new 手动创建后重试"; exit 1; }
}

echo "==> 2/3 推送代码到 $BRANCH"
cd "$(dirname "$0")"
rm -rf .git
git init -q -b "$BRANCH"
git add -A
git -c user.name="${GIT_USER:-zodiac-trend-bot}" \
    -c user.email="${GIT_EMAIL:-zodiac-trend-bot@users.noreply.github.com}" \
    commit -qm "update $(date +%F)" || true
git remote remove origin 2>/dev/null || true
git remote add origin "https://x-access-token:${TOKEN}@github.com/${REPO}.git"
git push -f origin "$BRANCH"
git remote remove origin   # 凭据立即清除
echo "推送完成,git 配置中已无令牌"

echo "==> 3/3 启用 Pages(分支模式: $BRANCH 根目录)"
HTTP=$(curl -s -o /tmp/_pages.json -w '%{http_code}' -X POST "${AUTH[@]}" \
  "$API/repos/$REPO/pages" -d "{\"source\":{\"branch\":\"$BRANCH\",\"path\":\"/\"}}" || true)
if [ "$HTTP" = "409" ]; then   # 已存在 → 更新配置
  HTTP=$(curl -s -o /tmp/_pages.json -w '%{http_code}' -X PUT "${AUTH[@]}" \
    "$API/repos/$REPO/pages" -d "{\"source\":{\"branch\":\"$BRANCH\",\"path\":\"/\"}}" || true)
fi
case "$HTTP" in
  200|201) echo "Pages 已启用 ($BRANCH /)";;
  *) echo "Pages 配置返回 HTTP $HTTP: $(cat /tmp/_pages.json 2>/dev/null)"
     echo "→ 兜底: 仓库 Settings → Pages → Source 选 'Deploy from a branch' → $BRANCH /(root)";;
esac

OWNER="${REPO%%/*}"; NAME="${REPO##*/}"
echo "================================================"
echo "  完成。稍等 30~60 秒访问:"
echo "  https://${OWNER}.github.io/${NAME}/"
echo "================================================"
