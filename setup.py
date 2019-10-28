import subprocess

from setuptools import Command, find_packages, setup

# -----------------------------------------------------------------------------


def system(command):
    class SystemCommand(Command):
        user_options = []

        def initialize_options(self):
            pass

        def finalize_options(self):
            pass

        def run(self):
            subprocess.check_call(command, shell=True)

    return SystemCommand


# -----------------------------------------------------------------------------

setup(
    name="Fourmat",
    version="0.3.0",
    description="A library for batteries-included linting and autoformatting",
    url="https://github.com/4Catalyzer/fourmat",
    author="Giacomo Tagliabue",
    author_email="giacomo@gmail.com",
    license="MIT",
    classifiers=(
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ),
    keywords="lint autoformat black flake8 isort",
    packages=find_packages(),
    package_data={"fourmat": ("assets/*.*", "assets/.*")},
    install_requires=(
        "click >= 7",
        # Pin these to avoid unplanned messy diffs.
        "black==19.3b0",
        "flake8-bugbear==18.8.0",
        "flake8==3.6.0",
        "isort== 4.3.9",
    ),
    python_requires=">=3.6",
    entry_points={"console_scripts": ("fourmat = fourmat:cli",)},
    cmdclass={"test": system("tox")},
)
