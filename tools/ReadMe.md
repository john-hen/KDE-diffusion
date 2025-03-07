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
- Run code coverage: `python tools/coverage.py`
- Test docs build:   `python tools/docs.py`
- Test wheel build:  `python tools/wheel.py`
- Bump version number in `pyproject.toml`.
- Add dedicated commit for the version bump.
- Tag with version:  `git tag vx.y.z`
- Push to GitHub:    `git push && git push --tags`
- Check documentation build on Read-the-Docs.
- Fast-forward stable branch: `git branch --force stable`
- Create new release on GitHub and add release notes.
- Run `publish_release` GitHub action.
