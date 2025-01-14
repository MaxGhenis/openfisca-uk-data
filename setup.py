from setuptools import setup, find_packages

setup(
    name="openfisca-uk-data",
    version="0.1.5",
    description=(
        "A Python package to manage OpenFisca-UK-compatible microdata"
    ),
    url="http://github.com/ubicenter/openfisca-uk-data",
    author="Nikhil Woodruff",
    author_email="nikhil.woodruff@outlook.com",
    packages=find_packages(exclude="microdata"),
    install_requires=[
        "pandas",
        "pathlib",
        "tqdm",
        "tables",
        "h5py",
        "google-cloud-storage",
        "jupyter-book>=0.11.1",
        "sphinxcontrib-bibtex>=1.0.0",
    ],
    entry_points={
        "console_scripts": ["openfisca-uk-data=openfisca_uk_data.cli:main"],
    },
)
