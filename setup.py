from setuptools import setup, find_packages

test_requirements = [
    "pytest>=3",
]

if __name__ == "__main__":
    setup(
        setup_requires=["setuptools-git-versioning"],
        test_suite="test",
        tests_require=test_requirements,
        install_requires=["aiohttp==3.8.3"],
        name="swpclib",
    )
