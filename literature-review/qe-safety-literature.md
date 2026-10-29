# Quality Engineering Safety — Literature Thread

Status: drafted via four parallel research agents (2026-10-28), each
covering one safety sub-topic of the review's research roadmap
(`paper/sections/08_conclusion.tex` §"Research Roadmap: Ten Open
Problems"). All 36 cited papers/sources are recorded as new rows
(`SLR089`–`SLR124`) in `literature-review/papers-tracking.csv` and as
BibTeX entries in `paper/references.bib` under the "Quality
engineering safety" keyword block. This file preserves the full
per-paper synthesis and the proposed safety mechanism from each
sub-thread so they can be mined directly when drafting
`paper/sections/05_results.tex`, `06_discussion.tex`, and
`08_conclusion.tex`.

**Full-text status:** none of these 36 sources have been through
`scripts/fetch_full_papers.py` yet or dual-reviewer full-text
screening against `inclusion-exclusion-criteria.md` — treat them as
freshly identified candidates (title/abstract-level `include`), not
yet finalized primary studies. Several (Meta Engineering blog, MSc
thesis, IJAM/IJESTY practitioner-journal items, ISO/IEC standards
documents) are grey literature or standards text rather than
peer-reviewed venues and should be explicitly flagged as such wherever
cited in the manuscript (see `notes` column in `papers-tracking.csv`).

---

## 1. Security of Testing/Coding Agents (SLR089–SLR099)

### Literature
See `papers-tracking.csv` rows SLR089–SLR099 for full citation
metadata. Covers: InjecAgent (indirect prompt injection benchmark),
AgentDojo (dynamic attack/defense environment), RedCode (risky
execution/generation benchmark), QueryIPI (query-agnostic IPI on
coding agents), the AIDev PR-security-debt study, Kozak et al.
(benign-operation insecurity), VibeGuard (pre-publish security gate),
ROSA (metamorphic-fuzzing backdoor detection), Progent (privilege
control), IsolateGPT (execution isolation), SkillShield (prompt-space
defense).

### Synthesis
**(a) Empirically demonstrated risks.** Four concrete, measured threat
classes converge across this literature. *Indirect prompt injection
(IPI)* is the dominant, best-quantified risk: InjecAgent shows
ReAct-prompted GPT-4 is hijacked 24% of the time by malicious content
embedded in processed data (nearly doubling under reinforced attacker
prompts); AgentDojo confirms injection attacks reliably break some
(not all) security properties across 629 test cases. QueryIPI sharpens
this for coding agents: payloads hidden in *invariant* context (tool
descriptions, system prompts) rather than per-query triggers achieve
up to 87% success and transfer to real IDE-integrated agents — an
attacker need not predict a developer's query, only poison the
tool/plugin ecosystem a testing agent consults. *Risky/harmful code
generation and execution* is demonstrated at benchmark scale: RedCode's
4,050 test cases show agents inconsistently refuse technically risky
operations, and more capable models produce *more* sophisticated
malware once jailbroken — a capability/safety inversion. *Benign-
operation insecurity* is a distinct, underappreciated risk: Kozak et
al. find 21% of agent trajectories are insecure during ordinary,
non-adversarial software setup tasks (dominated by CWE-200 information
exposure) — testing agents leak secrets even without an attacker in
the loop. *Supply-chain contamination* of AI-generated artifacts is
now backed by production-scale evidence: the AIDev study finds 38.9%
of agent-authored PRs contain security smells (82.3% supply-chain
issues, 99.6% of critical smells are hardcoded credentials), and
existing human review catches only ~19% of leaked credentials before
merge — directly undermining "a human reviews the agent's output" as
a sufficient safety story for AI-generated tests and code.

**(b) Defenses and effectiveness/cost.** *Policy/privilege control*
(Progent) enforces least-privilege via SMT-verified symbolic rules
over tool calls with monotonic confinement, reducing attack success on
AgentDojo/ASB while preserving task utility. *Execution isolation*
(IsolateGPT, NDSS 2025) applies OS-style sandboxing between apps/tools,
blocking many known attacks at under 30% overhead for most queries.
*Prompt-space/lightweight defenses* (SkillShield) need no model-weight
access or auxiliary classifiers, matching a dedicated 8B guard
classifier's blocking rate at near-zero deployment cost (0.14% false-
refusal rate) — attractive for API-only deployers but weaker than
architectural isolation. For artifact hygiene, VibeGuard's pre-publish
gate achieves 100% recall/89.47% precision on packaging/secret-
exposure failures missed by conventional static analysis, and ROSA's
metamorphic fuzzing oracle detects planted backdoors in ~90 minutes
without reverse engineering.

**(c) What remains unsolved.** AgentDojo's own framing — attacks and
defenses are incomplete and co-evolving — remains the honest state of
the art. No defense has been evaluated against the query-agnostic,
tool-description-poisoning attack class (QueryIPI) at real
plugin-ecosystem scale; benign-operation insecurity (21% insecure
trajectories absent any attacker) suggests current alignment is
insufficient even without adversaries, with model-dependent mitigation
effectiveness (GPT-4.1 96.8% vs. others much lower); supply-chain
defenses (VibeGuard, Progent, ROSA) are validated only on small,
largely synthetic benchmarks, none stress-tested at the 16,112-file-
change AIDev scale; and there is no integrated, end-to-end evaluation
combining privilege control + execution isolation + artifact gating in
one testing-agent pipeline, nor a standard "test-oracle integrity"
benchmark analogous to RedCode/AgentDojo for adversarial manipulation
of generated test assertions/oracles themselves.

### Proposed Safety Mechanism: Trust Boundary for Test Agents (TBTA)
A three-layer defense-in-depth architecture for testing frameworks
that delegate test generation/execution to LLM agents, since no single
defense above is sufficient alone. **Layer 1 (ingestion boundary):**
all external content the agent consumes (issue text, API docs,
fixtures, tool/plugin descriptions) is treated as untrusted and passed
through a content-provenance tagger, keeping structured content
separate from instruction channels to blunt both classic and
query-agnostic IPI. **Layer 2 (execution boundary):** every tool call
(file writes, shell/test execution, dependency installs) is checked
against a Progent-style symbolic least-privilege policy enforced
inside an IsolateGPT-style isolated sandbox, so a successfully injected
instruction cannot escalate beyond the declared task scope. **Layer 3
(artifact gate):** before any AI-generated test/code is merged, it
passes a gate combining VibeGuard-style packaging/secret checks with a
ROSA-style metamorphic fuzzing oracle targeting the test suite itself
— checking not just that tests pass, but that oracles have not been
subtly weakened or backdoored. Because human review catches only a
minority of issues (~19% per the AIDev study), this gate is mandatory
and automated, not advisory. Motivates a public "Test-Oracle
Integrity" benchmark — analogous to RedCode/AgentDojo — for scoring
TBTA-style pipelines on both attack resistance and utility
preservation.

---

## 2. Oracle Independence & the AI-Testing-AI Circularity Problem (SLR100–SLR106)

### Literature
SLR100–SLR106: Bodicoat et al. (LLM-driven test oracle generation),
Molina & Gorla (test oracle automation / data leakage), CANDOR
(multi-agent consensus oracle generation), Wataoka et al.
(self-preference bias / perplexity), Panickssery et al.
(self-recognition ↔ self-preference causal link), Huang et al. (LLMs
cannot self-correct reasoning), Olausson et al. (self-repair limits in
code generation). Background only (not counted toward the 2021–2026
corpus, cite for definitional grounding): Segura et al. 2016,
"A Survey on Metamorphic Testing," IEEE TSE.

### Synthesis
**(a) Shared failure modes between generator and judge.** Panickssery,
Bowman & Feng show a model's ability to *recognize* its own
generations is linearly and causally correlated with the strength of
its self-preference bias when scoring them — measurable, not
coincidental. Wataoka, Takahashi & Ri supply the mechanism: LLM judges
systematically over-reward low-perplexity ("familiar," in-distribution)
outputs regardless of authorship, so any two models trained on
overlapping data/architectures tend to share blind spots even without
literal self-identity. At the reasoning level, Huang et al. show LLMs
cannot reliably detect flaws in their own reasoning chains without
external signal. Olausson et al. extend this to code concretely:
self-repair gains are modest and bottlenecked by the model's inability
to diagnose its own bugs, while an *external*, stronger critic
substantially improves repair. Molina & Gorla add a training-time
dimension: data leakage means an LLM's oracle judgments and an LLM's
code generations may be correlated via overlapping pretraining
corpora — a subtler, harder-to-detect circularity than same-session
self-evaluation.

**(b) Existing independence techniques.** Three families: (1)
*multi-agent consensus/panels* (CANDOR) — multiple reasoning agents
debate before an oracle is accepted, yielding 21+ point correctness
gains over a fine-tuned single-model baseline; (2) *context/
specification grounding* (Bodicoat et al.) — conditions oracle
generation on external intent/documentation rather than the
implementation alone; (3) *external/stronger critics* (Olausson et
al.) — substitute a genuinely different, more capable model or a human
for the self-feedback loop. Classical metamorphic/differential testing
(background) is a fourth, architecturally distinct strategy: relations
between related inputs/outputs that must hold regardless of which
model produced the implementation.

**(c) Effectiveness.** Real but partial. CANDOR's consensus reduces
hallucinated oracles vs. single-pass generation, but same-family
agents still share representational overlap — consensus among similar
models can produce *correlated* false confidence ("hallucinated
consensus") rather than true independence. Context-grounding improves
fidelity to intent but depends on external-spec quality/availability.
External-critic approaches show the clearest effect size but require a
genuinely separate (often costlier) model or human, undermining full
automation's economics.

**(d) Unsolved.** No paper demonstrates an oracle whose correctness
signal is architecturally guaranteed statistically independent of the
code-under-test's generative process when both originate from the LLM
ecosystem; "independence" is approximated via model/prompt diversity
or human/formal grounding, never proven. Data-leakage-induced
correlation is particularly unsolved — even cross-vendor panels may
share contaminated pretraining data. No standardized "oracle
independence" metric exists, analogous to self-preference metrics for
judges.

### Proposed Safety Mechanism: Provenance-Partitioned Oracle Verification (PPOV)
Require every automated test-oracle judgment to carry a verifiable
"provenance distance" score from the code-generation process it
evaluates; refuse verdicts below a minimum threshold. (1) Maintain a
registry mapping each pipeline model/tool to training-data lineage,
architecture family, and vendor. (2) Compute provenance distance
across three axes — model family (different base architecture/vendor
than the code generator), training-data overlap (via disclosed cutoff
dates/corpora or membership-inference proxies), and reasoning modality
(prefer non-generative oracles — metamorphic relations, property-based
invariants, formal specs, differential execution against independently
sourced reference implementations — over any LLM judge, treated as
provenance distance zero regardless of panel size). (3) Route
low-distance verdicts (same-model self-repair, same-family panels)
into an "advisory" tier that surfaces candidate bugs but cannot close
a test as passing; only high-distance signals (metamorphic/
differential checks, disclosed-non-overlapping cross-vendor panels, or
human review) certify correctness. (4) Log and periodically audit the
distribution of provenance distances actually used in production,
since self-preference/shared-blind-spot risk scales with
representational similarity — making provenance distance a measurable,
falsifiable proxy for oracle independence.

---

## 3. Self-Healing / Flaky-Test Stability (SLR107–SLR115)

### Literature
SLR107–SLR115: Alshammari et al. (flaky-failure classifier evaluation,
230K+ failures), CANNIER (Parry et al., rerun+ML hybrid detection),
Leinen et al. (detected vs. undetected flaky failures in industrial
CI), Parry et al. (systemic flakiness / co-occurring failures), Lam et
al. (flaky-test lifecycle, Microsoft, illusory fixes), Meta
Engineering (Probabilistic Flakiness Score, grey literature), Joseph
(zero-cost DOM-accessibility self-healing, small-scale preprint),
Rohamo (MSc thesis, LLM-based Robot Framework locator repair),
IJAM/Healenium comparison study.

### Synthesis
**(a) Evidence of masked regressions.** The clearest evidence comes
from the adjacent flaky-test-classification literature rather than
self-healing-locator papers themselves (which almost universally
measure only pass-rate recovery and maintenance savings). Alshammari
et al. show failure de-duplication — the same pattern-matching logic
underlying many auto-quarantine/self-healing triage systems — is
"entirely ineffective" in some projects, i.e., real failures get
matched against known-flaky signatures and discarded. Leinen et al.
frame the problem symmetrically as "detected vs. undetected" flaky
failures, implying any detector/healer boundary has a corresponding
undetected-failure population that includes real regressions
misclassified as noise. Lam et al.'s Microsoft study found developer-
or tool-claimed "fixes" to flaky tests frequently do not actually
change the test's failure behavior — "healing" labels asserted without
verifying causal effect, directly transferable to self-healing locator/
assertion tools marking a test "repaired" purely because it now passes
once.

**(b) Reported accuracy/false-positive rates.** CANNIER-style ML+rerun
hybrids reduce computation cost by an order of magnitude but trade off
some detection accuracy versus exhaustive rerunning; rerun-only methods
have an empirical recall ceiling — even 10,000 reruns catch only
roughly two-thirds of flaky tests, meaning the "ground truth" used to
validate downstream classifiers/healers is itself noisy. On the
self-healing-locator side, the Helsinki MSc thesis reports LLM-based
locator repair accuracy up to ~87.5% for the best model — roughly
1-in-8 automated heals pick a wrong element — while the Healenium/IJAM
comparison and the zero-cost accessibility-tree preprint report large
reductions in locator-failure rate (40–60%) and near-100% pass-rate
recovery, measured purely as "does the test pass again," not "does the
test still verify the same behavior."

**(c) Existing safeguards.** Weak and mostly indirect. Meta's PFS
rejects binary "flaky/not-flaky" and "healed/broken" labels in favor
of a continuously monitored probabilistic reliability score, so a
sudden *increase* in failure rate after a claimed fix/heal stays
visible rather than silently suppressed — the closest systematic
guardrail in this literature. CANNIER's rerun-triggering strategy keeps
an expensive-but-trustworthy oracle (repeated execution) in the loop
for cases the ML classifier is uncertain about. Beyond these, surveyed
self-healing-locator papers report no verification step confirming a
healed locator still targets the functionally equivalent UI element.

**(d) Unsolved.** No paper evaluates self-healing/auto-repair against
*injected real regressions* (mutation testing or deliberately seeded
functional bugs) to measure whether healed tests still catch them —
all surveyed self-healing-locator evaluations use cosmetic DOM/
attribute changes with no underlying functional change. No standard
metric analogous to classifier F1/precision-recall exists for "heal
correctness." Ground-truth flakiness datasets have known recall gaps
that propagate uncertainty downstream. The flaky-test-classification
literature (which has begun measuring misclassification risk
explicitly) and the self-healing-locator/tooling literature (which has
not) are studied in near-total isolation from each other.

### Proposed Safety Mechanism: Mutation-Gated Dual-Signal Heal Verification (MG-DSV)
Before any self-healing action (locator substitution, assertion
rewrite, flaky-quarantine decision) is committed, require a two-signal
check instead of relying on "test now passes" alone. **Signal 1
(mutation canary):** at heal time, automatically apply a small set of
cheap, targeted mutations to the application-under-test or DOM near
the healed element (e.g., inverting a visible label, nulling a
response field, flipping a button's enabled state) and re-run the
healed test — a genuinely sound heal must still *fail* against these
injected defects; if the healed test passes regardless, reject the
heal as having drifted onto an irrelevant element/assertion. **Signal
2 (semantic-equivalence signal):** compare pre-heal and post-heal
locators/assertions via an independent oracle (accessibility-role +
visible-text embedding similarity, or an LLM-as-judge prompted only
with "does target B serve the same function as target A," without
seeing pass/fail outcomes) to flag low-similarity heals for mandatory
human review rather than silent auto-commit. Only heals passing both
checks are auto-applied; others are logged as "quarantined-pending-
review" with full diff context, never silently merged — converting
"healed and passing" from a single, gameable signal into two
independent, cheap, automatically-computable checks targeting exactly
the failure mode of a heal that restores passing status without
restoring (or that masks) real defect-detection capability.

---

## 4. Governance, Accountability & Human-Agent Trust for L4–L5 Autonomy (SLR116–SLR124)

### Literature
SLR116–SLR124: ISO/IEC TR 29119-11:2020 (AI-system testing
guidelines), ISO/IEC TS 42119-2:2025 (AI testing overview), Feng,
McDonald & Zhang (five-level agent autonomy taxonomy + autonomy
certificates), Treude et al. (accountable agents / ToS analysis),
Cheng et al. (Three-Pillar Model for safe agent autonomy), IBM
Research CHI 2024 TREW workshop (trust/reliance in human-AI
workflows), Passi, Dhanorkar & Vorvoreanu (addressing overreliance on
AI, Microsoft Research), Ibrahim et al. (measuring/mitigating
overreliance), Kiran (HARA/ACEF human-AI collaboration model for
enterprise testing).

### Synthesis
**(a) What ISO/IEC/IEEE 29119 covers and does not.** The 29119 family,
extended by ISO/IEC TR 29119-11:2020 and further operationalized by
ISO/IEC TS 42119-2:2025, is squarely focused on *testing AI as the
system under test*: it supplies risk-based testing guidance,
acknowledges non-determinism and the oracle problem, and gestures at
ethics/bias/safety risk tiers. It conspicuously does not cover the
inverse, increasingly urgent scenario — AI acting *as the tester or
quality gatekeeper*. No clause addresses who or what may approve a
test suite, sign off on release quality, or merge a change with
reduced/no human review; no defined "autonomy level" for a testing
agent analogous to its AI-system risk tiers; no mechanism to certify
or audit an autonomous QA agent's decision authority. The standard
provides raw materials (risk tiers, traceability, lifecycle planning)
a governance extension could repurpose, but as written it is
agent-testing guidance, not agent-as-approver governance.

**(b) Trust/escalation research.** HCI/CSCW research (CHI
TRAIT/TREW workshop lineage, Microsoft Research and multi-institution
overreliance literature) establishes that trust calibration for
delegation-capable, LLM-based agents is qualitatively different from
trust in earlier decision-support tools: humans increasingly treat
these systems as collaborative counterparts, enabling richer division
of labor but producing automation bias and "appropriate reliance"
failures. Industry-adjacent work (Kiran's ACEF/HARA model; Feng et
al.'s five-level autonomy taxonomy) begins translating general
findings into QA-specific escalation mechanics — confidence-triggered
human review, criticality-weighted thresholds, role-based control
levels (Operator → Observer). None of this has been empirically
validated specifically in testing/QA contexts at top SE venues
(ICSE/FSE/ASE); it generalizes from general-purpose human-AI
interaction studies or comes from practitioner/vision papers, leaving
a validation gap.

**(c) Accountability gaps.** Treude et al.'s ToS analysis is the
clearest evidence that accountability for agent-mediated software work
is currently settled by contract, not engineering standard or
regulation: tool providers systematically shift correctness/safety/
compliance responsibility onto users, inconsistently across vendors.
No existing framework specifies who is accountable when an autonomous
agent approves a release, merges a PR after "passing" its own
generated tests, or waives a known risk. Feng et al.'s "Approver" and
"Observer" autonomy levels make vivid where this gap bites hardest:
once agents operate above "Collaborator," a human is no longer
meaningfully in the decision loop per quality judgment, yet standards
and contracts still assume a human decision-maker exists.

**(d) Unsolved.** No cross-mapping exists between an SAE-style
autonomy-level taxonomy (Feng et al.) and ISO/IEC 29119-style risk
tiers or certification artifacts; no empirical measurement of
appropriate-reliance calibration specifically for QA sign-off
decisions; no agreed escalation protocol validated at scale in real
SE settings; no accountability instrument (contract, standard, or
regulation) assigns traceable, auditable responsibility when a Level
4-5 agent's quality decision later proves wrong.

### Proposed Safety Mechanism: Autonomy-Tiered Quality Sign-off Protocol (ATQSP)
An extension to ISO/IEC TS 42119-2 / ISO/IEC TR 29119-11 binding Feng
et al.'s five-level autonomy taxonomy to the 29119 risk-tiering model
and a mandatory accountability artifact. Each autonomous QA agent is
issued an **Autonomy Certificate** scoped to a specific testing
responsibility (e.g., "regression test generation," "release gate
approval") and capped at one of the five levels (Operator…Observer).
The certificate's permitted level is risk-indexed: using 29119/
42119-2's existing risk categories (safety, security, privacy,
ethics), high-risk components can never be certified above
"Consultant" (agent proposes, human decides); low-risk components may
reach "Approver" or "Observer." Every sign-off action above
"Collaborator" level emits a machine-readable **Decision Record**
(confidence score, risk tier invoked, test evidence, and the specific
certificate clause authorizing the action) logged to an immutable
audit trail — operationalizing Kiran's ACEF escalation triggers
(confidence threshold, business criticality, risk tolerance) as formal
certificate conditions. Accountability is resolved by construction:
the certificate issuer (internal governance board or accredited third
party) is accountable for authorizing the autonomy ceiling; the
deploying organization is accountable for configuring risk tiers
correctly; the Decision Record is accountable evidence for post-
incident review — closing the contractual responsibility-shifting gap
documented by Treude et al.

---

## Cross-Thread Takeaways for the Manuscript

1. All four sub-threads independently converge on the same structural
   finding: **the "healed/passed/approved" signal currently used in
   practice is a single, gameable proxy that is not independently
   verified** — whether that signal is a self-healing locator's pass
   rate, an LLM oracle's verdict, a code agent's benign-looking tool
   call, or a human reviewer's sign-off on an agent-authored PR. Each
   proposed mechanism above (TBTA, PPOV, MG-DSV, ATQSP) follows the
   same pattern: require a **second, independently-sourced signal**
   before trusting the first.
2. Human review is repeatedly shown to be an insufficient backstop on
   its own (~19% credential-leak detection rate in the AIDev study;
   illusory "fixes" in Lam et al.; overreliance/automation-bias
   literature) — reinforcing that safety mechanisms for next-
   generation QE must be automated-by-default with human review as an
   escalation path, not the primary control.
3. This thread directly substantiates the roadmap items in
   `08_conclusion.tex`: items 1 (oracle independence), 4 (self-healing
   stability), 7 (security of testing agents), 8 (human-agent
   collaboration), 9 (circularity of AI testing AI), and 10
   (governance for L5) now each have a concrete literature base and a
   candidate mechanism, ready to be cited with the `\cite{}` keys added
   to `paper/references.bib`.
