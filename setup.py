import io, os, re
from glob import glob
from os.path import splitext, basename, join, dirname

from setuptools import Extension
from setuptools import find_packages
from setuptools import setup









def get_version(package:str)->str:
    """Return package version as listed in `__version__` in `__init__.py`."""
    with open(os.path.join(package, '__init__.py')) as f:
        init_py = f.read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)


def read(*names, **kwargs):
    with io.open(
        join(dirname(__file__), *names),
        encoding=kwargs.get('encoding', 'utf8')
    ) as fh:
        return fh.read()

with open("README.md", "r") as fh:
    long_description = fh.read()

__version__ = get_version("./src/rendre")

setup(
    name="rendre",
    version=__version__,
    author="Claudio Perez",
    author_email="claudio_perez@berkeley.edu",
    description="Utilities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/claudioperez/rendre",
    py_modules=[splitext(basename(path))[0] for path in glob("src/*.py")],
    include_package_data=True,
    package_data={"": ['*.html','*.tex']},
    zip_safe=False,
    packages=find_packages('src'),
    package_dir={'': 'src'},
    entry_points={
        'console_scripts': [
            'rendre = rendre.__main__:_main_',
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "coloredlogs",
        # 'aurore @ git+https://github.com/claudioperez/aurore@master',
        "aurore",
        "pyyaml",
        "jinja2"
    ]
)
