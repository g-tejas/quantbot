from gettext import install
from numpy import insert
import setuptools

setuptools.setup(
    name="plutuslib",
    version="0.1",
    description="code lib by gtejas",
    url="#",
    author="Tejas G.",
    install_requires=["opencv-python"],
    author_email="ttejasgarrepally@gmail.com",
    packages=setuptools.find_packages(),
    zip_safe=False
)