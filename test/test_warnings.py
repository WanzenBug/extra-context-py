import warnings

import pytest

import extra_context


def create_exception(msg):
    raise Exception(msg)


def create_exception_empty():
    raise Exception()


def create_warnings():
    warnings.warn("Foo")


@extra_context.provide_call_context
def decorated_exception(msg, _extra):
    raise Exception(msg)


@extra_context.provide_call_context
def decorated_warning(msg, _extra):
    warnings.warn(msg)


def test_exception_with_msg():
    with pytest.raises(Exception, match=r".*|- In context: x = 1.*"):
        with extra_context.provide_extra_context("x = 1"):
            create_exception("foo")


def test_exception_without_msg():
    with pytest.raises(Exception, match=r".*In context: x = 1.*"):
        with extra_context.provide_extra_context("x = 1"):
            create_exception_empty()


def test_warnings():
    with pytest.warns(UserWarning, match=r".*|- In context: x = 1.*"):
        with extra_context.provide_extra_context("x = 1"):
            create_warnings()


def test_decorator_exception():
    with pytest.raises(Exception, match=r".*|- In context: decorated_exception('foo', 2).*"):
        decorated_exception("foo", 2)


def test_decorator_warning():
    with pytest.warns(UserWarning, match=r".*|- In context: decorated_warning('bar', \_extra=\[\]).'"):
        decorated_warning("bar", _extra=[])
