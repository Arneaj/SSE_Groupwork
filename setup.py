from setuptools import setup, find_packages

setup(
    name="SSE_Groupwork",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'flask',
        'requests',
        'sqlalchemy',
        'python-dotenv',
        'pytest',
    ],
)
