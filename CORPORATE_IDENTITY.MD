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

The corporate colours, exactly as the 2023 site defines them (`cursedentertainment/styles/colors.css`):

```css
:root {
  --color-primary: #005184;
  --color-primary-light: #34A9E3;
  --color-primary-dark: #004067;
  --color-secondary: #007ab7;
  --color-tertiary: #f088e9;
  --color-accent: #168FCC;
  --color-white: #fff;
  --color-grey: #868686;
  --color-light-grey: #c2c2c2;
  --color-shadow: rgb(0, 23, 37);
  --color-text: var(--color-white);
}
```

| Swatch | Name | Hex | What it's for |
|---|---|---|---|
| ![](https://img.shields.io/badge/-%20%20%20%20%20%20-005184?style=flat-square) | Primary | `#005184` | Main brand blue; button hover |
| ![](https://img.shields.io/badge/-%20%20%20%20%20%20-34A9E3?style=flat-square) | Primary light | `#34A9E3` | Highlights, hover outlines |
| ![](https://img.shields.io/badge/-%20%20%20%20%20%20-004067?style=flat-square) | Primary dark | `#004067` | Buttons, tab hover, scrollbar hover |
| ![](https://img.shields.io/badge/-%20%20%20%20%20%20-007ab7?style=flat-square) | Secondary | `#007ab7` | **The page background**, header, tabs, scrollbar, badges |
| ![](https://img.shields.io/badge/-%20%20%20%20%20%20-168FCC?style=flat-square) | Accent | `#168FCC` | Accents |
| ![](https://img.shields.io/badge/-%20%20%20%20%20%20-f088e9?style=flat-square) | Tertiary (pink) | `#f088e9` | The pink: special buttons (the 18+ gate), the pink fade |
| ![](https://img.shields.io/badge/-%20%20%20%20%20%20-ffffff?style=flat-square) | White | `#ffffff` | All text, thin borders and lines |
| ![](https://img.shields.io/badge/-%20%20%20%20%20%20-868686?style=flat-square) | Grey | `#868686` | Muted |
| ![](https://img.shields.io/badge/-%20%20%20%20%20%20-c2c2c2?style=flat-square) | Light grey | `#c2c2c2` | Muted, light |
| ![](https://img.shields.io/badge/-%20%20%20%20%20%20-001725?style=flat-square) | Shadow | `#001725` (`rgb(0, 23, 37)`) | Shadow navy |

**Logo pinks** are drawn into the logo artwork and are not used for page colours. They blend from hot pink
`#f82098` to magenta `#f020d0`, with a black outline and a white outer rim.

**Program UIs** (apps, tools and windows; not the robots, and not the corporate site) use dark greys with Cursed pink:

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

## The look (from the 2023 site)

- **Page:** the background is secondary blue `#007ab7` and all text is white.
- **Type:** Futura everywhere, **light weight with 3px letter-spacing** on all text. Headings (`h1`, `h2`) are
  bold and centred, paragraphs are left-aligned, and lists have no bullets.
- **Header:** fixed at the top, in secondary blue, with a thin white line under it. The logo animates in over 2 seconds.
- **Buttons:** primary dark `#004067` with white text, 4px corners, 10 × 15px padding, 16px text. On hover they
  turn primary `#005184`.
- **Link tabs** (the online buttons): secondary blue with a thin white border and rounded `10px / 5px` corners.
  On hover they turn primary dark, with a primary-light `#34A9E3` border.
- **Pink pill buttons:** tertiary pink `#f088e9` with 40px round ends, in Futura light with 3px spacing. They're
  used for the 18+ gate.
- **18+ gate:** pictures stay blurred (10px) until you confirm, then sharpen over 0.8 seconds.
- **Scrollbar:** 10px wide, with a secondary-blue thumb with 5px corners that turns primary dark on hover.
- **Animations:**
  - `scale-fade`: things grow in from nothing.
  - `scale-fade2`: things shrink in from five times their size.
  - `image-fade`: pictures fade in.
  - `blink`: secondary flashing to primary.
  - `fade`: pink fading into secondary blue.
- **Corners:** soft. Use 4-16px on panels and cards, and round ends on pills and avatars.
- **Banner ads:** full width, with 10px corners.
- **Futura on the web:** the 2023 site asks Google Fonts for Futura, but Google Fonts doesn't have it. The site
  only shows Futura on PCs that have it installed. New sites load it with the `@font-face` block above.

## Voice

- **Tagline:** *It's Damn Fun*
- **Description:** "Cursed Entertainment: games, music, stories, films and tools. It's Damn Fun."
- **Tone:** campy 80s horror, with neon arcades and horror ads. Sophie, the mascot, is played straight-creepy.
- **Pillars:** Games · Augmented Reality · Music · AI · Software

## Logo

- **The mark:** a pink graffiti/horror **CURSED** (hot pink to magenta, black outline, white rim) over a thin,
  wide-spaced white **entertainment**.
- **Files** (in `cursedentertainment/images/logos/`):
  - `cursed-logo.png`: stacked, 1109 × 597.
  - `logo-wide.png`: wide, 2100 × 441, with "entertainment" in white.
  - `logo-wide-grey.png`: wide, 2100 × 441, with "entertainment" in grey. It's the one used in README footers.
- **Favicon:** `cursedFavicon.png`.
- **QR codes:** in `images/qr-codes/`. The site QR is pink `#e0408a` on white, in a near-black `#111118` frame
  with "cursedentertainment" under it.
- **Banner ads:** in `images/banner-ads/` (`araknia-ad.png`, `cechat-ad.png`, `nystylla-ad.jpg`).

## Credit

`Farica☆Kimora © Cursed Entertainment`: the © symbol, never "(c)".

---

<div align="center">© Cursed Entertainment 2026</div>
