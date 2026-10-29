# Python Refresher Practice With Notes

A small Tkinter calculator for practicing Python functions, state, callbacks, and GUI events. The comments explain the Python and Tkinter terms used in the project.

See the [architecture diagrams](docs/architecture.md) for the component and event-flow views.

## Versioning

The current version is recorded in `VERSION`. Update it in every commit so each commit has its own version: increment the patch number for fixes and documentation, the minor number for backward-compatible features, and the major number for incompatible changes. Published Git tags and releases use the same number with a `v` prefix.

## Run

Python 3.10 or newer is required. From this folder, run:

```powershell
python calculator.py
```

The interface supports mouse clicks and keyboard input. Use `Escape` to clear, `Backspace` to delete a digit, and `Enter` to calculate.

See the [GUI cheat sheet](scripts/GUI-CHEATSHEET.md) for all key and button actions.

## Error handling

Invalid numeric text, unsupported operations, division by zero, and results too large for a finite `float` display show `Error`. The calculator clears its pending operation so you can start again by entering a digit or pressing `C`.

Unexpected Python exceptions, including Tk callback exceptions, are appended with a timestamp and traceback to `calculator-crash.log` beside the script. Expected calculator errors are handled on the display and are not logged as crashes. This text log can contain local file paths and exception details, so review it before sharing.

## Memory management

Python manages ordinary object memory through reference counting and cyclic garbage collection. Closing the root Tk window destroys its child widgets; avoid keeping extra references to widgets or callbacks after the window closes, because reachable objects cannot be collected. The crash-log file is opened with a context manager so it closes even if writing fails.

## Headless stress tests

Run without starting Tk or opening a display:

```powershell
python tests/run_headless.py
```

The unit suite checks normal results and failures, then stresses each arithmetic operator at least 10,000 times. The runner also benchmarks each operator 10,000 times by default and prints elapsed time and operations per second. It writes per-operator measurements to `test-results/python-benchmark.csv`; increase the workload with `--iterations 100000`. Results are ignored by Git because timings depend on the machine and current system load.

## Disaster recovery

Restore the latest known-good release into a new, empty folder (PowerShell):

```powershell
.\scripts\recover.ps1 -Version v1.2.2 -Destination ..\python-calculator-recovered
```

The script refuses to overwrite an existing destination. The source has no user data to restore; after recovery, run `python calculator.py` in the new folder.

## Companion C build scan

The companion C project's Windows build has this [VirusTotal report](https://www.virustotal.com/gui/file/c2d090beaf424d32058f8362d444213d66d156cf99a4b64da8e623204fa624ce) for SHA-256 `C2D090BEAF424D32058F8362D444213D66D156CF99A4B64DA8E623204FA624CE`. On 2026-10-29, 2 of 71 engines flagged it: Bkav Pro (`W32.Malware.139374E5`) and Webroot (`Win.Malware.Gen`). The other 69 reported undetected. This is not a clean verdict; generic detections can be false positives, but that has not been independently confirmed. Review the live report and use your own security judgment. VirusTotal submissions are shared with its security community.

## Topics practiced

- Functions, parameters, return values, and exceptions
- Type annotations and floating-point number formatting
- Tkinter windows, widgets, variables, and grid layout
- Event bindings, callbacks, closures, and shared state