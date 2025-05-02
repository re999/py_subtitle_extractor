import setuptools

with open("VERSION") as f:
    version = f.read().strip()

setuptools.setup(
    name="py_subtitle_extractor",
    version=version,
    author="Your Name",
    author_email="you@example.com",
    description="Pure-Python MKV/MP4 subtitle extractor",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/YourUser/py_subtitle_extractor",
    packages=["py_subtitle_extractor"],
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[],  # no external deps
)