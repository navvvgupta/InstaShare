from setuptools import setup, find_packages

setup(
    name='ApnaHub',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'bcrypt',
        'inquirer',
        'mongoengine',
        'tqdm',
        'pyfiglet',
        'termcolor'
    ],
    entry_points={
        'console_scripts': [
            'apnahub-server=server.server:server',
            'apnahub-client=client.client:client',
        ],
    },
    author='Apna Hub',
    author_email='apnahub@gmail.com',
    description='A CLI based P2P file sharing platform over LAN',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/navvvgupta/apna-hub',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
