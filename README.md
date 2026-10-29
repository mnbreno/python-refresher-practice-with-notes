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
.\scripts\recover.ps1 -Version v1.2.6 -Destination ..\python-calculator-recovered
```

The script refuses to overwrite an existing destination. The source has no user data to restore; after recovery, run `python calculator.py` in the new folder.

## Security status

This repository contains Python source, not a packaged executable, and that source has not been scanned as a binary. The companion C v1.2.8 release includes a new Windows executable whose [VirusTotal report](https://www.virustotal.com/gui/file/b9aeec49fec212a73dcb9b3aced5a67a486c1cf3a1142924f5898b7d7540f030) showed **0 of 69 detections** in the analysis dated 2026-10-29 at 17:20:38 EDT. Bkav Pro and Webroot both reported Undetected. This result applies only to that exact C executable. See the [C project executable and scan notes](https://github.com/mnbreno/c-refresher-practice-with-notes#executable-and-virustotal-report) for its checksum and build details.

## Topics practiced

- Functions, parameters, return values, and exceptions
- Type annotations and floating-point number formatting
- Tkinter windows, widgets, variables, and grid layout
- Event bindings, callbacks, closures, and shared state
