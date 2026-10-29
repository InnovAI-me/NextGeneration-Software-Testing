"""Export the two manuscript chart datasets to editable .xlsx files for
submission, matching Elsevier's "charts as XLS/XLSX" guidance (the
compiled PDF charts are vector pgfplots graphics, not spreadsheet data,
so a separate editable source is provided here).
"""
from openpyxl import Workbook
from openpyxl.chart import BarChart, Reference

# --- Figure 1: Publication-year distribution (fig:pub-trend) ---
wb1 = Workbook()
ws1 = wb1.active
ws1.title = "Figure 1 data"
ws1.append(["Publication year", "Studies"])
pub_trend = [
    (2018, 1), (2019, 1), (2020, 4), (2021, 2), (2022, 1),
    (2023, 14), (2024, 46), (2025, 40), (2026, 39),
]
for year, count in pub_trend:
    ws1.append([year, count])

chart1 = BarChart()
chart1.title = "Publication-year distribution (149-study corpus)"
chart1.x_axis.title = "Publication year"
chart1.y_axis.title = "Studies"
data1 = Reference(ws1, min_col=2, min_row=1, max_row=len(pub_trend) + 1)
cats1 = Reference(ws1, min_col=1, min_row=2, max_row=len(pub_trend) + 1)
chart1.add_data(data1, titles_from_data=True)
chart1.set_categories(cats1)
ws1.add_chart(chart1, "D2")
wb1.save("Figure_1_data.xlsx")

# --- Figure 2: Study counts per taxonomy category (fig:category-dist) ---
wb2 = Workbook()
ws2 = wb2.active
ws2.title = "Figure 2 data"
ws2.append(["Category", "Studies"])
category_dist = [
    ("Mutation testing with LLMs", 2),
    ("Agentic software engineering foundations", 3),
    ("API testing", 3),
    ("LLM-based fuzzing", 3),
    ("Bug reproduction and test-based issue validation", 3),
    ("Self-adaptive systems and runtime testing", 4),
    ("Benchmarks and data contamination", 4),
    ("Mobile GUI agents", 4),
    ("Multi-agent and agentic test generation", 5),
    ("Industrial case studies", 5),
    ("GUI, mobile and web testing agents", 6),
    ("Unit test generation with LLMs", 8),
    ("CI failure triage and flaky-test classification", 9),
    ("Surveys and literature reviews", 10),
    ("Test oracles and assertions", 10),
    ("Flaky tests and self-healing tests", 11),
    ("Human factors: trust and acceptance", 15),
    ("Security of coding and testing agents", 15),
]
for category, count in category_dist:
    ws2.append([category, count])

chart2 = BarChart()
chart2.type = "bar"  # horizontal, matching the xbar orientation in the PDF
chart2.title = "Study counts per taxonomy category"
chart2.x_axis.title = "Studies"
chart2.y_axis.title = "Category"
data2 = Reference(ws2, min_col=2, min_row=1, max_row=len(category_dist) + 1)
cats2 = Reference(ws2, min_col=1, min_row=2, max_row=len(category_dist) + 1)
chart2.add_data(data2, titles_from_data=True)
chart2.set_categories(cats2)
ws2.add_chart(chart2, "D2")
wb2.save("Figure_2_data.xlsx")

print("Wrote Figure_1_data.xlsx and Figure_2_data.xlsx")
