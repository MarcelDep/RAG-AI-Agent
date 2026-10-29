import re

LLM = re.compile(r"language model|\bLLMs?\b|\bGPT|llama|mistral", re.I)

EXCLUDE_TITLE = re.compile(
    r"data(set)? pruning|data(set)? selection|edge pruning|text-to-speech|\bTTS\b|"
    r"\bVQ\b|vq-|vector quantiz", re.I)

STRONG = {
    "quantization": r"quantiz",
    "pruning": r"\bprun(e|ed|ing)\b|sparsif",
    "kv_cache": r"kv[- ]?cache|key[- ]value (cache|eviction)",
    "speculative": r"speculative (decoding|sampling)",
    "inference_cost": (r"inference (efficien|speed|latency|accelerat)"
                       r"|efficient inference|accelerat\w* (inference|decoding|generation)"
                       r"|fast(er)? (inference|decoding|generation)"),
    "compression": (r"model compression|compress\w* (the )?(model|llm|language model|kv|cache)"
                    r"|low-bit|early[- ]exit"),
    "serving": r"(llm|model|inference) serving|serving (system|engine|framework)",
}
WEAK = {
    "efficient": r"\befficien",
    "speed": r"latency|speed-?up|\bfaster\b",
    "distill": r"distill",
    "lowrank": r"low-rank",
    "memory": r"memory[- ](footprint|usage|cost|consumption|efficient)",
    "moe": r"mixture[- ]of[- ]experts|\bMoE\b",
}

RULE = {
    "version": "v3",
    "llm": LLM.pattern,
    "exclude_title": EXCLUDE_TITLE.pattern,
    "strong": STRONG,
    "weak": WEAK,
    "logic": ("title not excluded AND LLM term anywhere AND (a strong term in "
              "title+keywords OR >=2 distinct strong terms in title+keywords+abstract "
              "OR (>=1 strong AND >=2 distinct weak terms))"),
}


def parts(p):
    c = p["content"]
    title = c.get("title", {}).get("value", "")
    kws = " ".join(c.get("keywords", {}).get("value", []))
    abstract = c.get("abstract", {}).get("value", "")
    return title, f"{title} {kws}", abstract


def found(text, table):
    return {k for k, pat in table.items() if re.search(pat, text, re.I)}


def explain(p):
    title, head, abstract = parts(p)
    full = f"{head} {abstract}"
    return {
        "excluded": bool(EXCLUDE_TITLE.search(title)),
        "llm": bool(LLM.search(full)),
        "strong_head": found(head, STRONG),
        "strong_all": found(full, STRONG),
        "weak_all": found(full, WEAK),
    }


def matches(p):
    e = explain(p)
    if e["excluded"] or not e["llm"]:
        return False
    return bool(
        e["strong_head"]
        or len(e["strong_all"]) >= 2
        or (e["strong_all"] and len(e["weak_all"]) >= 2)
    )