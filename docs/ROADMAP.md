# Roadmap

## v0.5 (experimental, branch `v0.5-experimental`)

Goal: faster sections on large assemblies. Ordered by expected gain / effort:

0. ✅ **Timing output** (`DEBUG_TIMING`) – measure slice / faces / hatch / background per update before optimizing.
1. ✅ **Skip objects the plane does not touch** – bounding-box test before slicing.
2. **Hatch without booleans** – discretize the section outline, compute the hatch lines with scanline math (numpy) and draw them as Coin line nodes; convert to real geometry only for *Freeze*. Removes the `MAX_HATCH_LINES` pressure.
3. ✅ **Adaptive update delay** – delay the next update by the duration of the last one.
4. **Incremental updates** – process objects one by one with a `QTimer` so the UI stays responsive on big assemblies.
5. **GPU section fill (research)** – stencil-buffer capping with a hatch texture, as done in other FreeCAD forks. Needs raw OpenGL calls through Coin and may depend on the FreeCAD build.

Measured on a 60-solid demo (10×6 drilled boxes), YZ plane, no cache: slice time per update
~240 ms without the bounding-box test, ~85 ms with it (54 of 60 objects skipped). Slicing is
the dominant cost, so the next step is item 3/4 (adaptive delay, incremental updates).

**Fast drag preview (new):** while dragging, objects whose exact slice took more than
`FAST_PREVIEW_MS` (60 ms) are outlined from their tessellation with numpy and drawn as a Coin line
node; the exact section is computed when the drag ends. Test part (80-tooth gear, 12 holes):
exact slice ~830 ms, mesh outline ~0.5 ms (length differs by 0.06 %); a full drag update went from
~520 ms to ~9 ms. The exact slice on release is still a single blocking call (see item 4).

## Status (2026-10-10)

- v0.4.0 is released. v0.5-experimental has timing output, bbox skipping, fast drag preview and
  adaptive delay; tested by the author on a real gear assembly (drag updates ~2 ms, no leftover lines
  after the stale-segment fix `da416e5`). Announced on the FreeCAD forum; waiting for feedback.
- Real-assembly timings (2 solids): exact slice 200-540 ms, up to ~2.5 s where the plane cuts the
  gear teeth; hatch 12-35 ms, fill/edges a few ms. Slicing with OpenCascade is the only real cost.

## Next: mesh-based section pipeline (flag `MESH_SECTION`, idea stage)

Build contour, hatch and fill from the tessellation instead of OpenCascade, keep the old path
for comparison and for *Freeze*:

1. Contour: chain the plane/triangle segments into closed loops (key the cut points by mesh edge id).
2. Hatch: scanline clipping of the hatch lines against the loops (even-odd rule, holes for free),
   drawn as Coin line nodes; per-object angle/spacing so neighbouring parts hatch differently.
3. Fill: Coin polygons from the loops (holes need a small triangulation, e.g. keyhole bridging).
4. Exact geometry only for *Freeze*; mesh tolerance configurable, finer mesh after a drag ends.
Trade-off: curves look polygonal at coarse tolerance.

Also open: incremental exact updates (item 4), hatch/fill during drag.

## Ideas after that

- Arbitrary plane direction (angles / "align to view").
- Several planes at once (X, Y, Z) for corner sections.
- Per-object "do not clip" option.
