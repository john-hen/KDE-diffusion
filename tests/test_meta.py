"""Tests the `meta` module."""

from kde_diffusion import meta
import re


def test_meta():
    assert meta.name == 'KDE-diffusion'
    assert re.match(r'\d+\.\d+\.\d+', meta.version)
    assert meta.summary
