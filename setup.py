import glob
import os

from setuptools import setup, find_packages

here = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(here, "README.md")) as f:
    long_description = f.read()

setup(
    name="pandoc-purl",
    version="0.2.0",
    
    description="Dynamic document generation for Pandoc in Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    
    url="https://github.com/lamyj/pandoc-purl",
    
    author="Julien Lamy",
    author_email="lamy@unistra.fr",
    
    license="MIT",
    
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        
        "Environment :: Console",
        
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Science/Research",
        
        "Topic :: Communications :: File Sharing",
        "Topic :: System :: Archiving :: Mirroring",
        
        "License :: OSI Approved :: MIT License",
        
        "Programming Language :: Python :: 3",
        
        "Topic :: Documentation",
        "Topic :: Education",
        "Topic :: Scientific/Engineering",
        "Topic :: Text Processing :: Filters",
        "Topic :: Text Processing :: Markup :: Markdown"
    ],
    
    keywords=[
        "pandoc", "markdown", "pandoc-filter", "literate programming",
        "dynamic document", "reproducible research"],

    packages=find_packages(),
    include_package_data=True,
    install_requires=["pandocfilters"],
    
    entry_points={ "console_scripts": [ "pandoc-purl=pandoc_purl.main:main"] },
)
