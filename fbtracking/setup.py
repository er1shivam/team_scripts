from distutils.core import setup

setup(
    name="dfy_tracking",
    packages=["dfy_tracking"],
    version="0.1",
    license="MIT",
    description="This is a library to be used with the dfysetters.com team. It allows us to analyse our messages and extract data from them",
    author="Louis-Rae",
    author_email="louisrae@settersandspecialists.com",
    url="https://github.com/louisrae",
    download_url="https://github.com/user/reponame/archive/v_01.tar.gz",  # I explain this later on
    keywords=[
        "data",
        "tracking",
        "pandas",
    ],
    install_requires=[  # I get to this in a second
        "validators",
        "beautifulsoup4",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],
)
