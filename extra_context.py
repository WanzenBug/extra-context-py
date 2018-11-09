"""
extra_context
=============

Provides:
 * A context manager for providing more context for expetions/warnings
 * A decorator for using function arguments as context

 Example:
    >>> import warnings
    >>> from extra_context import provide_call_context
    >>>
    >>> @provide_call_context
    >>> def w(x):
    >>>    warnings.warn("Oops")
    >>>
    >>> w(42)
    UserWarning: Oops
      |- In context: w(42)
      warnings.warn("Oops")
"""

import contextlib
import warnings
import functools

__all__ = [
    "provide_call_context",
    "provide_extra_context",
]


class WrappedWarning(Warning):
    def __init__(self, warning, msg_ctx):
        self.warning = warning
        self.msg_ctx = msg_ctx

    def __str__(self):
        return (str(self.warning) +
                "\n  |- In context: {}".format(self.msg_ctx))


@contextlib.contextmanager
def provide_extra_context(msg="", *_a, **kwargs):
    old_warn = warnings.showwarning
    if kwargs:
        msg += ", ".join("{k}={v}".format(k=k, v=repr(v)) for k, v in kwargs.items())

    def wrapped_show(message, category, filename, lineno, file=None, line=None):
        new_warn = WrappedWarning(message, msg)
        old_warn(new_warn, category, filename, lineno, file, line)

    warnings.showwarning = wrapped_show

    try:
        yield
    except Exception as ex:
        if ex.args:
            msg = '{}\n  |- In context: {}'.format(ex.args[0], msg)
        else:
            msg = "In context: {}".format(msg)
        ex.args = (msg,) + ex.args[1:]
        raise
    finally:
        warnings.showwarning = old_warn


def provide_call_context(f):
    """Wraps a function to provide more context on warnings

    Any warning generated while running the body of the wrapped function will
    be annotated with the arguments passed to it.

    >>> import warnings
    >>> from extra_context import provide_call_context
    >>>
    >>> @provide_call_context
    >>> def w(x):
    >>>    warnings.warn("Oops")
    >>>
    >>> w(42)
    UserWarning: Oops
      |- In context: w(42)
      warnings.warn("Oops")


    """
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        func_name = f.__name__
        args_fmt = ", ".join(map(repr, args))
        kwargs_fmt = ", ".join(("{}={}".format(k, repr(v)) for k, v in kwargs.items()))
        sep = ", " if args_fmt and kwargs_fmt else ""
        ctx_str = "{func}({args}{sep}{kwargs})".format(func=func_name, args=args_fmt, sep=sep, kwargs=kwargs_fmt)

        with provide_extra_context(ctx_str):
            return f(*args, *kwargs)

    return wrapped
