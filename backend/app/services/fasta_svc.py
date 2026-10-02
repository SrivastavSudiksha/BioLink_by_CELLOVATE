import io
import re
from typing import Any

from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqUtils import gc_fraction

NUC_SET = set("ACGTURYSWKMBDHVN")
STOPS = {"TAA", "TAG", "TGA"}


def analyze_fasta(text: str) -> dict[str, Any]:
    text = (text or "").strip()
    if not text:
        raise ValueError("Empty FASTA input")

    if not text.startswith(">"):
        text = ">sequence\n" + text

    try:
        records = list(SeqIO.parse(io.StringIO(text), "fasta"))
    except Exception as e:
        raise ValueError("Could not parse FASTA") from e
    if not records:
        raise ValueError("Could not parse FASTA")

    rec = records[0]
    seq = re.sub(r"\s+", "", str(rec.seq)).upper()
    if not seq:
        raise ValueError("Empty sequence")
    seq_obj = Seq(seq)
    length = len(seq)

    is_nuc = all(c in NUC_SET for c in seq)
    if not is_nuc:
        seq_type, unit, gc = "protein_or_mixed", "aa", None
    elif "U" in seq and "T" not in seq:
        seq_type, unit, gc = "RNA", "bp", round(gc_fraction(seq_obj) * 100, 2)
    else:
        seq_type, unit, gc = "DNA", "bp", round(gc_fraction(seq_obj) * 100, 2)

    orfs: list[dict[str, Any]] = []
    if is_nuc and length >= 30:
        orfs = _find_orfs(seq.replace("U", "T"), min_aa=10)

    translation = None
    if is_nuc and length >= 3:
        if orfs:
            best = orfs[0]
            sub = seq[best["start"] - 1 : best["end"]]
        else:
            sub = seq
        sub = sub[: len(sub) // 3 * 3]
        translation = str(Seq(sub).translate(to_stop=True))[:200]

    return {
        "id": rec.id or "sequence",
        "description": rec.description or "",
        "type": seq_type,
        "length": length,
        "unit": unit,
        "gc_percent": gc,
        "unique_symbols": len(set(seq)),
        "orfs": orfs[:10],
        "translation_preview": translation,
        "disclaimer": (
            "Research/educational analysis only. Does not diagnose disease or interpret clinical pathogenicity."
        ),
    }


def _find_orfs(seq: str, min_aa: int = 10) -> list[dict[str, Any]]:
    min_bp = min_aa * 3
    n = len(seq)
    found: list[dict[str, Any]] = []
    for frame in range(3):
        start: int | None = None
        for i in range(frame, n - 2, 3):
            codon = seq[i : i + 3]
            if start is None:
                if codon == "ATG":
                    start = i
            elif codon in STOPS:
                length = i + 3 - start
                if length >= min_bp:
                    found.append(
                        {"frame": frame + 1, "start": start + 1, "end": i + 3, "length_bp": length}
                    )
                start = None
    found.sort(key=lambda o: -o["length_bp"])
    return found
