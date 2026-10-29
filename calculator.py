import math
from datetime import datetime
from pathlib import Path
import sys
import traceback
from types import TracebackType
import tkinter as tk

# tkinter is a standard-library GUI module. The `as tk` import creates a shorter
# local name, so tk.Button refers to tkinter.Button throughout this file.
#
# A function definition uses def, a Python keyword. In calculate(...), left is a
# parameter; the value 2 in calculate(2, "+", 3) is an argument. An expression
# such as 2 + 3 evaluates to a value, while a statement such as x = 5 binds that
# value to a name.
#
# tkinter classes such as Tk, Button, and Entry are constructors for GUI objects
# called widgets. root = tk.Tk() creates a Tk instance; display = tk.Entry(...)
# creates an Entry instance. A method is a function accessed through an object,
# as in display_var.get(). A keyword argument names its setting, such as text="7";
# root in tk.Button(root, ...) is a positional argument.
# Python strings do not have a fixed 63-character limit; their practical limit
# is available memory. This calculator reads the display text with float(), so
# the number of significant decimal digits is limited by floating-point
# precision, not by a fixed input buffer. float values usually keep about 15-17
# significant decimal digits; formatting below chooses at most 12 for display.
#
# This program uses separate functions instead of a custom class. calculate owns
# arithmetic, format_number owns display formatting, and main builds the GUI.
# Keeping these responsibilities separate makes each part easier to follow and
# lets both mouse and keyboard events use the same press function.
#
# Memory management: Python allocates objects as they are needed and reclaims
# unreachable objects with reference counting and cyclic garbage collection.
# Tk widgets belong to their parent window, so closing the root window destroys
# its child widgets. Avoid keeping extra global references to widgets or callbacks
# after closing the window; long-lived references can keep objects reachable.
# Python manages ordinary objects automatically, but external resources such as
# open files should still be closed with `with` so cleanup happens on every path.
#
# Crash log: log_uncaught_exception records a timestamp and formatted traceback
# for unexpected top-level and Tk callback exceptions. It opens the log in append
# mode with a context manager, so the file handle closes after every write. The
# log is diagnostic text, not a memory dump, and can include local file paths.
#
# Error handling: calculate raises an exception when an operation is invalid or
# produces a non-finite result. The button callback catches these expected math
# and conversion errors, shows "Error", and clears pending state so input can
# continue after the user enters a new digit or presses C.
# Unexpected exceptions are written to calculator-crash.log with their traceback.
# Expected calculator errors are handled on the display and are not crash logs.

CRASH_LOG = Path(__file__).with_name("calculator-crash.log")


def log_uncaught_exception(
    exception_type: type[BaseException],
    exception: BaseException,
    exception_traceback: TracebackType | None,
) -> None:
    """Append an uncaught exception and traceback to the local crash log."""
    crash_record = (
        f"\n[{datetime.now().astimezone().isoformat()}] Uncaught exception\n"
        + "".join(traceback.format_exception(
            exception_type, exception, exception_traceback
        ))
    )
    try:
        # `with` closes the file even if writing the record raises an exception.
        with CRASH_LOG.open("a", encoding="utf-8") as crash_file:
            crash_file.write(crash_record)
    except OSError:
        # If logging itself fails, preserve the normal Python error report.
        sys.__excepthook__(exception_type, exception, exception_traceback)

# Keep arithmetic independent from tkinter so a GUI event handler can call the
# same tested operation logic for every input method.
def calculate(left: float, operator: str, right: float) -> float:
    """Return the result of adding, subtracting, multiplying, or dividing.

    The float annotations document the values expected by this function; Python
    does not enforce annotations at runtime. The GUI converts display text to
    float before calling calculate.
    """
    if not math.isfinite(left) or not math.isfinite(right):
        raise ValueError("Calculator inputs must be finite numbers")

    if operator == "+":
        result = left + right
    elif operator == "-":
        result = left - right
    elif operator == "*":
        result = left * right
    elif operator == "/":
        if right == 0:
            raise ZeroDivisionError("Cannot divide by zero")
        result = left / right
    else:
        raise ValueError(f"Unsupported operator: {operator}")

    if not math.isfinite(result):
        raise OverflowError("The result is too large to display")
    return result


# The Entry widget displays strings, so convert a numeric result to display text
# in one function. The .12g format means at most 12 significant digits, not 12
# digits after the decimal point.
def format_number(value: float) -> str:
    """Remove .0 from whole answers and limit output to 12 significant digits."""
    if not math.isfinite(value):
        raise ValueError("Cannot display a non-finite number")
    return str(int(value)) if value.is_integer() else format(value, ".12g")


def main() -> None:
    # main owns GUI setup. An event is an input or window-system notification;
    # examples here include a button click, key press, or window close request.
    # Tkinter's default callback handler writes tracebacks to stderr. Point it
    # and Python's top-level exception hook at the same crash-log writer.
    sys.excepthook = log_uncaught_exception
    root = tk.Tk()
    root.report_callback_exception = log_uncaught_exception
    root.title("Calculator")
    root.resizable(False, False)

    # StringVar is tkinter's observable string container. Linking it with
    # textvariable makes the Entry show its value; calling set() updates the UI.
    display_var = tk.StringVar(value="0")
    display = tk.Entry(
        root,
        textvariable=display_var,
        justify="right",
        state="readonly",
        font=("Segoe UI", 18),
        width=16,
    )
    display.grid(row=0, column=0, columnspan=4, padx=8, pady=8, sticky="nsew")

    # These variables are the calculator's state between separate GUI events.
    # After an operator click, stored_value keeps the first operand and
    # pending_operator records the operation until the next input arrives.
    stored_value: float | None = None
    pending_operator: str | None = None
    start_new_number = True

    def show_error() -> None:
        """Show a safe error state and discard any unfinished calculation."""
        nonlocal stored_value, pending_operator, start_new_number
        # Clear both the display status and saved operands so a later click
        # cannot accidentally continue a calculation that already failed.
        display_var.set("Error")
        stored_value = None
        pending_operator = None
        start_new_number = True

    def press(label: str) -> None:
        # This is an event handler: each button's command callback calls it with
        # that button's label. nonlocal lets this nested function update the state
        # variables defined in main instead of creating new local variables.
        nonlocal stored_value, pending_operator, start_new_number

        current_text = display_var.get()

        if label == "C":
            stored_value = None
            pending_operator = None
            start_new_number = True
            display_var.set("0")
            return

        if label == "DEL":
            if not start_new_number:
                shortened = current_text[:-1]
                display_var.set(shortened if shortened and shortened != "-" else "0")
            return

        if label.isdigit() or label == ".":
            if label == "." and not start_new_number and "." in current_text:
                return
            if start_new_number or current_text == "Error":
                display_var.set("0." if label == "." else label)
            elif label == ".":
                display_var.set(current_text + ".")
            elif current_text == "0":
                display_var.set(label)
            else:
                display_var.set(current_text + label)
            start_new_number = False
            return

        if label in {"+", "-", "*", "/"}:
            if current_text == "Error":
                return
            try:
                current_value = float(current_text)
                if pending_operator is not None and not start_new_number:
                    current_value = calculate(
                        stored_value, pending_operator, current_value
                    )
                    display_var.set(format_number(current_value))
                stored_value = current_value
                pending_operator = label
                start_new_number = True
            except (ValueError, ZeroDivisionError, OverflowError):
                # GUI callbacks need to catch expected input/math errors so a
                # bad value shows on the display instead of escaping the event loop.
                show_error()
            return

        if label == "=" and pending_operator is not None and stored_value is not None:
            try:
                result = calculate(stored_value, pending_operator, float(current_text))
                display_var.set(format_number(result))
                stored_value = None
                pending_operator = None
                start_new_number = True
            except (ValueError, ZeroDivisionError, OverflowError):
                show_error()

    # Store layout data as (label, row, column) tuples, then create all buttons in
    # one loop. This keeps placement data together and avoids duplicating setup.
    buttons = [
        ("C", 1, 0), ("DEL", 1, 1), ("/", 1, 2), ("*", 1, 3),
        ("7", 2, 0), ("8", 2, 1), ("9", 2, 2), ("-", 2, 3),
        ("4", 3, 0), ("5", 3, 1), ("6", 3, 2), ("+", 3, 3),
        ("1", 4, 0), ("2", 4, 1), ("3", 4, 2), ("=", 4, 3),
        ("0", 5, 0), (".", 5, 1),
    ]
    for label, row, column in buttons:
        button = tk.Button(
            root,
            text=label,
            width=5,
            height=2,
            # command takes a callback, a function tkinter will call later after
            # a click. The default argument captures this iteration's label now;
            # without it, every lambda would look up the loop's final label later.
            command=lambda button_label=label: press(button_label),
        )
        button.grid(row=row, column=column, padx=3, pady=3, sticky="nsew")

    def handle_key(event: tk.Event) -> str | None:
        """Translate a Tk key event into the matching calculator action."""
        # bind_all registers this handler for key events in the application.
        # tkinter supplies an Event object containing fields such as keysym
        # (the key's symbolic name) and char (the text character, when available).
        key = event.keysym
        if key in {"Return", "KP_Enter"}:
            press("=")
        elif key == "BackSpace":
            press("DEL")
        elif key == "Escape":
            press("C")
        elif event.char and event.char in "0123456789.+-*/":
            press(event.char)
        else:
            return None
        # Returning "break" is tkinter's event-propagation signal: stop processing
        # this key event in other bindings after the calculator handles it.
        return "break"

    # A binding maps an event pattern to a callback. <Key> matches key presses;
    # bind_all applies this mapping across the application instead of one widget.
    root.bind_all("<Key>", handle_key)
    # mainloop is tkinter's event loop. It waits for events and dispatches each
    # event to the registered callback; it returns after the window is closed.
    root.mainloop()


# Python sets __name__ to "__main__" when this file is run as a script. The guard
# starts the GUI in that case, but importing this module only defines its functions.
if __name__ == "__main__":
    main()