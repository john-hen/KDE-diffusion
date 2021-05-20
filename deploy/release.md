Steps to take when releasing a new version:
* Bump version number and enter current date in `__init__.py`.
* Add a dedicated commit for the version bump.
* Tag the commit with the version number, for example: `git tag -a v1.0.3`.
* Enter the release notes as an annotation.
* Push the commit (but not the tag): `git push origin main`.
* Check that documentation built successfully on Read-the-Docs.
* Publish on PyPI by running `deploy/publish.py`.
* Check that meta information is correct on PyPI.
* Then push the tag: `git push --tags`.
* Create a new release on GitHub and add the release notes.
