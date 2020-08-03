from setuptools import setup

setup(name='fdlogs',
      version='0.1.0',
      author='xmonarch',
      author_email='xmonarch64@gmail.com',
      packages=['fdlogs'],
      scripts=['bin/fdlogs'],
      description="Follow docker container logs and survive restarts",
      install_requires=['argparse'],
      license="GPLv2",
      platforms=["Independent"],
      keywords="docker logs follow",
      url="https://github.com/xmonarch/fdlogs",
      classifiers=[
          "Intended Audience :: Developers",
          "License :: OSI Approved :: GNU General Public License (GPL)",
          "Operating System :: OS Independent",
          "Programming Language :: Python",
          "Programming Language :: Python :: 3.8",
      ]
      )
