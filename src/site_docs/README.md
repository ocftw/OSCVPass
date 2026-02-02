# OSCVPass 開源貢獻者申請方案

- [ ] 調整新的專案頁面，1.0 版本
- [ ] 新增 2.0 參與方案

## 自動更新 `approved/` 專案資訊（GitHub / GitLab）

`zh-tw/approved/*.md` 內的條目可以用腳本自動抓 GitHub / GitLab 上的專案資訊後回寫，降低人工維護成本。

- **會做的事**
  - 解析 `- [label](url), ... , _desc_` 類型的條目
  - 從 GitHub/GitLab URL 推導出對應 repo/project（即使 URL 是 PR/issue/commit 也會推導），但 **不會改原本 URL**
  - 將 `_desc_` **覆蓋**為 GitHub/GitLab 的專案 description，並在後面加上 stats（`:star:` stars / `:octicons-repo-forked-24:` forks / `:date:` updated / `:material-license:` license；帳號頁面則會用 `:material-account-group:` followers / `:octicons-repo-24:` repos）
  - 若 API 沒有 description（空值），會保留原本 `_desc_`，避免把描述洗成空白
  - 會對每個分類頁的清單做排序：**有 `:date:` 的排在前面，依日期新→舊；同一天則依 `:star:` 數字多→少**

### 執行方式

在 repo 根目錄：

```bash
cd src/site_docs

# 先看會改什麼（dry-run，不寫檔）
uv run python scripts/update_approved_from_vcs.py

# 套用變更（寫回 zh-tw/approved/*.md）
uv run python scripts/update_approved_from_vcs.py --write

# 只排序（不打 API、不更新描述/統計；用現有的 :date:/:star: 來排）
uv run python scripts/update_approved_from_vcs.py --sort-only --write

# 只更新單一分類頁（例如 linux-kernel.md）
uv run python scripts/update_approved_from_vcs.py --only-files linux-kernel.md --write

# 關閉排序（保留原本順序）
uv run python scripts/update_approved_from_vcs.py --no-sort --write
```

### API Token（建議）

大量專案更新時，建議提供 token 以降低 rate limit 影響：

```bash
export GITHUB_TOKEN="..."
export GITLAB_TOKEN="..."  # 可選
```

### 快取（可選）

腳本預設只會讀取快取（若存在），不會寫入快取檔；需要時可加上：

```bash
uv run python scripts/update_approved_from_vcs.py --write-cache
```


