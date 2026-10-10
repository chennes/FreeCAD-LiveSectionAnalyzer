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

## Mesh-based section pipeline (checkbox *Section engine*, flag `MESH_SECTION`)

Implemented on this branch; **not yet run inside FreeCAD** (see "Verified" below). Contour, hatch and
fill are built from the tessellation instead of OpenCascade and drawn as Coin nodes. The old path stays
for comparison (untick the checkbox) and is always used by *Freeze*.

1. ✅ Contour: the tessellation is welded (vertices clustered by gaps along x/y/z, per solid), the
   plane/triangle segments are keyed by mesh edge id and chained into closed loops. Open chains whose
   ends meet within 1e-4 of the object's diagonal are joined (cracks).
2. ✅ Hatch: scanline clipping of the lines against the loops (even-odd rule, holes for free), numpy only.
   Lines are anchored at the origin, so the pattern does not swim while the plane moves.
   `MESH_HATCH_STYLES` gives each object its own angle and spacing factor.
3. ✅ Fill: nesting depth of the loops (outer / hole / island), holes joined to the outer loop by keyhole
   bridging, drawn as concave Coin polygons (`SoShapeHints` unknown face type).
4. ✅ Exact geometry only for *Freeze*. `MESH_TOL_REL` (coarse, while dragging) and `MESH_TOL_FINE_REL`
   (after the drag) set the mesh tolerance; hatch and fill are also drawn while dragging
   (`MESH_DRAG_HATCH`).

Trade-off: curves look polygonal at coarse tolerance.

Verified (`python3 tests/test_mesh_core.py`, synthetic meshes, outside FreeCAD): welding, loop chaining
(box, tube, torus, star-shaped gear, plane through vertices, cracks), loop nesting, keyhole bridging
(no self-crossings, area preserved), hatch length = area / spacing at any angle. On a 190 000-triangle
test mesh: weld 46 ms (once per mesh), loops 9 ms, hatch a few ms.

Still to check in FreeCAD: that Coin tessellates the bridged polygons correctly, the pivy field calls,
timings on real assemblies, and how the mesh section compares with the exact one on curved parts.

Also open: incremental exact updates (item 4 above).

## Ideas after that

- Arbitrary plane direction (angles / "align to view").
- Several planes at once (X, Y, Z) for corner sections.
- Per-object "do not clip" option.
