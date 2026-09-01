#!/usr/bin/env python3
"""
Apply the fleet setup to any mounted EdgeTX radio SD (GX12 or Pocket).
Usage: python3 apply_radio_setup.py "/Volumes/NO NAME" [path/to/boot.wav]

Does, idempotently:
  MODEL (MODELS/model00.yml):
    - name -> "QUAD"
    - CH5-8 (destCh 4-7) srcRaw -> SA / SB / SC / SD  (arm / mode / turtle / aux)
    - delete mixes destCh >= 8
    - remove any voice callouts (customFn) and switch warnings (switchWarning)
  RADIO (RADIO/radio.yml):
    - manuallyEdited: 1  (so EdgeTX accepts the hand-edit / recomputes checksum)
    - dontPlayHello: 1   (silence stock jingle so only boot.wav plays)
    - boot-sound global function: ON -> PLAY_TRACK boot -> 1x
  SOUNDS: copy boot.wav into SOUNDS/en/
NOTE: keeps each radio's own board/calibration in radio.yml. Boot GF is per-radio (radio.yml is board-specific), which is why this runs per radio rather than copying radio.yml.
"""
import sys, os, shutil

SD = sys.argv[1].rstrip("/")
BOOTWAV = sys.argv[2] if len(sys.argv) > 2 else None
MODEL = f"{SD}/MODELS/model00.yml"
RADIO = f"{SD}/RADIO/radio.yml"
SOUNDS = f"{SD}/SOUNDS/en"

SW = {4: "SA", 5: "SB", 6: "SC", 7: "SD"}  # destCh -> switch

# ---- backup ----
for p in (MODEL, RADIO):
    if os.path.exists(p):
        shutil.copy(p, p + ".bak")

# ---------------- MODEL ----------------
with open(MODEL) as f:
    lines = f.readlines()

# name -> QUAD (first name under header)
for i, l in enumerate(lines):
    if l.startswith("   name: ") and lines[i-1].rstrip("\n") == "header: ":
        lines[i] = '   name: "QUAD"\n'
        break
else:
    # fallback: header block may have different spacing; set the model header name
    for i, l in enumerate(lines):
        if l.rstrip() == "header:":
            # next name line
            for j in range(i+1, min(i+6, len(lines))):
                if lines[j].strip().startswith("name:"):
                    lines[j] = '   name: "QUAD"\n'
                    break
            break

# remap CH5-8 srcRaw by locating each mix entry's destCh then its srcRaw
i = 0
while i < len(lines):
    s = lines[i].strip()
    if s.startswith("destCh:"):
        try:
            ch = int(s.split(":")[1])
        except ValueError:
            i += 1; continue
        if ch in SW:
            # find srcRaw within this entry (next ~3 lines)
            for j in range(i+1, min(i+4, len(lines))):
                if lines[j].strip().startswith("srcRaw:"):
                    indent = lines[j][:len(lines[j]) - len(lines[j].lstrip())]
                    lines[j] = f'{indent}srcRaw: "{SW[ch]}"\n'
                    break
    i += 1

# delete mixes destCh >= 8  (from the ' -' before destCh:8 to before expoData:)
start = None
for i, l in enumerate(lines):
    if l.strip() == "destCh: 8":
        start = i - 1 if lines[i-1].strip() == "-" else i
        break
if start is not None:
    end = next((j for j in range(start, len(lines)) if lines[j].startswith("expoData:")), None)
    if end is not None:
        del lines[start:end]

# remove callouts (customFn before thrTraceSrc) and switch warnings (switchWarning before rssiSource)
def del_block(lines, start_key, next_key):
    st = next((i for i, l in enumerate(lines) if l.rstrip() == start_key.rstrip()), None)
    if st is None: return
    en = next((j for j in range(st+1, len(lines)) if lines[j].startswith(next_key)), None)
    if en is not None: del lines[st:en]

del_block(lines, "customFn:", "thrTraceSrc:")
del_block(lines, "switchWarning:", "rssiSource:")

with open(MODEL, "w") as f:
    f.writelines(lines)

# ---------------- RADIO ----------------
with open(RADIO) as f:
    rl = f.readlines()

def set_kv(rl, key, val):
    for i, l in enumerate(rl):
        if l.startswith(key + ":") and not l.strip().endswith(":"):
            rl[i] = f"{key}: {val}\n"; return
for k in ("manuallyEdited", "dontPlayHello"):
    set_kv(rl, k, 1)

# add boot-sound global function if not already present
if not any(l.strip() == 'def: "boot,1,1x"' for l in rl):
    block = ('customFn: \n'
             '   0:\n      swtch: "ON"\n      func: PLAY_TRACK\n      def: "boot,1,1x"\n')
    idx = next((i for i, l in enumerate(rl) if l.startswith("serialPort:")), None)
    if idx is not None:
        rl.insert(idx, block)
    else:
        rl.append(block)

with open(RADIO, "w") as f:
    f.writelines(rl)

# ---------------- SOUNDS ----------------
if BOOTWAV and os.path.exists(BOOTWAV):
    os.makedirs(SOUNDS, exist_ok=True)
    shutil.copy(BOOTWAV, f"{SOUNDS}/boot.wav")

print(f"Applied fleet setup to {SD}")
