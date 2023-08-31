# 實習紀錄

## ChAoS-UnItY

- [GitHub](https://github.com/ChAoSUnItY)
- [OSCVPass 實習後記](https://hackmd.io/@chaos-unity/B1lVrbia2)
- 實習時間：2023/07 ~ 2023/08

## 關於我

我是 [ChAoS](https://github.com/ChAoSUnItY) ，於 2023 的暑期中在 OCF 實習，很榮幸地能夠被分配到 OSCVPass 的專案整治，也很感謝 [Toomore](https://github.com/toomore) 在實習期間指導。

## 目前進度

目前 OSCVPass 移植到 Pretalx 。已正式上線於[該網站](https://apply-for-oscvpass.ocf.tw/)。

### [GitHub](https://github.com/ocftw/OSCVPass)

GitHub 的部分已經大致上整治完成：

且新增了 project 和 tracking issue 的機制： project 用於追蹤各 issue / pull request 的進度及影響範圍，讓團隊成員及社群可以更方便的檢閱感興趣的 issue / pull request 的進度 ； tracking issue 則用於整合各 issue 到一個大項目 (issue) 中，方便檢閱該大項目中的進度是否有其他問題。

每個分支都有不同的作用：
- main 主要用於主持 OSCVPass 的靜態網頁並固定同步至 GitHub Pages ， 包括[介紹頁](https://oscvpass.ocf.tw/)以及[文檔](https://oscvpass.ocf.tw/docs/)。
- docs 要用來擺放暫存的靜態網頁和文檔，完善後透過 pull request 的機制合併至 main 分支中。
（需要注意的是如果其他成員有暫存的進度在 docs 分支上，請另外開一個分支防止進度衝突，並在 pull request 被合併後自行刪除，[當然我會更建議這樣做](#Pull-request)。）
- pretalx 用於存放pretalx docker設定檔。

關於 issue 和 pull requests 工作流程的機制，詳見[關於工作流程](#關於工作流程)。

### [Pretalx](https://apply-for-oscvpass.ocf.tw/)

已完成問卷和email寄送的部分，詳細的 remote control 可以參考[這裡](https://github.com/ocftw/OSCVPass/issues/19)。

- [x] 問卷
- [ ] Email寄送
    - [x] 手動
    - [ ] 自動 (參考 [Issue 9](https://github.com/ocftw/OSCVPass/issues/31))

## 給後續完善 OSCVPass 的成員

截至 8/29/23 ， Pretalx 尚未發布 2.3.2 後的正式版本，目前該版本存在以下幾個問題：
- 無法將 Additional Speaker 選項隱藏
Additional Speaker 在 OSCVPass 的申請表單是無效的資訊/欄位。
- Api 尚未研究完全
串接的部分目前是規劃使用 COSCUP SecretaryKit 裡面的 python 腳本，但由於 COSCUP 端的說明文檔尚未完善，且實習也接近尾聲，故目前暫緩轉移腳本。
- 自動化流程缺失
目前尚未實作自動化流程，無法自動定期將年會資訊寄送給合格的 OSCVPass 會員。
- 權限不明
根據 Pretalx 官方的文檔，雖然可以創建 superuser 作為初始管理員，但針對新創用戶的權限提拔目前尚未找到正確的流程，可能需要詢問官方或是對 COSCUP pretalx 有經驗之人員。

## 關於工作流程

> 若您是社群貢獻者，可以直接創建 issue / pull request ，後續團隊會自動幫你處理 issue / pull request 的分類以及 issue tracking 和 pull request review。

### Issue

Issue 創建後，若 issue 具有一定大小，需要後續追蹤，請在 OSCVPass 的 project 中的 tracking 類別裡面找最相似的類別，於該 tracking issue 中編輯新增你的 issue ；也請順道將創建的 issue 分類在 project 的對應狀態分類中。

若沒有編輯 tracking issue 的權限的話，請通知 [Toomore](https://github.com/toomore) 協助處理權限。

### Pull request

> 至後續完善 OSCVPass 的團隊成員，我建議本地端的進度放在自己的 fork 上，防止進度衝突和保持 OSCVPass 專案庫的分支整潔。

Pull requests 創建後，請待其他 OSCVPass 的成員分配分類標籤，並請等待至少 1 位成員 review 變更後再合併進去。

若該 pull request 是為了關閉 issue 的話，請在說明主旨中寫出 *Fixes #[...]* ，方便後續合併之後能夠自動關閉 issue ，詳細用語(法)與關閉機制請參考[官方說明文檔](https://docs.github.com/en/issues/tracking-your-work-with-issues/linking-a-pull-request-to-an-issue#linking-a-pull-request-to-an-issue-using-a-keyword)。

---
