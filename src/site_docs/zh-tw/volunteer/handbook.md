---
title: 志工手冊
subtitle: 協作流程、工具使用與溝通規範
description: "OSCVPass 志工手冊，包含協作流程、工具使用說明與溝通規範，讓你快速上手並有效參與專案。"
icon: material/book-open-variant
---

# :material-book-open-variant: 志工手冊

歡迎加入 OSCVPass 志工團隊！這份手冊將協助你了解如何與團隊協作、使用各種工具，以及有效溝通。

## 協作原則

OSCVPass 是一個**遠端、非全職、非即時待命**的志工專案，我們重視：

- **自主與彈性**：你可以選擇適合自己的時間與任務
- **透明與開放**：所有討論與決策都公開在 GitHub 上
- **互助與尊重**：遇到問題隨時提問，我們一起成長
- **不燃燒志工**：我們希望你能長期參與，而不是短期燃燒

!!! tip "記住"
    如果你發現自己無法負荷，或需要暫停一陣子，請隨時告訴我們，沒有人會責怪你！

## 使用工具與平台

### GitHub

GitHub 是我們的主要協作平台，所有工作都在這裡進行。

#### GitHub Issues

**用途**：追蹤任務、回報問題、提出建議

- **瀏覽 Issues**：前往 [OSCVPass Issues](https://github.com/ocftw/OSCVPass/issues){target="_blank"}
- **認領任務**：在 Issue 中留言「我想認領這個任務」或 `/assign @yourself`
- **提問**：遇到問題直接在 Issue 中留言詢問
- **建立新 Issue**：發現新問題或有新想法時，可以自行建立

**尋找適合的任務**：

- `good first issue`：適合新手的簡單任務
- `help wanted`：需要協助的任務
- 依標籤篩選：`documentation`、`design`、`content`、`community` 等

#### GitHub Pull Requests (PR)

**用途**：提交你的工作成果

**基本流程**：

1. Fork 專案到你的帳號（建議）或在專案中建立新分支
2. 在本地端完成修改
3. 提交 Pull Request
4. 等待至少 1 位成員 review
5. 根據回饋修改（如有需要）
6. 合併進主分支

**PR 標題格式**：

```
[類別] 簡短描述

範例：
[Docs] 更新志工手冊內容
[Design] 新增申請流程圖
[Fix] 修正錯字與連結
```

**關閉 Issue**：若 PR 是為了解決某個 Issue，請在描述中寫：

```
Fixes #123
Closes #456
```

#### GitHub Discussions

**用途**：非正式討論、腦力激盪、自我介紹

- **自我介紹**：加入後請在 [Discussions](https://github.com/ocftw/OSCVPass/discussions){target="_blank"} 發文介紹自己
- **提案討論**：想法還不成熟時，可以先在這裡討論
- **經驗分享**：分享你在專案中的學習與心得

#### GitHub Projects

**用途**：追蹤專案整體進度

- 前往 [OSCVPass Projects](https://github.com/orgs/ocftw/projects/3){target="_blank"}
- 可以看到所有任務的狀態：待辦、進行中、已完成
- 了解目前專案的重點工作

### Slack（如有使用）

**用途**：即時溝通、快速提問

- 非即時待命，不需要立即回覆
- 適合簡短的詢問與協調
- 重要決策仍需記錄在 GitHub 上

### Email

**用途**：正式通知、重要公告

- 專案聯絡信箱：<oscvpass@ocf.tw>
- 重要事項會透過 email 通知

## 溝通規範

### 何時使用哪個工具？

| 情境 | 使用工具 | 範例 |
|------|---------|------|
| 認領任務、回報進度 | GitHub Issues | 「我想認領 #123」 |
| 提交工作成果 | GitHub Pull Requests | 提交文件修改 |
| 想法討論、腦力激盪 | GitHub Discussions | 「我們是否該新增 XX 功能？」 |
| 快速詢問、協調時間 | Slack（如有） | 「明天會議幾點開始？」 |
| 正式申請、重要通知 | Email | 請假通知、退出專案 |

### 回覆時效期待

我們是**非即時待命**的志工團隊：

- **一般問題**：1-3 天內回覆
- **緊急問題**：24 小時內回覆（請在訊息中標註「緊急」）
- **會議邀請**：至少提前 3 天通知

!!! note "提醒"
    如果你發現某個問題超過 3 天沒人回應，請再次 tag 相關人員或在 Slack 提醒。

### 有效提問技巧

好的提問可以幫助你更快得到解答：

1. **說明背景**：你在做什麼任務？
2. **描述問題**：遇到什麼問題？預期結果是什麼？
3. **附上資訊**：錯誤訊息、截圖、相關連結
4. **已嘗試的方法**：你已經試過哪些解決方式？

範例：

```markdown
我在更新 approved/open-source.md 時（Issue #123），
執行 `uv run python scripts/update_approved_from_vcs.py --write` 後，
出現以下錯誤訊息：

[錯誤訊息或截圖]

我已經試過：
- 確認 Python 版本是 3.13
- 重新安裝相依套件

請問該如何解決？
```

## 會議與同步

### 定期會議（待確認）

- **頻率**：（待團隊決定，例如：每月一次或每季一次）
- **形式**：線上會議（Google Meet / Jitsi）或非同步會議（文字討論）
- **時間**：會提前至少 3 天通知
- **參與方式**：非強制參加，但歡迎出席

### 非同步協作

大部分工作都可以非同步進行：

- 在 GitHub 上留言討論
- 透過 Pull Request review 提供回饋
- 在自己方便的時間完成任務

## 任務執行流程

### 1. 選擇任務

- 瀏覽 [Issues](https://github.com/ocftw/OSCVPass/issues){target="_blank"} 或 [Projects](https://github.com/orgs/ocftw/projects/3){target="_blank"}
- 選擇標記為 `good first issue` 或符合你專業的任務
- 評估時間：確認你在未來 1-2 週有時間完成

### 2. 認領任務

- 在 Issue 中留言：「我想認領這個任務」
- 等待確認（通常會立即確認）
- Issue 會被標記為 `in progress`

### 3. 執行任務

- 如有疑問，隨時在 Issue 中提問
- 定期更新進度（例如：「已完成 50%」）
- 如需延期或無法完成，請提早告知

### 4. 提交成果

- 透過 Pull Request 提交
- 在 PR 描述中說明你做了什麼
- 連結相關 Issue（`Fixes #123`）

### 5. Review 與修改

- 等待其他成員 review
- 根據回饋進行修改
- Review 通過後會被合併

### 6. 完成與慶祝

- Issue 自動關閉
- 感謝你的貢獻！🎉

## 如果遇到困難

### 技術問題

- **GitHub 操作**：參考 [GitHub 官方文件](https://docs.github.com/zh){target="_blank"} 或在 Discussions 提問
- **MkDocs 相關**：查看 [MkDocs 文件](https://www.mkdocs.org/){target="_blank"} 或詢問其他志工
- **Python 腳本**：在相關 Issue 中提問，或查看 [資源清單](resources.md)

### 時間管理

- **太忙碌**：可以暫時不認領新任務
- **需要暫停**：在 Discussions 或 email 告知，隨時歡迎回來
- **任務延期**：在 Issue 中說明，沒有人會責怪你

### 人際溝通

- **意見不同**：在 GitHub 上理性討論，尊重不同觀點
- **感到孤單**：在 Discussions 找其他志工聊天
- **需要協助**：聯繫專案負責人或其他資深志工

## 暫停與離開

### 暫時休息

如果你需要暫停一陣子：

1. 在 Discussions 或 email 告知大家
2. 將進行中的任務交接或標記為 `help wanted`
3. 隨時歡迎你回來

### 正式離開

如果你決定離開專案：

1. 發送 email 到 <oscvpass@ocf.tw> 告知
2. 完成手上任務或進行交接
3. 分享你的經驗與建議（選填）

!!! success "感謝你的付出"
    無論你參與多久，都已經為台灣開源生態做出貢獻。我們會記得你的努力！

## 進階參與

### 成為 Reviewer

當你熟悉專案後，可以：

- Review 其他人的 Pull Requests
- 協助回答新手問題
- 參與專案決策討論

### 跨角色合作

- 不同專業背景的志工可以一起合作
- 例如：設計 + 文件志工合作製作懶人包
- 在 Discussions 提出合作想法

### 提出改進建議

- 發現流程可以優化？建立 Issue 提出
- 有新功能想法？在 Discussions 討論
- 想改進志工體驗？直接修改這份手冊並提交 PR

## 常見問題 FAQ

### 我不會寫程式，可以參與嗎？

可以！OSCVPass 有很多不需要寫程式的任務，例如：文件撰寫、設計、內容企劃、社群經營等。

### 我每週只有 1 小時，可以參與嗎？

可以！選擇符合你時間的小任務即可。

### 我可以同時認領多個任務嗎？

建議先專注完成一個任務，再認領下一個，避免分散精力。

### 我做錯了怎麼辦？

沒關係！GitHub 有版本控制，所有修改都可以還原。放心嘗試，從錯誤中學習。

### 我可以邀請朋友一起參與嗎？

當然歡迎！請他們參考[志工招募頁面](index.md)，寄信到 <oscvpass@ocf.tw> 申請。

---

**有任何問題？**

- 查看[資源清單](resources.md)
- 在 [GitHub Discussions](https://github.com/ocftw/OSCVPass/discussions){target="_blank"} 提問
- 寄信到 <oscvpass@ocf.tw>
