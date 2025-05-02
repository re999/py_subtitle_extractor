import setuptools

with open("VERSION") as f:
    version = f.read().strip()

setuptools.setup(
    name="py_subtitle_extractor",
    version=version,
    author="Re999",
    author_email="dariusz23@gmail.com",
    description="Pure-Python MKV subtitle extractor",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/re999/py_subtitle_extractor",
    packages=["py_subtitle_extractor"],
    python_requires=">=3.8",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[]
)