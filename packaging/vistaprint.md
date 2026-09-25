---
type: reference
name: packaging-vistaprint
last_updated: 2026-09-24
tags: [packaging, vistaprint, opendrone, branding, compliance]
---

# OpenDrone retail packaging: content spec and Vistaprint procedure

Black & gold retail boxes for the OpenDrone SKUs, printed via Vistaprint
("Productdozen"). This doc defines what goes on every panel, the exact legal
strings, and the print procedure. The sole compliance basis is
`../../../compliance/CE.md`. This file controls
artwork and production only; it must not invent or override legal copy.

## Theme

- **Ground:** near-black `#0a0a0a` (brand Near Black). **Art/type accent:** packaging gold `#C9A227`.
- The canonical screen and production colours are defined in `../BRAND.md`, `../tokens/` and `../standards/`; black/gold is a packaging-only direction. Use the generated OpenDrone and Incutec lockups from this repository.
- Board artwork: flat gold vector front/back renders of each PCB, generated from the real KiCad files with `../../../scripts/hardware/kicad/packaging_art.py` (SVG, print-ready). `--color` and `--body` are required (the packaging design owns the palette); for the black box pass `--color '#C9A227' --holes '#0a0a0a' --body '#0a0a0a'`. See `../../../scripts/README.md`.

## Panel-by-panel content

### Front (face)
- **OpenDrone** product name, marketed form: e.g. *OpenESC 30x30*, *OpenFC Lite Mini*, *OpenRX Lite* (`../../../stock/product_skus.json` for the canonical list).
- Gold board art (front side of the board is the default face; the ESC's back is the better-looking side, pick per SKU).
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
| OpenRX Lite U.FL (OPENRX-LITE-UFL) | `ExpressLRS 2.4 GHz receiver · U.FL` |
| OpenFrame 3 (OPENFRAME-3) | `3-inch freestyle frame · carbon fibre` |
| OpenFrame 5 (OPENFRAME-5) | `5-inch freestyle frame · carbon fibre` |

Sources for the last three rows: OpenRX Lite U.FL is the OpenRX Lite board
(2.4 GHz, SX1281, ExpressLRS, 10.0 x 11.5 mm) with a U.FL antenna connector in
place of the ceramic antenna (`OpenDrone/hardware/OpenRX-Lite-UFL` README). The
frames are CNC carbon fibre sets in 3" and 5" freestyle sizes with an aluminium
camera mount pair (`OpenDrone/hardware/OpenFrame` README). Frames have no PCB,
so the gold board-art rule below does not apply to them; their face art is not
defined.

### Box fit for the three added SKUs

No box size, board grade or Vistaprint order is recorded for any SKU, so none of
these is a derived spec. Each is **proposed, not yet ordered**.

| SKU | Contents envelope | Box | Material and print |
|---|---|---|---|
| OPENRX-LITE-UFL | same 10.0 x 11.5 mm board as OPENRX-LITE | the OPENRX-LITE box, which is itself unsized | as OPENRX-LITE: Productdozen, CMYK digital, matte, black and gold theme above |
| OPENFRAME-3 | flat stack 112 x 50 x 37 mm, fasteners excluded | Productdozen, inner at least 122 x 60 x 42 mm | Productdozen, CMYK digital, matte; board grade unknown |
| OPENFRAME-5 | flat stack 147 x 67.6 x 48.5 mm, fasteners excluded | Productdozen, inner at least 157 x 78 x 54 mm | Productdozen, CMYK digital, matte; board grade unknown |

Fit calculation. Part sizes come from the Dongguan Silt Metal quotation sheets
of 2026-08-10 (`sourcing/files/email/dongguan-silt-metal/`), whose plate
thicknesses match `OpenDrone/hardware/OpenFrame/docs/DESIGN.md`. That geometry is
the pre-reset design; the OpenFrame README states the CAD is not finalised, so
re-run this when the drawings change.

- 3": footprint is the largest plate outline, top plate 112 x 32.5 mm against
  bottom and middle plates 50 mm wide, so 112 x 50 mm. Stack height: 4 arms at
  4.0 + bottom 2.5 + middle 2.5 + top 2.0 + cross 4.0 + two camera mounts at
  5.0 = 37.0 mm.
- 5": footprint top plate 147 mm long, bottom and middle plates 67.6 mm wide, so
  147 x 67.6 mm. Stack height: 4 arms at 6.0 + bottom 3.0 + middle 3.0 + top 2.5
  + cross 6.0 + two camera mounts at 5.0 = 48.5 mm. The 5" camera mount on that
  sheet repeats the 3" dimension (39.53 x 26.5 x 5.0 mm), so its height is
  unverified.
- Minimum inner box = envelope plus 5 mm clearance per side on length and width
  and 5 mm on height, rounded up to whole millimetres.
- The only packaging bought so far, the RAJAPACK 18 x 26.5 cm padded mailer
  (order 2493987), is the outer shipping layer and not a retail box. Both flat
  stacks fit its face (180 x 265 mm against 112 x 50 and 147 x 67.6 mm), but its
  usable thickness is not recorded, so it is not proposed as the box.

- "Open Source Hardware" line or the OSHW-style gear mark: the open design is the differentiator; it earns front-panel space.

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

### Variable data: print as a label, not on the box
Vistaprint boxes are fixed-artwork bulk prints. Everything unit- or
batch-specific goes on a small in-house label applied to a reserved matte area
(~50×25 mm) on the back panel:
- `SN: [batch]-[serial]` (GPSR traceability)
- EAN-13 barcode: **no GTINs exist yet anywhere in the vault**; the area is
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
- The INCUTEC word mark was filed as an EU trade mark on 3 July 2026 and is
  not registered yet; OpenDrone is not filed. Use TM, not (R), on packaging.
- Manufacturer identity and contact come from `CE.md`, including
  `contact@opendrone.be`; other documents are not authoritative for the box.

## Vistaprint procedure

1. **Product:** Vistaprint "Productdozen" (mailer/tuck box). The editor shows
   the flat dieline (e.g. 39.84 × 27.05 cm for the mid-size box) with bleed
   ("Uitloop") and fold lines. Pick the smallest box that fits board + ESD bag +
   insert card; prefer **one shared box size across all 30×30/20×20 SKUs** so
   art changes are the only per-SKU cost.
2. **Skip the "Beschrijf uw ontwerpidee" design service.** All artwork is
   generated locally (board SVGs + brand vectors + this copy spec); the service
   adds a round-trip with a designer who has none of the compliance context.
3. **Workflow:** download Vistaprint's dieline template for the chosen box,
   compose the full flat sheet (Inkscape/Illustrator) with the gold SVGs placed
   per panel, export a single PDF, and use **"Upload ontwerp"** on the
   Buitenkant (outside) surface. Only fall back to the in-browser editor for
   text tweaks; it can't handle the vector art placement precisely.
4. **Color:** Vistaprint product boxes are CMYK digital print, no foil/spot
   gold. Convert gold `#C9A227` to CMYK ≈ `C20 M32 Y95 K10` and check a single
   proof box before a volume run; rich black `C40 M40 Y40 K100` for the ground.
   Matte finish suits the flat-vector look better than gloss.
5. **Files Vistaprint accepts:** PDF preferred for print surfaces; PNG/JPG under
   10 MB for the design-service brief (not used) and editor uploads.
6. **Order sizing:** box unit price drops steeply with quantity, so the
   small-quantity editor price is a trap. Order per-SKU volume aligned with
   the first production batch, one proof unit first.

## Insert card

Per `CE.md`: front = product name + quick-start wiring + product-specific
safety warnings + `Full manual: opendrone.be/docs/[product]`;
back = open-source notice (CERN-OHL-S-2.0 + source URL), WEEE disposal, DoC
reference, manufacturer info, bilingual (NL/FR) warning block. Vistaprint
flyers/postcards print these cheaply in the same black/gold theme.
