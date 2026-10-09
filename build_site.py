"""Az önálló index.html előállítása a GitHub Pages-hez.

Használat:  python build_site.py
Forrás:     cegkapu-utmutato.html (claude.ai-artifact formátum: nincs benne <!doctype>/<head>)
Eredmény:   index.html (teljes HTML-dokumentum, ezt szolgálja ki a GitHub Pages)

A szövegeket mindig a cegkapu-utmutato.html-ben javítsd, utána futtasd ezt
és a pdf/build_pdf.py-t is.
"""
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
SOURCE = HERE / "cegkapu-utmutato.html"
TARGET = HERE / "index.html"

HEAD = """<!doctype html>
<html lang="hu">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="description" content="Útmutató külföldi tulajdonú cégeknek a Cégkapu (Company Gate, Ungarisches Firmenportal) és az Ügyfélkapu+ használatához – magyarul, angolul és németül.">
<meta name="color-scheme" content="light dark">
<style>[hidden] { display: none !important; }</style>
"""


def main() -> None:
    src = SOURCE.read_text(encoding="utf-8")
    # Az artifact elején a <title>, a betűtípus-linkek és a <style> a fejrészbe valók,
    # a többi a törzsbe: a határ az első <header> elem.
    split = src.index('<header class="header">')
    head_part, body_part = src[:split], src[split:]
    html = f"{HEAD}{head_part.strip()}\n</head>\n<body>\n{body_part.strip()}\n</body>\n</html>\n"
    TARGET.write_text(html, encoding="utf-8")
    print("kész:", TARGET.name)


if __name__ == "__main__":
    main()
