---
title: 如何挑選開源授權條款
subtitle: 瞭解七種常見的開源授權條款與其限制、相容性、合規
icon: material/license
status: new
---

# 如何挑選開源授權條款

!!! question ""

    :material-account-question: 什麼是符合 OSI、FSF 認可的開源條款？

在 [OSI](https://opensource.org/license){target="_blank"} 與 [FSF](https://www.fsf.org/licensing/){target="_blank"} 所認可的開源授權條款數量相當多，對於新手來說短時間無法選擇該採用哪一種授權條款，這裡整理了幾個常見的開源授權條款，可以針對專案類型、希望使用你的開源專案後再次開源的程度來介紹。

## 什麼是 Copyleft 反著作權

**Copyleft（反著作權）**是一種授權機制，允許他人自由使用、修改和分發作品，但要求所有衍生作品同樣適用相同的開放條款。通過這種方式，Copyleft 保證了即使經過修改和再發行，作品及其衍生作品都保持開放和自由。

將較於 **Copyright（著作權）**是法律賦予創作者的一種權利，保護其作品不被未經許可的使用、複製或散播。著作權自作品創作完成之時起即自動產生，通常不需要註冊。而 Copyleft 促進自由軟體與內容的共享，以及確保開放資源在未來依然保持開放性質。被授權者必須繼續遵循 Copyleft 協議的要求，這通常意味着任何基於原作品的改編版本也必須在相同的自由條款下分發。

!!! info ""

    :material-account-alert: 有時你會聽到「著左權」的名詞，其中文翻譯與著作權 Copyright、Copyleft 的右、左相對的翻譯方式。

| 比較 | Copyleft（反著作權）                                                                                       | Copyright（著作權）                                                                                                    |
| ---- | ---------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| 定義 | 一種授權機制，允許他人自由使用、修改和分發作品，其所有衍生作品同樣適用相同的開放條款。                     | 著作權是法律賦予的權利，保護作品不被未經許可的使用、複製或散播。著作權自作品創作完成之時起即自動產生，通常不需要註冊。 |
| 目標 | 促進自由軟體與內容的共享，確保開放資源在未來依然保持開放。                                                 | 旨在保護創作者的原創作品，並賦予他們專有控制權。                                                                       |
| 限制 | 被授權者必須繼續遵循 Copyleft 協議的要求，這通常意味着任何基於原作品的改編版也必須在相同的自由條款下分發。 | 持有著作權的人可以限制他人對該作品的使用。未經許可使用的行為可能構成侵權。                                             |

## 什麼是開源？

請先參考 OSI 的「[開源定義（The Open Source Definition）](./open-source-definition.md){target="_blank"}」的定義，在「開源定義」的前三項是開源的主要核心：**開放原始碼、自由散佈、衍生著作**。

### 開放原始碼（Open Source）

<figure markdown="span">
  ![圖片出至「開放源碼授權概觀（上）」](https://yurenju.blog/posts/2018-07-03_%E9%96%8B%E6%94%BE%E6%BA%90%E7%A2%BC%E6%8E%88%E6%AC%8A%E6%A6%82%E8%A7%80%E4%B8%8A/images/1.png){width="80%"}
</figure>

!!! quote ""

    圖片出自「[開放源碼授權概觀（上）](https://yurenju.blog/zh/posts/2018-07-03_%E9%96%8B%E6%94%BE%E6%BA%90%E7%A2%BC%E6%8E%88%E6%AC%8A%E6%A6%82%E8%A7%80%E4%B8%8A){target="_blank"}」，圖片為 Firefox Logo 與一張用程式碼拼成的文字圖像，代表建構 Firefox 是看得到程式碼的專案。

軟體的原始碼必須可被取得，且是開發者「最適合修改」的形式。不能只提供難以閱讀的機器產生碼，也不能故意混淆原始碼。

* 必須提供原始碼，或提供清楚且不設門檻的取得方式（例如公開下載連結）。
* 允許任何人依此原始碼自行建置（compile、build）軟體。
* 原始碼不得刻意混淆，不能只給前處理器或轉換器輸出的中介形式。

開放原始碼不等於「免費」。你可以為載體、通路或服務收費，但不能以授權費作為門檻阻擋取得原始碼。通常會在 GitHub 上公開程式碼與 LICENSE，發佈二進位檔時同時提供對應版本的原始碼或取得方式。

### 自由散佈（Free Redistribution）

<figure markdown="span">
  ![圖片出至「開放源碼授權概觀（上）」](https://yurenju.blog/posts/2018-07-03_%E9%96%8B%E6%94%BE%E6%BA%90%E7%A2%BC%E6%8E%88%E6%AC%8A%E6%A6%82%E8%A7%80%E4%B8%8A/images/2.png){width="80%"}
</figure>

!!! quote ""

    圖片出自「[開放源碼授權概觀（上）](https://yurenju.blog/zh/posts/2018-07-03_%E9%96%8B%E6%94%BE%E6%BA%90%E7%A2%BC%E6%8E%88%E6%AC%8A%E6%A6%82%E8%A7%80%E4%B8%8A){target="_blank"}」，圖片由左至右解釋，Firefox 原始碼透過 git 為作版本控制，再透過支援 git 的 Github、Gitlab 給予使用者拉取（Pull）原始碼修改。不只一個使用者可以透過 git 取得，任何人都可以在公開的網路上找到 Firefox 的原始碼。

授權不得限制任何人重新散佈軟體（包含原版或與其他軟體打包），也不得要求額外的授權費或權利金。你可以賣光碟、放官網下載、跟其他程式一起打包販售或提供。

* 允許轉售或免費分享，不需事先逐案徵得作者同意。
* 不得強制收取版稅；可收取媒體、通路與服務費（例如下載流量、技術支援）。

「自由」指的是使用與再散佈的自由度，不是指價格一定為零。例如：Linux 發行版收費販售實體安裝與企業售後技術支援，仍符合自由散佈。

### 衍生著作（Derived Works）

<figure markdown="span">
  ![圖片出至「開放源碼授權概觀（上）」](https://yurenju.blog/posts/2018-07-03_%E9%96%8B%E6%94%BE%E6%BA%90%E7%A2%BC%E6%8E%88%E6%AC%8A%E6%A6%82%E8%A7%80%E4%B8%8A/images/3.png){width="80%"}
</figure>

!!! quote ""

    圖片出自「[開放源碼授權概觀（上）](https://yurenju.blog/zh/posts/2018-07-03_%E9%96%8B%E6%94%BE%E6%BA%90%E7%A2%BC%E6%8E%88%E6%AC%8A%E6%A6%82%E8%A7%80%E4%B8%8A){target="_blank"}」，圖片由左至右解釋，Chrome 瀏覽器開源版本的 Chromium（BSD）、Electron（MIT）。Slack、VS Code 大多是把自家應用程式（JavaScript、TypeScript）跑在 Electron（內含 Chromium）上，並和 Electron 一起打包成安裝檔發佈。Slack：使用 Electron 但通常不修改 Electron/Chromium，因此屬於「集合發佈」。**Slack** 本體可閉源；但需附上 Electron/Chromium 與其他第三方套件的授權告示，並滿足可能的 LGPL 義務。**VS Code：**微軟官方發佈版包含商標與額外條款；而上游 Code - OSS 是 MIT 開源。社群的 [VSCodium](https://vscodium.com/){target="_blank"} 就是從 Code - OSS「衍生」並重新包裝散佈，完全符合衍生著作可再散佈的精神。

授權必須允許修改原始碼、建立衍生作品（例如 fork、採用 patch、合併到其他程式），並允許把這些修改版散佈出去。

* 寬鬆授權（MIT、BSD、Apache-2.0）：允許在保留告示前提下，將衍生品以開源或閉源方式散佈。
* 互惠／強著作權傳染授權（GPL、AGPL、LGPL）：若散佈衍生品（或與之形成單一作品），必須以相同或相容的自由軟體授權開源。

例如：在開源專案上加功能並發佈修改版；或將其 fork 成新專案，依原授權規範保留告示並釋出。

## 常見的開源授權條款

!!! question ""

    :material-account-question: 我是開源貢獻者新手，我該怎麼挑選開源授權條款？

以下將介紹幾個常用的開源授權條款，其差異在分發（distribution）的嚴謹程度。

<figure markdown="span">
    ![Open Source](./assets/images/open-source-distribution.svg)
    <figcaption>圖片：常見的開源授權條款其分發的嚴謹程度。</figcaption>
</figure>

### AGPL

<small>SPDX：`AGPL-3.0-or-later`</small>

AGPL（GNU Affero General Public License, GNU AGPL），強 Copyleft + 網路互動條款。若他人提供你的服務（SaaS），也必須開源對應修改。

:material-file-document-check-outline:{style="color: blue;"} 主要義務：

* 向網路互動的使用者提供對應完整原始碼。
* 保留版權與授權聲明、變更標示。
* 授與專利許可、專利訴訟終止條款。

**:material-check-circle:{style="color: green;"} 適合用於：**避免「雲端服務商挾持」、你希望雲端服務商回饋與修改。

**:material-close-circle:{style="color: red;"} 可能不適合：**商業採用阻力較大；與封閉核心混用困難。

:octicons-arrow-switch-16:{style="color: orange;"} 相容性：

* 可與 GPLv3 程式碼相容，但 AGPL 通常決定最終的釋出。
* 與 GPLv2-only 不相容。

:octicons-alert-16:{style="color: fuchsia;"} 常見誤解：

* 誤以為僅發佈二進位才需釋出原始碼，但重點在 AGPL 網路服務互動也觸發。

:material-file-sign:{style="color: purple;"} 合規清單：

* 提供可得的完整源碼（含建置腳本）。
* 清楚標示網路部署下的取得方式（例如頁尾連結）。

:octicons-repo-forked-16:{style="color: brown;"} 著名專案：Mastodon、immich、Grafana

### GPL

<small>SPDX：`GPL-3.0-or-later`、`GPL-2.0-only`</small>

GNU General Public Licenses（GNU GPL 或 GPL），GPL 目前分為 v2 與 v3 版本並行，強 Copyleft。分發修改版或與其連結的組合作品時，需以 GPL 開放原始碼。

:material-file-document-check-outline:{style="color: blue;"} 主要義務：

* 分發時提供完整對應原始碼與建置方式。
* 保留版權與授權聲明、修改標示。
* v3 含專利授權、反規避（anti-tivoization）；v2 無明確專利授權。

**:material-check-circle:{style="color: green;"} 適合用於：**希望衍生作品保持開源，促進社群回饋。

**:material-close-circle:{style="color: red;"} 可能不適合：**與專有元件連結困難；部分企業有合規顧慮。

:octicons-arrow-switch-16:{style="color: orange;"} 相容性：

* GPLv3 與 Apache-2.0 相容；GPLv2-only 與 Apache-2.0 不相容
* MIT、BSD、MPL 在條件下可併入 GPL 專案（由 GPL 最終決定）。

:octicons-alert-16:{style="color: fuchsia;"} 常見誤解：

* 「只要不商業就不用遵守」：錯！是否分發才是關鍵。
* 「動態連結不算」：連結是否形成衍生作品需個案判斷。

:material-file-sign:{style="color: purple;"} 合規清單：

* 發佈二進位即需提供源碼或可得方式（連結、書面要約）。
* 提供對應物件檔（若用 LGPL 例外或允許重連結的需求）。

:octicons-repo-forked-16:{style="color: brown;"} 著名專案：Linux kernel（GPLv2-only）、Git（GPLv2）

### LGPL

<small>SPDX：`LGPL-3.0-or-later`、`LGPL-2.1-or-later`</small>

GNU Lesser General Public License（LGPL），LGPL 目前分為 2.1 與 3.0 並行、弱 Copyleft，針對「函式庫」。允許專有應用連結，但修改函式庫本身需開源，且須允許使用者可替換、重連結。

:material-file-document-check-outline:{style="color: blue;"} 主要義務：

* 修改函式庫需開源、連結的應用可專有。
* 靜態連結時通常需提供可重連結的物件檔或其他機制。

**:material-check-circle:{style="color: green;"} 適合用於：**希望函式庫本身維持開放，但不限制使用者應用的授權。

**:material-close-circle:{style="color: red;"} 可能不適合：**對裝置鎖定或重新連結限制敏感的場域。

:octicons-arrow-switch-16:{style="color: orange;"} 相容性：

* 可被專有程式連結（遵守替換條件）。
* 與 GPLv3 相容；2.1 與 3.0 細節不同。

:octicons-alert-16:{style="color: fuchsia;"} 常見誤解：

* 「用 LGPL 就等於能任意封閉」：函式庫可封閉連結，但函式庫修改不行（需開放）。

:material-file-sign:{style="color: purple;"} 合規清單：

* 附上 LGPL 文本與函式庫的變更說明。
* 提供重連結途徑（物件檔、動態連結、插件機制）。

:octicons-repo-forked-16:{style="color: brown;"} 著名專案：glibc、Qt（提供雙授權包含 LGPL）

### MPL

<small>SPDX：`MPL-2.0`</small>

Mozilla Public License（MPL），檔案層級 Copyleft。修改的 MPL 檔案需保留 MPL；可與專有碼並存於同一專案。

:material-file-document-check-outline:{style="color: blue;"} 主要義務：

* 修改過的 MPL 檔案需公開源碼與保留聲明。
* 允許將 MPL 檔與其他授權檔組合進行混合，包括私有授權條款。
* 含專利授權與終止條款。

**:material-check-circle:{style="color: green;"} 適合用於：**希望改動能回饋，但又不想對整個專案施加強 Copyleft。

**:material-close-circle:{style="color: red;"} 可能不適合：**要求整體衍生作品都必須 GPL 式釋出。

:octicons-arrow-switch-16:{style="color: orange;"} 相容性：

* 可與許多授權共存；可啟用「[Secondary License](https://zh.wikipedia.org/zh-tw/%E5%A4%9A%E9%87%8D%E8%A8%B1%E5%8F%AF){target="_blank"}」與 GPL 家族相容（除非標注不相容）。

:octicons-alert-16:{style="color: fuchsia;"} 常見誤解：

* 「用了 MPL 就不能商用」：可商用，僅對修改檔案有義務。

:material-file-sign:{style="color: purple;"} 合規清單：

* 修改檔案保留版頭與授權；提供修改檔案之源碼取得方式。

:octicons-repo-forked-16:{style="color: brown;"} 著名專案：Firefox、Thunderbird、Rust（部分）

### Apache

<small>SPDX：`Apache-2.0`</small>

寬鬆式授權，附明確專利授權與 NOTICE 要求，對企業友好。

:material-file-document-check-outline:{style="color: blue;"} 主要義務：

* 保留版權與授權聲明。
* 保留或合併上游 NOTICE 內容（若存在）。
* 明確專利授權與專利訴訟終止條款；商標不授權。

**:material-check-circle:{style="color: green;"} 適合用於：**最大化採用與商業友善，同時需要專利風險防護。

**:material-close-circle:{style="color: red;"} 可能不適合：**需強制回饋修改的專案。

:octicons-arrow-switch-16:{style="color: orange;"} 相容性：

* 與 GPLv3 相容；與 GPLv2-only 不相容。
* 可與 MIT、BSD、MPL 共存。

:octicons-alert-16:{style="color: fuchsia;"} 常見誤解：

* 「沒有 Copyleft 就不用保留聲明」：仍須保留版權與授權聲明、NOTICE。

:material-file-sign:{style="color: purple;"} 合規清單：

* 附 LICENSE 與 NOTICE（若有）。
* 保留檔案內的版權、作者標示。

:octicons-repo-forked-16:{style="color: brown;"} 著名專案：Kubernetes、Android（多數元件）

### BSD

<small>SPDX：`BSD-2-Clause`、`BSD-3-Clause`</small>

Berkeley Software Distribution（BSD），極簡寬鬆授權。2-Clause 最簡；3-Clause 多一條「不得暗示背書」條款。無明確專利授權。

:material-file-document-check-outline:{style="color: blue;"} 主要義務：

* 保留版權與免責聲明。
* 3-Clause 多「不得使用作者、機構名義背書」。

**:material-check-circle:{style="color: green;"} 適合用於：**最小限制、最大化採用；學術與基礎建設常見。

**:material-close-circle:{style="color: red;"} 可能不適合：**需要專利授權明確性的企業環境（可考慮 Apache-2.0）。

:octicons-arrow-switch-16:{style="color: orange;"} 相容性：

* 可被 GPL、Apache、MIT 等納入。

:octicons-alert-16:{style="color: fuchsia;"} 常見誤解：

* 「BSD 不需要附授權檔」：需保留授權與免責聲明。

:material-file-sign:{style="color: purple;"} 合規清單：

* 保留 LICENSE 與檔案中版權標示。

:octicons-repo-forked-16:{style="color: brown;"} 著名專案：FreeBSD、OpenBSD、Go（BSD-3-Clause）

### MIT

<small>SPDX：`MIT`</small>

最常見的寬鬆授權，要求保留版權與授權聲明。無明確專利授權。

:material-file-document-check-outline:{style="color: blue;"} 主要義務：

* 保留版權與授權全文；免責聲明。

**:material-check-circle:{style="color: green;"} 適合用於：**最低摩擦、廣泛採用、前端與庫生態常見。

**:material-close-circle:{style="color: red;"} 可能不適合：**需要專利授權明確性（考慮 Apache-2.0）。

:octicons-arrow-switch-16:{style="color: orange;"} 相容性：

* 幾乎與所有主流授權相容，可被 GPL 專案納入。

:octicons-alert-16:{style="color: fuchsia;"} 常見誤解：

* 「MIT 代表完全不需標示」：仍需保留版權與授權。

:material-file-sign:{style="color: purple;"} 合規清單：

* 在原始碼與二進位散布中保留 LICENSE 文本。

:octicons-repo-forked-16:{style="color: brown;"} 著名專案：React、Rails、Node.js

## 其他延伸閱讀

如果還需要更深入瞭解開源授權條款的資訊可以參考以下的文章介紹：

1. [開源授權常識補充包(2024 版)](https://blog.darkthread.net/blog/opensource-licenses/){target="_blank"}, 黑暗執行緒
2. [開放源碼授權概觀（上）](https://yurenju.blog/zh/posts/2018-07-03_%E9%96%8B%E6%94%BE%E6%BA%90%E7%A2%BC%E6%8E%88%E6%AC%8A%E6%A6%82%E8%A7%80%E4%B8%8A){target="_blank"}, Yuren's Blog
3. [開放源碼授權概觀（下）](https://yurenju.blog/zh/posts/2018-07-03_%E9%96%8B%E6%94%BE%E6%BA%90%E7%A2%BC%E6%8E%88%E6%AC%8A%E6%A6%82%E8%A7%80%E4%B8%8B){target="_blank"}, Yuren's Blog
4. [法律源地](https://web-archive-2025.openfoundry.org/law-and-licensing){target="_blank"} - OpenFoundry（web-archive-2025）
5. [Choose an open source license](https://choosealicense.com/){target="_blank"}

!!! info ""

    :material-account-star: 對於開源授權條款的使用或法律諮詢，可以寄信到開放文化基金會 <hi@ocf.tw> 詢問。

*[SPDX]: 軟體包資料交換規範（Software Package Data Exchange）簡稱 SPDX，是軟體材料表（SBOM）的開源標準 。
