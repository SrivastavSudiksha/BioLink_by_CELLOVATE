"""Literature-grounded problem statement templates (diabetes + cancer/MODY)."""
from __future__ import annotations

PAPERS = [
    {
        "id": "RP-01",
        "keys": ["cross-dataset", "cross dataset", "domain-adaptive", "domain adaptive", "generaliz", "transfer"],
        "title": "Domain-adaptive diabetes prediction across heterogeneous cohorts",
        "problem": "Cross-dataset diabetes prediction",
        "statement": "How can diabetes prediction models maintain reliable performance across different populations and datasets?",
        "solution": "Develop a domain-adaptive ML model trained and validated across multiple independent diabetes datasets.",
        "why": "Single-cohort models often lose discrimination and calibration on new populations.",
        "gap": "Limited multi-dataset training recipes and sparse external AUROC/calibration reporting.",
        "approach": "Domain adaptation / transfer learning with multi-dataset validation; report AUROC and calibration by cohort.",
        "data": "Pima Indians Diabetes; NHANES; UCI diabetes; external hospital cohorts",
        "outcome": "A domain-adaptive risk model with documented cross-dataset performance (research prototype).",
        "cite": "research_paper.csv RP-01",
    },
    {
        "id": "RP-02",
        "keys": ["early-stage", "early stage", "early risk", "incident", "prediabetes"],
        "title": "Early risk stratification for incident type 2 diabetes",
        "problem": "Early-stage diabetes risk prediction",
        "statement": "How can AI identify individuals at high risk of developing diabetes before clinical diagnosis?",
        "solution": "Develop an explainable ML model using demographic, lifestyle, clinical and biochemical features for early risk prediction.",
        "why": "A multi-year prevention window exists before clinical T2D diagnosis.",
        "gap": "Missing labs in primary care; limited validation in young adults.",
        "approach": "Explainable gradient boosting on demographic + lifestyle + biochemical features with SHAP.",
        "data": "Prospective cohorts; NHANES; primary-care style tables",
        "outcome": "Transparent early-risk scores for prevention program triage (research use).",
        "cite": "research_paper.csv RP-02",
    },
    {
        "id": "RP-03",
        "keys": ["missing", "imputation", "incomplete"],
        "title": "Robust diabetes prediction under missing clinical parameters",
        "problem": "Missing clinical data",
        "statement": "How can diabetes prediction remain accurate when important clinical or laboratory parameters are missing?",
        "solution": "Develop an ML model using missing-data imputation and robust feature-learning techniques.",
        "why": "Real-world tables frequently lack insulin or other labs.",
        "gap": "MNAR bias and lack of open missingness benchmarks.",
        "approach": "Median/MICE imputation, missingness indicators, HistGradientBoosting; sensitivity analysis.",
        "data": "Pima; UCI; incomplete EHR-style tables",
        "outcome": "Missing-data-robust pipeline with uncertainty flags (research).",
        "cite": "research_paper.csv RP-03",
    },
    {
        "id": "RP-04",
        "keys": ["personalized", "treatment", "response", "therapy"],
        "title": "Personalized treatment-response prediction in type 2 diabetes",
        "problem": "Personalized diabetes treatment",
        "statement": "How can AI predict which treatment strategy may be more effective for an individual patient?",
        "solution": "Develop a personalized treatment-response prediction model using patient characteristics, clinical history and treatment outcomes.",
        "why": "Response to metformin, SGLT2i, GLP-1RA is heterogeneous.",
        "gap": "Confounding by indication; limited genetic/adherence data.",
        "approach": "Patient-level outcome models with clear uncertainty; external validation required.",
        "data": "Trial and observational treatment registries; EHR outcomes",
        "outcome": "Research ranking of strategies — not prescribing advice.",
        "cite": "research_paper.csv RP-04",
    },
    {
        "id": "RP-05",
        "keys": ["complication", "nephropathy", "retinopathy", "cardiovascular", "multi-task", "multitask"],
        "title": "Multi-task prediction of diabetes complications",
        "problem": "Diabetes complication prediction",
        "statement": "How can AI predict the risk of developing diabetes-related complications at an early stage?",
        "solution": "Develop multi-task ML models to predict complications such as nephropathy, retinopathy and cardiovascular risk.",
        "why": "Early complication risk enables targeted monitoring.",
        "gap": "Label noise; unequal follow-up; under-represented groups.",
        "approach": "Multi-task shared representation with separate complication heads.",
        "data": "Longitudinal diabetes registries; complication-coded EHR",
        "outcome": "Early multi-task risk research tool with population calibration notes.",
        "cite": "research_paper.csv RP-05",
    },
    {
        "id": "RP-06",
        "keys": ["explainable", "shap", "xai", "interpret"],
        "title": "Explainable AI for diabetes diagnosis and risk scoring",
        "problem": "Explainable diabetes diagnosis",
        "statement": "How can diabetes prediction models provide clinically understandable explanations for their predictions?",
        "solution": "Develop an explainable AI framework that identifies and visualizes the most influential biomarkers and clinical features.",
        "why": "Black-box scores are hard to audit in biomedical settings.",
        "gap": "Unstable attributions under correlated features.",
        "approach": "SHAP / feature attribution with clinician-facing ranking of biomarkers.",
        "data": "Public diabetes tables; hospital laboratory panels",
        "outcome": "Audit-ready explanation reports for research models.",
        "cite": "research_paper.csv RP-06",
    },
    {
        "id": "RP-07",
        "keys": ["multimodal", "multi-modal", "imaging", "retinal", "fusion"],
        "title": "Multimodal fusion for diabetes prediction",
        "problem": "Multimodal diabetes prediction",
        "statement": "How can information from clinical records, biomarkers, lifestyle data and medical images be integrated for improved diabetes prediction?",
        "solution": "Develop a multimodal AI model that combines heterogeneous biomedical data sources for disease prediction.",
        "why": "Imaging and lifestyle signals can complement labs in specialized settings.",
        "gap": "Data alignment cost; missing modalities at inference; privacy of images.",
        "approach": "Early/late fusion with graceful degradation when modalities are absent.",
        "data": "Multimodal research cohorts; retinal + tabular pairs",
        "outcome": "Practical multimodal research pipeline.",
        "cite": "research_paper.csv RP-07",
    },
    {
        "id": "RP-08",
        "keys": ["population", "south-asian", "south asian", "icmr", "ancestry", "ethnic"],
        "title": "Population-aware diabetes risk models",
        "problem": "Population-specific diabetes prediction",
        "statement": "How can AI models account for differences in genetic, environmental and lifestyle factors across populations?",
        "solution": "Develop population-aware ML models using demographic, environmental and clinical features and evaluate their generalizability.",
        "why": "Models trained on one population often miscalibrate on another.",
        "gap": "Sparse open South-Asian labeled datasets for deep models.",
        "approach": "Stratified training, demographic/environmental features, external validation by region.",
        "data": "ICMR-INDIAB-style targets; multi-ethnic biobanks; regional EHR",
        "outcome": "Population-aware benchmarks and recalibration recipes (research).",
        "cite": "research_paper.csv RP-08",
    },
    {
        "id": "RP-09",
        "keys": ["biomarker", "feature selection", "panel", "clustering"],
        "title": "AI-driven biomarker combination discovery for diabetes",
        "problem": "Biomarker discovery for diabetes",
        "statement": "How can AI identify combinations of biomarkers that may improve early detection and disease-risk stratification?",
        "solution": "Apply feature selection, clustering and machine-learning techniques to discover potentially informative biomarker combinations.",
        "why": "Combinations of markers may outperform single-marker rules for early strata.",
        "gap": "Replication failure common; cost of novel assays.",
        "approach": "Stability selection, clustering, multivariate panels with external validation.",
        "data": "Proteomic/metabolomic panels; clinical chemistry tables",
        "outcome": "Candidate biomarker combinations for follow-up studies.",
        "cite": "research_paper.csv RP-09",
    },
    {
        "id": "RP-10",
        "keys": ["literature", "research gap", "nlp", "mining", "pubmed", "gap discovery"],
        "title": "NLP literature mining for diabetes research-gap discovery",
        "problem": "Automated research-gap discovery",
        "statement": "How can AI analyse multiple diabetes research papers to identify recurring limitations, unexplored combinations and emerging research gaps?",
        "solution": "Develop an NLP-based literature-mining system that extracts methods, datasets, findings, limitations and future directions from papers and generates evidence-based research problems.",
        "why": "Manual literature review is slow for students and resource-limited labs.",
        "gap": "Hallucination risk without retrieval grounding; citation accuracy must be audited.",
        "approach": "Abstract chunking, embeddings, RAG + LLM extraction of methods/limitations/future work.",
        "data": "PubMed diabetes abstracts; curated review sets",
        "outcome": "Evidence-based problem statements with citations.",
        "cite": "research_paper.csv RP-10",
    },
]

CANCER = {
    "id": "CA-01",
    "keys": ["cancer", "brca", "tp53", "tumor", "oncolog", "vus"],
    "title": "BRCA1/BRCA2 VUS pathogenicity triage",
    "problem": "Cancer variant classification",
    "statement": "Classify BRCA1/BRCA2 variants from sequence and annotation data (pathogenic vs benign vs VUS) to support research on hereditary breast and ovarian cancer risk.",
    "solution": "Fine-tuned protein language models + ClinVar-labeled data + interpretable pathogenicity scores (research triage).",
    "why": "Approximately 5–10% of breast/ovarian cancers link to pathogenic BRCA variants; VUS volume is high.",
    "gap": "Clinical classification is slow and costly.",
    "approach": "ESM-style embeddings + gradient boosting + SHAP; ClinVar/gnomAD features.",
    "data": "ClinVar, BRCA Exchange, gnomAD, UniProt",
    "outcome": "VUS triage tool prioritizing expert geneticist review (research prototype).",
    "cite": "NCBI Gene BRCA1/2 · ClinVar",
}

MODY = {
    "id": "MO-01",
    "keys": ["mody", "gck", "hnf1", "monogenic"],
    "title": "MODY vs T1/T2 discrimination support",
    "problem": "MODY screening research",
    "statement": "Distinguish MODY subtypes from Type 1/Type 2 using clinical + genetic features to support precision-therapy research.",
    "solution": "Rule-based clinical filters + supervised classifiers on GCK/HNF1A variant annotations and glucose patterns.",
    "why": "Misdiagnosis of MODY as T1/T2 is common.",
    "gap": "Genetic testing is not universally available.",
    "approach": "Clinical triage scores + variant annotation features.",
    "data": "ClinVar MODY panels; NCBI Gene GCK, HNF1A",
    "outcome": "Decision-support triage for genetic testing prioritization (research/educational).",
    "cite": "ClinVar · NCBI Gene · WHO/ICMR guidance",
}


def match_statement(query: str) -> dict:
    q = (query or "").lower()
    best, best_hits = None, 0
    for p in PAPERS + [CANCER, MODY]:
        hits = sum(1 for k in p["keys"] if k in q)
        if hits > best_hits:
            best_hits = hits
            best = p
    if best_hits == 0:
        if any(x in q for x in ("cancer", "brca", "tp53")):
            return CANCER
        if any(x in q for x in ("mody", "gck")):
            return MODY
        return PAPERS[0]
    return best  # type: ignore
