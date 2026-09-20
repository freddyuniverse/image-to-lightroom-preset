---
name: image-to-lightroom-preset
description: Analyze an uploaded reference photo's visual grade and create an exportable Lightroom or Adobe Camera Raw XMP develop preset. Use for image-to-preset, reference color grading, and reusable photographic looks.
---
# Image to Lightroom Preset

Turn a reference image into a carefully inferred, reusable grade and a downloadable `.xmp` preset. Use visual reasoning to select settings, then the bundled exporter for deterministic XML. This is an agent workflow, not a trained automatic style-transfer model.

## Inspect and interpret
1. View the supplied image. Resolve local attachments first when paths are supplied; if unreadable, use the visible attachment for qualitative analysis and disclose that pixel measurements were unavailable. Never claim to inspect unavailable bytes.
2. Identify tone curve, black floor, highlight roll-off, shadow/midtone/highlight color biases, selective saturation, skin hue and luminance, microcontrast, grain, and edge falloff. Separate scene content, makeup, colored lighting, and background materials from likely editing. A large green backdrop alone does not justify green skin.
3. State the 3–5 defining traits and confidence. A finished JPEG cannot uniquely reveal its original settings. Never promise exact recovery or identical results across cameras and lighting.
4. With one reference, infer a moderate transferable grade. With a separate target, inspect both and account for target exposure/WB before deciding the creative settings. Do not normalize deliberately dark reference images simply because their average brightness is low.

## Build
Read `references/grading.md` for controls and portability decisions. Write a JSON recipe with `name`, `group`, `description`, `settings`, and optional `curves`. Run:

```bash
python3 <skill-dir>/scripts/export_xmp.py recipe.json output.xmp
```

Use only supported controls listed in the exporter; it rejects unknown fields, invalid values, and nonmonotonic curves. Prefer adjusting the exporter deliberately against Adobe documentation to silently dropping needed settings. Leave exposure, temperature/tint, camera profiles, sharpening, lens correction, crop, transforms, and local masks out of a general creative preset unless requested and appropriate. When temperature is requested, choose the RAW Kelvin or non-RAW slider fields described in the reference; do not mix them or promise a universal offset. Omitted settings retain the target photo's values. Name the preset descriptively and put it in a recognizable group. Never embed reference-image paths or personal metadata.

## Validate and deliver
- Run the exporter and parse the output. Confirm unique uppercase 32-character UUID, correct namespaces, preset metadata, RDF-localized name/group, supported ranges, and intended controls.
- Distinguish XML validation from actual Lightroom import/render validation. If Lightroom/Camera Raw is unavailable, explicitly say the result has not been rendered in Lightroom; do not represent another renderer or a generated image as proof of XMP behavior.
- Interpret “use this skill on this image” as extracting a preset from that reference. If asked to apply the resulting XMP to pixels, use an available Adobe renderer. If unavailable, deliver the preset and explain the rendering limitation. Offer an illustrative preview only when useful, labeled as approximate, using the environment's authorized image-editing tools.
- Do not grade an already graded reference again as a fidelity test. Recommend a separate unedited photo for meaningful testing; a same-image application merely stacks the inferred look.
- Save the XMP as a persistent user artifact using the environment's file workflow. Provide its download link and concise import steps. Keep recipe JSON internal unless requested. Mention any intentionally omitted exposure/WB controls.
- Iterate from the user's Lightroom screenshot/export, matching skin, white objects, and shadow detail before chasing background hue. Change only controls supported by evidence.
