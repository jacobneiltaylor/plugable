import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="plugable",
    version="0.1.0",
    author="Jacob Neil Taylor",
    author_email="me@jacobtaylor.id.au",
    description="A framework for writing extensible Python components",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jacobneiltaylor/plugable",
    package_dir={'': 'src'},
    packages=setuptools.find_packages(where='src'),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
