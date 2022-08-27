Tools automating tasks during local development


Steps to take when releasing a new version:
* Bump version number in `mph/meta.py`.
* Add dedicated commit for the version bump.
* Tag commit with version number, e.g. `git tag v1.0.4`.
* Run code linter: `flake8`.
* Run code coverage: `python tools/coverage.py`.
* Test docs build: `python tools/docs.py`.
* Test wheel build: `python tools/wheel.py`.
* Push to GitHub: `git push && git push --tags`.
* Check documentation build on Read-the-Docs.
* Create new release on GitHub and add release notes.
* Publish to PyPI: `python tools/publish.py`.
