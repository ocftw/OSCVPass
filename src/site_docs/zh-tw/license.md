---
title: 常見的開源授權條款
icon: material/license
---

# 常見的開源授權條款

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

## 常見的開源授權條款

!!! question ""

    :material-account-question: 我是開源貢獻者新手，我該怎麼挑選開源授權條款？

請先參考 OSI 的「[開源定義（The Open Source Definition）](./open-source-definition.md){target="_blank"}」的定義，在「開源定義」的前三項是開源的主要核心：**自由再發佈、開放原始碼、自由修改的衍生作品**。

以下將介紹幾個常用的開源授權條款，其差異在分發（distribution）的嚴謹程度。

![Open Source](./assets/images/open-source-distribution.svg)

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

### GPL

### LGPL

### MPL

### Apache

### BSD

### MIT

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
