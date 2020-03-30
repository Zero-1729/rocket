from setuptools import setup

setup(name="stellar_tools",
    version='0.8.0',
    description="Rocket lang 'stellar' tools",
    author="Zero-1729",
    author_email="zero1729@protonmail.com",
    py_modules=["wallice", "custom_syntax", "astprinter", "genast"],
    package_dir={"": "."},
    license="MIT")
