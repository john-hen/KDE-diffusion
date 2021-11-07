"""Tests the `meta` module."""

from kde_diffusion import meta
import re


def test_meta():
    fields = ['title', 'synopsis', 'version', 'date', 'author', 'copyright',
              'license']
    for field in fields:
        assert hasattr(meta, field)
        assert isinstance(getattr(meta, field), str)
    assert meta.title == 'KDE-diffusion'
    assert meta.synopsis
    assert re.match(r'\d+\.\d+\.\d+', meta.version)
    assert re.match(r'\d\d\d\d–\d\d–\d\d', meta.date)
    assert meta.author
    assert meta.copyright
    assert meta.license
