from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in muasasa/__init__.py
from muasasa import __version__ as version

setup(
	name="muasasa",
	version=version,
	description="trade",
	author="smart",
	author_email="smart",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
