#!/usr/bin/env python3
"""產生「即將／已到期」的續約提醒名單，並（選擇性）透過 AWS SES 寄送。

對應 issue #23：過往貢獻者反映沒有收到續約（Renew）通知，希望在 COSCUP 前
一兩個月主動提醒回來更新資格。

資料流：

    核准名單 CSV（含 start_date / mail / nickname）
      │  計算到期日（start_date ＋ N 年，預設 1 年）
      ▼
    篩出在 [now − expired_within, now ＋ within] 區間到期者
      │
      ▼
    輸出 renew CSV（欄位：date,nickname,mail）── 給 tpl/expired.html 使用
      │  （加上 --send）
      ▼
    awssestools.send_expired() 透過 AWS SES 寄出

設計原則：

  * 預設「只篩名單、不寄信」，讓你先肉眼檢查名單再決定寄送。
  * 篩選流程不需要 setting.py 或 AWS 憑證即可在本機執行與測試。
  * 真正寄送沿用既有、已驗證的 ``awssestools.send_expired``，避免重造輪子。

用法見 README.md 的「年度續約提醒」一節。
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

import arrow


def _pick(row: dict[str, str], primary: str, fallback: str | None = None) -> str:
    """取 ``primary`` 欄位，空白時退回 ``fallback``，並去除前後空白。"""
    value = (row.get(primary) or '').strip()
    if not value and fallback:
        value = (row.get(fallback) or '').strip()
    return value


def _expiration(row: dict[str, str], *, date_col: str, start_col: str,
                years: int) -> arrow.Arrow | None:
    """算出該筆的到期日。

    優先使用既有的到期日欄位（``date_col``）；沒有時改用起始日
    （``start_col``）往後加 ``years`` 年。兩者皆無或無法解析則回傳 None。
    """
    raw_date = _pick(row, date_col)
    if raw_date:
        try:
            return arrow.get(raw_date)
        except (ValueError, arrow.parser.ParserError):
            return None

    raw_start = _pick(row, start_col)
    if not raw_start:
        return None
    try:
        return arrow.get(raw_start).shift(years=years)
    except (ValueError, arrow.parser.ParserError):
        return None


def collect(path: Path, *, now: arrow.Arrow, within: int, expired_within: int,
            years: int, status_col: str, status_value: str,
            date_col: str, start_col: str,
            nickname_col: str, name_col: str,
            mail_col: str, mail2_col: str) -> list[dict[str, str]]:
    # pylint: disable=too-many-arguments,too-many-locals
    """讀核准名單 CSV，回傳落在續約提醒區間內的名單。

    區間為 ``[now − expired_within 天, now ＋ within 天]``，涵蓋「即將到期」
    與「剛過期」兩種需要提醒的對象。回傳欄位為 ``date / nickname / mail``，
    正是 ``tpl/expired.html`` 與 ``awssestools.send_expired`` 所需。
    """
    lower = now.shift(days=-expired_within)
    upper = now.shift(days=+within)

    picked: list[dict[str, str]] = []
    with path.open(encoding='UTF8') as files:
        for row in csv.DictReader(files):
            # 有 status 欄時，只處理「通過」者；沒有則不過濾。
            if status_col in row and status_value:
                if (row.get(status_col) or '').strip() != status_value:
                    continue

            exp = _expiration(row, date_col=date_col, start_col=start_col,
                              years=years)
            if exp is None:
                continue
            if not lower <= exp <= upper:
                continue

            mail = _pick(row, mail_col, mail2_col).lower()
            if '@' not in mail:
                continue

            nickname = _pick(row, nickname_col, name_col)
            picked.append({
                'date': exp.format('YYYY-MM-DD'),
                'nickname': nickname or mail,
                'mail': mail,
            })

    picked.sort(key=lambda r: r['date'])
    return picked


def write_csv(rows: list[dict[str, str]], path: Path) -> None:
    """輸出 renew 名單為 ``date,nickname,mail`` 三欄 CSV。"""
    with path.open('w+', encoding='UTF8') as files:
        writer = csv.DictWriter(files, fieldnames=('date', 'nickname', 'mail'))
        writer.writeheader()
        writer.writerows(rows)


def main(argv: list[str] | None = None) -> int:
    """CLI 進入點：解析參數、篩名單、輸出 CSV，並可選擇寄送。"""
    parser = argparse.ArgumentParser(
        description='產生續約提醒名單，並可選擇透過 AWS SES 寄送（issue #23）。')
    parser.add_argument('--source', required=True, type=Path,
                        help='核准名單 CSV（需含起始日與 email 欄位）')
    parser.add_argument('--out', type=Path, default=Path('./renew.csv'),
                        help='輸出的續約名單 CSV 路徑（預設 ./renew.csv）')
    parser.add_argument('--within-days', type=int, default=60,
                        help='納入「未來 N 天內到期」者（預設 60）')
    parser.add_argument('--expired-within-days', type=int, default=0,
                        help='也納入「過去 N 天內已過期」者（預設 0＝不納入）')
    parser.add_argument('--years', type=int, default=1,
                        help='資格效期年數，用於由起始日推算到期日（預設 1）')
    parser.add_argument('--today',
                        help='覆寫「今天」（YYYY-MM-DD），方便測試／回溯')

    # 欄位名稱（預設沿用 awssestools.process_csv 的慣例）
    parser.add_argument('--status-col', default='status')
    parser.add_argument('--status-value', default='通過')
    parser.add_argument('--date-col', default='expiration_date',
                        help='若來源已有到期日欄位則直接採用')
    parser.add_argument('--start-col', default='start_date')
    parser.add_argument('--nickname-col', default='nickname')
    parser.add_argument('--name-col', default='name')
    parser.add_argument('--mail-col', default='mail')
    parser.add_argument('--mail2-col', default='mail2')

    parser.add_argument('--send', action='store_true',
                        help='篩完後實際呼叫 AWS SES 寄送（需要 mails/setting.py）')
    parser.add_argument('--no-dry-run', action='store_true',
                        help='搭配 --send：真的寄給所有人（否則只寄一封測試信）')
    args = parser.parse_args(argv)

    if not args.source.exists():
        parser.error(f'找不到來源檔案：{args.source}')

    now = arrow.get(args.today) if args.today else arrow.now()

    rows = collect(
        args.source, now=now,
        within=args.within_days, expired_within=args.expired_within_days,
        years=args.years,
        status_col=args.status_col, status_value=args.status_value,
        date_col=args.date_col, start_col=args.start_col,
        nickname_col=args.nickname_col, name_col=args.name_col,
        mail_col=args.mail_col, mail2_col=args.mail2_col,
    )

    write_csv(rows, args.out)

    print(f'基準日：{now.format("YYYY-MM-DD")}　'
          f'區間：[−{args.expired_within_days}d, +{args.within_days}d]')
    print(f'符合續約提醒者：{len(rows)} 位　→　已寫入 {args.out}')
    for row in rows:
        flag = '即將' if arrow.get(row['date']) >= now else '已'
        print(f"  {row['date']}  {flag}到期  {row['nickname']}  <{row['mail']}>")

    if not rows:
        return 0

    if not args.send:
        print('\n（僅產生名單，未寄信。確認名單後可加 --send 寄出。）')
        return 0

    # 寄送路徑才需要 setting.py / AWS 憑證，故延後 import。
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import awssestools  # noqa: E402  pylint: disable=import-outside-toplevel

    dry_run = not args.no_dry_run
    if dry_run:
        print('\n[dry-run] 僅寄一封測試信到 setting.TESTMAIL；確認無誤後加 --no-dry-run。')
    else:
        print(f'\n[正式寄送] 即將寄給 {len(rows)} 位收件者……')
    awssestools.send_expired(str(args.out), dry_run=dry_run)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
