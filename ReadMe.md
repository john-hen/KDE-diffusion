﻿# KDE-diffusion
*Kernel density estimation via diffusion in 1d and 2d*

Provides the fast, adaptive kernel density estimator based on linear
diffusion processes for one-dimensional and two-dimensional input data
as outlined in the [2010 paper by Botev et al.][paper] The reference
implementation for [1d] and [2d], in Matlab, was provided by the paper's
first author, Zdravko Botev. This is a re-implementation in Python,
with added test coverage.

Find the full [documentation on Read-the-Docs][docs].

[paper]: https://dx.doi.org/10.1214/10-AOS799
[1d]:    https://mathworks.com/matlabcentral/fileexchange/14034
[2d]:    https://mathworks.com/matlabcentral/fileexchange/17204
[docs]:  https://kde-diffusion.readthedocs.io

[![release](
    https://img.shields.io/pypi/v/kde-diffusion.svg?label=release)](
    https://pypi.python.org/pypi/kde-diffusion)
[![downloads](
    https://pepy.tech/badge/kde-diffusion)](
    https://pepy.tech/project/kde-diffusion)
[![citation](
    https://zenodo.org/badge/263433787.svg)](
    https://zenodo.org/badge/latestdoi/263433787)
![coverage](tests/coverage.svg?raw=true)
[![documentation](
    https://readthedocs.org/projects/kde-diffusion/badge/?version=latest)](
    https://kde-diffusion.readthedocs.io/en/latest)
