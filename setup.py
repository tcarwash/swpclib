from setuptools import setup, find_packages

test_requirements = [
    "pytest>=3",
]

from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

if __name__ == "__main__":
    setup(
        setup_requires=["setuptools-git-versioning"],
        test_suite="test",
        long_description=long_description,
        long_description_content_type="text/markdown",
        tests_require=test_requirements,
        install_requires=["aiohttp>=3.8.1"],
        name="swpclib",
    )
