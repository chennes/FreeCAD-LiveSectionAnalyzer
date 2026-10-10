# Changelog

## 0.4.0
- Options now open in FreeCAD's Tasks panel with a standard Close button (falls back to a window if another task dialog is open; `PANEL_MODE` at the top of the macro).
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
