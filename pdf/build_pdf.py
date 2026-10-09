"""PDF összefoglalók generálása (HU, EN, DE) a webes útmutató szövegeiből.

Használat:  python pdf/build_pdf.py          → pdf/Cegkapu-utmutato-HU.pdf, -EN.pdf, -DE.pdf
            python pdf/build_pdf.py <arculat> → arculati változat (az arculat.py-t igényli)

A szövegek egyetlen forrása a ../cegkapu-utmutato.html (OFFICE, LINKS, STR).
Ha ott javítasz, futtasd újra ezt a szkriptet. A PDF-specifikus feliratok
(oldalcím, döntési ábra címkéi) a template.html PDFSTR objektumában vannak.
"""
import pathlib
import subprocess
import sys
import tempfile
import time

HERE = pathlib.Path(__file__).resolve().parent
GUIDE = HERE.parent / "cegkapu-utmutato.html"
TEMPLATE = HERE / "template.html"
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
LANGS = ["hu", "en", "de"]


def extract_data(src: str) -> str:
    start = src.index("const OFFICE = {")
    end = src.index("/* ============================================================\n   MŰKÖDÉS")
    return src[start:end]


def main() -> None:
    name = sys.argv[1] if len(sys.argv) > 1 else None
    data = extract_data(GUIDE.read_text(encoding="utf-8"))
    html = TEMPLATE.read_text(encoding="utf-8").replace("/*DATA*/", data)
    out_dir = HERE
    build = HERE / "build"
    if name:
        sys.path.insert(0, str(HERE.parent))
        import arculat
        html = arculat.apply(html, name, "pdf")
        out_dir = arculat.out_dir(name) / "pdf"
        out_dir.mkdir(parents=True, exist_ok=True)
        build = HERE / "build" / name
    build.mkdir(parents=True, exist_ok=True)
    page = build / "osszefoglalo.html"
    page.write_text(html, encoding="utf-8")

    for lang in LANGS:
        out = out_dir / f"Cegkapu-utmutato-{lang.upper()}.pdf"
        out.unlink(missing_ok=True)
        # Nyelvenként külön profil: közös profillal a következő indítás a még futó
        # példánynak adja át a feladatot, és csendben kilép. A zárfájlt az Edge a
        # kilépés után is fogja egy ideig, ezért a törlés hibáját elnyeljük.
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as profile:
            subprocess.run([
                EDGE, "--headless=new", "--disable-gpu", f"--user-data-dir={profile}",
                "--no-pdf-header-footer", "--virtual-time-budget=6000",
                f"--print-to-pdf={out}", f"{page.as_uri()}#{lang}",
            ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        # Az indító folyamat néha előbb lép ki, mint ahogy a PDF a lemezre kerül.
        for _ in range(60):
            if out.exists() and out.stat().st_size > 0:
                break
            time.sleep(0.5)
        else:
            raise SystemExit(f"Nem készült el: {out.name}")
        print("kész:", out)


if __name__ == "__main__":
    main()
