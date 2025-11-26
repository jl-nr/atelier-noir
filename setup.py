from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="atelier-noir",
    version="0.1.0",
    author="",
    description="Dark-themed image transformations for stylized preprocessing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/michal/atelier-noir",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Multimedia :: Graphics :: Graphics Conversion",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "Pillow>=9.0.0",
        "numpy>=1.20.0",
    ],
    entry_points={
        "console_scripts": [
            "atelier-noir=atelier_noir.cli:main",
        ],
    },
)
