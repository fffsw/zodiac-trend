# 生肖开奖走势 — GitHub Pages 部署包

本目录是可直接推送到 GitHub Pages 的完整静态站:

```
deploy/
├── index.html                      # 根路径跳转 → /zodiac_trend.html
├── zodiac_trend.html               # 走势图本体(单文件,离线亦可)
├── .nojekyll                       # 跳过 Jekyll 处理
├── deploy.sh                       # 一键:检查仓库→推送→启用 Pages(分支直出)
└── README.md
```

## 方式 A:一条命令(有 token 的机器上,包括我的沙箱)

```bash
GITHUB_TOKEN=ghp_xxxx REPO=你的用户名/zodiac-trend ./deploy.sh
```

稍等 30~60 秒访问 `https://你的用户名.github.io/zodiac-trend/`

> Token 建议用 **Fine-grained**:仅授权这个仓库、权限只要 **Contents: Read and write** + **Pages: Read and write**;用完即撤销。

## 方式 B:纯网页操作(不用脚本)

1. GitHub → New repository(公开)→ 名如 `zodiac-trend`;
2. 把本目录所有文件(含隐藏的 `.github/`、`.nojekyll`)上传到 `main`;
3. 仓库 Settings → Pages → Source 选 **Deploy from a branch** → `main` `/(root)`;
4. 保存后等 30~60 秒即可访问。

## 方式 C:把 token 给我,我在沙箱里执行

把 Fine-grained token 发我,我跑完立即从 git 配置移除凭据并提示你撤销。
**风险自担:任何人拿到该 token 都能操作被授权的仓库,建议用完马上撤销。**

## 后续更新图表

改完数据重新生成后(仓库根目录已有 `zodiac_trend.html`),再次执行:

```bash
GITHUB_TOKEN=... REPO=... ./deploy.sh
```

或直接 git push,页面立即更新(分支直出,无构建)。

## 本地/局域网预览(非 Pages)

```bash
python3 -m http.server 8000 --bind 0.0.0.0 --directory .
```
