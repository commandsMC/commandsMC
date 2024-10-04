import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

setup(
    name='minechat',
    version='0.0.1',
    url='https://github.com/commandsMC/minechat',
    license='MIT',
    author='Francisco Griman',
    author_email='grihardware@gmail.com',
    description='A simple library to create a chat bot for Minecraft.',
    long_description=(HERE / "README.md").read_text(encoding='utf-8'),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'javascript==1!1.2.1',
        'colorama==0.4.6'
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.12'
    ],
)