# Architecture

Everything lives in `macro/LiveSectionAnalyzer.FCMacro`.

## Classes

- **`LiveSectionAnalyzer(QDockWidget)`** – the panel and the update logic. Creates temporary document features (background, section, hatch), wires the UI and owns the gizmo.
- **`PlaneGizmo`** – Coin3D scene nodes (plane outline + arrow) with hit-testing in screen space and a drag computed from the closest point between the mouse ray and the plane-normal axis. Rendered under `SoFCUnifiedSelection` (on some builds nodes appended to the returned scene graph are not drawn) with a `SoAnnotation` root so it shows on top of transparent geometry.
- **`_GizmoEventFilter`** – Qt event filter on the 3D view viewport. Mouse events over the gizmo are consumed, so dragging does not rotate the camera or change selection.

## Objects

The panel lists every visible solid of the document as a `_Target` (object + shape in global coordinates, resolved with `Part.getShape` so parent/link placements are applied). Checked targets get a background copy, a slice, a fill, outline and hatch. The GPU clip plane sits at the root of the 3D view, so it clips everything; the gizmo is inserted *before* it and the in-plane overlays are nudged by `OVERLAY_OFFSET_REL` so they are not cut.

## Update pipeline

1. A 60 ms throttle timer (not restarted on every event) calls `update_section()`.
2. **Background**: GPU mode sets a `SoClipPlane` (`set_clip`); otherwise a boolean cut (`compute_cut_solid`).
3. **Section**: `get_slice()` uses `Shape.slice` (cached, `SLICE_CACHE_SIZE`), `make_faces()` builds faces (`Part::FaceMakerBullseye`).
4. **Hatch**: `build_hatch()` creates one boolean over all hatch lines, limited by `MAX_HATCH_LINES`.
5. While dragging, a quick mode skips hatch and boolean work; the full result is built on release.
6. Features are marked with `purgeTouched()` instead of a full recompute; view properties are written only when changed.

## Mirror

Mirror flips which side of the plane is kept (`flip` in `set_clip` / `compute_cut_solid`). The shape is never reflected.

## Freeze

`freeze_section()` forces a final update and copies background (always a real boolean cut), section and hatch into a `Frozen_Section_*` group.

## Tunables

`CLIP_KEEP_NEGATIVE`, `MAX_HATCH_LINES`, `SLICE_CACHE_SIZE` at the top of the file.
