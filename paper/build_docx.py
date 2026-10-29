"""
build_docx.py
Converts the LaTeX manuscript into a fully formatted, publication-ready DOCX file
aligned with Elsevier / Computer Science Review author guidelines using python-docx.
"""

import os
import re
import sys
from pathlib import Path
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent
OUTPUT_DOCX = BASE_DIR / "NextGen-Software-Testing-SLR.docx"

LABEL_MAP = {
    # Sections
    'sec:introduction': '1',
    'sec:background': '2',
    'sec:methodology': '3',
    'sec:related-work': '4',
    'sec:results': '5',
    'sec:discussion': '6',
    'sec:threats': '7',
    'sec:validity': '7',
    'sec:conclusion': '8',
    'sec:qe-safety': '5.4',
    'sec:safety-framework': '6.2',
    'sec:saaqe-validation': '6.4',
    # Subsections
    'subsec:review-protocol': '3.1',
    'subsec:search-strategy': '3.2',
    'subsec:study-selection': '3.3',
    'subsec:quality-assessment': '3.4',
    'subsec:data-extraction': '3.5',
    'subsec:prior-surveys-gen': '4.1',
    'subsec:prior-surveys-agentic': '4.2',
    'subsec:pub-trends': '5.1',
    'subsec:rq1-taxonomy': '5.2',
    'subsec:rq2-autonomy': '5.3',
    # Figures & Tables
    'fig:pub-trend': '1',
    'fig:category-dist': '2',
    'fig:taxonomy-dist': '2',
    'tab:taxonomy': '1',
    'tab:saaqe-components': '2',
    'tab:saaqe-data': '3',
}

def parse_bib_file(bib_path):
    """Parser to extract BibTeX entries into a dict of {key: formatted_string}."""
    if not bib_path.exists():
        return {}
    content = bib_path.read_text(encoding="utf-8")
    entries = {}
    pattern = re.compile(r'@(\w+)\s*\{\s*([^,]+),([^@]*?)\n\}', re.DOTALL)
    for match in pattern.finditer(content):
        key = match.group(2).strip()
        body = match.group(3)
        fields = {}
        for f in re.finditer(r'(\w+)\s*=\s*[\{"](.*?)[}"]', body, re.DOTALL):
            fields[f.group(1).lower()] = re.sub(r'\s+', ' ', f.group(2)).strip()
        
        author = fields.get('author', 'Unknown Author')
        title = fields.get('title', 'Untitled')
        year = fields.get('year', '')
        journal = fields.get('journal') or fields.get('booktitle') or fields.get('institution') or ''
        
        ref_text = f"{author}, {title}, {journal} ({year})."
        entries[key] = ref_text
    return entries

def clean_latex(text, bib_dict, citation_map):
    """Converts LaTeX markup to clean plain text with mapped citation numbers."""
    if not text:
        return ""
        
    def cite_repl(m):
        keys = [k.strip() for k in m.group(1).split(',')]
        nums = []
        for k in keys:
            if k not in citation_map:
                citation_map[k] = len(citation_map) + 1
            nums.append(str(citation_map[k]))
        return f"[{', '.join(nums)}]"

    text = re.sub(r'\\cite\{([^}]+)\}', cite_repl, text)
    text = re.sub(r'(?<!\\)%.*$', '', text, flags=re.MULTILINE)
    
    def ref_repl(m):
        ref_key = m.group(1).strip()
        return LABEL_MAP.get(ref_key, ref_key.split(':')[-1].replace('-', ' '))

    text = re.sub(r'\\ref\{([^}]+)\}', ref_repl, text)
    text = re.sub(r'\\eqref\{([^}]+)\}', lambda m: f"({LABEL_MAP.get(m.group(1).strip(), m.group(1))})", text)
    
    text = re.sub(r'\\label\{[^}]+\}', '', text)
    text = re.sub(r'\\centering\b', '', text)
    text = re.sub(r'\\(small|footnotesize|scriptsize|normalsize|large|Large)\b', '', text)
    
    text = re.sub(r'\\textbf\{([^}]+)\}', r'\1', text)
    text = re.sub(r'\\textit\{([^}]+)\}', r'\1', text)
    text = re.sub(r'\\emph\{([^}]+)\}', r'\1', text)
    text = re.sub(r'\\texttt\{([^}]+)\}', r'\1', text)
    text = re.sub(r'\\url\{([^}]+)\}', r'\1', text)
    text = re.sub(r'\\href\{[^}]+\}\{([^}]+)\}', r'\1', text)
    
    text = text.replace(r'---', '—')
    text = text.replace(r'--', '–')
    text = text.replace(r'``', '"').replace(r"''", '"')
    text = text.replace(r'\%', '%')
    text = text.replace(r'\&', '&')
    text = text.replace(r'\$', '$')
    text = text.replace(r'\rightarrow', '→')
    text = text.replace(r'\kappa', 'κ')
    text = text.replace(r'\le', '≤')
    text = text.replace(r'\ge', '≥')
    text = text.replace('~', ' ')
    
    text = re.sub(r'[ \t]+', ' ', text)
    return text.strip()

def build_docx(sections_data, citations_list, output_file):
    doc = Document()
    
    # Page Setup: A4, 1-inch margins
    for s in doc.sections:
        s.page_width = Inches(8.27)
        s.page_height = Inches(11.69)
        s.top_margin = Inches(1.0)
        s.bottom_margin = Inches(1.0)
        s.left_margin = Inches(1.0)
        s.right_margin = Inches(1.0)
        
    # Set default Normal style font
    normal_style = doc.styles['Normal']
    normal_font = normal_style.font
    normal_font.name = 'Times New Roman'
    normal_font.size = Pt(12)
    normal_font.color.rgb = RGBColor(0, 0, 0)
    
    # Title
    title = sections_data.get("title", "")
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(12)
    p_title.paragraph_format.space_after = Pt(8)
    run_title = p_title.add_run(title)
    run_title.font.name = 'Times New Roman'
    run_title.font.size = Pt(16)
    run_title.font.bold = True
    
    # Authors
    authors = sections_data.get("authors", "")
    if authors:
        for a_line in authors.split('\n'):
            p_auth = doc.add_paragraph()
            p_auth.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_auth.paragraph_format.space_before = Pt(2)
            p_auth.paragraph_format.space_after = Pt(2)
            run_auth = p_auth.add_run(a_line.strip())
            run_auth.font.name = 'Times New Roman'
            run_auth.font.size = Pt(11)
            
    # Abstract
    abstract = sections_data.get("abstract", "")
    if abstract:
        p_abs_h = doc.add_paragraph()
        p_abs_h.paragraph_format.space_before = Pt(16)
        p_abs_h.paragraph_format.space_after = Pt(4)
        run_abs_h = p_abs_h.add_run("Abstract")
        run_abs_h.font.name = 'Times New Roman'
        run_abs_h.font.size = Pt(13)
        run_abs_h.font.bold = True
        
        p_abs = doc.add_paragraph()
        p_abs.paragraph_format.space_before = Pt(4)
        p_abs.paragraph_format.space_after = Pt(12)
        p_abs.paragraph_format.line_spacing = 1.5
        p_abs.paragraph_format.left_indent = Inches(0.25)
        p_abs.paragraph_format.right_indent = Inches(0.25)
        run_abs = p_abs.add_run(abstract)
        run_abs.font.name = 'Times New Roman'
        run_abs.font.size = Pt(11)
        run_abs.font.italic = True

    # Highlights
    highlights = sections_data.get("highlights", [])
    if highlights:
        p_hl_h = doc.add_paragraph()
        p_hl_h.paragraph_format.space_before = Pt(12)
        p_hl_h.paragraph_format.space_after = Pt(4)
        run_hl_h = p_hl_h.add_run("Highlights")
        run_hl_h.font.name = 'Times New Roman'
        run_hl_h.font.size = Pt(13)
        run_hl_h.font.bold = True
        
        for hl in highlights:
            p_hl = doc.add_paragraph(style='List Bullet')
            p_hl.paragraph_format.space_before = Pt(2)
            p_hl.paragraph_format.space_after = Pt(2)
            run_hl = p_hl.add_run(hl)
            run_hl.font.name = 'Times New Roman'
            run_hl.font.size = Pt(11)

    # Keywords
    keywords = sections_data.get("keywords", "")
    if keywords:
        p_kw = doc.add_paragraph()
        p_kw.paragraph_format.space_before = Pt(8)
        p_kw.paragraph_format.space_after = Pt(18)
        run_kwh = p_kw.add_run("Keywords: ")
        run_kwh.font.name = 'Times New Roman'
        run_kwh.font.size = Pt(11)
        run_kwh.font.bold = True
        run_kwt = p_kw.add_run(keywords)
        run_kwt.font.name = 'Times New Roman'
        run_kwt.font.size = Pt(11)

    # Sections Content
    for sec in sections_data.get("sections", []):
        stype = sec["type"]
        text = sec.get("text", "")
        
        if stype == "heading1":
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(18)
            p.paragraph_format.space_after = Pt(6)
            p.paragraph_format.keep_with_next = True
            r = p.add_run(text)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(14)
            r.font.bold = True
        elif stype == "heading2":
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(12)
            p.paragraph_format.space_after = Pt(4)
            p.paragraph_format.keep_with_next = True
            r = p.add_run(text)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(12)
            r.font.bold = True
        elif stype == "table":
            caption = sec.get("caption", "")
            if caption:
                p_cap = doc.add_paragraph()
                p_cap.paragraph_format.space_before = Pt(12)
                p_cap.paragraph_format.space_after = Pt(4)
                p_cap.paragraph_format.keep_with_next = True
                r_cap = p_cap.add_run(caption)
                r_cap.font.name = 'Times New Roman'
                r_cap.font.size = Pt(11)
                r_cap.font.bold = True
                
            rows = sec.get("rows", [])
            if rows:
                num_cols = max(len(r) for r in rows)
                table = doc.add_table(rows=len(rows), cols=num_cols)
                table.style = 'Table Grid'
                table.alignment = WD_TABLE_ALIGNMENT.CENTER
                for r_idx, row_data in enumerate(rows):
                    row = table.rows[r_idx]
                    for c_idx, cell_value in enumerate(row_data):
                        if c_idx < len(row.cells):
                            cell = row.cells[c_idx]
                            cell.text = str(cell_value)
                            for cp in cell.paragraphs:
                                cp.paragraph_format.space_before = Pt(2)
                                cp.paragraph_format.space_after = Pt(2)
                                for cr in cp.runs:
                                    cr.font.name = 'Times New Roman'
                                    cr.font.size = Pt(10)
                                    if r_idx == 0:
                                        cr.font.bold = True
                p_after = doc.add_paragraph()
                p_after.paragraph_format.space_after = Pt(6)
        elif stype == "figure":
            caption = sec.get("caption", "")
            p_fig = doc.add_paragraph()
            p_fig.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_fig.paragraph_format.space_before = Pt(10)
            p_fig.paragraph_format.space_after = Pt(10)
            r_fig = p_fig.add_run(caption)
            r_fig.font.name = 'Times New Roman'
            r_fig.font.size = Pt(11)
            r_fig.font.italic = True
            r_fig.font.bold = True
        elif stype == "bullet":
            p = doc.add_paragraph(style='List Bullet')
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.line_spacing = 1.5
            r = p.add_run(text)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(12)
        elif stype == "paragraph":
            if text.strip():
                p = doc.add_paragraph()
                p.paragraph_format.space_before = Pt(0)
                p.paragraph_format.space_after = Pt(6)
                p.paragraph_format.line_spacing = 1.5
                r = p.add_run(text)
                r.font.name = 'Times New Roman'
                r.font.size = Pt(12)

    # Declarations
    for decl_title, decl_text in sections_data.get("declarations", []):
        p_dec_h = doc.add_paragraph()
        p_dec_h.paragraph_format.space_before = Pt(16)
        p_dec_h.paragraph_format.space_after = Pt(4)
        p_dec_h.paragraph_format.keep_with_next = True
        r_dec_h = p_dec_h.add_run(decl_title)
        r_dec_h.font.name = 'Times New Roman'
        r_dec_h.font.size = Pt(13)
        r_dec_h.font.bold = True
        
        p_dec = doc.add_paragraph()
        p_dec.paragraph_format.space_before = Pt(0)
        p_dec.paragraph_format.space_after = Pt(6)
        p_dec.paragraph_format.line_spacing = 1.5
        r_dec = p_dec.add_run(decl_text)
        r_dec.font.name = 'Times New Roman'
        r_dec.font.size = Pt(12)

    # References
    if citations_list:
        p_ref_h = doc.add_paragraph()
        p_ref_h.paragraph_format.space_before = Pt(18)
        p_ref_h.paragraph_format.space_after = Pt(6)
        p_ref_h.paragraph_format.keep_with_next = True
        r_ref_h = p_ref_h.add_run("References")
        r_ref_h.font.name = 'Times New Roman'
        r_ref_h.font.size = Pt(14)
        r_ref_h.font.bold = True
        
        for num, ref in enumerate(citations_list, 1):
            p_ref = doc.add_paragraph()
            p_ref.paragraph_format.space_before = Pt(2)
            p_ref.paragraph_format.space_after = Pt(3)
            p_ref.paragraph_format.line_spacing = 1.15
            p_ref.paragraph_format.left_indent = Inches(0.3)
            p_ref.paragraph_format.first_line_indent = Inches(-0.3)
            r_ref = p_ref.add_run(f"[{num}] {ref}")
            r_ref.font.name = 'Times New Roman'
            r_ref.font.size = Pt(10)

    doc.save(str(output_file))

def main():
    print("Collecting manuscript content...")
    bib_dict = parse_bib_file(BASE_DIR / "references.bib")
    citation_map = {}
    
    sections_data = {
        "title": "The Next Generation of Software Testing: A Critical Review of Agentic AI, Self-Adaptive Test Frameworks, and Autonomous Quality Engineering",
        "authors": "Author (Independent Researcher)\nCorrespondence: author@example.com",
        "abstract": "",
        "highlights": [
            "Systematic review of agentic AI in software testing across 149 studies.",
            "18-category taxonomy from unit test generation to self-healing agents.",
            "Synthesis of QE safety: oracle circularity, self-healing, and security.",
            "Four candidate safety mechanisms proposed for autonomous test agents.",
            "Ten-item research roadmap for reaching high-autonomy quality engineering."
        ],
        "keywords": "software testing; test automation; agentic AI; large language models; self-healing test automation; systematic literature review; software quality assurance",
        "sections": [],
        "declarations": []
    }

    # Extract abstract from main.tex
    main_tex = (BASE_DIR / "main.tex").read_text(encoding="utf-8")
    m_abs = re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}', main_tex, re.DOTALL)
    if m_abs:
        sections_data["abstract"] = clean_latex(m_abs.group(1), bib_dict, citation_map)

    # Process each section file
    sec_files = [
        ("1. Introduction", BASE_DIR / "sections" / "01_introduction.tex"),
        ("2. Background and Motivation", BASE_DIR / "sections" / "02_background.tex"),
        ("3. Research Methodology", BASE_DIR / "sections" / "03_methodology.tex"),
        ("4. Related Work", BASE_DIR / "sections" / "04_related_work.tex"),
        ("5. Results and Analysis", BASE_DIR / "sections" / "05_results.tex"),
        ("6. Discussion", BASE_DIR / "sections" / "06_discussion.tex"),
        ("7. Threats to Validity", BASE_DIR / "sections" / "07_threats_to_validity.tex"),
        ("8. Conclusion and Future Work", BASE_DIR / "sections" / "08_conclusion.tex"),
    ]

    for title, s_path in sec_files:
        if not s_path.exists():
            continue
        sections_data["sections"].append({"type": "heading1", "text": title})
        content = s_path.read_text(encoding="utf-8")
        
        lines = content.split('\n')
        para_buf = []
        in_table = False
        table_rows = []
        table_caption = ""
        in_figure = False
        fig_cap_buf = []
        in_fig_cap = False

        def flush_para():
            nonlocal para_buf
            if para_buf:
                raw_p = " ".join(para_buf)
                cleaned = clean_latex(raw_p, bib_dict, citation_map)
                if cleaned:
                    sections_data["sections"].append({"type": "paragraph", "text": cleaned})
                para_buf = []

        for line in lines:
            line_str = line.strip()
            if not line_str or line_str.startswith('%'):
                flush_para()
                continue
            
            # Skip environment boundaries that shouldn't leak into prose
            if any(line_str.startswith(env) for env in [
                r'\begin{itemize}', r'\end{itemize}', r'\begin{enumerate}', r'\end{enumerate}',
                r'\begin{center}', r'\end{center}', r'\centering'
            ]):
                flush_para()
                continue

            if line_str.startswith(r'\label{'):
                continue
            
            # Subsections
            if r'\subsection{' in line_str:
                flush_para()
                m_sub = re.search(r'\\subsection\{([^}]+)\}', line_str)
                if m_sub:
                    sections_data["sections"].append({"type": "heading2", "text": m_sub.group(1)})
                continue

            # Tables
            if r'\begin{table}' in line_str:
                flush_para()
                in_table = True
                table_rows = []
                table_caption = ""
                continue
            
            if in_table:
                if r'\caption{' in line_str:
                    m_cap = re.search(r'\\caption\{([^}]+)\}', line_str)
                    if m_cap:
                        table_caption = clean_latex(m_cap.group(1), bib_dict, citation_map)
                elif '&' in line_str and not line_str.startswith('\\begin') and not line_str.startswith('\\caption'):
                    cells = [clean_latex(c, bib_dict, citation_map) for c in line_str.replace('\\\\', '').split('&')]
                    if any(cells):
                        table_rows.append(cells)
                elif r'\end{table}' in line_str:
                    in_table = False
                    if table_rows:
                        sections_data["sections"].append({"type": "table", "caption": table_caption, "rows": table_rows})
                continue

            # Figures
            if r'\begin{figure}' in line_str:
                flush_para()
                in_figure = True
                fig_cap_buf = []
                in_fig_cap = False
                continue

            if in_figure:
                if r'\caption{' in line_str:
                    in_fig_cap = True
                    part = line_str[line_str.find(r'\caption{') + 9:]
                    if '}' in part:
                        fig_cap_buf.append(part.split('}')[0])
                        in_fig_cap = False
                    else:
                        fig_cap_buf.append(part)
                elif in_fig_cap:
                    if '}' in line_str:
                        fig_cap_buf.append(line_str.split('}')[0])
                        in_fig_cap = False
                    else:
                        fig_cap_buf.append(line_str)
                elif r'\end{figure}' in line_str:
                    in_figure = False
                    fig_cap_text = clean_latex(" ".join(fig_cap_buf), bib_dict, citation_map)
                    sections_data["sections"].append({
                        "type": "figure",
                        "caption": f"[Figure: {fig_cap_text}]" if fig_cap_text else "[Figure]"
                    })
                continue

            # List items
            if line_str.startswith(r'\item'):
                flush_para()
                item_text = clean_latex(re.sub(r'^\\item\s*', '', line_str), bib_dict, citation_map)
                sections_data["sections"].append({"type": "bullet", "text": item_text})
                continue

            para_buf.append(line_str)
        flush_para()

    # Declarations
    sections_data["declarations"] = [
        ("Funding", "This review did not receive any specific grant from funding agencies in the public, commercial, or not-for-profit sectors. The author conducted this study independently without external financial support."),
        ("Declaration of Competing Interest", "The author declares that they have no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper."),
        ("Declaration of Generative AI and AI-Assisted Technologies", "During the preparation of this work, the author used AI-assisted tools for literature search assistance and text formatting. After using these tools, the author reviewed and edited the content as needed and takes full responsibility for the content of the publication."),
        ("Data Availability", "The search log, screening records (inclusion/exclusion decisions), and per-study data-extraction forms that support the findings of this review are maintained in a structured project archive and are available from the author upon reasonable request. All cited datasets and benchmarks are publicly available from their original sources referenced in the bibliography."),
        ("Acknowledgment", "The author thanks the anonymous reviewers for their constructive feedback.")
    ]

    # Build ordered citations list
    sorted_citations = sorted(citation_map.items(), key=lambda x: x[1])
    citations_list = [bib_dict.get(k, f"Citation key: {k}") for k, _ in sorted_citations]

    print(f"Generating DOCX via python-docx at: {OUTPUT_DOCX}")
    build_docx(sections_data, citations_list, OUTPUT_DOCX)
    print("DOCX file generated successfully!")

if __name__ == "__main__":
    main()
