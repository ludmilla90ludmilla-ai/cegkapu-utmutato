"""A webes útmutató ellenőrzése fej nélküli Edge-dzsel.

Használat:  python check_guide.py [hash ...]
            pl. python check_guide.py hu en-ut-a de-kesz-b

Eredmény az ellenorzes/ mappában (nincs verziókövetve):
  teszt.png        – „ALL OK”, ha a három nyelv (hu/en/de) szótára ugyanazokat a
                     kulcsokat tartalmazza, és mind a 33 képernyő (11 × 3 nyelv)
                     hiba nélkül megjelenik; különben a hibák listája
  <hash>.png       – asztali (1280 px) képernyőkép a megadott képernyőkről
  <hash>-mobil.png – ugyanez 390 px széles iframe-ben (telefonos nézet)
"""
import pathlib
import subprocess
import sys
import tempfile
import time

HERE = pathlib.Path(__file__).resolve().parent
SOURCE = HERE / "cegkapu-utmutato.html"
OUT = HERE / "ellenorzes"
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
HEAD = ('<!doctype html><html><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1"></head><body>')

TEST = """
<pre id="test" style="position:fixed;inset:0;z-index:99;margin:0;padding:20px;background:#fff;color:#000;font:16px monospace;white-space:pre-wrap"></pre>
<script>
window.onerror = (m) => { document.getElementById("test").textContent += "ERR " + m + "\\n"; };
setTimeout(() => {
  const out = [];
  const paths = (o, p = "") => typeof o !== "object" || o === null ? [p + ":" + typeof o]
    : Object.keys(o).flatMap(k => paths(o[k], p + "." + k));
  const hu = new Set(paths(STR.hu));
  for (const l of Object.keys(STR).filter(l => l !== "hu")) {
    const s = new Set(paths(STR[l]));
    for (const x of hu) if (!s.has(x)) out.push(l + " HIÁNYZIK " + x);
    for (const x of s) if (!hu.has(x)) out.push(l + " FÖLÖSLEGES " + x);
  }
  for (const l of Object.keys(STR)) for (const id of SCREENS) {
    try { lang = l; id.startsWith("kesz-") ? VIEWS.kesz(id.slice(5)) : VIEWS[id](); }
    catch (e) { out.push("MEGJELENÍTÉS " + l + " " + id + " " + e.message); }
  }
  document.getElementById("test").textContent += (out.join("\\n") || "ALL OK");
}, 300);
</script>
"""


def shoot(url: str, png: pathlib.Path, size: str) -> None:
    png.unlink(missing_ok=True)
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as profile:
        subprocess.run([
            EDGE, "--headless=new", "--disable-gpu", "--hide-scrollbars", f"--user-data-dir={profile}",
            "--virtual-time-budget=4000", f"--window-size={size}", f"--screenshot={png}", url,
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for _ in range(40):
        if png.exists() and png.stat().st_size > 0:
            print("kész:", png.relative_to(HERE))
            return
        time.sleep(0.5)
    print("NEM KÉSZÜLT EL:", png.name)


def main() -> None:
    OUT.mkdir(exist_ok=True)
    src = SOURCE.read_text(encoding="utf-8")
    preview = OUT / "preview.html"
    preview.write_text(HEAD + src + "</body></html>", encoding="utf-8")
    test = OUT / "teszt.html"
    test.write_text(HEAD + src + TEST + "</body></html>", encoding="utf-8")

    shoot(test.as_uri(), OUT / "teszt.png", "1000,300")
    for h in sys.argv[1:] or ["hu", "en-ut-a", "de-kesz-b"]:
        shoot(f"{preview.as_uri()}#{h}", OUT / f"{h}.png", "1280,1400")
        frame = OUT / f"mobil-{h}.html"
        frame.write_text(
            '<!doctype html><html><body style="margin:0;background:#888;padding:10px">'
            f'<iframe src="preview.html#{h}" style="width:390px;height:1500px;border:0;background:#fff"></iframe>'
            "</body></html>", encoding="utf-8")
        shoot(frame.as_uri(), OUT / f"{h}-mobil.png", "420,1520")


if __name__ == "__main__":
    main()
