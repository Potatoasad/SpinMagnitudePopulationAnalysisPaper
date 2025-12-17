# save as tikz_rgb_to_gray.py  (Python 3)
import re, sys, pathlib, shutil

# sRGB-ish luminance weights (fast & "good enough" for diagrams)
W = (0.2126, 0.7152, 0.0722)

# Regex matches: {rgb, 255:red, 238; green, 0; blue, 0 }
PAT = re.compile(
    r"""\{ \s* rgb \s* , \s* 255 \s* : \s*
        red \s* , \s* (?P<R>\d{1,3}) \s* ; \s*
        green \s* , \s* (?P<G>\d{1,3}) \s* ; \s*
        blue \s* , \s* (?P<B>\d{1,3}) \s*
        \}""",
    re.IGNORECASE | re.VERBOSE,
)

def to_gray(m):
    R, G, B = (int(m.group('R')), int(m.group('G')), int(m.group('B')))
    # clamp just in case, then compute gray and clamp again
    R = max(0, min(255, R)); G = max(0, min(255, G)); B = max(0, min(255, B))
    gray = round(W[0]*R + W[1]*G + W[2]*B)
    gray = max(0, min(255, gray))
    # keep the same TikZ/xcolor "rgb, 255" model, but with R=G=B=gray
    return f"{{rgb, 255:red, {gray}; green, {gray}; blue, {gray} }}"

def convert_file(p: pathlib.Path):
    txt = p.read_text(encoding="utf-8", errors="ignore")
    new = PAT.sub(to_gray, txt)
    if new != txt:
        shutil.copy2(p, p.with_suffix(p.suffix + ".bak"))  # backup once
        p.write_text(new, encoding="utf-8")
        return True
    return False

def main(paths):
    any_changed = False
    for name in paths:
        p = pathlib.Path(name)
        if p.is_file():
            if convert_file(p):
                print(f"grayscaled: {p}")
                any_changed = True
        else:
            for f in p.rglob("*"):
                if f.suffix.lower() in {".tex", ".tikz"} and f.is_file():
                    if convert_file(f):
                        print(f"grayscaled: {f}")
                        any_changed = True
    if not any_changed:
        print("No rgb,255 color blocks found (or nothing to change).")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python tikz_rgb_to_gray.py <file_or_dir> [more ...]")
        sys.exit(1)
    main(sys.argv[1:])
