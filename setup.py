import setuptools

with open("README.md", "r") as raw_readme:
    readme = raw_readme.read()

setuptools.setup(
    name="symmetric",
    version="1.0.0",
    url="https://github.com/daleal/symmetric",
    project_urls={
        "Documentation": "https://github.com/daleal/symmetric",
        "Code": "https://github.com/daleal/symmetric",
        "Issue tracker": "https://github.com/daleal/symmetric/issues",
    },
    license="MIT License",
    author="Daniel Leal",
    author_email="dlleal@uc.cl",
    maintainer="daleal",
    maintainer_email="dlleal@uc.cl",
    description="A simple wrapper over Flask to speed up basic "
                "API deployments.",
    long_description=readme,
    long_description_content_type="text/markdown",
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    install_requires=[
        "flask>=1.1.1",
    ],
)
