# Reading-Focus Guide - Remaining Studies (not in the Top-28 core set)

For each remaining study, read only the section(s) that address the
**research gap / contribution** listed below (Introduction + the specific
Results/Discussion subsection), rather than the full paper cover-to-cover.
Full-text reading is still required before any inclusion/exclusion or
citation decision (see `literature-review/inclusion-exclusion-criteria.md`)
-- this guide only tells you *where to focus* your reading time.

Priority legend: **MEDIUM** = peer-reviewed/known venue, read in full when time
allows; **LOW** = preprint/grey literature/thesis, skim the focus item first and
verify venue/peer-review status before citing; **SKIP** = currently unverifiable
(no accessible abstract/copy found yet) - needs manual sourcing first.

Covers 81 of 113 studies (the other 32 are the core
set already listed separately as 'key papers to read first').

## API testing (2)

| Study | Year | Venue | Title | Focus when reading | Priority |
|---|---|---|---|---|---|
| P2 | 2025 | arXiv | AutoRestTest tool paper | Usable tooling for multi-agent API testing | MEDIUM (peer-reviewed/known venue) |
| P3 | 2024 | ICSE (New Ideas and Emerging Results) | Leveraging Large Language Models to Improve REST API Testing (RESTGPT) | Extracting testable rules from natural-language descriptions in API specifications | MEDIUM (peer-reviewed/known venue) |

## Benchmarks and data contamination (4)

| Study | Year | Venue | Title | Focus when reading | Priority |
|---|---|---|---|---|---|
| SLR029 | 2025 | ICLR | TestGenEval: A Real World Unit Test Generation and Test Completion Benchmark | Earlier benchmarks lacked real-world tests and mutation score; LLMs still perform poorly | MEDIUM (peer-reviewed/known venue) |
| SLR030 | 2025 | LLM4Code workshop at ICSE | Are Large Language Models Memorizing Bug Benchmarks? | Strong memorization of Defects4J by some models, so results on it may be inflated | MEDIUM (peer-reviewed/known venue) |
| SLR031 | 2023 | arXiv | The GitHub Recent Bugs Dataset for Evaluating LLM-based Debugging Applications | Need for bugs collected after model training cut-offs | MEDIUM (peer-reviewed/known venue) |
| SLR032 | 2024 | arXiv (check venue) | On Inter-dataset Code Duplication and Data Leakage in Large Language Models | Large overlap between Defects4J and training corpora such as The Stack | LOW (grey-lit/preprint - verify before citing) |

## Bug reproduction and test-based issue validation (1)

| Study | Year | Venue | Title | Focus when reading | Priority |
|---|---|---|---|---|---|
| SLR027 | 2023 | arXiv | Follow-up evaluation of LIBRO with 15 LLMs | Open-source models reach about 70% of the closed model's performance; reproducibility with open models | MEDIUM (peer-reviewed/known venue) |

## CI failure triage and flaky-test classification (6)

| Study | Year | Venue | Title | Focus when reading | Priority |
|---|---|---|---|---|---|
| SLR042 | 2025 | ASE (industry showcase) | LogSage: An LLM-Based Framework for CI/CD Failure Detection and Remediation with Industrial Validation | Root-cause analysis of CI failures from noisy logs | MEDIUM (peer-reviewed/known venue) |
| SLR043 | 2026 | Chalmers master's thesis | LLM-based log analysis in industrial CI environments | Practitioner views and workflow impact of LLM log analysis | LOW (grey-lit/preprint - verify before citing) |
| SLR045 | 2026 | PROFES workshop / arXiv | Chatting about flaky tests with standard LLMs: an empirical exploration | General LLMs are only marginally better than random guessing | MEDIUM (peer-reviewed/known venue) |
| SLR046 | 2025 | arXiv | Fine-tuning and few-shot learning for flaky-test detection and classification | Comparing fine-tuning with few-shot learning for flakiness | MEDIUM (peer-reviewed/known venue) |
| SLR047 | 2024 | arXiv | A Large Language Model Approach to Identify Flakiness in C++ Projects | Flakiness research focuses on Java and Python; C++ is underexplored | MEDIUM (peer-reviewed/known venue) |
| SLR048 | 2026 | arXiv | NeuroFlake: A Neuro-Symbolic LLM Framework for Flaky Test Classification | Different root causes of flakiness need different fixes | MEDIUM (peer-reviewed/known venue) |

## Flaky tests and self-healing tests (3)

| Study | Year | Venue | Title | Focus when reading | Priority |
|---|---|---|---|---|---|
| H1 | 2025 | ICST (journal-first, check) | FlakyFix: Using Large Language Models for Predicting Flaky Test Fix Categories and Test Code Repair | Only flakiness caused by test code; 51–83% of repaired tests pass | LOW (grey-lit/preprint - verify before citing) |
| H2 | — | University of Helsinki thesis | LLM-based self-healing locators for Robot Framework web UI tests | Locator repair works only with large LLMs; small models fail | LOW (grey-lit/preprint - verify before citing) |
| H3 | 2026 | arXiv | Paper with a related-work review of locator repair | Cites up to 73% of industrial Selenium failures as caused by broken locators, not real regressions | MEDIUM (peer-reviewed/known venue) |

## GUI, mobile and web testing agents (5)

| Study | Year | Venue | Title | Focus when reading | Priority |
|---|---|---|---|---|---|
| G2 | 2023 | arXiv | Chatting with GPT-3 for Zero-Shot Human-Like Mobile Automated GUI Testing | Earlier, smaller-scale version of GPTDroid | MEDIUM (peer-reviewed/known venue) |
| G3 | 2023 | arXiv | Autonomous Large Language Model Agents Enabling Intent-Driven Mobile GUI Testing (DroidAgent) | Moves from coverage to intent-driven goals; task-success figures differ between versions | MEDIUM (peer-reviewed/known venue) |
| G4 | 2024 | arXiv | NaviQAte: Functionality-Guided Web Application Navigation | Task success only about 44%; exploring broad web functionality remains hard | MEDIUM (peer-reviewed/known venue) |
| G5 | 2024 | arXiv | A Feature-Based Approach to Generating Comprehensive End-to-End Tests (AutoE2E) | No benchmark existed for feature coverage of end-to-end tests (introduces E2EBench) | MEDIUM (peer-reviewed/known venue) |
| G6 | 2026 | arXiv | WebTestPilot: VLM agents testing web apps against natural-language specifications | Telling LLM hallucinations apart from real application bugs when inferring oracles | MEDIUM (peer-reviewed/known venue) |

## Human factors: trust and acceptance (6)

| Study | Year | Venue | Title | Focus when reading | Priority |
|---|---|---|---|---|---|
| SLR054 | 2024 | IEEE Transactions on Software Engineering, 50(5), 1264–1280 | Shaken, Not Stirred: How Developers Like Their Amplified Tests | How maintainers judge and edit generated tests before accepting them | MEDIUM (peer-reviewed/known venue) |
| SLR055 | 2023 | ICSE (journal-first) | Developer-Centric Test Amplification | Generated tests must be understandable and editable by developers | MEDIUM (peer-reviewed/known venue) |
| SLR056 | 2025 | arXiv | Mapping the Trust Terrain: LLMs in Software Engineering – Insights and Perspectives | Trust varies by task; developers hesitate to rely on LLMs for test generation | MEDIUM (peer-reviewed/known venue) |
| SLR057 | 2024 | arXiv | Generating verifications for manual tests with LLMs | Professional testers agreed with only about 40% of generated verifications | MEDIUM (peer-reviewed/known venue) |
| SLR058 | 2025 | TU Delft master's thesis | PyTestGuard: IDE support for developers using LLM-generated unit tests | Developers want quality feedback before trusting generated tests | LOW (grey-lit/preprint - verify before citing) |
| SLR059 | 2024 | TU Delft PhD thesis | Test Amplification For and With Developers | Developer involvement in automated test amplification | LOW (grey-lit/preprint - verify before citing) |

## Industrial case studies (4)

| Study | Year | Venue | Title | Focus when reading | Priority |
|---|---|---|---|---|---|
| SLR037 | 2025 | arXiv | Test code generation at Ericsson using Program Analysis Augmented Fine Tuned LLMs | Plain prompting invents functions that don't exist; needs retrieval and static analysis | MEDIUM (peer-reviewed/known venue) |
| SLR038 | 2024 | arXiv | Exploring the Integration of Large Language Models in Industrial Test Maintenance Processes | Predicting which tests need maintenance after a code change | MEDIUM (peer-reviewed/known venue) |
| SLR039 | 2025 | CIbSE | Unit Test Generation with LLMs in Industrial Environments: Challenges, Evolution, and Practical Lessons | Few long-term industrial studies; maintainability of generated tests | MEDIUM (peer-reviewed/known venue) |
| SLR040 | 2026 | arXiv | Context Matters: Improving the Practical Reliability of LLM-Based Unit Test Generation (CATGen) | Generated tests often fail to compile in industrial code | MEDIUM (peer-reviewed/known venue) |

## LLM-based fuzzing (1)

| Study | Year | Venue | Title | Focus when reading | Priority |
|---|---|---|---|---|---|
| Z3 | 2023 | arXiv (check venue) | Large Language Models are Edge-Case Fuzzers (FuzzGPT) | Generating unusual edge-case inputs rather than typical programs | LOW (grey-lit/preprint - verify before citing) |

## Mobile GUI agents (2)

| Study | Year | Venue | Title | Focus when reading | Priority |
|---|---|---|---|---|---|
| SLR034 | 2024 | arXiv | AUITestAgent: Automatic Requirements Oriented GUI Function Testing | Verifying stated requirements in GUI tests; industrial use at Meituan | MEDIUM (peer-reviewed/known venue) |
| SLR035 | 2024 | arXiv | Vision-driven Automated Mobile GUI Testing via Multimodal Large Language Model (VisionDroid) | Lack of oracles limits detection to crash bugs; targets non-crash functional bugs | MEDIUM (peer-reviewed/known venue) |

## Multi-agent and agentic test generation (1)

| Study | Year | Venue | Title | Focus when reading | Priority |
|---|---|---|---|---|---|
| SLR021 | 2025 | arXiv | HPCAgentTester: Multi-agent test generation for HPC code | Testing parallel code (OpenMP, MPI) is largely unaddressed by LLM test tools | MEDIUM (peer-reviewed/known venue) |

## Mutation testing with LLMs (2)

| Study | Year | Venue | Title | Focus when reading | Priority |
|---|---|---|---|---|---|
| M1 | 2024 | arXiv | A Comprehensive Study on Large Language Models for Mutation Testing | LLM mutants are closer to real bugs than rule-based ones; headline figures differ between versions | MEDIUM (peer-reviewed/known venue) |
| M2 | 2024 | arXiv | LLMorpheus: Mutation Testing using Large Language Models | Fixed mutation operators cannot produce realistic, bug-like mutants; JavaScript only | MEDIUM (peer-reviewed/known venue) |

## Original list (29 papers) (29)

| Study | Year | Venue | Title | Focus when reading | Priority |
|---|---|---|---|---|---|
| SLR060 | 2026 | ResearchGate upload (venue unknown) | From AI-Assisted Testing to Autonomous Quality Engineering: Agent-Based Investigation and Reproduction of CI Failures | Not confirmed: the abstract could not be read and no other copy was found | SKIP (unverifiable) |
| SLR061 | 2026 | arXiv preprint | Trajectory-Aware Benchmark Subset Selection for Cost-Efficient Software Engineering Agent Regression Testing | Re-running full benchmarks after each change to a coding agent is too costly, and random subsets are unreliable; a 10% trajectory-based subset keeps error under 5% at about 90% lower token cost | MEDIUM (peer-reviewed/known venue) |
| SLR062 | 2026 | EMNLP 2026 (Main Conference) | Framework and Benchmark for Code-Driven Agentic Testing in Web Development | Existing web-testing evaluations use fixed checklists, so the real bug-finding ability of vision-language models is untested; on the new CATTest benchmark (102 AI-generated web apps), mainstream models perform poorly | MEDIUM (peer-reviewed/known venue) |
| SLR063 | 2026 | SCAM 2026 (Engineering Track) | Code Health in LLM-Based Test Generation: Effectiveness and Token Efficiency | Whether code maintainability affects how well LLMs generate tests; code health is only a modest predictor of test effectiveness, but healthier code needs fewer input tokens | MEDIUM (peer-reviewed/known venue) |
| SLR064 | 2026 | arXiv preprint | Testing and Evaluation of Agentic AI Systems In Military Command and Control | Agentic properties break eight assumptions behind established test and evaluation methods (review of 240 practices), so passing tests may not show how a fielded system will behave | MEDIUM (peer-reviewed/known venue) |
| SLR065 | 2026 | arXiv preprint | On the risk of coding before testing: An empirical study on LLM-based test generation workflow | Tests generated by an LLM after seeing faulty code inherit its errors: they detect 14% of faults versus 25% for independently generated tests. This questions whether LLM tests are an independent check | MEDIUM (peer-reviewed/known venue) |
| SLR066 | 2026 | International Journal of Technology (IJTech), Vol. 17, No. 4, DOI 10.14716/ijtech.v17i4.8380 | Agentic Artificial Intelligence in Software Engineering: Integration Points, Architectural Frameworks, Empirical Evaluation, and Governance | Lack of guidance on where agentic AI fits in the SDLC and how governance constrains it; four enterprise cases suggest shorter cycle times and higher test coverage, but the authors say results are context-specific | MEDIUM (peer-reviewed/known venue) |
| SLR067 | 2026 | ORCAS 2026 workshop, co-located with SAFECOMP 2026 | (Over)Reliance on Test Agents in AI-Assisted Software Testing | Engineers may accept test-agent outputs without checking them; frames this as a loss of control over test design and as weak assurance evidence, and proposes a framework for studying it | MEDIUM (peer-reviewed/known venue) |
| SLR068 | 2026 | arXiv preprint (submitted to Artificial Intelligence Review) | Beyond Component Testing: Validating Agentic AI Systems | Mapping study of 262 papers: work on validating agentic AI focuses on behaviour, while validity over time is the least covered area (14 papers); whole decision sequences need validating, not single outputs | MEDIUM (peer-reviewed/known venue) |
| SLR069 | 2026 | arXiv preprint | From Determinism to Delegation: AI-Native Software Engineering and the Evolution of the Agentic Engineer | Position paper: the shift from writing code to supervising agents changes how correctness and accountability work; argues oversight is the key engineering skill. No empirical evaluation | MEDIUM (peer-reviewed/known venue) |
| SLR070 | 2026 | OpenAI report, also arXiv 2606.26959 (grey literature) | The Shift to Agentic AI: Evidence From Codex | Usage data on adoption of agentic coding tools; growing delegation of long tasks. Says nothing specific about testing quality, and internal figures may be biased | LOW (grey-lit/preprint - verify before citing) |
| SLR071 | 2026 | arXiv preprint | AI Harness Engineering: A Runtime Substrate for Foundation-Model Software Agents | Agent unreliability is usually blamed on the model alone; argues the runtime "harness" matters and defines four levels (H0–H3). Higher levels produce more verification evidence (reproduction logs, verification reports). Validated on a single controlled task | MEDIUM (peer-reviewed/known venue) |
| SLR072 | 2026 | arXiv preprint | Rethinking Software Engineering for Agentic AI Systems | Position paper: as code becomes cheap, SE should reorganise around orchestration, rigorous verification of AI output, and human–AI teamwork. No empirical evaluation | MEDIUM (peer-reviewed/known venue) |
| SLR073 | 2026 | FSE 2026 (Software Engineering Education track) | Large Language Models for Software Testing Education: an Experience Report | Little evidence on how students' ad hoc LLM use affects testing skills; finds weak prompting habits, especially for test-script generation | MEDIUM (peer-reviewed/known venue) |
| SLR074 | 2026 | arXiv preprint | Real Faults in Model Context Protocol (MCP) Software: a Comprehensive Taxonomy | No systematic understanding of real faults in MCP servers, which connect agents to tools; first large taxonomy (five categories), confirmed by practitioners. Relevant to testing agent tool chains | MEDIUM (peer-reviewed/known venue) |
| SLR075 | 2026 | MSR 2026 | Testing with AI Agents: An Empirical Study of Test Generation Frequency, Quality, and Coverage | Little is known about tests written by coding agents in real repositories; agents add about 16.4% of test-adding commits, with longer tests, more assertions and coverage comparable to human tests | MEDIUM (peer-reviewed/known venue) |
| SLR076 | 2026 | XP 2026 Workshop on Human-AI Collaboration in Agile Teams | Human-AI Collaboration for Scaling Agile Regression Testing: An Agentic-AI Teammate from Manual to Automated Testing | Test specifications pile up faster than they can be automated; industrial case at Hacon (Siemens): an agent copilot speeds up script writing, but human review is still needed for maintainability and domain correctness | MEDIUM (peer-reviewed/known venue) |
| SLR077 | 2026 | arXiv preprint | EGSS: Entropy-guided Stepwise Scaling for Reliable Software Engineering | High compute cost and unreliable candidate selection limit test-time scaling of agents; entropy-guided search plus test-suite augmentation raises SWE-Bench-Verified resolution by about 5–10% with 28% fewer tokens | MEDIUM (peer-reviewed/known venue) |
| SLR078 | 2026 | Anthropic report (grey literature) | 2026 Agentic Coding Trends Report | Industry trend report: developers use AI in about 60% of work but can fully delegate only 0–20% of tasks; names human oversight and security risk as trends. No peer review or testing-specific evidence | LOW (grey-lit/preprint - verify before citing) |
| SLR079 | 2025 | ResearchGate upload (venue unknown) | AI-Driven Automation of Software Testing to Enhance Software Quality and Enable Agentic AI | Not confirmed: the abstract could not be read and no other copy was found | SKIP (unverifiable) |
| SLR080 | 2024 | IJARCST, Vol. 7, No. 5, DOI 10.15662/IJARCST.2024.0705017 | AI-Powered Enterprise Quality Engineering through Intelligent Test Automation and Secure Cloud Infrastructure Platforms | Proposes a combined model (ML test creation, self-repairing tests, defect forecasting, cloud orchestration); benefits are claimed rather than shown in a rigorous evaluation | MEDIUM (peer-reviewed/known venue) |
| SLR081 | 2025 | Listed as IJGIS 2025 (author Prathap Raghavan, per Academia.edu) | A Self-Adaptive, AI-Powered Testing Framework for Cross-Platform Systems: An Architectural Design and Industrial Evaluation | Script-based cross-platform test automation is brittle and costly to maintain; proposes an ML-based self-adaptive framework. Industrial results could not be checked | LOW (grey-lit/preprint - verify before citing) |
| SLR082 | 2025 | ResearchGate upload (venue unknown) | AI-Driven Test Automation Frameworks for the Modern Software Quality Engineering | Not confirmed: the abstract could not be read and no other copy was found | SKIP (unverifiable) |
| SLR083 | 2025 | arXiv preprint | Software Testing with Large Language Models: An Interview Study with Practitioners | Testers learn to use LLMs by trial and error, without guidance; 15 interviews show an iterative prompting cycle and a strong need for human oversight because of hallucinations | MEDIUM (peer-reviewed/known venue) |
| SLR084 | 2025 | arXiv preprint | Large Language Models for Software Testing: A Research Roadmap | The field grows too fast to follow and lacks an organised overview; partially systematic review that groups studies and lists open challenges | MEDIUM (peer-reviewed/known venue) |
| SLR085 | 2025 | arXiv preprint (4-page position paper) | Agentic AI for Software: thoughts from Software Engineering community | Attention on code generation overlooks testing and repair, where trust matters; argues trustworthy agents need inferred developer intent (specifications) and AI-based verification | MEDIUM (peer-reviewed/known venue) |
| SLR086 | 2025 | arXiv preprint | AI Agentic Programming: A Survey of Techniques, Challenges, and Opportunities | Lack of structured understanding of coding agents; taxonomy of agent behaviour and architecture, but not testing-specific | MEDIUM (peer-reviewed/known venue) |
| SLR087 | 2025 | arXiv preprint (submitted 31 Dec 2024) | The Potential of LLMs in Automating Software Testing: From Generation to Reporting | Manual testing is slow and costly; an agent framework that generates unit tests and automates execution and reporting for Python and Java. Evaluation appears limited | MEDIUM (peer-reviewed/known venue) |
| SLR088 | 2020 | arXiv (submitted to AIST 2020 workshop) | Agent-Based Software Testing: A Definition and Systematic Mapping Study | First mapping of agent-based testing before LLMs (classic agent architectures, mostly the JADE framework); finds regression testing is a gap | MEDIUM (peer-reviewed/known venue) |

## Security of coding and testing agents (3)

| Study | Year | Venue | Title | Focus when reading | Priority |
|---|---|---|---|---|---|
| SLR051 | 2026 | ICML | RepoGuardBench: Repository-Borne Prompt Injection Attacks and Lightweight Defenses for Local Coding Agents | Attacks hidden in repositories; no defense was a clear winner | MEDIUM (peer-reviewed/known venue) |
| SLR052 | 2026 | arXiv | Memory-file prompt injection against coding agents | Injected memory files can attack current and future agent sessions | MEDIUM (peer-reviewed/known venue) |
| SLR053 | 2026 | Cloud Security Alliance research note | AI Coding Agent Sandbox Escapes: The Trust Handoff Flaw | Sandboxing alone does not stop agents being misused; grey literature | MEDIUM (peer-reviewed/known venue) |

## Self-adaptive systems and runtime testing (4)

| Study | Year | Venue | Title | Focus when reading | Priority |
|---|---|---|---|---|---|
| SA1 | 2018 | arXiv (check venue) | A Testing Scheme for Self-Adaptive Software Systems with Architectural Runtime Models | Notes the lack of a systematic approach to testing self-adaptive systems | LOW (grey-lit/preprint - verify before citing) |
| SA2 | 2019 | Book chapter (check) | Perpetual Assurances for Self-Adaptive Systems | Testing alone cannot guarantee that a self-adaptive system meets its requirements | LOW (grey-lit/preprint - verify before citing) |
| SA3 | 2021 | SEAMS (check) | How do we Evaluate Self-adaptive Software Systems? | Evaluation practice for MAPE-K-based systems is inconsistent | LOW (grey-lit/preprint - verify before citing) |
| SA4 | 2021 | Software Quality Journal, 29(2), 555–593 (library record; find the publisher DOI) | A survey on runtime testing of dynamically adaptable and distributed systems | Testing systems whose structure changes at runtime | LOW (grey-lit/preprint - verify before citing) |

## Surveys and literature reviews (4)

| Study | Year | Venue | Title | Focus when reading | Priority |
|---|---|---|---|---|---|
| SLR005 | 2024 | arXiv | From LLMs to LLM-based Agents for Software Engineering: A Survey of Current, Challenges and Future | Notes there is no unified standard or benchmark for deciding what counts as an LLM-based agent | MEDIUM (peer-reviewed/known venue) |
| SLR007 | 2025 | arXiv | Large Language Models for Unit Test Generation: Achievements, Challenges, and Opportunities | Unit level only; reports weak fault detection and no standard benchmarks | MEDIUM (peer-reviewed/known venue) |
| SLR008 | 2025 | arXiv | Systematic literature review of LLMs in unit testing (to March 2025) | Unit testing only; no agentic or system-level testing | MEDIUM (peer-reviewed/known venue) |
| SLR010 | 2024 | arXiv (SE 2030 workshop) | A Software Engineering Perspective on Testing Large Language Models: Research, Practice, Tools and Benchmarks | About testing of LLMs, not testing with LLMs; background only | MEDIUM (peer-reviewed/known venue) |

## Test oracles and assertions (2)

| Study | Year | Venue | Title | Focus when reading | Priority |
|---|---|---|---|---|---|
| O3 | 2024 | arXiv | TOGLL: Correct and Strong Test Oracle Generation with LLMs | Generalisation of oracle generation to unseen data | MEDIUM (peer-reviewed/known venue) |
| O4 | 2025 | arXiv | AugmenTest: Enhancing Tests with LLM-Driven Oracles | Data leakage in oracle benchmarks; best correct-assertion rate only 30% | MEDIUM (peer-reviewed/known venue) |

## Unit test generation with LLMs (2)

| Study | Year | Venue | Title | Focus when reading | Priority |
|---|---|---|---|---|---|
| SLR017 | 2024 | arXiv (check venue) | LLMs and prompting for unit test generation: a large-scale evaluation | Challenges earlier claims about in-context learning; results depend heavily on prompting | LOW (grey-lit/preprint - verify before citing) |
| SLR018 | 2024 | arXiv | Multi-language Unit Test Generation using LLMs | Shows plain LLM generation needs static-analysis guidance to compete with existing tools | MEDIUM (peer-reviewed/known venue) |
