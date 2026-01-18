import json
import os
import unicodedata
import math
from typing import List, Tuple

DATA_FILE = "data/tasks.json"
PROFILE_OUT = "data/profile.json"

def fnv1a_64(s: str) -> int:
    h = 0xcbf29ce484222325
    fnv_prime = 0x100000001b3
    for ch in s.encode("utf-8"):
        h ^= ch
        h = (h * fnv_prime) & 0xFFFFFFFFFFFFFFFF
    return h

def to_base36(n: int) -> str:
    if n == 0:
        return "0"
    alphabet = "0123456789abcdefghijklmnopqrstuvwxyz"
    out = []
    while n:
        n, r = divmod(n, 36)
        out.append(alphabet[r])
    return "".join(reversed(out))

def normalize_text(s: str) -> str:
    if s is None:
        return ""
    ns = unicodedata.normalize("NFC", s).strip()
    ns = " ".join(ns.split())
    return ns

def trigrams(s: str) -> List[str]:
    if not s:
        return []
    padded = f"  {s}  "
    return [padded[i:i+3] for i in range(len(padded)-2)]

def simple_phonetic(s: str) -> str:
    s = s.lower()
    s = normalize_text(s)
    out = []
    for ch in s:
        if 'a' <= ch <= 'z' or '0' <= ch <= '9':
            out.append(ch)
        else:
            out.append('-')

    res = []
    prev = None
    for c in out:
        if c == '-' and prev == '-':
            continue
        res.append(c)
        prev = c
  
    return "".join(res)[:12]

def task_signature(task: dict) -> dict:
    title = task.get("title", "") if isinstance(task, dict) else ""
    title_norm = normalize_text(title)
    trigs = trigrams(title_norm)
    phon = simple_phonetic(title_norm)

    t_hash = 0
    for tg in trigs:
        t_hash ^= fnv1a_64(tg)

    combined = (fnv1a_64(phon) ^ t_hash) & 0xFFFFFFFFFFFFFFFF

    uniq_terms = set(trigs)
    if not trigs:
        entropy = 0.0
    else:
        freq = {}
        for tg in trigs:
            freq[tg] = freq.get(tg, 0) + 1
        H = 0.0
        total = len(trigs)
        for cnt in freq.values():
            p = cnt / total
            H -= p * math.log2(p)
        
        Hmax = math.log2(total) if total > 1 else 1.0
        entropy = H / Hmax if Hmax > 0 else 0.0

    fingerprint = to_base36(combined)[:12]

    return {
        "id": task.get("id"),
        "title_norm": title_norm,
        "phonetic": phon,
        "trigram_count": len(trigs),
        "trigram_uniques": len(uniq_terms),
        "uniqueness_score": round(entropy, 4),
        "signature": fingerprint
    }

def profile_repository(tasks: List[dict], metadata: dict = None) -> dict:

    sigs = [task_signature(t) for t in tasks]

    n = len(sigs)
    scores = [s.get("uniqueness_score", 0.0) for s in sigs]
    avg = round(sum(scores)/n, 4) if n else 0.0
    minv = round(min(scores), 4) if n else 0.0
    maxv = round(max(scores), 4) if n else 0.0

    freq = {}
    for s in sigs:
        key = s["signature"]
        freq[key] = freq.get(key, 0) + 1

    top_sigs = sorted(freq.items(), key=lambda kv: (-kv[1], kv[0]))[:8]

    profile = {
        "repo_fingerprint": metadata.get("fingerprint") if metadata and isinstance(metadata, dict) else None,
        "n_tasks": n,
        "uniqueness": {"avg": avg, "min": minv, "max": maxv},
        "top_signatures": [{"sig": k, "count": v} for k, v in top_sigs],
        "sample_signatures": sigs[:10]
    }
    return profile

def generate_profile_write_out(task_file=DATA_FILE, metadata_file="data/metadata.json", out_file=PROFILE_OUT):
    tasks = []
    if os.path.exists(task_file):
        try:
            with open(task_file, "r", encoding="utf-8") as f:
                tasks = json.load(f)
                if not isinstance(tasks, list):
                    tasks = []
        except Exception:
            tasks = []
    meta = None
    if os.path.exists(metadata_file):
        try:
            with open(metadata_file, "r", encoding="utf-8") as f:
                meta = json.load(f)
        except Exception:
            meta = None

    profile = profile_repository(tasks, meta)

    os.makedirs(os.path.dirname(out_file) or ".", exist_ok=True)
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(profile, f, indent=2, ensure_ascii=False)

    return profile
