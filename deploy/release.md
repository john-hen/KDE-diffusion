Steps to take when releasing a new version:
* Bump version number and enter current date in `__init__.py`.
* Add dedicated commit for the version bump.
* Tag commit with version number, e.g. `git tag v1.0.3`.
* Push the commit: `git push origin main`.
* Check documentation build on Read-the-Docs.
* Publish on PyPI by running `deploy/publish.py`.
* Check that meta information is correct on PyPI.
* Push the tag: `git push --tags`.
* Create new release on GitHub and add release notes.
