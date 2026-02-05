# CLAUDE.md

此檔案提供 Claude Code (claude.ai/code) 在此程式碼庫中工作時的指引。

## 專案概覽

此目錄包含 OSCVPass（開源貢獻者快速通關專案）的 MkDocs 文件網站，由財團法人開放文化基金會（OCF）台灣主辦。網站包含文件、已核准專案列表和部落格文章—全部使用正體中文（台灣）。

## 常用指令

所有指令都應該在此目錄（`src/site_docs/`）中執行。

### MkDocs 網站

```bash
# 本地端即時預覽（預設：http://127.0.0.1:8000）
uv run mkdocs serve

# 建置文件網站
uv run mkdocs build

# 建置到指定目錄（例如：GitHub Pages）
uv run mkdocs build -d ../../docs
```

### 更新已核准專案的詳細資料

`update_approved_from_vcs.py` 腳本會從 GitHub/GitLab 抓取 `zh-tw/approved/*.md` 中專案的詳細資料：

```bash
# 預覽模式：顯示變更但不寫入檔案
uv run python scripts/update_approved_from_vcs.py

# 套用變更到 approved/*.md 檔案
uv run python scripts/update_approved_from_vcs.py --write

# 僅排序條目（不呼叫 API，使用現有的 :date:/:star: 標記）
uv run python scripts/update_approved_from_vcs.py --sort-only --write

# 只更新特定分類檔案
uv run python scripts/update_approved_from_vcs.py --only-files linux-kernel.md --write

# 關閉排序（保留原本順序）
uv run python scripts/update_approved_from_vcs.py --no-sort --write

# 啟用詳細記錄
uv run python scripts/update_approved_from_vcs.py --verbose --write
```

**重要**：大量更新時，建議設定 `GITHUB_TOKEN` 和選擇性設定 `GITLAB_TOKEN` 以避免觸及 API 速率限制：

```bash
export GITHUB_TOKEN="your_github_token"
export GITLAB_TOKEN="your_gitlab_token"  # 選填
uv run python scripts/update_approved_from_vcs.py --write
```

## 架構說明

### 內容結構

- **`zh-tw/`** - 所有正體中文內容（台灣用語）
  - **`approved/*.md`** - 已核准專案列表，依類型分類：
    - `open-source.md` - 開源專案
    - `community.md` - 社群貢獻
    - `program.md` - 程式語言貢獻
    - `security-web3.md` - 資安與 Web3
    - `language.md` - 程式語言開發
    - `l10n.md` - 在地化/翻譯工作
    - `image-sound.md` - 媒體貢獻
    - `app.md` - 應用程式開發
    - `chatbot-api.md` - 聊天機器人與 API 開發
    - `linux-kernel.md` - Linux 核心貢獻
    - `pull-request.md` - 一般 PR 貢獻
  - **`blog/posts/`** - 部落格文章
  - **`overrides/`** - 自訂 MkDocs 佈景主題覆寫
  - **`assets/`** - 圖片和靜態資源

### 已核准專案條目格式

每個已核准專案條目遵循以下 Markdown 格式：

```markdown
- [label](url), contributor_name, _description_ (stats)
```

其中統計資訊包含：
- `:star:` - GitHub/GitLab 星星數
- `:octicons-repo-forked-24:` - Fork 數
- `:date:` - 最後更新日期（365 天內會加粗：`**2026-01-24**`）
- `:material-license:` - 授權類型

帳號頁面則使用：
- `:material-account-group:` - 追蹤者數
- `:octicons-repo-24:` - 儲存庫數量

### 詳細資料更新腳本行為

`scripts/update_approved_from_vcs.py` 執行以下操作：

1. **解析**：從 approved/*.md 中提取 `- [label](url), contributor, _desc_` 條目
2. **URL 推論**：從 URL 推論出正規的 GitHub/GitLab 儲存庫（即使 URL 指向 PR/issue/commit），但**絕不會改變原本的 URL**
3. **抓取詳細資料**：呼叫 GitHub/GitLab API 取得儲存庫詳細資料
4. **描述更新**：用 API 傳回的儲存庫描述覆寫斜體的 `_description_`
   - 若 API 傳回空描述，會保留原本的 `_desc_` 文字
5. **統計後綴**：附加統計資訊標記（stars、forks、date、license）
6. **排序**：依日期排序（最新 → 最舊），相同日期則依星星數（最多 → 最少）
   - 有 `:date:` 標記的條目排在最前面
   - 相同日期依 `:star:` 數量排序
   - 沒有日期的條目保留在最下方，維持原本順序
7. **日期加粗**：365 天內的日期格式化為 `**YYYY-MM-DD**`

**快取系統**：
- 預設快取：`.cache/vcs_meta_cache.json`
- 預設 TTL：24 小時
- 預設腳本會讀取快取但不寫入（使用 `--write-cache` 可更新快取）

### MkDocs 設定

- **框架**：MkDocs 搭配 Material 佈景主題
- **語言**：`zh-TW`（正體中文 - 台灣）
- **外掛套件**：
  - `search` - 全文搜尋（中文 + 英文）
  - `social` - 社群卡片產生
  - `git-revision-date-localized` - 顯示檔案修改日期
  - `git-authors` - 顯示貢獻者
  - `blog` - 部落格功能與 RSS
  - `privacy` - 隱私友善的外部連結
- **主題功能**：導覽分頁、搜尋建議、編輯連結、深色模式

## Python 環境

本專案使用 `uv` 進行 Python 套件管理。

- **Python 版本**：3.13+
- **相依套件**：定義於 `pyproject.toml`
- **鎖定檔**：`uv.lock`
- **虛擬環境**：`.venv/`（由 uv 自動建立）

## 翻譯慣例

- 使用台灣用語（台灣 而非 臺灣）
- 所有文件內容皆使用正體中文
- 編輯 URI 指向 `main` 分支：`edit/main/src/site_docs/zh-tw/`
