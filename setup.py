from setuptools import setup, find_packages

setup(
    name='my_shell',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        # Add your dependencies here
    ],
    entry_points={
        'console_scripts': [
            'my_shell=my_shell.my_shell:main',
        ],
    },
    author='Rajeev Kumar',
    author_email='rajeevnita29@gmail.com',
    description='A custom shell in Python',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Rajeevnita1993/my_shell',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)