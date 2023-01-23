""" Python generator utilities """
import shutil
from pathlib import Path
from setuptools import setup, find_packages

here = Path(__file__).parent.resolve()

# Remove build and dist folders
shutil.rmtree(Path("build"), ignore_errors=True)
shutil.rmtree(Path("dist"), ignore_errors=True)

# Get the long description from the README file
long_description = (here / 'README.MD').read_text(encoding='utf-8')

with open('requirements.txt',encoding='utf8') as f:
    required = f.read().splitlines()

setup(
    name='bluesmet',
    version='0.1.0.dev1',
    author="SINTEF Ocean",
    description="SFIBlues Metocean library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_dir={"": "src"},
    packages=find_packages(where="src", exclude=["tests"]),
    install_requires=required,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
