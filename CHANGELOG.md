# Changelog

## 0.3.0
- Draggable 3D plane gizmo (Qt event filter on the 3D viewport; hover highlight).
- Mirror Background fixed: it now flips the kept half instead of reflecting the solid, so the object no longer moves.
- Gizmo drawn on top of transparent geometry.
- Closing the panel removes the dock widget completely.

## 0.2.0
- Performance rewrite: GPU clipping, slice-based section outline, single boolean hatch (capped), throttled updates, quick mode while dragging, slice cache, fewer recomputes and property writes.

## 0.1.0
- Initial macro: boolean-cut section with fill, edges and hatch.
