import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mdiki",
    version="0.0.1",
    author="nilo",
    author_email="nilo@team-tfm.com",
    description="minimalistic wiki based on markdown and git with wysiwyg editor",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dhavlik/mdiki",
    packages=setuptools.find_packages('src'),
    package_dir={'':'src'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
