"""FASTA analysis with Biopython. Research only — not diagnostic."""
from __future__ import annotations

import io
from typing import Any

from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqUtils import gc_fraction


def analyze_fasta(text: str) -> dict[str, Any]:
    text = (text or "").strip()
    if not text:
        raise ValueError("Empty FASTA input")

    # Allow raw sequence without header
    if not text.startswith(">"):
        text = ">sequence\n" + text

    records = list(SeqIO.parse(io.StringIO(text), "fasta"))
    if not records:
        raise ValueError("Could not parse FASTA")

    rec = records[0]
    seq = str(rec.seq).upper().replace(" ", "").replace("\n", "")
    seq_obj = Seq(seq)
    length = len(seq)

    # Type heuristic
    nuc_set = set("ACGTURYSWKMBDHVN")
    is_nuc = length > 0 and all(c in nuc_set for c in seq)
    if not is_nuc:
        seq_type = "protein_or_mixed"
        unit = "aa"
        gc = None
    elif "U" in seq and "T" not in seq:
        seq_type = "RNA"
        unit = "bp"
        gc = round(gc_fraction(seq_obj) * 100, 2)
    else:
        seq_type = "DNA"
        unit = "bp"
        gc = round(gc_fraction(seq_obj) * 100, 2)

    orfs: list[dict[str, Any]] = []
    if is_nuc and length >= 30:
        orfs = _find_orfs(seq, min_aa=10)

    translation = None
    if is_nuc and length >= 3:
        # Longest ORF translation if available, else frame 0
        if orfs:
            best = max(orfs, key=lambda o: o["length_bp"])
            sub = seq[best["start"] - 1 : best["end"]]
            translation = str(Seq(sub).translate(to_stop=True))[:200]
        else:
            translation = str(seq_obj.translate(to_stop=True))[:200]

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
    stops = {"TAA", "TAG", "TGA"}
    min_bp = min_aa * 3
    found: list[dict[str, Any]] = []
    for frame in range(3):
        i = frame
        while i + 3 <= len(seq):
            if seq[i : i + 3] == "ATG":
                j = i + 3
                while j + 3 <= len(seq):
                    codon = seq[j : j + 3]
                    if codon in stops:
                        length = j + 3 - i
                        if length >= min_bp:
                            found.append(
                                {
                                    "frame": frame + 1,
                                    "start": i + 1,
                                    "end": j + 3,
                                    "length_bp": length,
                                }
                            )
                        break
                    j += 3
            i += 3
    found.sort(key=lambda o: -o["length_bp"])
    return found
