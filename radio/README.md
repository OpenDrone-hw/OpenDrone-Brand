# OpenDrone EdgeTX fleet assets

OpenDrone-branded boot audio, radio images and the installer used to apply the
standard test-fleet model layout to a mounted EdgeTX SD card.

```sh
python3 apply_radio_setup.py "/Volumes/RADIO" boot.wav
```

The installer backs up `MODELS/model00.yml` and `RADIO/radio.yml` before it
changes them. It deliberately preserves each radio's board and calibration
data; the `.bin` files are retained reference images and must not be flashed
blindly onto a different model or hardware revision.

This directory owns OpenDrone-specific media and configuration only. Generic
bench procedures and resulting evidence belong in `incutec-org/incutec-testing`.
