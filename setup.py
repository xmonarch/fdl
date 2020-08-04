import pathlib

from setuptools import setup

setup(name='fdlogs',
      version='0.1.0',
      author='xmonarch',
      author_email='xmonarch64@gmail.com',
      packages=['fdlogs'],
      scripts=['bin/fdlogs'],
      description="Follow docker container logs and survive restarts",
      long_description=(pathlib.Path(__file__).parent / "README.md").read_text(),
      long_description_content_type="text/markdown",
      install_requires=['argparse'],
      license="GPLv2",
      platforms=["Independent"],
      keywords="docker logs follow",
      url="https://github.com/xmonarch/fdlogs",
      classifiers=[
          "Intended Audience :: Developers",
          "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
          "Operating System :: OS Independent",
          "Programming Language :: Python",
          "Programming Language :: Python :: 3.8",
      ]
      )
