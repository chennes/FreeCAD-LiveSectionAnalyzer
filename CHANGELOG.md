# Changelog

## Unreleased (v0.5-experimental)

- `DEBUG_TIMING`: per-update timings (background / slice / faces / fill / edges / hatch) in the Report view.
- Objects the plane does not touch are skipped by a bounding-box test before slicing (~3x faster on a 60-solid demo).
- Fast drag preview: slow objects are outlined from their tessellation (numpy) while the plane moves; the exact section follows when you let go. `FAST_PREVIEW_MS` sets the threshold. Needs numpy (bundled with FreeCAD); falls back to exact slicing without it.
- Adaptive update delay: the wait before the next update grows with the duration of the last one (60-250 ms).

## 0.4.0 – 2026-10-10
- The macro no longer needs a selection: with nothing selected it clips everything visible (scenes of up to 12 solids are sectioned completely, bigger ones start with nothing checked; `AUTO_SECTION_MAX_OBJECTS`).
- **Multiple objects / assemblies:** an *Objects* list shows every visible solid. The plane clips everything on screen; the checked objects also get a section fill, outline and hatch, tinted with their own colors. Freeze Section copies all checked objects.
- Options now open in FreeCAD's Tasks panel with a standard Close button (falls back to a window if another task dialog is open; `PANEL_MODE` at the top of the macro).
- Fixed: parts inside assemblies, links and App::Part containers jumped to their local position; the section now uses the shape with all placements applied and hides only the selected instance.
- Gizmo: bigger arrow pick area and the plane itself (surface and outline) can be dragged; `GIZMO_PICK_PLANE` turns the plane grab off.
- Panel is scrollable, shows a "more options below" hint, and has collapsible sections; Freeze Section stays visible at the bottom.

## 0.3.0
- Draggable 3D plane gizmo (Qt event filter on the 3D viewport; hover highlight).
- Mirror Background fixed: it now flips the kept half instead of reflecting the solid, so the object no longer moves.
- Gizmo drawn on top of transparent geometry.
- Closing the panel removes the dock widget completely.

## 0.2.0
- Performance rewrite: GPU clipping, slice-based section outline, single boolean hatch (capped), throttled updates, quick mode while dragging, slice cache, fewer recomputes and property writes.

## 0.1.0
- Initial macro: boolean-cut section with fill, edges and hatch.
