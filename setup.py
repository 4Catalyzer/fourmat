from setuptools import find_packages, setup

setup(
    name="fourmat",
    version="0.6.0",
    description="A library for batteries-included linting and autoformatting",
    url="https://github.com/4Catalyzer/fourmat",
    author="Giacomo Tagliabue",
    author_email="giacomo@gmail.com",
    license="MIT",
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3 :: Only",
    ],
    keywords="lint autoformat black flake8 isort",
    packages=find_packages(),
    package_data={"fourmat": ("assets/*.*", "assets/.*")},
    install_requires=(
        "click>=7",
        # Pin these to avoid unplanned messy diffs.
        "black==19.10b0",
        "flake8-bugbear==20.1.4",
        "flake8==3.8.3",
        "isort==5.0.6",
    ),
    entry_points={"console_scripts": ("fourmat = fourmat:cli",)},
)
