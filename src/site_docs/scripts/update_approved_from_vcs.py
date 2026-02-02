#!/usr/bin/env python3
"""
Update `zh-tw/approved/*.md` entries from GitHub/GitLab metadata.

Behavior (per repo conventions / requested plan):
- Parse Markdown list items like: `- [label](url), contributor, _desc_`
- Infer canonical GitHub/GitLab repo/project from the URL (even if URL points to PR/issue/commit),
  but DO NOT change the original URL in the docs.
- Overwrite the italic description with the platform description and append a stats suffix.
- Skip non GitHub/GitLab URLs.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from datetime import timedelta
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlparse
from urllib.request import Request, urlopen


GITHUB_API_BASE = "https://api.github.com"
GITLAB_API_BASE = "https://gitlab.com/api/v4"


MD_LINK_LINE_RE = re.compile(
    r"^(?P<indent>\s*)-\s+\[(?P<label>[^\]]+)\]\((?P<url>[^)]+)\)(?P<rest>.*)$"
)

# Find the description segment at end-of-line-ish: `, _desc_ ...tail...`
# Allow escaped underscores (e.g. `\_`) inside `_..._`.
DESC_SEGMENT_RE = re.compile(r",\s*_(?P<desc>(?:\\_|[^_])*)_(?P<tail>.*)$")


@dataclass(frozen=True)
class Target:
    # kind: "github_repo" | "github_account" | "gitlab_project"
    kind: str
    # canonical identifier, used as cache/memo key
    key: str


def _now_utc() -> datetime:
    return datetime.now(tz=timezone.utc)


def _parse_iso_to_date(iso_str: str | None) -> str | None:
    if not iso_str:
        return None
    s = iso_str.strip()
    if not s:
        return None
    # GitHub/GitLab often use trailing 'Z'
    if s.endswith("Z"):
        s = s[:-1] + "+00:00"
    try:
        dt = datetime.fromisoformat(s)
    except ValueError:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc).date().isoformat()


def _fmt_date_maybe_bold(yyyy_mm_dd: str) -> str:
    """
    If the date is within the last 365 days (UTC), emphasize it with bold markdown.
    Output is intended to be used as a value after `:date:`.
    """
    try:
        d = datetime.fromisoformat(yyyy_mm_dd).date()
    except ValueError:
        return yyyy_mm_dd
    today = _now_utc().date()
    if d >= (today - timedelta(days=365)):
        return f"**{yyyy_mm_dd}**"
    return yyyy_mm_dd


def _collapse_ws(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def _md_escape_italics(s: str) -> str:
    # underscore breaks `_..._` markdown italics; escape it
    return s.replace("\\", "\\\\").replace("_", "\\_")


def _md_unescape_italics(s: str) -> str:
    # Reverse the minimal escapes we introduce in `_md_escape_italics`.
    # Order matters: unescape `\\` first, then `\_`.
    return s.replace("\\\\", "\\").replace("\\_", "_")


def _strip_known_auto_suffix(tail: str) -> str:
    # On reruns, strip our own suffix so we don't duplicate.
    # We only strip a single parenthetical group if it looks like our stats.
    t = tail or ""
    m = re.match(r"^\s*\((?P<body>[^)]*)\)\s*$", t)
    if not m:
        return t
    body = (m.group("body") or "").strip()

    # Match our own generated stats format (including legacy variants).
    # Examples:
    # - ":star: 12, :octicons-repo-forked-24: 3, :date: 2026-02-02, :material-license: MIT"
    # - ":material-account-group: 123, :octicons-repo-24: 45, :date: 2026-01-01"
    stat_token = (
        r"(?:"
        r"★\d+"
        r"|:star:\s+\d+"
        r"|:octicons-repo-forked-24:\s+\d+"
        r"|forks\s+\d+"
        r"|followers\s+\d+"
        r"|repos\s+\d+"
        r"|:material-account-group:\s+\d+"
        r"|:octicons-repo-24:\s+\d+"
        r"|updated\s+\d{4}-\d{2}-\d{2}"
        r"|:date:\s+(?:\d{4}-\d{2}-\d{2}|\*\*\d{4}-\d{2}-\d{2}\*\*)"
        r"|license\s+[^,]+"
        r"|:material-license:\s+[^,]+"
        r")"
    )
    if re.fullmatch(rf"{stat_token}(?:,\s*{stat_token})*", body):
        return ""
    return t


def infer_target_from_url(url: str) -> Target | None:
    try:
        p = urlparse(url.strip())
    except ValueError:
        return None

    host = (p.netloc or "").lower()
    parts = [seg for seg in (p.path or "").split("/") if seg]
    if not host or not parts:
        return None

    if host in {"github.com", "www.github.com"}:
        owner = parts[0]
        if len(parts) >= 2:
            repo = parts[1]
            if repo.endswith(".git"):
                repo = repo[:-4]
            return Target(kind="github_repo", key=f"github_repo:{owner}/{repo}".lower())
        # Single segment -> user/org account
        return Target(kind="github_account", key=f"github_account:{owner}".lower())

    if host in {"gitlab.com", "www.gitlab.com"}:
        stop_words = {
            "-",
            "issues",
            "merge_requests",
            "commits",
            "commit",
            "pipelines",
            "milestones",
            "tags",
            "releases",
            "blob",
            "tree",
            "raw",
            "compare",
        }
        proj_parts: list[str] = []
        for seg in parts:
            if seg == "-":
                break
            if seg in stop_words and proj_parts:
                break
            proj_parts.append(seg)
        if len(proj_parts) < 2:
            return None
        path = "/".join(proj_parts)
        return Target(kind="gitlab_project", key=f"gitlab_project:{path}".lower())

    return None


def _http_get_json(url: str, headers: dict[str, str], *, max_retries: int = 5) -> dict[str, Any]:
    last_err: Exception | None = None
    for attempt in range(max_retries):
        try:
            req = Request(url, headers=headers, method="GET")
            with urlopen(req, timeout=30) as resp:
                raw = resp.read()
                return json.loads(raw.decode("utf-8"))
        except HTTPError as e:
            last_err = e

            retry_after = e.headers.get("Retry-After")
            if retry_after:
                try:
                    sleep_s = int(retry_after)
                except ValueError:
                    sleep_s = None
                if sleep_s is not None and sleep_s > 0:
                    time.sleep(min(sleep_s, 60))
                    continue

            # GitHub rate limit (403 with remaining=0)
            remaining = e.headers.get("X-RateLimit-Remaining")
            reset = e.headers.get("X-RateLimit-Reset")
            if e.code == 403 and remaining == "0" and reset:
                try:
                    reset_epoch = int(reset)
                except ValueError:
                    reset_epoch = None
                if reset_epoch:
                    wait_s = max(0, reset_epoch - int(time.time()) + 2)
                    time.sleep(min(wait_s, 120))
                    continue

            if e.code in {429, 500, 502, 503, 504}:
                time.sleep(min(2**attempt, 10))
                continue

            raise
        except URLError as e:
            last_err = e
            time.sleep(min(2**attempt, 10))

    assert last_err is not None
    raise last_err


def _github_headers() -> dict[str, str]:
    headers = {
        "User-Agent": "ocf-oscvpass-approved-updater",
        "Accept": "application/vnd.github+json",
    }
    token = os.getenv("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def _gitlab_headers() -> dict[str, str]:
    headers = {"User-Agent": "ocf-oscvpass-approved-updater"}
    token = os.getenv("GITLAB_TOKEN")
    if token:
        headers["PRIVATE-TOKEN"] = token
    return headers


def fetch_metadata(target: Target) -> dict[str, Any] | None:
    if target.kind == "github_repo":
        owner_repo = target.key.split(":", 1)[1]
        url = f"{GITHUB_API_BASE}/repos/{owner_repo}"
        return _http_get_json(url, _github_headers())

    if target.kind == "github_account":
        account = target.key.split(":", 1)[1]
        headers = _github_headers()
        user_url = f"{GITHUB_API_BASE}/users/{account}"
        user = _http_get_json(user_url, headers)
        if isinstance(user, dict) and user.get("type") == "Organization":
            # GitHub org endpoint provides `description`, while `/users` may not.
            org_url = f"{GITHUB_API_BASE}/orgs/{account}"
            try:
                org = _http_get_json(org_url, headers)
            except Exception:
                org = None
            if isinstance(org, dict):
                merged = dict(user)
                if org.get("description"):
                    merged["description"] = org.get("description")
                # Keep `bio` if present; otherwise fallback to org description for readability.
                if not merged.get("bio") and org.get("description"):
                    merged["bio"] = org.get("description")
                return merged
        return user

    if target.kind == "gitlab_project":
        path = target.key.split(":", 1)[1]
        url = f"{GITLAB_API_BASE}/projects/{quote(path, safe='')}"
        return _http_get_json(url, _gitlab_headers())

    return None


def build_desc_and_suffix(target: Target, meta: dict[str, Any], old_desc: str | None) -> tuple[str | None, str | None]:
    """
    Returns (new_desc, stats_suffix) where stats_suffix excludes leading space.
    If new_desc is None, caller should skip updating.
    """
    if target.kind == "github_repo":
        desc = _collapse_ws((meta.get("description") or "").strip())
        if not desc:
            desc = _collapse_ws((old_desc or "").strip())
        stars = meta.get("stargazers_count")
        forks = meta.get("forks_count")
        updated = _parse_iso_to_date(meta.get("pushed_at") or meta.get("updated_at"))
        lic = meta.get("license") or {}
        spdx = None
        if isinstance(lic, dict):
            spdx = lic.get("spdx_id")
        if spdx in {None, "", "NOASSERTION"}:
            spdx = None

        parts: list[str] = []
        if isinstance(stars, int):
            parts.append(f":star: {stars}")
        if isinstance(forks, int):
            parts.append(f":octicons-repo-forked-24: {forks}")
        if updated:
            parts.append(f":date: {_fmt_date_maybe_bold(updated)}")
        if spdx:
            parts.append(f":material-license: {spdx}")

        suffix = f"({', '.join(parts)})" if parts else None
        return (desc or None), suffix

    if target.kind == "gitlab_project":
        desc = _collapse_ws((meta.get("description") or "").strip())
        if not desc:
            desc = _collapse_ws((old_desc or "").strip())
        stars = meta.get("star_count")
        forks = meta.get("forks_count")
        updated = _parse_iso_to_date(meta.get("last_activity_at"))

        spdx = None
        lic = meta.get("license")
        if isinstance(lic, dict):
            spdx = lic.get("spdx_id") or lic.get("spdx_identifier") or lic.get("key") or lic.get("name")
        if isinstance(spdx, str):
            spdx = _collapse_ws(spdx)
            if not spdx or spdx.lower() in {"unknown", "noassertion"}:
                spdx = None

        parts: list[str] = []
        if isinstance(stars, int):
            parts.append(f":star: {stars}")
        if isinstance(forks, int):
            parts.append(f":octicons-repo-forked-24: {forks}")
        if updated:
            parts.append(f":date: {_fmt_date_maybe_bold(updated)}")
        if spdx:
            parts.append(f":material-license: {spdx}")

        suffix = f"({', '.join(parts)})" if parts else None
        return (desc or None), suffix

    if target.kind == "github_account":
        # For org/user accounts: prefer org description if available; fallback to bio.
        desc = _collapse_ws((meta.get("bio") or "").strip())
        if not desc:
            desc = _collapse_ws((meta.get("description") or "").strip())
        if not desc:
            desc = _collapse_ws((old_desc or "").strip())

        followers = meta.get("followers")
        repos = meta.get("public_repos")
        updated = _parse_iso_to_date(meta.get("updated_at"))

        parts: list[str] = []
        if isinstance(followers, int):
            parts.append(f":material-account-group: {followers}")
        if isinstance(repos, int):
            parts.append(f":octicons-repo-24: {repos}")
        if updated:
            parts.append(f":date: {_fmt_date_maybe_bold(updated)}")
        suffix = f"({', '.join(parts)})" if parts else None
        return (desc or None), suffix

    return None, None


def rewrite_line(line: str, *, new_desc: str, stats_suffix: str | None) -> str:
    nl = "\n" if line.endswith("\n") else ""
    s = line[:-1] if nl else line

    m = MD_LINK_LINE_RE.match(s)
    if not m:
        return line

    rest = m.group("rest")
    desc_match = DESC_SEGMENT_RE.search(rest)

    desc_md = _md_escape_italics(_collapse_ws(new_desc))
    suffix = stats_suffix

    if desc_match:
        before = rest[: desc_match.start()]
        tail = desc_match.group("tail") or ""
        tail = _strip_known_auto_suffix(tail)
        rebuilt = before + f", _{desc_md}_"
        if suffix:
            rebuilt += f" {suffix}"
        rebuilt += tail
        return f"{m.group('indent')}- [{m.group('label')}]({m.group('url')}){rebuilt}{nl}"

    # No existing italic desc -> append one.
    rebuilt = rest.rstrip()
    rebuilt += f", _{desc_md}_"
    if suffix:
        rebuilt += f" {suffix}"
    return f"{m.group('indent')}- [{m.group('label')}]({m.group('url')}){rebuilt}{nl}"


def load_cache(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def save_cache(path: Path, cache: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(cache, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def cache_get(cache: dict[str, Any], key: str, *, ttl_hours: int) -> dict[str, Any] | None:
    rec = cache.get(key)
    if not isinstance(rec, dict):
        return None
    fetched_at = rec.get("fetched_at")
    data = rec.get("data")
    if not isinstance(data, dict):
        return None
    if not isinstance(fetched_at, str):
        return None
    dt_str = fetched_at
    if dt_str.endswith("Z"):
        dt_str = dt_str[:-1] + "+00:00"
    try:
        fetched = datetime.fromisoformat(dt_str)
    except ValueError:
        return None
    if fetched.tzinfo is None:
        fetched = fetched.replace(tzinfo=timezone.utc)
    age_s = (_now_utc() - fetched.astimezone(timezone.utc)).total_seconds()
    if age_s > ttl_hours * 3600:
        return None
    return data


def cache_put(cache: dict[str, Any], key: str, data: dict[str, Any]) -> None:
    cache[key] = {"fetched_at": _now_utc().isoformat().replace("+00:00", "Z"), "data": data}


def process_file(
    md_path: Path,
    *,
    cache: dict[str, Any],
    memo: dict[str, dict[str, Any]],
    ttl_hours: int,
    progress: bool,
    file_idx: int,
    file_total: int,
) -> tuple[list[str], int, int]:
    """
    Returns (new_lines, changed_count, updated_entries_count)
    - changed_count: number of lines changed in this file
    - updated_entries_count: number of list items that we successfully updated
    """
    lines = md_path.read_text(encoding="utf-8").splitlines(keepends=True)
    out: list[str] = []
    changed = 0
    updated_entries = 0
    in_fence = False
    total_lines = len(lines)

    # Progress counters
    processed_lines = 0
    memo_hits = 0
    cache_hits = 0
    fetched = 0
    fetch_failed = 0

    if progress:
        print(
            f"[{file_idx}/{file_total}] processing {md_path} ({total_lines} lines)",
            file=sys.stderr,
        )

    for line in lines:
        processed_lines += 1
        if progress and processed_lines in {1, 50, 200}:
            print(
                f"  ... {processed_lines}/{total_lines} lines",
                file=sys.stderr,
            )
        elif progress and processed_lines % 500 == 0:
            print(
                f"  ... {processed_lines}/{total_lines} lines (updated {updated_entries}, fetched {fetched}, cache {cache_hits}, memo {memo_hits}, failed {fetch_failed})",
                file=sys.stderr,
            )

        stripped = line.strip()
        if stripped.startswith("```"):
            in_fence = not in_fence
            out.append(line)
            continue
        if in_fence:
            out.append(line)
            continue

        m = MD_LINK_LINE_RE.match(line[:-1] if line.endswith("\n") else line)
        if not m:
            out.append(line)
            continue

        url = m.group("url")
        target = infer_target_from_url(url)
        if not target:
            out.append(line)
            continue

        # Only process GitHub/GitLab inferred targets; non-matching hosts are already None.
        rest = m.group("rest")
        old_desc = None
        dm = DESC_SEGMENT_RE.search(rest)
        if dm:
            old_desc = _md_unescape_italics(dm.group("desc"))

        meta: dict[str, Any] | None = None
        if target.key in memo:
            memo_hits += 1
            meta = memo[target.key]
        else:
            cached = cache_get(cache, target.key, ttl_hours=ttl_hours)
            if cached is not None:
                cache_hits += 1
                meta = cached
            else:
                fetched += 1
                if progress and (fetched <= 5 or fetched % 25 == 0):
                    print(f"  fetching {fetched}: {target.key}", file=sys.stderr)
                try:
                    meta = fetch_metadata(target)
                except Exception:
                    fetch_failed += 1
                    meta = None
                if isinstance(meta, dict):
                    cache_put(cache, target.key, meta)
            if isinstance(meta, dict):
                memo[target.key] = meta

        if not isinstance(meta, dict):
            out.append(line)
            continue

        new_desc, suffix = build_desc_and_suffix(target, meta, old_desc)
        if not new_desc:
            out.append(line)
            continue

        new_line = rewrite_line(line, new_desc=new_desc, stats_suffix=suffix)
        if new_line != line:
            changed += 1
            updated_entries += 1
        out.append(new_line)

    if progress:
        print(
            f"[{file_idx}/{file_total}] done {md_path} (updated {updated_entries}, changed_lines {changed}, fetched {fetched}, cache {cache_hits}, memo {memo_hits}, failed {fetch_failed})",
            file=sys.stderr,
        )
    return out, changed, updated_entries


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--approved-dir",
        default="zh-tw/approved",
        help="Path to approved directory (default: zh-tw/approved).",
    )
    ap.add_argument(
        "--only-files",
        nargs="*",
        default=None,
        help="Only process these markdown filenames (e.g. app.md program.md).",
    )
    ap.add_argument(
        "--progress",
        action="store_true",
        help="Print progress to stderr while running.",
    )
    ap.add_argument(
        "--no-progress",
        action="store_true",
        help="Disable progress output.",
    )
    ap.add_argument(
        "--cache",
        default=".cache/vcs_meta_cache.json",
        help="Cache path (default: .cache/vcs_meta_cache.json).",
    )
    ap.add_argument(
        "--cache-ttl-hours",
        type=int,
        default=24,
        help="Cache TTL in hours (default: 24).",
    )
    ap.add_argument(
        "--write",
        action="store_true",
        help="Write updated markdown files.",
    )
    ap.add_argument(
        "--write-cache",
        action="store_true",
        help="Write cache file to disk (optional).",
    )
    ap.add_argument(
        "--verbose",
        action="store_true",
        help="Verbose logs.",
    )
    args = ap.parse_args()

    approved_dir = Path(args.approved_dir)
    cache_path = Path(args.cache)
    ttl_hours = int(args.cache_ttl_hours)
    progress = bool(args.progress or (not args.no_progress and sys.stderr.isatty()))

    if not approved_dir.exists() or not approved_dir.is_dir():
        print(f"approved dir not found: {approved_dir}", file=sys.stderr)
        return 2

    write_cache = bool(args.write_cache)
    cache: dict[str, Any] = load_cache(cache_path) if cache_path else {}
    memo: dict[str, dict[str, Any]] = {}

    md_files = sorted(p for p in approved_dir.glob("*.md") if p.is_file())
    if args.only_files:
        only = {Path(x).name for x in args.only_files}
        md_files = [p for p in md_files if p.name in only]
    total_changed_lines = 0
    total_updated_entries = 0
    changed_files: list[Path] = []

    if progress:
        print(f"processing {len(md_files)} files in {approved_dir}", file=sys.stderr)

    for i, md in enumerate(md_files, start=1):
        new_lines, changed, updated = process_file(
            md,
            cache=cache,
            memo=memo,
            ttl_hours=ttl_hours,
            progress=progress,
            file_idx=i,
            file_total=len(md_files),
        )
        if changed:
            changed_files.append(md)
            total_changed_lines += changed
            total_updated_entries += updated
            if args.write:
                md.write_text("".join(new_lines), encoding="utf-8")
        if args.verbose:
            print(f"{md}: changed_lines={changed}, updated_entries={updated}")

    if write_cache and cache_path:
        save_cache(cache_path, cache)

    if changed_files:
        print(f"updated entries: {total_updated_entries} (changed lines: {total_changed_lines})")
        for p in changed_files:
            print(f"- {p}")
    else:
        print("no changes")

    if not args.write:
        print("(dry-run) use --write to apply changes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

