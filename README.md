# idom-plotly

Plotly figures as a custom component for IDOM

# Installation

Use `pip` to install this package:

```bash
pip install idom-plotly
```

For a developer installation from source be sure to install [NPM](https://www.npmjs.com/) before running:

```bash
git clone https://github.com/idom-team/idom-plotly
cd idom-plotly
pip install -e . -r requirements.txt
```

# Releasing This Package

To release a new version of idom-plotly on PyPI:

1. Install [`twine`](https://twine.readthedocs.io/en/latest/) with `pip install twine`
2. Update the `version = "x.y.z"` variable in `idom-plotly/__init__.py`
3. `git` add the changes to `__init__.py` and create a `git tag -a x.y.z -m 'comment'`
4. Build the Python package with `python setup.py sdist bdist_wheel`
5. Check the build artifacts `twine check --strict dist/*`
6. Upload the build artifacts to [PyPI](https://pypi.org/) `twine upload dist/*`

To release a new version of `idom-plotly-react` on [NPM](https://www.npmjs.com/):

1. Update `js/package.json` with new npm package version
2. Clean out prior builds `git clean -fdx`
3. Install and publish `npm install && npm publish`
