# Roadmap

## v0.5 (experimental, branch `v0.5-experimental`)

Goal: faster sections on large assemblies. Ordered by expected gain / effort:

0. **Timing output** (`DEBUG_TIMING`) – measure slice / faces / hatch / background per update before optimizing.
1. **Skip objects the plane does not touch** – bounding-box test before slicing.
2. **Hatch without booleans** – discretize the section outline, compute the hatch lines with scanline math (numpy) and draw them as Coin line nodes; convert to real geometry only for *Freeze*. Removes the `MAX_HATCH_LINES` pressure.
3. **Adaptive update delay** – delay the next update by the duration of the last one.
4. **Incremental updates** – process objects one by one with a `QTimer` so the UI stays responsive on big assemblies.
5. **GPU section fill (research)** – stencil-buffer capping with a hatch texture, as done in other FreeCAD forks. Needs raw OpenGL calls through Coin and may depend on the FreeCAD build.

## Ideas after that

- Arbitrary plane direction (angles / "align to view").
- Several planes at once (X, Y, Z) for corner sections.
- Per-object "do not clip" option.
