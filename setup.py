from setuptools import setup, find_packages

setup(
    name="HadesC2",
    version="1.0",
    packages=find_packages(),
    install_requires=[
        "bcrypt",
    ],
    entry_points={
        "console_scripts": [
            "hadesc2=hades_c2:main",  # Assuming your main file is named hades_c2.py and main() is the entry function
        ],
    },
    description="HadesC2 Command and Control Interface for Warshipping Devices",
    author="Your Name",
    author_email="hackergeorge@protonmail.ch",
    url="https://github.com/hackergeorge/HadesC2",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
