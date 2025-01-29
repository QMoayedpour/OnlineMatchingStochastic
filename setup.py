from setuptools import setup, find_packages

setup(
    name="OMSR",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["pandas", "pulp", "numpy",
                      "matplotlib", "networkx"],
)