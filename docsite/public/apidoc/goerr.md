<!-- markdownlint-disable -->

# <kbd>module</kbd> `goerr`




**Global Variables**
---------------
- **messages**


---

## <kbd>class</kbd> `Err`
Errors manager 

### <kbd>method</kbd> `__init__`

```python
__init__(
    function: str = None,
    date: datetime = datetime.datetime(2022, 9, 8, 11, 31, 40, 139535),
    msg: str = None,
    errtype: str = None,
    errclass: str = None,
    line: int = None,
    file: str = None,
    code: str = None,
    tb: str = None,
    ex: Exception = None,
    caller: str = None,
    caller_msg: str = None
)
```

Datastructure of an error 




---

### <kbd>method</kbd> `debug`

```python
debug(*args) → Err
```

Creates a debug message 

---

### <kbd>method</kbd> `err`

```python
err(*args)
```

Creates an error 

---

### <kbd>method</kbd> `info`

```python
info(*args) → Err
```

Creates an info message 

---

### <kbd>method</kbd> `panic`

```python
panic(*args)
```

Creates a fatal error and exit 

---

### <kbd>method</kbd> `to_dict`

```python
to_dict()
```

Returns a dictionnary with the error elements 

---

### <kbd>method</kbd> `warning`

```python
warning(*args) → Err
```

Creates a warning message 


---

## <kbd>class</kbd> `Trace`
Tracess manager 

### <kbd>method</kbd> `__init__`

```python
__init__(
    function: str = None,
    date: datetime = datetime.datetime(2022, 9, 8, 11, 31, 40, 139535),
    msg: str = None,
    errtype: str = None,
    errclass: str = None,
    line: int = None,
    file: str = None,
    code: str = None,
    tb: str = None,
    ex: Exception = None,
    caller: str = None,
    caller_msg: str = None
)
```

Datastructure of an error 




---

### <kbd>method</kbd> `debug`

```python
debug(*args) → Err
```

Creates a debug message 

---

### <kbd>method</kbd> `err`

```python
err(*args)
```

Creates an error 

---

### <kbd>method</kbd> `info`

```python
info(*args) → Err
```

Creates an info message 

---

### <kbd>method</kbd> `panic`

```python
panic(*args)
```

Creates a fatal error and exit 

---

### <kbd>method</kbd> `to_dict`

```python
to_dict()
```

Returns a dictionnary with the error elements 

---

### <kbd>method</kbd> `trace`

```python
trace()
```

Print the errors trace if there are some errors 

---

### <kbd>method</kbd> `via`

```python
via(*args)
```

Creates an empty error to record in the stack trace 

---

### <kbd>method</kbd> `warning`

```python
warning(*args) → Err
```

Creates a warning message 


---

## <kbd>class</kbd> `Log`
Errors manager with logging 

### <kbd>method</kbd> `__init__`

```python
__init__(log_path=None)
```

Init Err with logger 




---

### <kbd>method</kbd> `debug`

```python
debug(*args) → Err
```

Creates a debug message 

---

### <kbd>method</kbd> `err`

```python
err(*args)
```

Creates an error 

---

### <kbd>method</kbd> `info`

```python
info(*args) → Err
```

Creates an info message 

---

### <kbd>method</kbd> `panic`

```python
panic(*args)
```

Creates a fatal error and exit 

---

### <kbd>method</kbd> `to_dict`

```python
to_dict()
```

Returns a dictionnary with the error elements 

---

### <kbd>method</kbd> `warning`

```python
warning(*args) → Err
```

Creates a warning message 


