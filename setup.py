from setuptools import setup, find_packages, Extension

LIBXML2_EXTENSIONS = [
    Extension(
        "florin_libxml2.xmlschemas",
        sources=["src/florin_libxml2/xmlschemasmodule.c"],
    )
]

setup(
    name="verifyxpathview",
    version="0.0.1",
    description="Visualizer for XPath satisfiability tests",
    author="Haja Florin-Gabriel",
    author_email="haja.fgabriel@gmail.com",
    package_dir={"": "src"},
    packages=find_packages("src"),
    classifiers=[
        "Development Status :: 1 - Planning",
        "Operating System :: Microsoft :: Windows",
        # TODO uncomment when Linux/POSIX support is stable
        #"Operating System :: POSIX",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    install_requires=[
        "networkx==3.1",
        'matplotlib; python_version < "3.9"',
    ],
    extras_require={
        "test": ["pytest"],
    },
    ext_modules=LIBXML2_EXTENSIONS,
)