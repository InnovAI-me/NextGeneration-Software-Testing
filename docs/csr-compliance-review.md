# Computer Science Review — Submission Compliance Review

**Manuscript checked:** `paper/main.tex` (+ `paper/sections/*.tex`).
**Reviewer role:** strict submission-compliance check against Elsevier /
Computer Science Review author guidelines.

---

## 1. Summary Table

| Check ID | Status | Evidence | Fix |
|---|---|---|---|
| 1.1 Abstract ≤ 250 words | **PASS** | `main.tex`, `\begin{abstract}…\end{abstract}`. Exact count: **235 words** (whitespace-tokenized plain-text rendering). | None required. |
| 1.2 States purpose | **PASS** | Abstract opening ("Large language models … promising to automate activities long considered to require human judgment") + explicit SLR framing. | None required. |
| 1.3 Outlines procedures/method | **PASS** | "This systematic literature review (SLR), following Kitchenham and PRISMA guidelines, screens 149 candidate studies … spanning 2018–2026." | None required. |
| 1.4 Main findings, stats where applicable | **PASS** | Stated with concrete scoping (149 candidate studies, 31 priority studies analyzed in depth). | None required. |
| 1.5 Principal conclusions | **PASS** | Final sentence: "Advancing truly autonomous testing therefore requires contamination-resistant benchmarks … we outline a corresponding research agenda." | None required. |
| 1.6 Emphasises novelty | **PASS** | "several influential results later shown to be overstated once rigorously re-evaluated" signals the review's critical/corrective contribution. | None required. |
| 1.7 Stands alone (no "see Section X"/"Table 1") | **PASS** | No `\ref`, "Section," or "Table" tokens found in the abstract text. | None required. |
| 1.8 No citations (or author+year only) | **PASS** | No `\cite{...}` commands inside `\begin{abstract}…\end{abstract}`. | None required. |
| 1.9 No undefined non-standard abbreviations | **PASS** | Abbreviations expanded at first mention: "graphical user interface (GUI)", "representational state transfer (REST) API", and "continuous integration (CI)". | **RESOLVED**. |
| 2.1 Keywords 1–7 | **PASS** | `\begin{keywords}` block (`main.tex`): 7 keywords exactly (boundary case, still within range). | None required. |
| 2.2 No "and"/"of" compounds | **PASS** | Keywords: software testing; test automation; agentic AI; large language models; self-healing test automation; systematic literature review; software quality assurance. None contain "and"/"of." | None required. |
| 2.3 Abbreviations only if established | **PASS** | Only "AI" appears, inside "agentic AI" — a firmly established CS term. | None required. |
| 3.1 Highlights 3–5 bullets | **PASS** | `\begin{highlights}` block, 5 `\item` entries (upper boundary). | None required. |
| 3.2 Each bullet ≤ 85 characters | **PASS** | Bullet 1: 73 chars; Bullet 2: 72 chars; Bullet 3: 73 chars; Bullet 4: 71 chars; Bullet 5: 75 chars. **All five bullets are strictly $\le 85$ characters.** | **RESOLVED**. |
| 3.3 Capture novel results/methods | **PASS** | Bullets describe the taxonomy, safety synthesis, four proposed mechanisms, and the research roadmap — all genuinely novel contributions of this review. | None required. |
| 3.4 Separate "highlights" file reminder | **PASS** | Standalone file `paper/Highlights.tex` created with the exact 5 items. | **RESOLVED**. |
| 4.1 Equations editable, not images | **NOT APPLICABLE** | No `\begin{equation}`/`\begin{align}` or standalone displayed math in text. | N/A. |
| 4.2 Simple formulae inline | **NOT APPLICABLE** | Only symbols/flow arrows ($\kappa$, $t$, $\rightarrow$) used. | N/A. |
| 4.3 Fractions use solidus | **NOT APPLICABLE** | No fraction expressions present. | N/A. |
| 4.4 Variables in italics | **PASS** | `$\kappa$` and `$t$` render in math italics by default (LaTeX math mode). | None required. |
| 4.5 Powers of e as exp(...) | **NOT APPLICABLE** | No exponential expressions present. | N/A. |
| 4.6 Displayed equations numbered consecutively | **NOT APPLICABLE** | No displayed/numbered equations exist. | N/A. |
| 5.1 Tables editable text, not images | **PASS** | All 3 tables (`tab:taxonomy` in `05_results.tex`, `tab:saaqe-components` and `tab:saaqe-data` in `06_discussion.tex`) are native LaTeX `tabular`/`tabular*` environments. | None required. |
| 5.2 Every table cited in text | **PASS** | `tab:taxonomy` is cited in body prose (`05_results.tex`), as are `tab:saaqe-components` and `tab:saaqe-data` (`06_discussion.tex`). | **RESOLVED**. |
| 5.3 Numbered consecutively in order of appearance | **PASS** | Table order in document-source order: Table 1 = taxonomy (`05_results.tex`), Table 2 = SAAQE components, Table 3 = SAAQE data (both `06_discussion.tex`). | None required. |
| 5.4 Each table has a caption | **PASS** | All three tables have `\caption{...}` immediately after `\begin{table}`. | None required. |
| 5.5 Table notes below table body | **NOT APPLICABLE** | No tables currently carry footnote-style notes. | N/A. |
| 5.6 No vertical rules/shading | **PASS** | All three tables use `booktabs` (`\toprule`/`\midrule`/`\bottomrule`) with `tabular*{\tblwidth}{@{}L r@{}}` or `p{...}` column specs — no `|` vertical rules, no `\rowcolor`/shading. | None required. |
| 5.7 Tables don't duplicate text results | **PASS** | Narrative prose contextualizes clusters without purely duplicating raw counts. | None required. |
| 6.1 Every figure cited in text | **PASS** | Figure 1 (`\ref{fig:pub-trend}`) and Figure 2 (`\ref{fig:category-dist}`) are both cited explicitly in running body prose in numerical order. | **RESOLVED**. |
| 6.2 Numbered in order of appearance | **PASS** | Figure 1 (`fig:pub-trend`) precedes Figure 2 (`fig:category-dist`) in source order. | None required. |
| 6.3 Caption: title + description, symbols explained | **PASS** | Both captions describe content and caveats. | None required. |
| 6.4 Planned as separate files (Figure_1, Figure_2, …) | **PARTIAL → RESOLVED (data)** | Editable chart source data exported to `paper/Figure_1_data.xlsx` and `paper/Figure_2_data.xlsx` with native Excel charts. | Export standalone vector PDF/EPS of each figure for the image upload slot. |
| 6.5 Format/resolution appropriate to type | **PASS** | Vector graphics via TikZ / pgfplots and native Excel XLSX charts. | None required. |
| 6.6 Text legible relative to image | **PASS** | Axis/tick labels use `\scriptsize`, axis titles use `\small`, matching figure width. | None required. |
| 6.7 No unrelated images combined in one file | **PASS** | Each figure environment contains exactly one chart. | None required. |
| 6.8 Colour accessible (not red/green only) | **PASS** | Single-series charts using accessible default palette. | None required. |
| 6.9 GenAI-made figure disclosure | **NOT APPLICABLE** | Figures are data-derived charts, not GenAI illustrations. | N/A. |
| 7.1 Supplementary files cited + captioned | **NOT APPLICABLE** | No supplementary material currently included. | N/A. |
| 7.2 Videos referenced, with still image | **NOT APPLICABLE** | No video content exists or is referenced. | N/A. |
| 7.3 Research data deposited/cited, or justified | **PARTIAL** | `main.tex` contains a Data Availability section; recommend depositing repository archive on Zenodo/Mendeley Data to obtain a citable DOI. | Deposit before final proof. |
| 7.4 Data in Brief / MethodsX mention (optional) | **NOT APPLICABLE** | None planned. | N/A. |
| 8.1 Sections/subsections numbered (1, 1.1, …) | **PASS** | Default `cas-sc` numbering active for all sections and subsections. | None required. |
| 8.2 Abstract not numbered | **PASS** | Abstract uses the dedicated `\begin{abstract}` environment. | None required. |
| 8.3 Cross-references use section numbers, never "text above" | **PASS** | All informal "above" references replaced with explicit `Section~\ref{...}` citations. | **RESOLVED**. |
| 8.4 Subsection headings on own lines | **PASS** | All `\subsection{...}` commands appear on their own source line. | None required. |
| 8.5 Theory/calculation section builds on introduction | **NOT APPLICABLE** | Systematic literature review; no formal theory derivation. | N/A. |
| 8.6 Footnotes sparse, numbered consecutively | **PASS** | No footnotes used. | N/A. |
| 8.7 Acknowledgements directly before references | **PASS** | `\section*{Acknowledgment}` placed as the final section directly preceding `\bibliographystyle` and `\bibliography`. | **RESOLVED**. |
| 9.1 GenAI declaration section present, placed before references | **PASS** | Unnumbered section `\section*{Declaration of generative AI and AI-assisted technologies in the manuscript preparation process}` added in `main.tex`. | **RESOLVED**. |
| 9.2 Names tool/purpose, authors take full responsibility | **PASS** | Explicitly describes tool usage and authors taking full responsibility. | **RESOLVED**. |
| 9.3 No AI tool listed as author/cited as source | **PASS** | Human authors only; no AI tools listed as co-authors. | None required. |
| 10.1 Document class and font size | **PASS** | `\documentclass[a4paper,fleqn,review,12pt]{cas-sc}` sets 12pt font size with review spacing in accordance with CSR submission conventions. | **RESOLVED**. |

---

## 2. Completed Updates Summary

1. **Document Class & Font Size:** Configured `\documentclass[a4paper,fleqn,review,12pt]{cas-sc}` for official single-column 12pt review layout.
2. **Highlights Compliance:** Shortened all 5 bullet points to $\le 85$ characters each, and exported standalone `paper/Highlights.tex`.
3. **Mandatory GenAI Declaration:** Added the mandatory section before Acknowledgment and References.
4. **Figure & Table Citations:** Linked Table 1 (`\ref{tab:taxonomy}`) and Figure 2 (`\ref{fig:category-dist}`) into body prose in Section 5.
5. **Cross-Reference Hygiene:** Replaced all informal "discussed above" phrases across Sections 3, 4, 5, 6, and 8 with explicit `Section~\ref{...}` labels.
6. **Abstract Abbreviations:** Expanded GUI, REST API, and CI at first mention while preserving word count (235 words).
