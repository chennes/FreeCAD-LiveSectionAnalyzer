# Contributing

Issues and pull requests are welcome.

- Report the FreeCAD version, OS and a short description (or a sample part) with every bug.
- Keep the macro a single self-contained `.FCMacro` file with no extra dependencies beyond FreeCAD, PySide and pivy.
- Test with a simple part and a complex one; check dragging the gizmo, Mirror Background on/off, and Freeze Section.
- Run `python -m py_compile macro/LiveSectionAnalyzer.FCMacro` and `python3 tests/test_mesh_core.py` before submitting.
- Update `CHANGELOG.md` for user-visible changes.

By contributing you agree your work is released under the MIT license.
