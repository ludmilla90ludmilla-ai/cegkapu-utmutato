# Cégkapu-útmutató

Interaktív útmutató külföldi tulajdonú magyarországi cégeknek: mi a Cégkapu és az Ügyfélkapu+, és hogyan vehetik fel könyvelőjüket ügykezelőnek a cég Cégkapujában. Magyarul, angolul és németül.

**Megnyitás:** https://ludmilla90ludmilla-ai.github.io/cegkapu-utmutato/

Nyelv és útvonal közvetlenül is megnyitható a link végére írt jelöléssel, például:

| Jelölés | Mit nyit meg |
|---|---|
| `#en` | angol nyitóoldal |
| `#de` | német nyitóoldal |
| `#en-ut-a` | saját Ügyfélkapu+ (Client Gate+) útvonal, angolul |
| `#de-ut-b` | ügyvédi útvonal, németül |

Nyomtatható összefoglaló (2 oldal): [magyar](pdf/Cegkapu-utmutato-HU.pdf) · [English](pdf/Cegkapu-utmutato-EN.pdf) · [Deutsch](pdf/Cegkapu-utmutato-DE.pdf)

## Frissítés

A szövegek egyetlen forrása a `cegkapu-utmutato.html` (az `STR` szótár nyelvenként). Javítás után:

```bash
python build_site.py
python pdf/build_pdf.py
```

Az első az `index.html`-t állítja elő (ezt szolgálja ki a GitHub Pages), a második a három PDF-et (Microsoft Edge kell hozzá).

Ellenőrzés: `python check_guide.py` – a nyelvi szótárak egyezését és mind a 33 képernyő megjelenítését nézi, és képernyőképeket készít az `ellenorzes/` mappába.

Az útmutató a 2026. októberi szabályokat követi. Források: tarhely.gov.hu, kau.gov.hu, a magyar külképviseletek tájékoztatói.
