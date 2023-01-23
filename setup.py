""" Python generator utilities """
import shutil
from pathlib import Path
from setuptools import setup

here = Path(__file__).parent.resolve()

# Remove build and dist folders
shutil.rmtree(Path("build"), ignore_errors=True)
shutil.rmtree(Path("dist"), ignore_errors=True)

setup()

shutil.rmtree(Path("build"), ignore_errors=True)