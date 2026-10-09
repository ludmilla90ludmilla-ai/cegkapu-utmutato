"""PDF összefoglalók generálása (HU, EN, DE) a webes útmutató szövegeiből.

Használat:  python pdf/build_pdf.py
Eredmény:   pdf/Cegkapu-utmutato-HU.pdf, -EN.pdf, -DE.pdf

A szövegek egyetlen forrása a ../cegkapu-utmutato.html (OFFICE, LINKS, STR).
Ha ott javítasz, futtasd újra ezt a szkriptet. A PDF-specifikus feliratok
(oldalcím, döntési ábra címkéi) a template.html PDFSTR objektumában vannak.
"""
import pathlib
import subprocess
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
    data = extract_data(GUIDE.read_text(encoding="utf-8"))
    html = TEMPLATE.read_text(encoding="utf-8").replace("/*DATA*/", data)
    build = HERE / "build"
    build.mkdir(exist_ok=True)
    page = build / "osszefoglalo.html"
    page.write_text(html, encoding="utf-8")

    for lang in LANGS:
        out = HERE / f"Cegkapu-utmutato-{lang.upper()}.pdf"
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
        print("kész:", out.name)


if __name__ == "__main__":
    main()
