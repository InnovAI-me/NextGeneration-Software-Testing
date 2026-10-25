"""
fetch_full_papers.py
=====================

Visit each study's URL in `literature-review/papers-tracking.csv`, locate a
"full text / PDF" download link on the landing page (or build one directly
for arXiv entries), download the PDF, optionally extract its text to
Markdown, and store the result(s) locally under
`data/papers/<study_id>.pdf` and/or `data/papers/<study_id>.md`.

IMPORTANT - copyright note
---------------------------
Downloaded PDFs/Markdown extracts are for personal research/screening use
only. They are kept out of git (see .gitignore: `data/papers/*`) because
redistributing publisher copyrighted text (ACM/IEEE/Springer/etc.) via a
public GitHub repo would be a copyright violation. Only the machine-readable
fetch manifest/log (`data/papers/fetch-log.csv`) is committed, so the team
can see what was retrieved and re-run this script to regenerate the actual
files.

Usage
-----
    python scripts/fetch_full_papers.py                      # fetch everything not yet downloaded (PDF + MD)
    python scripts/fetch_full_papers.py --study-id G1         # fetch a single study
    python scripts/fetch_full_papers.py --limit 10            # fetch the next 10 pending studies
    python scripts/fetch_full_papers.py --force               # re-download/re-convert even if files exist
    python scripts/fetch_full_papers.py --delay 3              # seconds to sleep between requests (politeness)
    python scripts/fetch_full_papers.py --format md            # keep only the extracted Markdown (deletes PDF after conversion)
    python scripts/fetch_full_papers.py --format pdf           # keep only the raw PDF (skip text extraction)

Strategy per study
-------------------
1. If `arxiv_id` is present, build the canonical arXiv PDF URL
   (https://arxiv.org/pdf/<id>.pdf) and download directly - this is the most
   reliable path and works for ~90% of the current reference set.
2. If the tracking-sheet `url` itself already points at a `.pdf` file, it is
   downloaded directly.
3. Otherwise, GET the study's `url`, parse the HTML with BeautifulSoup, and
   look for:
     - a `<meta name="citation_pdf_url">` tag (common aggregator convention)
     - a direct link ending in `.pdf`
     - an anchor whose text/aria-label contains "pdf", "full text",
       "download pdf", or "download full-text"
     - an arXiv-style URL embedded in the page (some aggregators link out)
   The first candidate found is downloaded. Candidate link resolution uses
   `urljoin` against the landing page URL so relative hrefs work.
4. If no PDF link can be found (common for paywalled ACM/IEEE/Springer pages,
   ResearchGate logins, or blocked hosts), the attempt is logged as
   `no_pdf_found` and the landing-page HTML is NOT saved as a substitute
   (avoids silently treating an abstract page as "full text read").
5. When Markdown output is requested (`--format md` or `both`, the default),
   the downloaded PDF's text is extracted page-by-page with PyMuPDF and
   written to `<study_id>.md` with a small front-matter header (study_id,
   title, authors, year, venue, source_url/pdf). Scanned/image-only PDFs
   that yield no extractable text are reported as `pdf_ok_md_failed`.
6. Every attempt (success or failure) is appended to
   `data/papers/fetch-log.csv` and mirrored into three columns added to
   `papers-tracking.csv`: `pdf_status`, `pdf_local_path`, `md_local_path`.

This script is intentionally conservative: it does not attempt to bypass
paywalls, CAPTCHAs, or login walls. Entries that fail should be fetched
manually (e.g., via institutional access) and dropped into
`data/papers/<study_id>.pdf`; re-running the script will skip files that
already exist unless `--force` is passed.
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
import time
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

try:
    import pymupdf as fitz  # preferred modern import name
except ImportError:  # pragma: no cover - fallback for older pymupdf releases
    import fitz  # type: ignore

REPO_ROOT = Path(__file__).resolve().parent.parent
TRACKING_CSV = REPO_ROOT / "literature-review" / "papers-tracking.csv"
PAPERS_DIR = REPO_ROOT / "data" / "papers"
FETCH_LOG = PAPERS_DIR / "fetch-log.csv"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0 Safari/537.36 "
        "SLR-research-bot/1.0 (+contact: repo maintainer)"
    )
}
REQUEST_TIMEOUT = 30  # seconds

PDF_LINK_TEXT_PATTERNS = re.compile(
    r"(download\s*pdf|full[\s-]*text|view\s*pdf|^pdf$|get\s*pdf|article\s*pdf)",
    re.IGNORECASE,
)
ARXIV_ID_IN_TEXT = re.compile(r"(\d{4}\.\d{4,5})(v\d+)?")


def arxiv_pdf_url(arxiv_id: str) -> str:
    """Build a canonical arXiv PDF URL from a bare arXiv id."""
    clean_id = arxiv_id.strip()
    return f"https://arxiv.org/pdf/{clean_id}.pdf"


def find_pdf_link_on_page(html: str, page_url: str) -> str | None:
    """Scan a landing page for the most likely 'read full paper' PDF link."""
    soup = BeautifulSoup(html, "html.parser")

    # 1) <meta name="citation_pdf_url" content="..."> - used by many
    #    publisher/aggregator sites (Google Scholar metadata convention).
    meta = soup.find("meta", attrs={"name": "citation_pdf_url"})
    if meta and meta.get("content"):
        return urljoin(page_url, meta["content"])

    # 2) Any anchor whose href ends in .pdf
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if href.lower().split("?")[0].endswith(".pdf"):
            return urljoin(page_url, href)

    # 3) Any anchor whose visible text / aria-label looks like a PDF /
    #    full-text download button.
    for a in soup.find_all("a", href=True):
        label = " ".join(
            filter(None, [a.get_text(" ", strip=True), a.get("aria-label", ""), a.get("title", "")])
        )
        if PDF_LINK_TEXT_PATTERNS.search(label):
            return urljoin(page_url, a["href"])

    # 4) An arXiv id embedded anywhere in the raw HTML (e.g. aggregator
    #    pages that mirror an arXiv abstract).
    match = ARXIV_ID_IN_TEXT.search(html)
    if match:
        return arxiv_pdf_url(match.group(1))

    return None


def download_file(url: str, dest: Path, session: requests.Session) -> tuple[bool, int | None, str]:
    """Download `url` to `dest`. Returns (success, http_status, message)."""
    try:
        with session.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT, stream=True) as resp:
            status = resp.status_code
            content_type = resp.headers.get("Content-Type", "")
            if status != 200:
                return False, status, f"HTTP {status}"
            if "pdf" not in content_type.lower() and not url.lower().endswith(".pdf"):
                # Some servers mislabel content-type; peek at the first bytes
                # for the %PDF magic number before trusting content-type.
                first_chunk = next(resp.iter_content(chunk_size=5), b"")
                if not first_chunk.startswith(b"%PDF"):
                    return False, status, f"Not a PDF (Content-Type: {content_type or 'unknown'})"
                dest.write_bytes(first_chunk + resp.raw.read())
                return True, status, "ok"
            dest.parent.mkdir(parents=True, exist_ok=True)
            with open(dest, "wb") as fh:
                for chunk in resp.iter_content(chunk_size=8192):
                    fh.write(chunk)
            return True, status, "ok"
    except requests.RequestException as exc:
        return False, None, f"{type(exc).__name__}: {exc}"


def pdf_to_markdown(pdf_path: Path, row: dict) -> str:
    """Extract text from a downloaded PDF and render it as a simple Markdown
    document with a small YAML-ish front matter header for traceability."""
    doc = fitz.open(pdf_path)
    try:
        pages_md = []
        for page_number, page in enumerate(doc, start=1):
            text = page.get_text("text").strip()
            if not text:
                continue
            pages_md.append(f"<!-- page {page_number} -->\n\n{text}")
        body = "\n\n---\n\n".join(pages_md)
    finally:
        doc.close()

    header_lines = [
        "---",
        f"study_id: {row.get('study_id', '')}",
        f"title: \"{(row.get('title') or '').replace(chr(34), chr(39))}\"",
        f"authors: \"{(row.get('authors') or '').replace(chr(34), chr(39))}\"",
        f"year: {row.get('year', '')}",
        f"venue: \"{(row.get('venue') or '').replace(chr(34), chr(39))}\"",
        f"source_url: {row.get('url', '')}",
        f"source_pdf: {pdf_path.name}",
        "---",
        "",
        f"# {row.get('title', '')}",
        "",
    ]
    return "\n".join(header_lines) + "\n" + body


def convert_pdf_to_md(pdf_path: Path, md_path: Path, row: dict) -> tuple[bool, str]:
    try:
        markdown = pdf_to_markdown(pdf_path, row)
        if not markdown.strip():
            return False, "PDF produced no extractable text (likely scanned/image-only)"
        md_path.write_text(markdown, encoding="utf-8")
        return True, "ok"
    except Exception as exc:  # pragma: no cover - defensive: corrupt/encrypted PDFs
        return False, f"{type(exc).__name__}: {exc}"


def _download_pdf(row: dict, session: requests.Session, dest: Path) -> dict:
    """Core download logic: tries arXiv direct URL, then a direct .pdf URL,
    then scrapes the landing page for a PDF/full-text link. Returns a result
    dict with pdf_url/local_path/status/http_code/message (no Markdown
    handling here - see fetch_one)."""
    study_id = row["study_id"].strip()
    url = (row.get("url") or "").strip()
    arxiv_id = (row.get("arxiv_id") or "").strip()

    result = {
        "study_id": study_id,
        "source_url": url,
        "pdf_url": "",
        "local_path": "",
        "status": "",
        "http_code": "",
        "message": "",
    }

    # Preferred path: arXiv entries have a reliable, stable PDF URL.
    if arxiv_id:
        pdf_url = arxiv_pdf_url(arxiv_id)
        ok, code, msg = download_file(pdf_url, dest, session)
        if ok:
            result.update(
                pdf_url=pdf_url,
                local_path=str(dest.relative_to(REPO_ROOT)),
                status="success",
                http_code=code,
                message=msg,
            )
            return result
        # Fall through to generic page-scraping if the direct arXiv URL fails
        # (e.g., id was mistyped or the paper was withdrawn).
        result["message"] = f"arXiv direct fetch failed ({msg}); trying landing page"

    if not url:
        result.update(status="error", message=result["message"] or "no url and no arxiv_id")
        return result

    # The tracking-sheet URL sometimes already points straight at a PDF file
    # (e.g. publisher/author "uploads/.../paper.pdf" links) - download it
    # directly instead of trying to parse it as an HTML landing page.
    if urlparse(url).path.lower().endswith(".pdf"):
        ok, code, msg = download_file(url, dest, session)
        if ok:
            result.update(
                pdf_url=url,
                local_path=str(dest.relative_to(REPO_ROOT)),
                status="success",
                http_code=code,
                message=msg,
            )
        else:
            result.update(pdf_url=url, status="error", http_code=code, message=msg)
        return result

    try:
        resp = session.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
    except requests.RequestException as exc:
        result.update(status="error", message=f"landing page fetch failed: {exc}")
        return result

    if not (200 <= resp.status_code < 300):
        result.update(status="error", http_code=resp.status_code, message=f"landing page HTTP {resp.status_code}")
        return result

    pdf_url = find_pdf_link_on_page(resp.text, resp.url)
    if not pdf_url:
        result.update(status="no_pdf_found", http_code=resp.status_code, message="no PDF/full-text link detected")
        return result

    ok, code, msg = download_file(pdf_url, dest, session)
    if ok:
        result.update(
            pdf_url=pdf_url,
            local_path=str(dest.relative_to(REPO_ROOT)),
            status="success",
            http_code=code,
            message=msg,
        )
    else:
        result.update(pdf_url=pdf_url, status="error", http_code=code, message=msg)
    return result


def fetch_one(row: dict, session: requests.Session, force: bool, fmt: str) -> dict:
    """Fetch the full text for one tracking-sheet row in the requested
    `fmt` ('pdf', 'md', or 'both'), handling skip-if-exists / --force and
    optional PDF -> Markdown conversion. A PDF is always downloaded
    internally when Markdown is requested (text extraction needs the PDF
    bytes); it is deleted afterwards if the caller only wants 'md'."""
    study_id = row["study_id"].strip()
    keep_pdf = fmt in ("pdf", "both")
    want_md = fmt in ("md", "both")
    pdf_dest = PAPERS_DIR / f"{study_id}.pdf"
    md_dest = PAPERS_DIR / f"{study_id}.md"

    already_satisfied = (not keep_pdf or pdf_dest.exists()) and (not want_md or md_dest.exists())
    if already_satisfied and not force:
        result = {
            "study_id": study_id,
            "source_url": (row.get("url") or "").strip(),
            "pdf_url": "",
            "local_path": str(pdf_dest.relative_to(REPO_ROOT)) if pdf_dest.exists() else "",
            "md_local_path": str(md_dest.relative_to(REPO_ROOT)) if md_dest.exists() else "",
            "status": "already_downloaded",
            "http_code": "",
            "message": "skipped (use --force to re-download)",
        }
        return result

    result = _download_pdf(row, session, pdf_dest)
    result.setdefault("md_local_path", "")

    if result["status"] == "success" and want_md:
        ok, msg = convert_pdf_to_md(pdf_dest, md_dest, row)
        if ok:
            result["md_local_path"] = str(md_dest.relative_to(REPO_ROOT))
        else:
            result["status"] = "pdf_ok_md_failed"
            result["message"] = f"{result['message']}; markdown conversion failed: {msg}"

    if result["status"] in ("success", "pdf_ok_md_failed") and not keep_pdf:
        pdf_dest.unlink(missing_ok=True)
        result["local_path"] = ""

    return result


def load_tracking_rows() -> tuple[list[dict], list[str]]:
    with open(TRACKING_CSV, newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        fieldnames = list(reader.fieldnames or [])
        rows = list(reader)
    return rows, fieldnames


def save_tracking_rows(rows: list[dict], fieldnames: list[str]) -> None:
    with open(TRACKING_CSV, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def append_fetch_log(entries: list[dict]) -> None:
    PAPERS_DIR.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "timestamp", "study_id", "source_url", "pdf_url",
        "local_path", "md_local_path", "status", "http_code", "message",
    ]
    file_exists = FETCH_LOG.exists()
    with open(FETCH_LOG, "a", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerows(entries)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--study-id", help="Fetch only this study_id (e.g. G1, SLR023).")
    parser.add_argument("--limit", type=int, default=None, help="Fetch at most N studies this run.")
    parser.add_argument("--force", action="store_true", help="Re-download/re-convert even if local files already exist.")
    parser.add_argument("--delay", type=float, default=2.0, help="Seconds to wait between requests (politeness).")
    parser.add_argument(
        "--format", choices=["pdf", "md", "both"], default="both",
        help="What to keep on disk: raw 'pdf', extracted 'md', or 'both' (default).",
    )
    args = parser.parse_args()

    if not TRACKING_CSV.exists():
        print(f"Tracking sheet not found: {TRACKING_CSV}", file=sys.stderr)
        return 1

    rows, fieldnames = load_tracking_rows()
    for col in ("pdf_status", "pdf_local_path", "md_local_path"):
        if col not in fieldnames:
            fieldnames.append(col)

    targets = rows
    if args.study_id:
        targets = [r for r in rows if r["study_id"].strip() == args.study_id.strip()]
        if not targets:
            print(f"No row with study_id={args.study_id!r} found.", file=sys.stderr)
            return 1
    if args.limit:
        targets = targets[: args.limit]

    PAPERS_DIR.mkdir(parents=True, exist_ok=True)
    session = requests.Session()
    log_entries = []
    by_id = {r["study_id"].strip(): r for r in rows}

    total = len(targets)
    for i, row in enumerate(targets, start=1):
        study_id = row["study_id"].strip()
        print(f"[{i}/{total}] {study_id}: {row.get('title', '')[:70]!r} ...", flush=True)
        result = fetch_one(row, session, force=args.force, fmt=args.format)
        print(f"    -> {result['status']} ({result['message']})")

        log_entries.append({"timestamp": time.strftime("%Y-%m-%d %H:%M:%S"), **result})
        by_id[study_id]["pdf_status"] = result["status"]
        by_id[study_id]["pdf_local_path"] = result["local_path"]
        by_id[study_id]["md_local_path"] = result.get("md_local_path", "")

        if result["status"] not in ("already_downloaded",):
            time.sleep(args.delay)

    append_fetch_log(log_entries)
    save_tracking_rows(list(by_id.values()), fieldnames)

    n_success = sum(1 for e in log_entries if e["status"] in ("success", "pdf_ok_md_failed"))
    n_skip = sum(1 for e in log_entries if e["status"] == "already_downloaded")
    n_fail = len(log_entries) - n_success - n_skip
    print(f"\nDone. {n_success} downloaded, {n_skip} already present, {n_fail} failed/needs manual fetch.")
    print(f"Files saved under: {PAPERS_DIR.relative_to(REPO_ROOT)} (format={args.format})")
    print(f"Manifest log: {FETCH_LOG.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
