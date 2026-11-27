# Cursed Entertainment: Corporate Identity

## Font

**FUTURA - ALL VARIANTS (BUT NO OTHER FONTS)**

**Where the rule applies:** corporate Cursed Entertainment material, meaning the website, homepages, ads and
anything else that speaks for the company. There it's Futura and nothing else: no Segoe UI, no system-ui, no
Arial, no Roboto, no Google Fonts, and no monospace either (code blocks are set in Futura too).

**Games** may use other fonts when the game needs them, though it isn't recommended: Futura is still the first
choice.

### The cuts

| Cut | File | Family name inside the file | CSS weight |
|---|---|---|---|
| Light | `futura light bt.ttf` | Futura Lt BT | 300 |
| Book | `Futura Book font.ttf` | Futura Bk BT | 400 |
| Book Italic | `Futura Book Italic font.ttf` | Futura Bk BT | 400 italic |
| Bold Italic | `Futura Bold Italic font.ttf` | Futura Md BT | 700 italic |
| Heavy | `Futura Heavy font.ttf` | Futura Hv BT | 700 / 800 |
| Heavy Italic | `Futura Heavy Italic font.ttf` | Futura Hv BT | 800 italic |
| Extra Black | `Futura Extra Black font.ttf` | Futura XBlk BT | 900 |
| Light Condensed | `Futura Light font.ttf` | Futura LtCn BT | `Futura Condensed` 300 |
| Bold Condensed | `Futura Bold font.ttf` | Futura BdCn BT | `Futura Condensed` 700 |

Watch out: the file called "Futura Bold" is really **Bold Condensed**, and "Futura Light" is really
**Light Condensed**. The upright light cut is `futura light bt.ttf`. There's no upright Bold, so bold text uses Heavy.

- **Body text:** Book
- **Headings and buttons:** Heavy
- **Logos, titles and big display text:** Extra Black
- **Captions and small print:** Light
- **Tall, narrow labels:** Condensed

### On the web

Put the font files in the site's `fonts/` folder and load them once, at the top of the main CSS:

```css
@font-face { font-family: "Futura"; font-weight: 300; src: local("FuturaBT-Light"), url("fonts/futura-light.ttf"); }
@font-face { font-family: "Futura"; font-weight: 400; src: local("FuturaBT-Book"), url("fonts/futura-book.ttf"); }
@font-face { font-family: "Futura"; font-weight: 400; font-style: italic; src: local("FuturaBT-BookItalic"), url("fonts/futura-book-italic.ttf"); }
@font-face { font-family: "Futura"; font-weight: 500 700; src: local("FuturaBT-Heavy"), url("fonts/futura-heavy.ttf"); }
@font-face { font-family: "Futura"; font-weight: 500 700; font-style: italic; src: local("FuturaBT-BoldItalic"), url("fonts/futura-bold-italic.ttf"); }
@font-face { font-family: "Futura"; font-weight: 800; src: local("FuturaBT-Heavy"), url("fonts/futura-heavy.ttf"); }
@font-face { font-family: "Futura"; font-weight: 800; font-style: italic; src: local("FuturaBT-HeavyItalic"), url("fonts/futura-heavy-italic.ttf"); }
@font-face { font-family: "Futura"; font-weight: 900; src: local("FuturaBT-ExtraBlack"), url("fonts/futura-extra-black.ttf"); }
@font-face { font-family: "Futura Condensed"; font-weight: 300; src: local("FuturaBT-LightCondensed"), url("fonts/futura-light-condensed.ttf"); }
@font-face { font-family: "Futura Condensed"; font-weight: 700; src: local("FuturaBT-BoldCondensed"), url("fonts/futura-bold-condensed.ttf"); }

body, button, input, select, textarea, code, pre { font-family: "Futura", sans-serif; }
```

`sans-serif` is only there as the browser's required last resort. It never stands in for Futura on purpose.

### Languages Futura can't write

This Futura has Latin letters with accents, quotes, dashes and ©. It has **no Cyrillic** (Русский, Српски),
**no Japanese, Chinese or Korean**, and **no ☆**. For those characters only, the browser borrows them from the
system. Everything else on the page stays Futura.

## Colours

**Corporate colours** are used for the websites, ads and anything with the logo:

| Name | Hex |
|---|---|
| Blue (primary) | `#005184` |
| Blue (secondary) | `#007ab7` |
| Blue (light) | `#34A9E3` |
| Blue (accent) | `#168FCC` |
| Blue (dark) | `#004067` |
| Pink (tertiary) | `#f088e9` |
| Greys | `#868686`, `#c2c2c2` |
| Shadow navy | `#001725` |
| White | `#ffffff` |

**Program UIs** (apps, tools, windows; not the robots) use dark greys with Cursed pink:

| Name | Hex |
|---|---|
| Backgrounds | `#1a1a1a`, `#242424`, `#2b2b2b` |
| Lines | `#3a3a3a` |
| Text | `#e6e6e6` |
| Muted text | `#9a9a9a` |
| Pink | `#e0408a` |
| Pink buttons | `#c2186b` |
| Pink links | `#f29cc0` |

Program UIs use solid colours only: no gradients, no glows and no drop shadows.

## Logo

The pink graffiti **CURSED** over a thin white **entertainment**.

## Credit

`Farica☆Kimora © Cursed Entertainment`: the © symbol, never "(c)".

---

<div align="center">© Cursed Entertainment 2026</div>
