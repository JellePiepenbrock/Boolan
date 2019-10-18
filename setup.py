import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="boolan-jpiepenbrock",
    version="0.0.1",
    author="Jelle Pipeenbrock",
    author_email="jellepiepenbrock@gmail.com",
    description="Analysis of Boolean functions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JellePiepenbrock/Boolan",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Ubuntu",
    ],
    python_requires='>=3.6',
)
