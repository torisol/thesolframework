#!/usr/bin/env python3
import sys, re, hashlib, json, argparse, os, shutil
from typing import Tuple, List

MARK_START = "<!-- SOL-CONTENT-START -->"
MARK_PROV  = "<!-- SOL-PROVENANCE-START -->"
HR_RE = re.compile(r'^(?:[-_*]\s?){3,}\s*$')  # --- *** ___ (with optional spaces)

def sha256_bytes(b: bytes) -> str:
    h = hashlib.sha256()
    h.update(b)
    return h.hexdigest()

def normalize_lf(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")

def split_content_provenance(text: str, include_separator=False, trim_newlines=True):
    # Marker mode
    if MARK_START in text and MARK_PROV in text:
        lines = text.split("\n")
        start_idx = None
        prov_idx = None
        for i, ln in enumerate(lines):
            if ln.strip() == MARK_START:
                start_idx = i
            if ln.strip() == MARK_PROV:
                prov_idx = i
        if start_idx is None or prov_idx is None or prov_idx <= start_idx:
            return split_content_provenance_heuristic(text)
        content_lines = lines[start_idx+1:prov_idx]
        if not include_separator and content_lines:
            last = content_lines[-1].strip()
            if HR_RE.fullmatch(last):
                content_lines = content_lines[:-1]
        content = "\n".join(content_lines)
        if trim_newlines:
            if content.startswith("\n"):
                content = content[1:]
            if content.endswith("\n"):
                content = content[:-1]
        provenance = "\n".join(lines[prov_idx:])
        return content, provenance, "markers"
    # Heuristic mode
    return split_content_provenance_heuristic(text)

def split_content_provenance_heuristic(text: str):
    # Split when an HR line precedes "Provenance"
    pattern = r'(?ims)^(?:[-_*]\s?){3,}\s*\n\s*Provenance[\s\S]*$'
    m = re.search(pattern, text)
    if m:
        j = m.start()
        return text[:j], text[j:], "heuristic"
    return text, "", "none"

def content_bytes_for_any(path: str, include_separator=False, keep_leading_trailing_newlines=False) -> bytes:
    # For .md, use content slice rules; for others, raw bytes
    if path.lower().endswith(".md"):
        raw = open(path, "rb").read()
        if raw.startswith(b"\xef\xbb\xbf"):
            raw = raw[3:]
        text = raw.decode("utf-8")
        text = text.replace("\r\n","\n").replace("\r","\n")
        c, _, _ = split_content_provenance(text, include_separator=include_separator, trim_newlines=not keep_leading_trailing_newlines)
        return c.encode("utf-8")
    return open(path, "rb").read()

def process_one(infile: str, out_dir: str = "", update_placeholders=False,
                include_separator=False, keep_leading_trailing_newlines=False,
                parent_hash: str = None) -> dict:
    base = os.path.basename(infile)
    stem, ext = os.path.splitext(base)
    out_dir = out_dir or os.path.dirname(infile)
    os.makedirs(out_dir, exist_ok=True)

    if infile.lower().endswith(".md"):
        raw = open(infile, "rb").read()
        if raw.startswith(b"\xef\xbb\xbf"):
            raw = raw[3:]
        text = raw.decode("utf-8")
        text = normalize_lf(text)

        content, provenance, mode = split_content_provenance(
            text,
            include_separator=include_separator,
            trim_newlines=not keep_leading_trailing_newlines
        )

        content_hash = sha256_bytes(content.encode("utf-8"))
        full_hash = sha256_bytes(text.encode("utf-8"))

        out_text = text
        if update_placeholders:
            out_text = out_text.replace("[FRAMEWORK_SHA256_PLACEHOLDER]", content_hash)
            out_text = out_text.replace("[ADDENDUM_SHA256_PLACEHOLDER]", content_hash)
            if parent_hash:
                out_text = out_text.replace("[PARENT_SHA256_PLACEHOLDER]", parent_hash)

        out_path = os.path.join(out_dir, f"{stem}.canonical{ext}")
        with open(out_path, "w", encoding="utf-8", newline="\n") as f:
            f.write(out_text)

        manifest = {
            "tool": "sol_canonicalize.py",
            "mode": mode,
            "file": infile,
            "out_file": out_path,
            "content_sha256": content_hash,
            "fullfile_sha256": full_hash,
        }
        if parent_hash:
            manifest["parent_sha256"] = parent_hash

    else:
        # Non-markdown: copy as-is, content_hash == full_hash
        data = open(infile, "rb").read()
        content_hash = sha256_bytes(data)
        full_hash = content_hash
        out_path = os.path.join(out_dir, base)
        shutil.copyfile(infile, out_path)
        manifest = {
            "tool": "sol_canonicalize.py",
            "mode": "binary",
            "file": infile,
            "out_file": out_path,
            "content_sha256": content_hash,
            "fullfile_sha256": full_hash,
        }
        if parent_hash:
            manifest["parent_sha256"] = parent_hash

    man_path = os.path.join(out_dir, f"{stem}.sig.json")
    with open(man_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
    return {"manifest": manifest, "manifest_path": man_path, "out_path": out_path}

def merkle_root_for(files: List[str], include_separator=False, keep_leading_trailing_newlines=False) -> Tuple[str, list]:
    leaves = []
    for p in files:
        b = content_bytes_for_any(p, include_separator=include_separator, keep_leading_trailing_newlines=keep_leading_trailing_newlines)
        leaves.append({"file": p, "content_sha256": sha256_bytes(b)})
    layer = [bytes.fromhex(l["content_sha256"]) for l in leaves]
    if not layer:
        return None, leaves
    import hashlib as _h
    while len(layer) > 1:
        if len(layer) % 2 == 1:
            layer.append(layer[-1])
        nxt = []
        for i in range(0, len(layer), 2):
            nxt.append(_h.sha256(layer[i] + layer[i+1]).digest())
        layer = nxt
    return layer[0].hex(), leaves

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("infiles", nargs="+", help="One or more files to canonicalize (Markdown or binary)")
    ap.add_argument("--out-dir", default="", help="Directory for outputs (.canonical.md/.sig.json or copies for binaries)")
    ap.add_argument("--update-placeholders", action="store_true", help="Fill [FRAMEWORK_SHA256_PLACEHOLDER], [ADDENDUM_SHA256_PLACEHOLDER], and [PARENT_SHA256_PLACEHOLDER] where present")
    ap.add_argument("--include-separator", action="store_true", help="Include HR line before provenance in MD content slice")
    ap.add_argument("--keep-leading-trailing-newlines", action="store_true", help="Do not trim a single leading/trailing newline from the MD content slice")
    ap.add_argument("--release-manifest", help="Write a release manifest JSON with a Merkle root over all inputs (content-only for .md, raw for others)")
    ap.add_argument("--parent", help="Path to parent file (its content hash will be computed and used to fill [PARENT_SHA256_PLACEHOLDER])")
    args = ap.parse_args()

    # Compute parent content hash if provided
    parent_hash = None
    if args.parent:
        b = content_bytes_for_any(args.parent, include_separator=args.include_separator, keep_leading_trailing_newlines=args.keep_leading_trailing_newlines)
        parent_hash = sha256_bytes(b)

    results = []
    for f in args.infiles:
        results.append(process_one(
            f,
            out_dir=args.out_dir,
            update_placeholders=args.update_placeholders,
            include_separator=args.include_separator,
            keep_leading_trailing_newlines=args.keep_leading_trailing_newlines,
            parent_hash=parent_hash
        ))

    root, leaves = merkle_root_for(
        args.infiles,
        include_separator=args.include_separator,
        keep_leading_trailing_newlines=args.keep_leading_trailing_newlines
    )
    release = {
        "inputs": [r["manifest"] for r in results],
        "merkle": {"root": root, "files": leaves}
    }
    if args.release_manifest:
        with open(args.release_manifest, "w", encoding="utf-8") as f:
            json.dump(release, f, indent=2)

    print(json.dumps(release, indent=2))

if __name__ == "__main__":
    main()
