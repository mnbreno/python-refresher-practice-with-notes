# Python Refresher Practice With Notes

A small Tkinter calculator for practicing Python functions, state, callbacks, and GUI events. The comments explain the Python and Tkinter terms used in the project.

## Versioning

The current version is recorded in `VERSION`. Update it in every commit so each commit has its own version: increment the patch number for fixes and documentation, the minor number for backward-compatible features, and the major number for incompatible changes. Published Git tags and releases use the same number with a `v` prefix.

## Run

Python 3.10 or newer is required. From this folder, run:

```powershell
python calculator.py
```

The interface supports mouse clicks and keyboard input. Use `Escape` to clear, `Backspace` to delete a digit, and `Enter` to calculate.

## Error handling

Invalid numeric text, unsupported operations, division by zero, and results too large for a finite `float` display show `Error`. The calculator clears its pending operation so you can start again by entering a digit or pressing `C`.

Unexpected Python exceptions, including Tk callback exceptions, are appended with a timestamp and traceback to `calculator-crash.log` beside the script. Expected calculator errors are handled on the display and are not logged as crashes. This text log can contain local file paths and exception details, so review it before sharing.

## Memory management

Python manages ordinary object memory through reference counting and cyclic garbage collection. Closing the root Tk window destroys its child widgets; avoid keeping extra references to widgets or callbacks after the window closes, because reachable objects cannot be collected. The crash-log file is opened with a context manager so it closes even if writing fails.

## Topics practiced

- Functions, parameters, return values, and exceptions
- Type annotations and floating-point number formatting
- Tkinter windows, widgets, variables, and grid layout
- Event bindings, callbacks, closures, and shared state