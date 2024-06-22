from setuptools import find_packages, setup

setup(
    name="fourmat",
    version="1.0.0",
    description="A library for batteries-included linting and autoformatting",
    url="https://github.com/4Catalyzer/fourmat",
    author="Giacomo Tagliabue",
    author_email="giacomo@gmail.com",
    license="MIT",
    python_requires=">=3.10",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3 :: Only",
    ],
    keywords="lint autoformat black flake8 isort",
    packages=find_packages(),
    package_data={"fourmat": ["assets/*.*", "assets/.*"]},
    install_requires=(
        "click>=8",
        "black==24.3.0",
        "flake8-bugbear>=24,<25",
        "flake8>=7,<8",
        "isort>=5,<6",
        "setuptools>=70",
    ),
    entry_points={"console_scripts": ("fourmat = fourmat:cli",)},
)
