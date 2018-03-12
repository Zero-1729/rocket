from setuptools import setup

setup(name="stellar",
    version='0.6.0',
    description="Rocket lang 'stellar' token utility",
    author="Zero-1729",
    author_email="abubakarnurkhalil@gmail.com",
    py_modules=[
        "tokens"
    ],
    package_dir={"": "utils/"},
    license="MIT")
