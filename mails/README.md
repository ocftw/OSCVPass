# mails

OSCVPass 透過 **AWS SES** 寄送樣板信件的工具與操作說明。
信件樣板放在 `tpl/`，寄送邏輯在 `awssestools.py`，續約提醒名單工具在 `send_renew.py`。

> 寄件者為已在 SES 驗證的 `oscvpass@ocf.tw`（見 `awssestools.py` 的 `MAIL_SOURCE`）。

## 環境設定

```bash
cd mails
cp setting.py.sample setting.py   # 填入 AWS 憑證、測試信箱、封鎖名單
uv sync                            # 安裝相依套件（arrow / boto3 / jinja2）
```

`setting.py` 已被 `.gitignore` 忽略，**請勿提交**。欄位說明見 `setting.py.sample`。

## 安全須知

- 幾乎所有寄送函式都支援 **`dry_run`**，預設只寄一封測試信到 `setting.TESTMAIL`。
- 確認名單與信件內容無誤後，再改為正式寄送（`dry_run=False` 或 `--no-dry-run`）。
- `setting.BLOCK` 內的信箱永遠不會收到信。

## 年度續約提醒（issue #23）

提醒「即將／已到期」的貢獻者回來更新資格，建議在 **COSCUP 前一兩個月**執行。

1. 從核准名單（Google Forms／試算表）匯出 CSV，至少包含：起始日
   （`start_date`）、暱稱（`nickname`，可退回 `name`）、email（`mail`，可退回
   `mail2`）；若有 `status` 欄則只會處理「通過」者。
2. 篩出名單並肉眼檢查（**不寄信**）：

   ```bash
   uv run python send_renew.py --source approved.csv --out renew.csv
   # 預設納入「未來 60 天內到期」者；要一併提醒剛過期者：
   uv run python send_renew.py --source approved.csv --out renew.csv --expired-within-days 60
   ```

   會印出每位的到期日與「即將／已」到期標記，並輸出 `renew.csv`
   （欄位 `date,nickname,mail`，對應 `tpl/expired.html`）。
3. 先寄一封測試信給自己（`setting.TESTMAIL`）：

   ```bash
   uv run python send_renew.py --source approved.csv --send
   ```

4. 確認無誤後正式寄給所有人：

   ```bash
   uv run python send_renew.py --source approved.csv --send --no-dry-run
   ```

常用參數：`--within-days N`（未來幾天內到期，預設 60）、`--expired-within-days N`
（也納入過去幾天內過期者，預設 0）、`--years N`（資格效期，預設 1）、`--today
YYYY-MM-DD`（覆寫基準日，方便測試）。完整參數見 `send_renew.py --help`。

> `.github/workflows/renew-reminder.yml` 會在每年 COSCUP 前自動開一張提醒
> issue，避免忘記執行上述流程。

## 審核結果通知（pass / 補件 / 拒絕）

`awssestools.py` 的 `process_csv()` 會依匯出名單的 `status` 欄分流到
`pass` / `insufficient_for` / `deny` 三類，再由 `send()` 套用對應樣板寄出。
範例已寫在 `awssestools.py` 的 `__main__` 區塊（預設註解、`dry_run=True`）：

```python
data = process_csv('./oscvpass_xxxxxx.csv', _all=False)  # 只寄尚未寄過（send 欄為空）者
send(data=data, case=('deny', 'insufficient_for', 'pass'), dry_run=True)
```

確認後將 `dry_run` 改為 `False` 正式寄送。

## 其他樣板

`tpl/` 內另有各研討會的優惠票券、年度總結、workshop 等一次性信件樣板，
對應 `awssestools.py` 內的 `send_*` 系列函式，依當年度需求取用。
