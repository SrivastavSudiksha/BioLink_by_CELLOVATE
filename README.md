# 🧬 BioLink

### An Explainable AI Platform for Cancer & Diabetes Research

## 🔬 Overview

**BioAI Assistant** is an explainable, evidence-grounded AI platform designed to support **cancer and diabetes research and education**.

The platform integrates biomedical literature retrieval, genomic sequence analysis, research gap discovery, explainable machine learning, and AI-assisted code generation into a single workflow.

### Core Workflow

**Raw Sequence → Biological Evidence → Literature → Research Gap → AI Solution → Working Code**

The platform is intended as a **research and educational tool, not a diagnostic or treatment system**.

---

## ❗ Problem Statement

Cancer and diabetes research involves large volumes of genomic, clinical, and scientific literature data. Researchers and students often face challenges such as:

- Converting raw FASTA sequences into interpretable biological insights
- Finding reliable and citable biomedical evidence
- Identifying research gaps from existing literature
- Converting research gaps into clear and testable problem statements
- Building explainable and population-aware ML models
- Understanding and validating AI-generated biomedical information

Existing AI systems may also generate answers without sufficient evidence or citations, which makes **grounding, explainability, and source traceability** especially important in biomedical research.

---

## 💡 Proposed Solution

BioAI Assistant combines **five integrated modules**:

### 1. 📚 Problem Statement Generator

An LLM-based literature mining system that extracts:

- Research methods
- Datasets
- Limitations
- Future directions
- Existing research gaps

It converts these findings into structured research problems containing:

- Proposed AI/ML solution
- Potential data sources
- Expected outcomes
- Supporting literature

---

### 2. 💬 Grounded Biomedical Q&A

A domain-specific **Retrieval-Augmented Generation (RAG)** chatbot using biomedical sources such as:

- PubMed
- NCBI Gene
- ClinVar

The system retrieves relevant evidence before generating responses and provides **numbered citations** for traceability.

The chatbot focuses on cancer and diabetes research and does not provide diagnosis or treatment recommendations.

---

### 3. 🧬 FASTA Analyzer

The FASTA Analyzer processes DNA, RNA, and protein sequences.

It performs:

- Sequence type detection
- Sequence length calculation
- GC-content analysis
- ORF detection
- Sequence translation
- BLAST-based sequence identification
- Gene identification
- ClinVar-based variant association lookup
- Plain-language biological interpretation

The goal is to transform raw sequence data into an interpretable research-oriented report.

---

### 4. 💻 Code Studio

Researchers can provide a research problem statement and generate runnable ML code.

The generated workflows focus on:

- Explainable ML
- Missing-data robustness
- Population-aware modeling
- Diabetes prediction
- Model interpretation

The generated code can also be iteratively revised according to the researcher's requirements.

---

### 5. 🧠 Domain-Adapted LLM

A lightweight open-source language model is adapted using **LoRA fine-tuning** on biomedical literature, particularly NCBI/PubMed abstracts.

The domain-adapted model is evaluated against a general-purpose LLM to investigate improvements in biomedical research assistance.

---

## ⚙️ Technical Architecture

### Data Sources

- **PubMed / NCBI E-utilities** – Biomedical literature
- **NCBI Gene** – Gene information
- **ClinVar** – Variant-disease associations
- **UniProt** – Protein information
- **Pima Indians Diabetes Dataset**
- **NHANES**
- **UCI datasets**

### AI / Machine Learning

- Large Language Models
- Retrieval-Augmented Generation (RAG)
- LoRA fine-tuning
- Embeddings
- FAISS vector search
- Scikit-learn
- SHAP

### Bioinformatics

- Biopython
- FASTA parsing
- ORF detection
- Sequence translation
- BLAST

### Application

- Streamlit
- Python
- REST APIs
- Vector databases

---

## 🔄 System Workflow

```text
                         ┌──────────────────────┐
                         │      Researcher      │
                         └──────────┬───────────┘
                                    │
             ┌──────────────────────┼──────────────────────┐
             │                      │                      │
             ▼                      ▼                      ▼
      FASTA Sequence          Research Query       Problem Statement
             │                      │                      │
             ▼                      ▼                      ▼
      Sequence Analysis        RAG Retrieval        Literature Mining
             │                      │                      │
       ┌─────┴─────┐                │                ┌─────┴─────┐
       ▼           ▼                ▼                ▼           ▼
     BLAST      ClinVar       Biomedical LLM      Methods     Research Gaps
       │           │                │                │           │
       └─────┬─────┘                │                └─────┬─────┘
             │                      │                      │
             └──────────────────────┼──────────────────────┘
                                    ▼
                         ┌──────────────────────┐
                         │ Evidence-Grounded AI │
                         └──────────┬───────────┘
                                    │
                  ┌─────────────────┼─────────────────┐
                  ▼                 ▼                 ▼
            Bioinformatics      Cited Answer       ML Code
               Report                              
                  │                 │                 │
                  └─────────────────┼─────────────────┘
                                    ▼
                         ┌──────────────────────┐
                         │  Research Insights  │
                         └──────────────────────┘
