"""Code Studio — explainable ML starters."""
from __future__ import annotations

from fastapi import APIRouter
from pydantic import BaseModel, Field

router = APIRouter()

TEMPLATES = {
    "domain": '''# BioLink — Domain-adaptive / cross-dataset diabetes risk
# Research only. Validate on each target population.
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score

def train_domain_model(X, y, X_ext=None, y_ext=None):
    pipe = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
        ("clf", HistGradientBoostingClassifier(
            max_depth=4, learning_rate=0.08, max_iter=200, random_state=42)),
    ])
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.25, stratify=y, random_state=42)
    pipe.fit(Xtr, ytr)
    print("Internal AUROC:", round(roc_auc_score(yte, pipe.predict_proba(Xte)[:, 1]), 3))
    if X_ext is not None:
        print("External AUROC:", round(roc_auc_score(y_ext, pipe.predict_proba(X_ext)[:, 1]), 3))
    return pipe
# Not a medical device.
''',
    "missing": '''# BioLink — Missing-data-robust diabetes classifier
from sklearn.impute import SimpleImputer
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.pipeline import Pipeline

pipe = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("clf", HistGradientBoostingClassifier(random_state=42)),
])
# Optionally add missingness indicator columns. Research use only.
''',
    "explain": '''# BioLink — Explainable T2D risk (SHAP notes)
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
# import shap

pipe = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("clf", HistGradientBoostingClassifier(max_depth=4, random_state=42)),
])
# After fit: use shap.Explainer on the classifier for local explanations.
# Not clinical advice.
''',
    "cancer": '''# BioLink — BRCA-style pathogenicity classifier starter
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.impute import SimpleImputer

# Features: conservation, gnomAD AF, domain flags; labels from ClinVar
imp = SimpleImputer(strategy="median")
clf = GradientBoostingClassifier(n_estimators=150, max_depth=3, learning_rate=0.05, random_state=42)
# Research triage only — not ACMG clinical classification.
''',
    "default": '''# BioLink — generic explainable ML scaffold
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import HistGradientBoostingClassifier

pipe = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler()),
    ("clf", HistGradientBoostingClassifier(random_state=42)),
])
# Validate externally. Not a medical device.
''',
}


def pick(prompt: str) -> tuple[str, str]:
    p = (prompt or "").lower()
    if any(x in p for x in ("brca", "cancer", "variant", "pathogen")):
        return "cancer", TEMPLATES["cancer"]
    if any(x in p for x in ("missing", "imput")):
        return "missing", TEMPLATES["missing"]
    if any(x in p for x in ("shap", "explain")):
        return "explain", TEMPLATES["explain"]
    if any(x in p for x in ("cross", "domain", "population", "dataset")):
        return "domain", TEMPLATES["domain"]
    if any(x in p for x in ("diabetes", "t2d", "risk")):
        return "explain", TEMPLATES["explain"]
    return "default", TEMPLATES["default"]


class CodeRequest(BaseModel):
    prompt: str = Field(..., min_length=1, max_length=400)


@router.post("/generate")
def generate_code(body: CodeRequest):
    key, code = pick(body.prompt)
    return {
        "template": key,
        "language": "python",
        "code": code,
        "disclaimer": "Research/educational starter code only — not for clinical deployment.",
    }


@router.get("/templates")
def list_templates():
    return {"templates": list(TEMPLATES.keys())}
