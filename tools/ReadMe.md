## Developer tools

These are simple helper scripts to run the various development tools, such as
pyTest and Sphinx. See the doc-strings of the individual scripts for details.


### Local development

For local development, it is recommended (but not strictly necessary) to
install [UV]. Then install the project from source by running `uv sync` in the
root folder.

[UV]: https://docs.astral.sh/uv


### Releasing a new version

- Run code linter:   `python tools/lint.py`
- Run test suite:    `python tools/test.py`
- Run code coverage: `python tools/coverage.py`
- Test docs build:   `python tools/docs.py`
- Test wheel build:  `python tools/wheel.py`
- Bump version number in `pyproject.toml`.
- Add dedicated commit for the version bump.
- Push to GitHub: `git push origin main`
- Check "latest" documentation build on Read-the-Docs.
- Run `publish_release` GitHub action.
- Create release tag on GitHub.
- Create new release on GitHub and add release notes.
- Fast-forward stable branch:    `git branch --force stable`
- Update "stable" documentation: `git push origin stable`
