# Python Calculator Architecture

This diagram shows the main runtime components and how input becomes a displayed result. It is an architecture/UML-style view; the code uses functions and Tkinter objects rather than a custom class hierarchy.

```mermaid
flowchart LR
    User[User]
    Keys[Keyboard input]
    Mouse[Mouse click]
    Tk["Tkinter event loop<br/>root.mainloop()"]
    KeyHandler["handle_key(event)"]
    Press["press(label)<br/>event handler"]
    State["Calculator state<br/>stored_value<br/>pending_operator<br/>start_new_number"]
    DisplayVar["StringVar<br/>display_var"]
    Entry["Entry widget<br/>display"]
    Calculate["calculate(left, operator, right)"]
    Format["format_number(value)"]
    Error["show_error()<br/>reset pending state"]
    CrashHook["log_uncaught_exception()"]
    CrashLog[("calculator-crash.log")]

    User --> Keys
    User --> Mouse
    Keys --> Tk
    Mouse --> Tk
    Tk -->|"bound key event"| KeyHandler
    KeyHandler -->|"translate key to label"| Press
    Tk -->|"button command callback"| Press
    Press <--> State
    Press -->|"parse operands and request operation"| Calculate
    Calculate -->|"numeric result"| Format
    Format --> DisplayVar
    Press -->|"set display text"| DisplayVar
    DisplayVar --> Entry
    Calculate -.->|"expected math/input failure"| Error
    Error --> DisplayVar
    Tk -.->|"unexpected callback exception"| CrashHook
    CrashHook --> CrashLog
```

## Interaction sequence

```mermaid
sequenceDiagram
    actor User
    participant Tk as Tkinter event loop
    participant Handler as press(label)
    participant State as Calculator state
    participant Math as calculate(...)
    participant Display as StringVar / Entry

    User->>Tk: Click a button or press a bound key
    Tk->>Handler: Invoke callback with button label
    Handler->>State: Read or update saved operand and operator
    alt digit or decimal point
        Handler->>Display: Update current input text
    else operator selected
        Handler->>Math: Calculate previous pair if one is pending
        Math-->>Handler: Return numeric result or raise an error
        Handler->>State: Save current operand and selected operator
    else equals selected
        Handler->>Math: Calculate saved left and displayed right operand
        Math-->>Handler: Return result
        Handler->>Display: Format and show result
    end
    Display-->>User: Tkinter refreshes the visible display
```

The `calculate` function is independent of Tkinter, allowing headless tests to exercise arithmetic without creating a GUI. Expected calculation failures are caught by the event handler and shown as `Error`; unexpected callback failures are written to the crash log.
