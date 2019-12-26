from setuptools import setup

setup(
    name="kops",
    version="0.1.0",
    description="Shell for Kubernetes Operations",
    url="http://github.com/cbanek/kops",
    author="Christine Banek",
    author_email="cbanek@gmail.com",
    packages=["kops"],
    install_requires=["kubernetes", "npyscreen"],
    scripts=["bin/kops"],
    zip_safe=False,
)
