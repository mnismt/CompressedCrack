from setuptools import setup, find_packages

setup(
    name="compressedcrack",
    version="1.0.3",
    description="A command-line tool to crack password-protected compressed files using brute force.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Minh Thanh",
    author_email="thanhdoantranminh@gmail.com",
    url="https://github.com/mnismt/CompressedCrack",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    keywords=["brute force", "password cracking", "compressed files"],
    install_requires=["patool>=2.2.0", "click"],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "compressedcrack = compressedcrack.main:main"
        ]
    },
    license="MIT",
)
