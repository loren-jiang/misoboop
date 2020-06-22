import pytest
from core.utils import remove_backslash_escaped, remove_html_tags, lazify_images, strip_leading_trailing_spaces


@pytest.mark.parametrize("input,expected",
                         [
                             ("hello\nworld", "hello world"),
                             ("\nhello \n world", " hello world"),
                         ])
def test_remove_backslash_escaped(input, expected):
    assert remove_backslash_escaped(input)==expected


@pytest.mark.parametrize("input,expected",
                         [
                             ("<div>hello</div>", "hello"),
                         ])
def test_remove_html_tags(input, expected):
    assert remove_html_tags(input)==expected


@pytest.mark.parametrize("input,expected",
                         [
                             ("  abc   ", "abc"),
                             ("abc      \n", "abc"),
                             ("    abc", "abc")
                         ])
def test_lazify_images(input, expected):
    pass


@pytest.mark.parametrize("input,expected",
                         [
                             ("  abc   ", "abc"),
                             ("abc      \n", "abc"),
                             ("    abc", "abc"),
                             (" a b c ", "a b c")
                         ])
def test_strip_leading_trailing_spaces(input, expected):
    assert strip_leading_trailing_spaces(input) == expected
