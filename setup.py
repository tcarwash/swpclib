from setuptools import setup, find_packages

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("README.rst") as history_file:
    history = history_file.read()

test_requirements = [
    "pytest>=3",
]

if __name__ == "__main__":
    setup(
        setup_requires=["setuptools-git-versioning"],
        test_suite="test",
        tests_require=test_requirements,
        name="swpclib",
    )
