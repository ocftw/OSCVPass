# 規劃藍圖

<!-- toc -->

## 計畫緣起

OSCVPass 原來自 [COSCUP 開源貢獻方案](https://blog.coscup.org/2020/07/oscvpass.html)，但因為 COSCUP 不再需要報名入場，因此將此方案貢獻給開放文化基金會 OCF 繼續規劃與執行。

不論是在 COSCUP 期間所執行的計畫或是移交給 OCF 的規劃，都是希望可以多多鼓勵大家參與開源文化的貢獻，不論是在程式碼的貢獻或是以開源精神、開放文化的方式產出的作品都會是 OSCVPass 所希望能回饋的貢獻者！

## 流程說明

計畫流程大致上整理如下表，依運作流程項目解說，目前計畫面臨的問題與希望可以改善的下一步。

[![OSCVPass process flow](https://oscvpass.ocf.tw/img/oscvpass.svg)](https://oscvpass.ocf.tw/img/oscvpass.svg)

- ➊ 申請表單：目前是使用 Google Forms 作為申請表使用，但申請項目越來越多元，無法涵蓋表單的欄位定義與申請類型的情況。
- ➋ 審核委員：目前審核委員由社群夥伴參與，一個月一名委員負責審核，但會因為當月其他因素無法在原定時間內審核完畢。
- ➌➍ 審核方式（通過、補件、不通過）：目前審核的方式採取比較寬送的標準，無標準量化的機制。
- ➎ 寄送審核結果通知信：通知信透過 AWS SES 大量寄送樣板信件。
- ➏ 收錄開源貢獻者資料庫：目前是使用 Google Forms 表單標記已通過。
- ➐ 合作研討會：每年參與的研討會。
- ➑ 專案貢獻頁面：目前是使用靜態網頁呈現，問題在於整理與分類方式為人工手動方式進行。
- ➒ 研討會宣傳：在各研討會宣傳申請計畫。

## 基礎工程

由於專案申請流程目前存在大量的手工操作程序，而累積的申請案件越來越多、也漸漸影響到每一次通知前的準備。因此在 2023 下半年度開始計畫重構目前計畫的基礎建設，優化其流程！

近期進度：

- 2023/08/01 目前 ➊ 已開始測試使用 Pretalx 來解決 ➋➌➍ 的流程優化問題。

### 工程進度

秉持著開放的精神，我們將目前重構的工程進度都回報在 [Project](https://github.com/orgs/ocftw/projects/3) 上，歡迎持續追蹤並給予我們建議，感謝！

> **Note:** 可參考[如何參與](community-contribute.md)加入我們一起改善！
