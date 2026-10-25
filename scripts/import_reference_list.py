"""
import_reference_list.py

One-off/re-runnable importer that converts the curated Excel reference
list ("NextGeneration Software Testing - AgenticAI - Reference list.xlsx")
into version-controlled, plain-text research artifacts:

  1. literature-review/papers-tracking.csv
       Consolidated tracking sheet (one row per candidate study),
       merging:
         - Sheet2 ("Publication year / Venue / Title / URL / Research gap")
           -> authoritative year, venue, URL, research-gap notes, and
              (for section 19) link-verification notes.
         - Sheet1 ("# / Title / Authors / Venue / Link / Status")
           -> author names and original working IDs, merged in by
              matching category + row order where both sheets overlap.

  2. paper/references.bib
       BibTeX stubs for every study with a resolvable arXiv ID (parsed
       from the URL), plus @misc stubs for the remaining studies so
       every record has a stable citation key.

Usage:
    python scripts/import_reference_list.py ["<path to .xlsx>"]

If no path is given, the repository's own copy at
data/raw/reference-list.xlsx is used.
"""

from __future__ import annotations

import csv
import pathlib
import re
import sys

import openpyxl

ROOT = pathlib.Path(__file__).resolve().parents[1]
DEFAULT_XLSX = ROOT / "data" / "raw" / "reference-list.xlsx"

ARXIV_RE = re.compile(r"arxiv\.org/abs/([0-9]{4}\.[0-9]{4,5})(v\d+)?", re.IGNORECASE)
CATEGORY_RE = re.compile(r"^\s*(\d+)\.\s*(.+?)\s*$")
SHEET1_ID_RE = re.compile(r"^[A-Z]{1,3}\d+$")


def arxiv_id_from_url(url):
    if not isinstance(url, str):
        return None
    m = ARXIV_RE.search(url)
    return m.group(1) if m else None


def slugify_category(name: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return slug


def parse_sheet1(wb):
    """Return {category_name: [ {id, title, authors}, ... ]} from Sheet1."""
    ws = wb["Sheet1"]
    rows = list(ws.iter_rows(values_only=True))
    categories: dict[str, list[dict]] = {}
    current_cat = None
    for row in rows:
        # Sheet1 data lives in columns E:J -> zero-based indices 4..9
        col = list(row[4:10]) if len(row) >= 10 else list(row[4:]) + [None] * (6 - len(row[4:]))
        vals = col
        non_none = [v for v in vals if v is not None]
        if not non_none:
            continue
        # Category marker: single populated cell starting with "N. "
        if len(non_none) == 1 and isinstance(non_none[0], str):
            m = CATEGORY_RE.match(non_none[0])
            if m:
                current_cat = m.group(2)
                categories.setdefault(current_cat, [])
                continue
            # free-text note row (e.g. "O2 is useful for..."); skip
            continue
        sid = vals[0]
        if not isinstance(sid, str) or not SHEET1_ID_RE.match(sid.strip()):
            continue  # header row ('#', ...) or malformed row
        title, authors = vals[1], vals[2]
        if current_cat is None:
            continue
        categories[current_cat].append(
            {"id": sid.strip(), "title": title, "authors": authors}
        )
    return categories


def parse_sheet2(wb):
    """Return list of dicts: category, year, venue, title, url, gap, link_check."""
    ws = wb["Sheet2"]
    rows = list(ws.iter_rows(values_only=True))
    records = []
    current_cat = None
    for row in rows:
        # A category marker can appear in any column due to merged cells in
        # the source workbook (most often column 0, occasionally column 3).
        match_idx, match_text = None, None
        for i, v in enumerate(row):
            if isinstance(v, str):
                m = CATEGORY_RE.match(v)
                if m:
                    match_idx, match_text = i, m.group(2)
                    break
        other_non_none = [v for i, v in enumerate(row) if i != match_idx and v is not None]

        if match_idx is not None:
            current_cat = match_text
            if not other_non_none:
                continue  # row is purely a category marker, no data to extract
            if match_idx != 0:
                # Category label landed in a data column with no companion
                # data elsewhere on the row; nothing usable to extract.
                continue
            rest = list(row[1:])
            if rest and isinstance(rest[0], str) and rest[0].strip() == "Publication year":
                continue
        else:
            rest = list(row[1:])
            if not rest or rest[0] is None:
                continue
            if isinstance(rest[0], str) and rest[0].strip() == "Publication year":
                continue
            if current_cat is None:
                continue
        year, venue, title, url = (rest + [None] * 4)[:4]
        gap = rest[4] if len(rest) > 4 else None
        link_check = rest[5] if len(rest) > 5 else None
        if not title:
            continue
        records.append(
            {
                "category": current_cat,
                "year": year,
                "venue": venue,
                "title": title,
                "url": url,
                "research_gap": gap,
                "link_check": link_check,
            }
        )
    return records


def merge(sheet1_cats, sheet2_records):
    """Zip Sheet1 authors/IDs onto Sheet2 records by category + row order."""
    cat_cursors = {cat: 0 for cat in sheet1_cats}
    merged = []
    auto_counter = 1
    for rec in sheet2_records:
        cat = rec["category"]
        s1_list = sheet1_cats.get(cat)
        authors, orig_id = None, None
        if s1_list is not None:
            idx = cat_cursors[cat]
            if idx < len(s1_list):
                authors = s1_list[idx]["authors"]
                orig_id = s1_list[idx]["id"]
                cat_cursors[cat] += 1
        study_id = orig_id or f"SLR{auto_counter:03d}"
        if orig_id is None:
            auto_counter += 1
        merged.append({**rec, "authors": authors, "study_id": study_id})
    return merged


def write_tracking_csv(merged, out_path: pathlib.Path):
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "study_id",
        "category",
        "year",
        "venue",
        "title",
        "authors",
        "url",
        "arxiv_id",
        "research_gap",
        "link_check",
        "decision_title_abstract",
        "decision_full_text",
        "quality_score",
        "technique_category",
        "automation_level",
        "notes",
    ]
    with out_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for rec in merged:
            writer.writerow(
                {
                    "study_id": rec["study_id"],
                    "category": rec["category"],
                    "year": rec["year"] or "",
                    "venue": rec["venue"] or "",
                    "title": rec["title"] or "",
                    "authors": rec["authors"] or "",
                    "url": rec["url"] or "",
                    "arxiv_id": arxiv_id_from_url(rec["url"]) or "",
                    "research_gap": rec["research_gap"] or "",
                    "link_check": rec["link_check"] or "",
                    "decision_title_abstract": "include",
                    "decision_full_text": "",
                    "quality_score": "",
                    "technique_category": "",
                    "automation_level": "",
                    "notes": "",
                }
            )
    print(f"Wrote {len(merged)} rows -> {out_path}")


def bib_key(rec, seen):
    year = str(rec["year"]) if rec["year"] not in (None, "", "—") else "nd"
    authors = rec["authors"]
    if authors and authors not in ("—",):
        # Prefer a readable author-year key (standard convention) when a
        # real author name was recovered from Sheet1.
        first_author = re.split(r"[,\s]", authors.strip())[0].lower()
        first_author = re.sub(r"[^a-z]", "", first_author) or "anon"
        base = f"{first_author}{year}"
    else:
        # Fall back to the tracking-sheet study_id so the citation key
        # stays traceable to literature-review/papers-tracking.csv even
        # when no author name could be recovered (categories 1-5, 19).
        base = f"{rec['study_id'].lower()}{year}"
    key = base
    i = 1
    while key in seen:
        i += 1
        key = f"{base}{chr(96 + i)}"
    seen.add(key)
    return key


def escape_bib(text):
    if not text:
        return ""
    return str(text).replace("{", "\\{").replace("}", "\\}")


def write_bib(merged, out_path: pathlib.Path):
    seen_keys = set()
    entries = []
    for rec in merged:
        key = bib_key(rec, seen_keys)
        rec["bib_key"] = key
        aid = arxiv_id_from_url(rec["url"])
        title = escape_bib(rec["title"])
        authors = escape_bib(rec["authors"]) if rec["authors"] and rec["authors"] not in ("—",) else "Unknown"
        year = rec["year"] if rec["year"] not in (None, "", "—") else "n.d."
        venue = escape_bib(rec["venue"]) if rec["venue"] else ""
        url = rec["url"] or ""
        keywords = escape_bib(rec["category"]) if rec.get("category") else ""
        if aid:
            entry = (
                f"@misc{{{key},\n"
                f"  title        = {{{{{title}}}}},\n"
                f"  author       = {{{authors}}},\n"
                f"  year         = {{{year}}},\n"
                f"  eprint       = {{{aid}}},\n"
                f"  archivePrefix= {{arXiv}},\n"
                f"  note         = {{{venue}}},\n"
                f"  keywords     = {{{keywords}}},\n"
                f"  url          = {{{url}}}\n"
                f"}}"
            )
        else:
            entry = (
                f"@misc{{{key},\n"
                f"  title        = {{{{{title}}}}},\n"
                f"  author       = {{{authors}}},\n"
                f"  year         = {{{year}}},\n"
                f"  howpublished = {{{venue}}},\n"
                f"  keywords     = {{{keywords}}},\n"
                f"  url          = {{{url}}}\n"
                f"}}"
            )
        entries.append(entry)

    header = (
        "% =====================================================================\n"
        "% Auto-generated bibliography imported from the curated reference list\n"
        "% (NextGeneration Software Testing - AgenticAI - Reference list.xlsx)\n"
        "% Generated by scripts/import_reference_list.py -- do not hand-edit the\n"
        "% generated block below; re-run the script instead. Add manually curated\n"
        "% entries (e.g. kitchenham2007, page2021prisma) ABOVE this marker.\n"
        "% =====================================================================\n"
    )
    marker_start = "% --- BEGIN IMPORTED REFERENCES (auto-generated) ---\n"
    marker_end = "\n% --- END IMPORTED REFERENCES (auto-generated) ---\n"

    existing = out_path.read_text(encoding="utf-8") if out_path.exists() else ""
    if marker_start in existing:
        pre = existing.split(marker_start)[0]
    else:
        pre = existing.rstrip() + "\n\n"

    with out_path.open("w", encoding="utf-8") as f:
        f.write(pre)
        f.write(marker_start)
        f.write(header)
        f.write("\n\n".join(entries))
        f.write(marker_end)
    print(f"Wrote {len(entries)} BibTeX entries -> {out_path}")
    return entries


def main():
    xlsx_path = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path(DEFAULT_XLSX)
    if not xlsx_path.exists():
        print(f"ERROR: source workbook not found: {xlsx_path}")
        sys.exit(1)

    wb = openpyxl.load_workbook(xlsx_path, data_only=True)
    sheet1_cats = parse_sheet1(wb)
    sheet2_records = parse_sheet2(wb)
    merged = merge(sheet1_cats, sheet2_records)

    tracking_csv = ROOT / "literature-review" / "papers-tracking.csv"
    bib_path = ROOT / "paper" / "references.bib"

    write_tracking_csv(merged, tracking_csv)
    write_bib(merged, bib_path)


if __name__ == "__main__":
    main()
