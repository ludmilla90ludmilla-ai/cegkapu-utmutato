"""Az önálló index.html előállítása a GitHub Pages-hez.

Használat:  python build_site.py            → index.html (viktoriawp.eu arculat, ez a tároló)
            python build_site.py <arculat>  → arculati változat (az arculat.py-t igényli)
Forrás:     cegkapu-utmutato.html (claude.ai-artifact formátum: nincs benne <!doctype>/<head>)

A szövegeket mindig a cegkapu-utmutato.html-ben javítsd, utána futtasd ezt
és a pdf/build_pdf.py-t is – arculatonként.
"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
SOURCE = HERE / "cegkapu-utmutato.html"

HEAD = """<!doctype html>
<html lang="hu">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="description" content="Útmutató külföldi tulajdonú cégeknek a Cégkapu (Company Gate, Ungarisches Firmenportal) és az Ügyfélkapu+ használatához – magyarul, angolul és németül.">
<meta name="color-scheme" content="{scheme}">
<style>[hidden] {{ display: none !important; }}</style>
"""


def main() -> None:
    name = sys.argv[1] if len(sys.argv) > 1 else None
    src = SOURCE.read_text(encoding="utf-8")
    scheme = "light dark"
    target = HERE / "index.html"
    if name:
        import arculat
        src = arculat.apply(src, name, "web")
        scheme = arculat.ARCULATOK[name].get("color_scheme", scheme)
        target = arculat.out_dir(name) / "index.html"
        target.parent.mkdir(exist_ok=True)
    # Az artifact elején a <title>, a betűtípus-linkek és a <style> a fejrészbe valók,
    # a többi a törzsbe: a határ az első <header> elem.
    split = src.index('<header class="header">')
    head_part, body_part = src[:split], src[split:]
    html = f"{HEAD.format(scheme=scheme)}{head_part.strip()}\n</head>\n<body>\n{body_part.strip()}\n</body>\n</html>\n"
    target.write_text(html, encoding="utf-8")
    print("kész:", target)


if __name__ == "__main__":
    main()
