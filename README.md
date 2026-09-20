# Image to Lightroom Preset

![Image to Lightroom Preset preview](assets/preset-preview.png)

A skill by @FreddyUnivers3 for turning a reference photo's look into an editable Lightroom / Adobe Camera Raw XMP preset.

Upload a photo to an image-capable agent, ask for a preset, and get a reusable starting point for its color and contrast. Fork it, change the workflow, and make it your own.

## What it does

- Guides visual analysis of tone curves, color, skin, highlights, and shadows.
- Separates likely grading choices from lighting, makeup, and set design.
- Exports XMP with validated control ranges, curves, namespaces, and preset metadata.
- Supports selective color, split toning, grain, and optional white balance.

This is an agent skill plus a deterministic exporter. The Python script accepts a **JSON recipe**, not an image. An image-capable agent analyzes your reference and writes that recipe. A single finished photo cannot reveal the exact original editing settings.

## Use the skill

Download or clone this repository. Install the folder with your agent's supported skill installer, or ask it to read `SKILL.md` and follow its workflow. Your agent needs image understanding, Python 3.9+, and permission to write files. The exporter uses only Python's standard library.

Example prompt:

> Use image-to-lightroom-preset on this reference. Create an exportable XMP inspired by its colors and contrast, preserve natural skin, and explain any limitations.

## Run the example

```bash
python3 scripts/export_xmp.py examples/emerald-afterhours.json Emerald-Afterhours.xmp
python3 -m unittest discover -s tests -v
```

Import the XMP through **File > Import Profiles & Presets** in Lightroom desktop, or **Develop > Presets > + > Import Presets** in Lightroom Classic. Find it under **Freddy Universe - Reference Looks**.

### Emerald Afterhours

Deep emerald shadows, rich blacks, warm skin, and vivid red accents. The included revised example uses contrast **+24** and non-RAW temperature **+10**. Its white balance is intended for JPEG and other non-RAW photos. For RAW photos, remove the `IncrementalTemperature` / `IncrementalTint` fields and set WB for the shot, or use explicit `Temperature` / `Tint` values in a separate recipe. Do not mix the two WB families.

Exposure and camera profiles remain untouched. Presets set their included values; they are not guaranteed additive adjustments to existing edits. Test on a separate unedited photo rather than applying the look twice to an already graded reference.

## Validation and limitations

The exporter validates XML structure and settings. Lightroom import and rendering have **not** been tested here. Camera profiles, lighting, file type, and existing edits affect the result. The README preview is supplied by the repository owner; it is not an automated rendering test.

## Contribute

Fork the repo and open a pull request. For new controls, include an Adobe serialization reference and a focused test. For visual feedback, include the file type, Lightroom version, and before/after examples you have permission to share. Distinguish illustrative previews from actual Adobe renders.

## License

MIT. See [LICENSE](LICENSE).
