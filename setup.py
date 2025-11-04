from setuptools import setup, find_packages

setup(
    name="project-wizard",
    version="0.3.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "click>=8.1.0",
        "jinja2>=3.1.0",
        "pyyaml>=6.0",
        "pydantic>=2.0.0",
        "requests>=2.31.0",
        "python-dotenv>=1.0.0",
        "rich>=13.0.0",
        "questionary>=2.0.0",
        "gitpython>=3.1.0",
    ],
    entry_points={
        "console_scripts": [
            "project-wizard=app.main:cli",
        ],
    },
    author="Jonathan Ives",
    description="Interactive project management wizard for OpenProject",
    python_requires=">=3.8",
)
