function escapeHtml(str){return String(str).replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));}
const RESEARCH_PAPERS=[
{id:"RP-01",keys:["cross-dataset","cross dataset","domain-adaptive","domain adaptive","generaliz","transfer"],title:"Domain-adaptive diabetes prediction across heterogeneous cohorts",problem:"Cross-dataset diabetes prediction",statement:"How can diabetes prediction models maintain reliable performance across different populations and datasets?",solution:"Develop a domain-adaptive ML model trained and validated across multiple independent diabetes datasets.",why:"Single-cohort models often lose discrimination and calibration on new populations.",gap:"Limited multi-dataset training and sparse external AUROC/calibration reporting.",approach:"Domain adaptation with multi-dataset validation; report AUROC and calibration by cohort.",data:"Pima; NHANES; UCI diabetes; external cohorts",outcome:"Domain-adaptive risk model with documented cross-dataset performance (research).",cite:"research_paper.csv RP-01"},
{id:"RP-02",keys:["early-stage","early stage","early risk","incident","prediabetes"],title:"Early risk stratification for incident type 2 diabetes",problem:"Early-stage diabetes risk prediction",statement:"How can AI identify individuals at high risk of developing diabetes before clinical diagnosis?",solution:"Develop an explainable ML model using demographic, lifestyle, clinical and biochemical features for early risk prediction.",why:"Multi-year prevention window before clinical T2D.",gap:"Missing labs; limited validation in young adults.",approach:"Explainable gradient boosting + SHAP on lifestyle/clinical features.",data:"Prospective cohorts; NHANES",outcome:"Transparent early-risk scores for prevention research.",cite:"research_paper.csv RP-02"},
{id:"RP-03",keys:["missing","imputation","incomplete"],title:"Robust diabetes prediction under missing clinical parameters",problem:"Missing clinical data",statement:"How can diabetes prediction remain accurate when important clinical or laboratory parameters are missing?",solution:"Develop an ML model using missing-data imputation and robust feature-learning techniques.",why:"Real-world tables often lack key labs.",gap:"MNAR bias; few open missingness benchmarks.",approach:"Median/MICE imputation, missingness indicators, HistGradientBoosting.",data:"Pima; UCI; incomplete EHR-style tables",outcome:"Missing-data-robust pipeline with uncertainty flags.",cite:"research_paper.csv RP-03"},
{id:"RP-04",keys:["personalized","treatment","response","therapy"],title:"Personalized treatment-response prediction in type 2 diabetes",problem:"Personalized diabetes treatment",statement:"How can AI predict which treatment strategy may be more effective for an individual patient?",solution:"Develop a personalized treatment-response prediction model using patient characteristics, clinical history and treatment outcomes.",why:"Response to therapies is heterogeneous.",gap:"Confounding by indication; limited genetic data.",approach:"Patient-level outcome models with uncertainty; external validation.",data:"Trial/observational registries; EHR outcomes",outcome:"Research ranking of strategies — not prescribing advice.",cite:"research_paper.csv RP-04"},
{id:"RP-05",keys:["complication","nephropathy","retinopathy","cardiovascular","multi-task","multitask"],title:"Multi-task prediction of diabetes complications",problem:"Diabetes complication prediction",statement:"How can AI predict the risk of developing diabetes-related complications at an early stage?",solution:"Develop multi-task ML models to predict complications such as nephropathy, retinopathy and cardiovascular risk.",why:"Early complication risk enables targeted monitoring.",gap:"Label noise; unequal follow-up.",approach:"Multi-task shared representation with separate heads.",data:"Longitudinal registries; complication-coded EHR",outcome:"Early multi-task risk research tool.",cite:"research_paper.csv RP-05"},
{id:"RP-06",keys:["explainable","shap","xai","interpret"],title:"Explainable AI for diabetes diagnosis and risk scoring",problem:"Explainable diabetes diagnosis",statement:"How can diabetes prediction models provide clinically understandable explanations for their predictions?",solution:"Develop an explainable AI framework that identifies and visualizes the most influential biomarkers and clinical features.",why:"Black-box scores are hard to audit.",gap:"Unstable attributions under correlated features.",approach:"SHAP / feature attribution with clinician-facing ranking.",data:"Public diabetes tables; laboratory panels",outcome:"Audit-ready explanation reports for research models.",cite:"research_paper.csv RP-06"},
{id:"RP-07",keys:["multimodal","multi-modal","imaging","retinal","fusion"],title:"Multimodal fusion for diabetes prediction",problem:"Multimodal diabetes prediction",statement:"How can information from clinical records, biomarkers, lifestyle data and medical images be integrated for improved diabetes prediction?",solution:"Develop a multimodal AI model that combines heterogeneous biomedical data sources for disease prediction.",why:"Imaging and lifestyle can complement labs.",gap:"Alignment cost; missing modalities; privacy.",approach:"Early/late fusion with graceful degradation.",data:"Multimodal cohorts; retinal + tabular pairs",outcome:"Practical multimodal research pipeline.",cite:"research_paper.csv RP-07"},
{id:"RP-08",keys:["population","south-asian","south asian","icmr","ancestry","ethnic"],title:"Population-aware diabetes risk models",problem:"Population-specific diabetes prediction",statement:"How can AI models account for differences in genetic, environmental and lifestyle factors across populations?",solution:"Develop population-aware ML models using demographic, environmental and clinical features and evaluate their generalizability.",why:"Models often miscalibrate across populations.",gap:"Sparse open South-Asian labeled sets.",approach:"Stratified training; external validation by region.",data:"ICMR-INDIAB-style targets; multi-ethnic biobanks",outcome:"Population-aware benchmarks (research).",cite:"research_paper.csv RP-08"},
{id:"RP-09",keys:["biomarker","feature selection","panel","clustering"],title:"AI-driven biomarker combination discovery for diabetes",problem:"Biomarker discovery for diabetes",statement:"How can AI identify combinations of biomarkers that may improve early detection and disease-risk stratification?",solution:"Apply feature selection, clustering and machine-learning techniques to discover potentially informative biomarker combinations.",why:"Panels may outperform single markers.",gap:"Replication failure; assay cost.",approach:"Stability selection; multivariate panels; external validation.",data:"Proteomic/metabolomic panels; clinical chemistry",outcome:"Candidate biomarker combinations for follow-up.",cite:"research_paper.csv RP-09"},
{id:"RP-10",keys:["literature","research gap","nlp","mining","pubmed","gap discovery"],title:"NLP literature mining for diabetes research-gap discovery",problem:"Automated research-gap discovery",statement:"How can AI analyse multiple diabetes research papers to identify recurring limitations, unexplored combinations and emerging research gaps?",solution:"Develop an NLP-based literature-mining system that extracts methods, datasets, findings, limitations and future directions from papers and generates evidence-based research problems.",why:"Manual review is slow for resource-limited labs.",gap:"Hallucination without grounding.",approach:"Abstract chunking, embeddings, RAG + LLM extraction.",data:"PubMed diabetes abstracts",outcome:"Evidence-based problem statements with citations.",cite:"research_paper.csv RP-10"}
];
const CANCER_TMPL={id:"CA-01",keys:["cancer","brca","tp53","tumor","oncolog","vus"],title:"BRCA1/BRCA2 VUS pathogenicity triage",problem:"Cancer variant classification",statement:"Classify BRCA1/BRCA2 variants from sequence and annotation data (pathogenic vs benign vs VUS) for hereditary breast/ovarian cancer research.",solution:"Protein LMs + ClinVar labels + interpretable scores (research triage, not clinical report).",why:"VUS volume overwhelms lab capacity.",gap:"Slow costly classification.",approach:"ESM-style embeddings + gradient boosting + SHAP.",data:"ClinVar, BRCA Exchange, gnomAD, UniProt",outcome:"VUS triage research tool.",cite:"NCBI Gene BRCA1/2 · ClinVar"};
const MODY_TMPL={id:"MO-01",keys:["mody","gck","hnf1","monogenic"],title:"MODY vs T1/T2 discrimination support",problem:"MODY screening research",statement:"Distinguish MODY subtypes from Type 1/Type 2 using clinical + genetic features for precision-therapy research.",solution:"Clinical filters + supervised models on GCK/HNF1A annotations.",why:"Misdiagnosis is common.",gap:"Genetic testing access.",approach:"Clinical triage + variant annotation features.",data:"ClinVar MODY panels; NCBI Gene GCK, HNF1A",outcome:"Research decision-support for testing prioritization.",cite:"ClinVar · NCBI Gene"};
document.addEventListener("DOMContentLoaded",()=>{
const landing=document.getElementById("landing"),app=document.getElementById("app"),mainSearch=document.getElementById("mainSearch"),searchBtn=document.getElementById("searchBtn"),homeBtn=document.getElementById("homeBtn"),appSearch=document.getElementById("appSearch");
function openApp(m="statements"){landing.classList.add("hidden");app.classList.remove("hidden");switchModule(m)}
function goHome(){app.classList.add("hidden");landing.classList.remove("hidden");mainSearch.value="";mainSearch.focus()}
function switchModule(name){document.querySelectorAll(".mod-tab").forEach(t=>{const a=t.dataset.module===name;t.classList.toggle("active",a);t.setAttribute("aria-selected",a?"true":"false")});document.querySelectorAll(".module").forEach(m=>m.classList.toggle("active",m.id==="mod-"+name))}
document.querySelectorAll(".mod-tab").forEach(t=>t.addEventListener("click",()=>switchModule(t.dataset.module)));
document.querySelectorAll(".quick-btn").forEach(b=>b.addEventListener("click",()=>openApp(b.dataset.module)));
function handleSearch(){const q=(mainSearch.value||"").trim().toLowerCase();let mod="statements";
if(q.includes("fasta")||q.includes("sequence")||q.includes("orf"))mod="fasta";
else if(q.includes("code")||q.includes("ml")||q.includes("shap")||q.includes("studio"))mod="code";
else if(q.includes("qa")||q.includes("chat")||q.includes("question")||((q.includes("diabetes")||q.includes("cancer")||q.includes("brca")||q.includes("mody"))&&!q.includes("problem")&&!q.includes("statement")&&q.length>2))mod="qa";
openApp(mod);
if(mod==="statements"&&q){const d=document.getElementById("domainInput");if(d)d.value=mainSearch.value.trim()}
if(mod==="qa"&&q){const c=document.getElementById("chatInput");if(c)c.value=mainSearch.value.trim()}
if(mod==="code"&&q){const p=document.getElementById("codePrompt");if(p)p.value=mainSearch.value.trim()}}
searchBtn.addEventListener("click",handleSearch);
mainSearch.addEventListener("keydown",e=>{if(e.key==="Enter")handleSearch()});
homeBtn.addEventListener("click",goHome);
if(appSearch)appSearch.addEventListener("keydown",e=>{if(e.key==="Enter"){const q=appSearch.value.trim().toLowerCase();if(q.includes("fasta"))switchModule("fasta");else if(q.includes("code")||q.includes("ml"))switchModule("code");else if(q.includes("qa")||q.includes("chat"))switchModule("qa");else switchModule("statements")}});
function matchPaper(query){const q=(query||"").toLowerCase();let best=null,bestHits=0;const all=RESEARCH_PAPERS.concat([CANCER_TMPL,MODY_TMPL]);
all.forEach(p=>{const hits=p.keys.filter(k=>q.includes(k)).length;if(hits>bestHits){bestHits=hits;best=p}});
if(!best||bestHits===0){if(q.includes("cancer")||q.includes("brca")||q.includes("tp53"))return CANCER_TMPL;if(q.includes("mody")||q.includes("gck"))return MODY_TMPL;return RESEARCH_PAPERS[0]}return best}
function renderStatement(p){const box=document.getElementById("statementResult");box.innerHTML=`<p><strong>Research problem:</strong> ${escapeHtml(p.problem)}</p><p><strong>Problem statement:</strong> ${escapeHtml(p.statement)}</p><p><strong>Why it matters:</strong> ${escapeHtml(p.why)}</p><p><strong>Current gap:</strong> ${escapeHtml(p.gap)}</p><p><strong>Proposed AI solution:</strong> ${escapeHtml(p.solution)}</p><p><strong>Approach:</strong> ${escapeHtml(p.approach)}</p><p><strong>Data sources:</strong> ${escapeHtml(p.data)}</p><p><strong>Expected outcome:</strong> ${escapeHtml(p.outcome)}</p><p class="cite">Source: ${escapeHtml(p.cite)} · ${escapeHtml(p.title)}</p>`;box.classList.remove("hidden")}
document.getElementById("generateBtn").addEventListener("click",()=>{const btn=document.getElementById("generateBtn");const domain=(document.getElementById("domainInput").value||"").trim();btn.disabled=true;btn.innerHTML='<span class="loading"></span> Generating…';setTimeout(()=>{renderStatement(matchPaper(domain));btn.disabled=false;btn.textContent="Generate Statement"},400)});
const browse=document.getElementById("problemBrowse");
RESEARCH_PAPERS.forEach(p=>{const div=document.createElement("div");div.className="sample-card clickable";div.innerHTML=`<h4>${escapeHtml(p.problem)}</h4><p>${escapeHtml(p.statement.slice(0,100))}…</p>`;div.addEventListener("click",()=>{document.getElementById("domainInput").value=p.problem;renderStatement(p)});browse.appendChild(div)});
const KB=[
{keys:["brca1","brca2","breast","ovarian"],ans:"BRCA1/BRCA2 are tumor-suppressor genes in homologous recombination. Pathogenic germline variants raise lifetime breast cancer risk (~55–72% BRCA1; ~45–69% BRCA2) and ovarian/prostate/pancreatic risk. Guidelines discuss enhanced screening and risk-reducing surgery — decisions rest with patients and clinicians.\n\n[1] NCBI Gene BRCA1 (672), BRCA2 (675)\n[2] ClinVar"},
{keys:["tp53","li-fraumeni","p53"],ans:"TP53 regulates cell-cycle arrest and apoptosis. Germline pathogenic variants cause Li-Fraumeni syndrome. Somatic TP53 mutations are among the most common in human cancers.\n\n[1] NCBI Gene TP53 (7157)\n[2] ClinVar"},
{keys:["mody","gck","hnf1a","monogenic"],ans:"MODY is monogenic diabetes, often autosomal dominant, onset before ~25. GCK-MODY: mild stable hyperglycemia. HNF1A-MODY: progressive, often sulfonylurea-responsive. Misdiagnosis as T1/T2 is common.\n\n[1] NCBI Gene GCK, HNF1A\n[2] ClinVar MODY panels"},
{keys:["tcf7l2","type 2","t2d","polygenic"],ans:"TCF7L2 is a strong common T2D locus. Polygenic scores plus lifestyle can stratify risk; validate in target populations (e.g. South-Asian).\n\n[1] DIAMANTE GWAS\n[2] NCBI Gene TCF7L2\n[3] ICMR-INDIAB"},
{keys:["cross-dataset","domain-adaptive","generaliz","population"],ans:"Models trained on one dataset often lose AUROC/calibration on others. Domain-adaptive training and population-aware features help. Report external AUROC by subgroup.\n\n[1] research_paper.csv RP-01, RP-08"},
{keys:["missing","imputation"],ans:"Median/MICE imputation, missingness indicators, and tree models preserve discrimination under MAR missingness. Flag uncertainty for MNAR cases.\n\n[1] research_paper.csv RP-03"},
{keys:["explainable","shap","xai"],ans:"SHAP ranks biomarkers and clinical features per prediction for auditability. Attributions can be unstable with correlated features; not a diagnosis.\n\n[1] research_paper.csv RP-06"},
{keys:["glp-1","glp1","semaglutide"],ans:"GLP-1 receptor agonists enhance glucose-dependent insulin secretion and reduce appetite. CVOT literature reported MACE reduction. Research context only — not prescribing advice.\n\n[1] WHO EML\n[2] CVOT literature"}
];
function kbReply(query){const q=query.toLowerCase();let best=null,bestHits=0;KB.forEach(e=>{const hits=e.keys.filter(k=>q.includes(k)).length;if(hits>bestHits){bestHits=hits;best=e}});if(!best||bestHits===0)return "No strong match. Try: BRCA1, TP53, MODY, cross-dataset, missing data, SHAP.\n\nDisclaimer: Research use only — not medical advice.";return best.ans+"\n\nDisclaimer: Research/educational use only — not medical diagnosis or treatment advice."}
function appendMsg(role,text){const box=document.getElementById("chatBox");const div=document.createElement("div");div.className="msg "+role;if(role==="assistant")div.innerHTML=`<span class="avatar" aria-hidden="true">🧬</span><div class="bubble">${text.replace(/\n/g,"<br>")}</div>`;else div.innerHTML=`<div class="bubble">${escapeHtml(text)}</div>`;box.appendChild(div);box.scrollTop=box.scrollHeight}
function sendChat(){const input=document.getElementById("chatInput");const q=(input.value||"").trim();if(!q)return;appendMsg("user",q);input.value="";const btn=document.getElementById("sendBtn");btn.disabled=true;setTimeout(()=>{appendMsg("assistant",kbReply(q));btn.disabled=false},350)}
document.getElementById("sendBtn").addEventListener("click",sendChat);
document.getElementById("chatInput").addEventListener("keydown",e=>{if(e.key==="Enter")sendChat()});
const DEMO_SEQ=">demo_dna_fragment\nATGGAGGAGCCGCAGTCAGATCCTAGCGTCGAGCCCCCTCTGAGTCAGGAAACATTTTCAGACCTATGGAAACTACTTCCTGAAAACAACGTTCTGTCCCCCTTGCCGTCCCAAGCAATGGATGATTTGATGCTGTCCCCGGACGATATTGAACAATGGTTCACTGAAGACCCAGGTCCAGATGAAGCTCCCAGAATGCCAGAGGCTGCTCCCCCCGTGGCCCCTGCACCAGCAGCTCCTACACCGGCGGCCCCTGCACCAGCCCCCTCCTGGCCCCTGTCATCTTCTGTCCCTTCCCAGAAAACCTACCAGGGCAGCTACGGTTTCCGTCTGGGCTTCTTGCATTCTGGGACAGCCAAGTCTGTGACTTGCACGTACTCCCCTGCCCTCAACAAGATGTTTTGCCAACTGGCCAAGACCTGCCCTGTGCAGCTGTGGGTTGATTCCACACCCCCGCCCGGCACCCGCGTCCGCGCCATGGCCATCTACAAGCAGTCACAGCACATGACGGAGGTTGTGAGGCGCTGCCCCCACCATGAGCGCTGCTCAGATAGCGATGGTCTGGCCCCTCCTCAGCATCTTATCCGAGTGGAAGGAAATTTGCGTGTGGAGTATTTGGATGACAGAAACACTTTTCGACATAGTGTGGTGGTGCCCTATGAGCCGCCTGAGGTCTGGTTTGCAACTGGGGTCTCTGGG";
document.getElementById("loadDemoFasta").addEventListener("click",()=>{document.getElementById("fastaInput").value=DEMO_SEQ});
document.getElementById("fastaFile").addEventListener("change",e=>{const f=e.target.files[0];if(!f)return;const r=new FileReader();r.onload=ev=>{document.getElementById("fastaInput").value=ev.target.result};r.readAsText(f)});
const REFS={tp53:{name:"TP53 (demo)",note:"Guardian of the genome. Demo only."},brca1:{name:"BRCA1 (demo)",note:"HR repair gene. Demo only."},ins:{name:"INS (demo)",note:"Insulin gene. Demo only."},gck:{name:"GCK (demo)",note:"MODY-related. Demo only."}};
function findSimpleOrfs(seq,minLen=30){const stops=new Set(["TAA","TAG","TGA"]);const orfs=[];for(let frame=0;frame<3;frame++){let i=frame;while(i+3<=seq.length){if(seq.slice(i,i+3)==="ATG"){let j=i+3;while(j+3<=seq.length){const c=seq.slice(j,j+3);if(stops.has(c)){const len=j+3-i;if(len>=minLen)orfs.push({start:i+1,end:j+3,frame:frame+1,length:len});break}j+=3}}i+=3}}return orfs.slice(0,8)}
document.getElementById("analyzeBtn").addEventListener("click",()=>{const raw=(document.getElementById("fastaInput").value||"").trim();if(!raw){alert("Paste or upload a FASTA sequence first.");return}const btn=document.getElementById("analyzeBtn");btn.disabled=true;btn.innerHTML='<span class="loading"></span> Analyzing…';setTimeout(()=>{const lines=raw.split(/\r?\n/);let id="sequence",seq="";lines.forEach(line=>{if(line.startsWith(">"))id=line.slice(1).trim()||id;else seq+=line.trim()});seq=seq.toUpperCase().replace(/[^A-Z*]/g,"");const len=seq.length;const isNuc=len>0&&/^[ACGTURYSWKMBDHVN]+$/.test(seq);const type=!isNuc?"Protein / mixed":seq.includes("U")&&!seq.includes("T")?"RNA":"DNA";const unit=isNuc?"bp":"aa";const gc=isNuc&&len?(((seq.match(/[GC]/g)||[]).length/len)*100).toFixed(2)+"%":"n/a";let orfHtml="";if(isNuc&&len>=30){const orfs=findSimpleOrfs(seq);orfHtml=orfs.length?`<p><strong>Simple ORF scan</strong>:</p><ul style="margin:.4rem 0 .8rem 1.2rem;font-size:.88rem;color:var(--text-muted)">`+orfs.map(o=>`<li>Frame ${o.frame}: ${o.start}–${o.end} (${o.length} bp)</li>`).join("")+`</ul>`:`<p style="font-size:.88rem;color:var(--text-muted)">No ORFs ≥30 bp found.</p>`}const refKey=document.getElementById("refSelect").value;let refHtml="";if(refKey!=="none"&&REFS[refKey]){const r=REFS[refKey];refHtml=`<div class="ok-box">📎 <strong>${escapeHtml(r.name)}</strong><br>${escapeHtml(r.note)}</div>`}document.getElementById("fastaResult").innerHTML=`<h3 style="margin-bottom:.75rem;font-weight:600;">📄 ${escapeHtml(id)}</h3><div class="metrics"><div class="metric"><span class="label">Type</span><span class="value">${type}</span></div><div class="metric"><span class="label">Length</span><span class="value">${len.toLocaleString()} ${unit}</span></div><div class="metric"><span class="label">GC</span><span class="value">${gc}</span></div><div class="metric"><span class="label">Unique</span><span class="value">${new Set(seq).size}</span></div></div>${orfHtml}${refHtml}<div class="ok-box">✅ Basic analysis complete. Does not diagnose disease.</div>`;document.getElementById("fastaResult").classList.remove("hidden");btn.disabled=false;btn.textContent="Analyze Sequence"},400)});
const CODE={
domain:`# BioAI — Domain-adaptive / cross-dataset diabetes risk
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
        ("clf", HistGradientBoostingClassifier(max_depth=4, learning_rate=0.08, max_iter=200, random_state=42)),
    ])
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.25, stratify=y, random_state=42)
    pipe.fit(Xtr, ytr)
    print("Internal AUROC:", round(roc_auc_score(yte, pipe.predict_proba(Xte)[:, 1]), 3))
    if X_ext is not None:
        print("External AUROC:", round(roc_auc_score(y_ext, pipe.predict_proba(X_ext)[:, 1]), 3))
    return pipe
# Not a medical device.
`,
missing:`# BioAI — Missing-data-robust diabetes classifier
from sklearn.impute import SimpleImputer
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.pipeline import Pipeline
pipe = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("clf", HistGradientBoostingClassifier(random_state=42)),
])
# Research use only.
`,
explain:`# BioAI — Explainable T2D risk (SHAP notes)
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
# import shap
pipe = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("clf", HistGradientBoostingClassifier(max_depth=4, random_state=42)),
])
# After fit: shap.Explainer on the classifier for local explanations.
# Not clinical advice.
`,
cancer:`# BioAI — BRCA-style pathogenicity classifier starter
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.impute import SimpleImputer
# Features: conservation, gnomAD AF, domain flags; labels from ClinVar
imp = SimpleImputer(strategy="median")
clf = GradientBoostingClassifier(n_estimators=150, max_depth=3, learning_rate=0.05, random_state=42)
# Research triage only — not ACMG clinical classification.
`,
default:`# BioAI — generic explainable ML scaffold
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
`};
function pickCode(prompt){const p=(prompt||"").toLowerCase();if(p.includes("brca")||p.includes("cancer")||p.includes("variant"))return CODE.cancer;if(p.includes("missing")||p.includes("imput"))return CODE.missing;if(p.includes("shap")||p.includes("explain"))return CODE.explain;if(p.includes("cross")||p.includes("domain")||p.includes("population")||p.includes("dataset"))return CODE.domain;if(p.includes("diabetes")||p.includes("t2d")||p.includes("risk"))return CODE.explain;return CODE.default}
document.getElementById("genCodeBtn").addEventListener("click",()=>{const prompt=(document.getElementById("codePrompt").value||"").trim();const btn=document.getElementById("genCodeBtn");btn.disabled=true;btn.innerHTML='<span class="loading"></span> Generating…';setTimeout(()=>{document.getElementById("codeOutput").textContent=pickCode(prompt||"explainable diabetes");document.getElementById("codeResult").classList.remove("hidden");btn.disabled=false;btn.textContent="Generate Code"},400)});
document.getElementById("copyCodeBtn").addEventListener("click",()=>{navigator.clipboard.writeText(document.getElementById("codeOutput").textContent).then(()=>{const b=document.getElementById("copyCodeBtn");const o=b.textContent;b.textContent="Copied!";setTimeout(()=>{b.textContent=o},1500)}).catch(()=>alert("Copy failed"))});
const codePrompts=document.getElementById("codePrompts");
[["Cross-dataset / domain-adaptive","cross-dataset diabetes domain adaptation"],["Missing clinical data","missing data imputation diabetes model"],["Explainable risk (SHAP)","explainable T2D risk with SHAP"],["Cancer variant classifier","BRCA pathogenicity classifier ClinVar"]].forEach(([title,prompt])=>{const div=document.createElement("div");div.className="sample-card clickable";div.innerHTML=`<h4>${title}</h4><p>${escapeHtml(prompt)}</p>`;div.addEventListener("click",()=>{document.getElementById("codePrompt").value=prompt;document.getElementById("genCodeBtn").click()});codePrompts.appendChild(div)});
mainSearch.focus();
});
