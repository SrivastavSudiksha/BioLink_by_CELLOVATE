"""Curated offline knowledge base (cancer / diabetes). Used when PubMed is offline or as supplement."""
from __future__ import annotations

KB = [
    {
        "keys": ["brca1", "brca2", "breast", "ovarian"],
        "answer": (
            "BRCA1 and BRCA2 are tumor-suppressor genes involved in DNA repair via homologous recombination. "
            "Pathogenic germline variants increase lifetime breast cancer risk (approximately 55–72% for BRCA1 and "
            "45–69% for BRCA2 in many series) and also elevate ovarian, prostate, and pancreatic cancer risk. "
            "Risk-management options discussed in clinical guidelines include enhanced screening and risk-reducing "
            "surgery; decisions belong with patients and qualified clinicians."
        ),
        "sources": [
            "NCBI Gene: BRCA1 (ID 672), BRCA2 (ID 675)",
            "ClinVar",
            "Hereditary breast/ovarian cancer literature",
        ],
    },
    {
        "keys": ["tp53", "li-fraumeni", "p53"],
        "answer": (
            "TP53 regulates cell-cycle arrest and apoptosis. Pathogenic germline variants cause Li-Fraumeni syndrome "
            "(early-onset sarcomas, breast cancer, brain tumors, adrenocortical carcinoma). Somatic TP53 mutations "
            "are among the most frequently altered genes in human cancers."
        ),
        "sources": ["NCBI Gene: TP53 (ID 7157)", "ClinVar", "WHO Classification of Tumours"],
    },
    {
        "keys": ["mody", "gck", "hnf1a", "monogenic"],
        "answer": (
            "MODY (Maturity-Onset Diabetes of the Young) is monogenic diabetes, usually autosomal dominant, often with "
            "onset before age 25, non-obese phenotype, and family history. GCK-MODY presents with mild stable fasting "
            "hyperglycemia (pharmacologic treatment often unnecessary). HNF1A-MODY is progressive and typically "
            "responsive to sulfonylureas. Misdiagnosis as Type 1 or Type 2 is common; genetic testing enables precision approaches."
        ),
        "sources": ["NCBI Gene: GCK, HNF1A", "ClinVar MODY panels", "WHO/ICMR diabetes guidance"],
    },
    {
        "keys": ["tcf7l2", "type 2", "t2d", "polygenic"],
        "answer": (
            "TCF7L2 is among the strongest common genetic loci for Type 2 diabetes (e.g. rs7903146 risk allele often "
            "~1.4× per allele). PPARG and KCNJ11 are also established. Polygenic risk combined with lifestyle factors "
            "can stratify risk; genetic risk is modifiable by lifestyle. Models should be validated in the target population."
        ),
        "sources": ["DIAMANTE GWAS", "NCBI Gene: TCF7L2", "ICMR-INDIAB"],
    },
    {
        "keys": ["cross-dataset", "domain-adaptive", "generaliz", "population"],
        "answer": (
            "Diabetes prediction models trained on a single cohort often lose discrimination and calibration on external "
            "populations or datasets. Domain-adaptive training, multi-dataset validation, and population-aware features "
            "reduce the gap. Report external AUROC and calibration by subgroup."
        ),
        "sources": ["Domain-adaptation literature", "Public diabetes datasets (Pima, NHANES, UCI)"],
    },
    {
        "keys": ["missing", "imputation"],
        "answer": (
            "Missing laboratory values are common in real-world tables. Median or multiple imputation, missingness "
            "indicators, and tree-based models (e.g. histogram gradient boosting) can preserve useful discrimination "
            "under missing-at-random assumptions. MNAR bias remains difficult; surface uncertainty to users."
        ),
        "sources": ["Missing-data methodology", "scikit-learn imputation"],
    },
    {
        "keys": ["explainable", "shap", "xai"],
        "answer": (
            "SHAP and related attribution methods rank clinical features and biomarkers for individual predictions, "
            "improving auditability of research models. Attributions can be unstable under correlated features and "
            "are not a substitute for clinical judgment."
        ),
        "sources": ["SHAP documentation", "Explainable ML in biomedicine reviews"],
    },
    {
        "keys": ["glp-1", "glp1", "semaglutide", "liraglutide"],
        "answer": (
            "GLP-1 receptor agonists enhance glucose-dependent insulin secretion, suppress glucagon, slow gastric "
            "emptying, and reduce appetite. Cardiovascular outcome trials have reported MACE reductions for several agents. "
            "This is research context only — not prescribing advice."
        ),
        "sources": ["WHO Essential Medicines List", "CVOT literature (e.g. LEADER, SUSTAIN-6)"],
    },
]


def match_kb(query: str) -> dict | None:
    q = query.lower()
    best, best_hits = None, 0
    for entry in KB:
        hits = sum(1 for k in entry["keys"] if k in q)
        if hits > best_hits:
            best_hits = hits
            best = entry
    if best_hits == 0:
        return None
    return best


SCOPE_HINTS = (
    "cancer", "diabetes", "tumor", "brca", "tp53", "mody", "glucose", "insulin",
    "oncolog", "breast", "ovarian", "t2d", "type 2", "type 1", "glp", "biomarker",
    "gene", "variant", "mutation", "retinopathy", "nephropathy", "polygenic",
)


def in_scope(query: str) -> bool:
    q = query.lower()
    return any(h in q for h in SCOPE_HINTS)
