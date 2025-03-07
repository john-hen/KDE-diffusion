"""Measures code coverage by test suite."""

from subprocess import run
from pathlib import Path


root = Path(__file__).parent.parent

print('Running test suite.')
run(['pytest', '--cov'], cwd=root)

print('Exporting coverage report.')
run(['coverage', 'html', '--directory=build/coverage'], cwd=root)

print('Rendering coverage badge.')
badge = root/'tests'/'coverage.svg'
run(['coverage-badge', '-f', '-o', str(badge)], cwd=root)
