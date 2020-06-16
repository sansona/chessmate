import pathlib

from setuptools import find_packages, setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="chessmate",
    version="1.0.8",
    description="Framework for defining and analyzing chess engines",
    keywords="Chess chess",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/sansona/chessmate",
    author="Jiaming Chen",
    author_email="jiaming.justin.chen@gmail.com",
    license="GPL",
    packages=find_packages(),
    install_requires=['python_chess'],
    include_package_data=True)
