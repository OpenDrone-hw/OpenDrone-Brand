---
type: reference
name: packaging-vistaprint
last_updated: 2026-07-03
tags: [packaging, vistaprint, opendrone, branding, compliance]
---

# OpenDrone retail packaging — content spec + Vistaprint procedure

Black & gold retail boxes for the OpenDrone SKUs, printed via Vistaprint
("Productdozen"). This doc defines what goes on every panel, the exact legal
strings, and the print procedure. The sole compliance basis is
`../../../compliance/CE.md`. This file controls
artwork and production only; it must not invent or override legal copy.

## Theme

- **Ground:** near-black `#0a0a0a` (brand Near Black). **Art/type accent:** packaging gold `#C9A227`.
- The canonical screen and production colours are defined in `../BRAND.md`, `../tokens/` and `../standards/`; black/gold is a packaging-only direction. Use the generated OpenDrone and Incutec lockups from this repository.
- Board artwork: flat gold vector front/back renders of each PCB, generated from the real KiCad files with `../../../scripts/hardware/kicad/packaging_art.py` (SVG, print-ready). For the black box pass `--holes '#0a0a0a' --body '#0a0a0a'`. See `../../../scripts/README.md`.

## Panel-by-panel content

### Front (face)
- **OpenDrone** product name, marketed form: e.g. *OpenESC 30x30*, *OpenFC Lite Mini*, *OpenRX Lite* (`../../../stock/product_skus.json` for the canonical list).
- Gold board art (front side of the board is the default face; the ESC's back is the better-looking side — pick per SKU).
- One spec line, gold, max ~6 words. Per current SKUs:

| SKU | Spec line |
|---|---|
| OpenESC 30x30 (OPENESC-3030) | `4-in-1 ESC · 3-6S · 60 A/channel · AM32` |
| OpenESC 20x20 (OPENESC-2020) | `4-in-1 ESC · 3-6S · 40 A/channel · AM32` |
| OpenFC Lite (OPENFC-LITE-3030) | `Flight controller · 2-6S · Betaflight` |
| OpenFC Lite Mini (OPENFC-LITE-2020) | `Flight controller · 2-6S · Betaflight` |
| OpenRX Lite (OPENRX-LITE) | `ExpressLRS 2.4 GHz receiver` |
| OpenRX Mono (OPENRX-MONO) | `ExpressLRS 868 MHz + 2.4 GHz` |
| OpenRX Gemini (OPENRX-GEMINI) | `ExpressLRS true-diversity receiver` |

- "Open Source Hardware" line or the OSHW-style gear mark — the open design is the differentiator; it earns front-panel space.

### Back (legal + info panel)
Resolve legal fields from the canonical product record at artwork approval:

```
[Product Name]
Model: [internal SKU]        (SN/batch: see label note below)

[manufacturer legal name, postal address and contact from CE.md]

[CE only when canonical status is READY]   [WEEE crossed-out bin if applicable]
Open Source Hardware: CERN-OHL-S-2.0
Source & docs: [source and documentation URL approved against CE.md]
[QR → opendrone.be/doc/[sku]]
Made in China · Designed in Belgium
```

- **Radio SKUs (OpenRX family) additionally:** use only the final frequency bands and measured maximum power recorded in `CE.md` after its declaration gates pass. Do not print design limits as measured declarations.
- **Warning block:** derive the short form from the completed product risk assessment and instructions referenced by the canonical technical-file requirements:
  `WARNING: Not a toy. Intended for users aged 18+ with FPV drone assembly experience. Risk of fire if wired incorrectly. Full manual: opendrone.be/docs/[product]`
- Language: follow the Member-State language rule in `CE.md`; do not treat English-only box copy or an online manual as a blanket substitute for required supplied instructions.

### Sides
- Spine 1: product name + spec line (readable on a shelf).
- Spine 2: `OpenDrone by Incutec` wordmark + `opendrone.be`.

### Variable data — print as a label, not on the box
Vistaprint boxes are fixed-artwork bulk prints. Everything unit- or
batch-specific goes on a small in-house label applied to a reserved matte area
(~50×25 mm) on the back panel:
- `SN: [batch]-[serial]` (GPSR traceability)
- EAN-13 barcode — **no GTINs exist yet anywhere in the vault**; the area is
  reserved until GS1 codes are assigned. Product and bundle identity must match
  the declaration unit in `CE.md`.
- Hardware revision (e.g. `V1.0`).

This keeps one box print run valid across batches and revisions.

## Hard constraints before print

- **Do not apply or use packaging bearing CE unless the exact declaration unit
  is `READY`, every canonical gate passes and its DoC is signed.** Reserve the
  CE/WEEE zone for a controlled label until then.
- Resolve WEEE producer registration and marking against authoritative company
  and compliance evidence before approving artwork; WEEE is separate from CE
  and the DoC.
- Trademarks unregistered (`compliance/ip/trademark-registration.md`): use ™,
  never ®.
- Manufacturer identity and contact come from `CE.md`, including
  `contact@opendrone.be`; other documents are not authoritative for the box.

## Vistaprint procedure

1. **Product:** Vistaprint "Productdozen" (mailer/tuck box). The editor shows
   the flat dieline (e.g. 39.84 × 27.05 cm for the mid-size box) with bleed
   ("Uitloop") and fold lines. Pick the smallest box that fits board + ESD bag +
   insert card; prefer **one shared box size across all 30×30/20×20 SKUs** so
   art changes are the only per-SKU cost.
2. **Skip the €12 "Beschrijf uw ontwerpidee" design service.** All artwork is
   generated locally (board SVGs + brand vectors + this copy spec); the service
   adds a round-trip with a designer who has none of the compliance context.
3. **Workflow:** download Vistaprint's dieline template for the chosen box,
   compose the full flat sheet (Inkscape/Illustrator) with the gold SVGs placed
   per panel, export a single PDF, and use **"Upload ontwerp"** on the
   Buitenkant (outside) surface. Only fall back to the in-browser editor for
   text tweaks — it can't handle the vector art placement precisely.
4. **Color:** Vistaprint product boxes are CMYK digital print — no foil/spot
   gold. Convert gold `#C9A227` to CMYK ≈ `C20 M32 Y95 K10` and check a single
   proof box before a volume run; rich black `C40 M40 Y40 K100` for the ground.
   Matte finish suits the flat-vector look better than gloss.
5. **Files Vistaprint accepts:** PDF preferred for print surfaces; PNG/JPG under
   10 MB for the design-service brief (not used) and editor uploads.
6. **Order sizing:** box unit price drops steeply with quantity; the €45.91
   editor price is the small-quantity trap. Order per-SKU volume aligned with
   the first production batch, one proof unit first.

## Insert card

Per `CE.md`: front = product name + quick-start wiring + product-specific
safety warnings + `Full manual: opendrone.be/docs/[product]`;
back = open-source notice (CERN-OHL-S-2.0 + source URL), WEEE disposal, DoC
reference, manufacturer info, bilingual (NL/FR) warning block. Vistaprint
flyers/postcards print these cheaply in the same black/gold theme.
