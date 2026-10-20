#!/usr/bin/env python3
"""Render data.json into one self-contained timeline.html (no external dependencies).

Usage:  python3 build.py            # validate + build
        python3 build.py --check    # validate only
"""
import json, os, re, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data.json")
TEMPLATE = os.path.join(HERE, "template.html")
OUT = os.path.join(HERE, "timeline.html")
COPIES = ["/workspace/timeline/timeline.html"]
PLACEHOLDER = "/*__TIMELINE_DATA__*/null"
DATE_RE = re.compile(r"^-?\d{1,6}(-(0[1-9]|1[0-2])(-(0[1-9]|[12]\d|3[01]))?)?$")
TYPES = {"book", "documentary", "article", "other"}
PRECISIONS = {"year", "month", "day"}


def validate(d):
    errs, warns = [], []
    cats = {c["id"] for c in d.get("categories", [])}
    srcs = {s["id"] for s in d.get("sources", [])}
    for s in d.get("sources", []):
        if s.get("type") not in TYPES:
            warns.append(f"source {s['id']}: type '{s.get('type')}' not one of {sorted(TYPES)}")
        if s.get("readFinished") and not DATE_RE.match(str(s["readFinished"])):
            errs.append(f"source {s['id']}: bad readFinished '{s['readFinished']}'")
    seen = set()
    for e in d.get("events", []):
        eid = e.get("id", "?")
        if eid in seen:
            errs.append(f"duplicate event id: {eid}")
        seen.add(eid)
        for k in ("id", "title", "start", "category"):
            if not e.get(k):
                errs.append(f"event {eid}: missing '{k}'")
        for k in ("start", "end"):
            v = e.get(k)
            if v not in (None, "") and not DATE_RE.match(str(v)):
                errs.append(f"event {eid}: bad {k} date '{v}' (use YYYY, YYYY-MM or YYYY-MM-DD; negative year = BCE)")
            if v and str(v).lstrip("-").split("-")[0] == "0":
                errs.append(f"event {eid}: year 0 does not exist (1 BCE is -1)")
        if e.get("datePrecision") and e["datePrecision"] not in PRECISIONS:
            errs.append(f"event {eid}: datePrecision must be year|month|day")
        if e.get("category") and e["category"] not in cats:
            warns.append(f"event {eid}: unknown category '{e['category']}' (will get a grey lane)")
        for s in e.get("sources", []):
            if s not in srcs:
                errs.append(f"event {eid}: unknown source '{s}'")
    return errs, warns


def main():
    with open(DATA, encoding="utf-8") as f:
        d = json.load(f)
    errs, warns = validate(d)
    for w in warns:
        print("warning:", w)
    for e in errs:
        print("ERROR:", e)
    if errs:
        sys.exit(1)
    print(f"ok: {len(d.get('events', []))} events, {len(d.get('sources', []))} sources, {len(d.get('categories', []))} categories")
    if "--check" in sys.argv:
        return
    with open(TEMPLATE, encoding="utf-8") as f:
        tpl = f.read()
    blob = json.dumps(d, ensure_ascii=False, separators=(",", ":"))
    blob = blob.replace("<", "\\u003c").replace("\u2028", "\\u2028").replace("\u2029", "\\u2029")
    if PLACEHOLDER not in tpl:
        sys.exit("template placeholder missing")
    html = tpl.replace(PLACEHOLDER, blob)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(html)
    print("wrote", OUT)
    for c in COPIES:
        try:
            os.makedirs(os.path.dirname(c), exist_ok=True)
            shutil.copyfile(OUT, c)
            print("copied to", c)
        except OSError as ex:
            print("warning: could not copy to", c, ex)


if __name__ == "__main__":
    main()
