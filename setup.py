import platform
from setuptools import setup, find_packages, Extension


CURRENT_ARCH = platform.architecture()
BITNESS, CURRENT_OS = CURRENT_ARCH


# TODO fix for Mac
LIBXML2_BUILD_DIR = {
    ("32bit", "WindowsPE"): "C:/libxml2/build-VS2022/Debug",
    ("64bit", "WindowsPE"): "C:/libxml2/build-VS2022/x64/Debug",
}

INCLUDE_DIRS = {
    "WindowsPE": ["C:/libxml2/include", "C:/libiconv-win-build/include"],
}

LIBXML2_EXTENSIONS = [
    Extension(
        "florin_libxml2.xmlschemas",
        sources=["src/florin_libxml2/xmlschemasmodule.c"],
        libraries=["libxml2"],
        
        # TODO replace with a user-defined or a renamed libxml2 that contains xmlSchemaVerifyXPath API
        library_dirs=[LIBXML2_BUILD_DIR.get(CURRENT_ARCH)],
        
        # TODO replace with more generic include directories; fix Mac support
        include_dirs=INCLUDE_DIRS.get(CURRENT_OS),
        
        # Arguments to produce debugging symbols on Windows
        extra_compile_args=["/Zi", "/Od"],
        extra_link_args=["/DEBUG"],
    )
]

setup(
    name="verifyxpathview",
    description="Visualizer for XPath satisfiability tests",
    author="Haja Florin-Gabriel",
    author_email="haja.fgabriel@gmail.com",
    version="0.0.1",
    python_requires=">=3.8",
    package_dir={"": "src"},
    packages=find_packages("src"),
    classifiers=[
        "Development Status :: 1 - Planning",
        "Operating System :: Microsoft :: Windows",
        
        # TODO fix Linux support
        #"Operating System :: POSIX",
        #"Operating System :: POSIX :: Linux",
        
        # TODO fix macOS support
        #"Operating System :: MacOS",
        #"Operating System :: MacOS :: MacOSX",
        
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    install_requires=[
        "networkx==3.1",
        'matplotlib==3.7.5',
    ],
    extras_require={
        # the plugin https://github.com/microsoft/PTVS requires the deprecated function
        # pytest.compat._translate_non_printable
        "test": ["pytest==8.0.2"],
    },
    ext_modules=LIBXML2_EXTENSIONS,
)