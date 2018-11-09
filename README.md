# extra-context

Sometimes, when you get warnings and exeptions, backtraces are just not enough.
For example, you have a loop with 10.000 iterations. In the 1000th iteration there is an 
exception in a function you called. So you would like to have more context for the error message.

There are 2 options
* give more context at the site the exception occured
  * Only possible if you control the exception/warning generation
  * Sometimes, there is not enough context to begin with (i.e. you are calling some common utility function)
  
* Provide additional context as the exception/warning is passed up the call stack
  * Can be "opt-in" in user-code, no changes in libraries required.
  * Also works for warnings (which normally don't provide backtrace information)

## Examples

The main example that inspired writing this library:
```python
to_process = { "file1": {...}, "file2": {...}, ...}

for k, v in to_process.items():
    cleaned = clean_data(v)
    write_output(k, cleaned)
```

If there is an exception or warning somewhere in `clean_data(v)`, the "context" i.e. from which
file the data came is lost. The backtrace could look something like:
```
  File "clean.py", line 35, in clean_data
ZeroDivisionError: division by zero
```

Now, with this library you can give extra context to your error messages

```python
from extra_context import provide_extra_context

to_process = { "file1": {...}, "file2": {...}, ...}

for k, v in to_process.items():
    with provide_extra_context(filename=k):
        cleaned = clean_data(v)
        write_output(k, cleaned)
```

This would report the same error as:
```
  File "clean.py", line 35, in clean_data
ZeroDivisionError: division by zero
  |- In context: filename='file4'
```

### Decorator
There is also a decorator that reports the function arguments in case of an error

```python
import warnings
from extra_context import provide_call_context

@provide_call_context
def w(x):
    warnings.warn("Oops")

w(42)
```

This reports:
```
UserWarning: Oops
  |- In context: w(42)
  warnings.warn("Oops")
``` 


## License

Copyright 2018 Moritz Wanzenböck

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

