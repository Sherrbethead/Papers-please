from setuptools import setup, find_packages


setup(
    name='papers-please',
    version='0.1.0',
    description='Ultra light version of "Papers, please" game.',
    license='Apache License 2.0',
    author='Sherbethead',
    author_email='bakanovsergs@gmail.com',
    packages=find_packages(),
    py_modules=['game'],
    install_requires=[
        'faker', 'names', 'colorama', 'termcolor',
    ],
    entry_points={
        'console_scripts': [
            'papersplease = game:main',
        ],
    },
)
