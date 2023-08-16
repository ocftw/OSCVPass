# 開發流程

若要直接在docker上啟動環境，可以直接參見[在Docker上執行OSCVPass](#在Docker上執行OSCVPass)。

<!-- toc -->

## Pretalx建置 (用於Pretalx核心開發)

> 本章節主要說明如何建置官方Pretalx的程式碼。

完整建置流程可以參照[官方說明][official_build]

### 前置作業

需要先安裝以下工具：

|工具|Debian套件名稱|
|-|-|
|python 3.6+||
|pip 3|`python3-pip`|
|python-dev 3|`python3-dev`|
|python-venv 3|`python3-venv`|
|libffi|`libffi-dev`|
|gettext|`gettext`|
|git|`git`|

- 部分套件需要編譯器建置，若安裝失敗可先確認套件`build-essential`是否安裝。

### 開啟虛擬Python環境

```bash
python3 -m venv env
source env/bin/activate
```

- Ubuntu/Debian

由於部分套件版本較舊，建議可先執行以下指令更新必要套件：

```bash
sudo pip3 install -U pip setuptools wheel
```

### 複製原始碼

```bash
git clone https://github.com/pretalx/pretalx.git
cd pretalx/
```

### 初始環境建置

首先安裝主程式所需要的相依函式庫：

```bash
(env)$ cd src
(env)$ pip3 install --upgrade-strategy eager -Ue ".[dev]"
```

接著，複製靜態檔案至`STATIC_ROOTS`資料夾中，並初始化本地資料庫：

```bash
(env)$ python manage.py collectstatic --noinput
(env)$ python manage.py migrate
```

為了能夠登入並操作，您需要創建至少一位具有管理員權限的帳號：

```bash
(env)$ python manage.py init
```

此外，若您開發上即刻需要一個用於測試的活動，您可以執行以下指令來創建：

```bash
(env)$ python manage.py create_test_event
```

### 語言檔案 (可選)

由於Pretalx預設僅有英文語文檔案已經事前編譯完成，若您需要使用其他語言，您需要執行以下指令：

```bash
(env)$ python manage.py compilemessages
```

### 啟動環境

```bash
(env)$ python manage.py runserver
```

## 在Docker上執行OSCVPass

> 本章節主要說明如何在本地端的docker上運行OSCVPass。

詳細執行流程可以參照[pretalx-docker官方說明][official_docker]

### 複製原始碼

```bash
$ git clone -b pretalx https://github.com/ocftw/OSCVPass.git
$ cd OSCVPass/
```

### 直接執行

- 運行測試環境

```bash
$ cd pretalx/
$ docker compose -f ./docker-compose.yml up
```

- 運行生產環境

```bash
$ cd pretalx/
$ docker compose -f ./docker-compose_prod.yml up
```

## 雜項

- 關於GitHub上的分支
  - main - 用於Github Pages上託管說明文檔
  - docs - 用於暫存新版的說明文檔。
  - pretalx - 用於儲存OSCVPass所使用的pretalx docker設定檔

[official_build]: https://docs.pretalx.org/developer/setup.html
[official_docker]: https://github.com/pretalx/pretalx-docker/README.md