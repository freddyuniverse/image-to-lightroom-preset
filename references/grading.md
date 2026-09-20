# Grading decisions

## Portable choices
Use the Camera Raw namespace `http://ns.adobe.com/camera-raw-settings/1.0/`. Emit a Normal preset, not a camera profile. Do not require Adobe Color or a camera-specific DCP, as these can restrict JPEG use. Set supports-color, monochrome, normal/high dynamic range, and scene/output referred flags without claiming all versions were tested. Modern Lightroom/ACR is the intended importer.

Use ProcessVersion 11.0 for the established 2012 tone controls plus Texture. Use `Contrast2012`, `Highlights2012`, `Shadows2012`, `Whites2012`, `Blacks2012`, `Clarity2012`; do not substitute legacy controls. Use `ToneCurvePV2012` and Red/Green/Blue suffixes for point curves with RDF sequences of `x, y` pairs. Custom point curves should have increasing x, nondecreasing y, and x endpoints 0/255. A low endpoint raises matte blacks; a gentle toe keeps depth without crushing skin. Avoid strong contrast in both sliders and curves.

HSL uses `HueAdjustment`, `SaturationAdjustment`, `LuminanceAdjustment` followed by Red, Orange, Yellow, Green, Aqua, Blue, Purple, or Magenta. Preserve orange/red skin by using smaller shifts than foliage. Selective color cannot reproduce spatial lighting or background replacement.

Split-toning fields provide a conservative interoperable two-zone tint: `SplitToningShadowHue`, `SplitToningShadowSaturation`, `SplitToningHighlightHue`, `SplitToningHighlightSaturation`, `SplitToningBalance`. Low saturation helps protect neutral clothing. For more complex modern color-grading fields, verify their current serialization against an Adobe-exported example before extending the exporter.

Grain in a small JPEG can be compression noise; add it only when visually justified. Do not derive sharpening radius or noise reduction from a resized reference. Default to no forced vignette because actual set lighting can produce the falloff.

## Requested white balance
Use `Temperature` (2000–50000 K) and `Tint` (-150–150) for an explicit RAW white-balance setting. Use `IncrementalTemperature` and `IncrementalTint` (-100–100) for the non-RAW Temp/Tint sliders, such as JPEG references. The exporter sets `WhiteBalance="Custom"` automatically and rejects mixed WB families. Incremental is Adobe's field name, not a guarantee of adding that amount to every existing RAW white balance. State the intended file type; do not promise a universal Kelvin offset. For a preset intended to span RAW and JPEG, preserve WB by default and use subtle color grading for creative warmth, or offer separate WB variants when requested.

## Recipe example
```json
{"name":"Soft Editorial","group":"Reference Looks","description":"Inferred from supplied reference; exposure and WB preserved.","settings":{"Contrast2012":8,"Highlights2012":-15,"SaturationAdjustmentOrange":-4},"curves":{"ToneCurvePV2012":[[0,3],[48,42],[128,130],[208,214],[255,252]]}}
```

## Sources and import
- Adobe Camera Raw namespace: https://developer.adobe.com/xmp/docs/xmp-namespaces/crs/
- Adobe sample serialization: https://github.com/AdobeDocs/cis-photoshop-api-docs/blob/main/sample-code/lr-sample-app/crs.xml
- Adobe import help: https://helpx.adobe.com/lightroom/desktop/kb/faq-install-presets-profiles.html
- Lightroom Classic: https://helpx.adobe.com/lightroom-classic/desktop/process-and-develop-photos/apply-presets.html

Lightroom desktop: File > Import Profiles & Presets. Lightroom Classic: Develop > Presets > + > Import Presets. Choose the XMP and locate its named group. Adjust exposure and white balance for the receiving photo separately. Check current Adobe help if the interface differs.
