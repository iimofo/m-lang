from setuptools import setup, find_packages

setup(
    name='m-lang',  # Name of your package
    version='0.1.0',  # Version of your package
    description='A programming language interpreter for M-',  # Brief description
    author='Mofo',  # Your name
    author_email='mustafahashem9944@gmail.com',  # Your email
    url='',  # URL to the project (if hosted on GitHub)
    packages=find_packages(),  # Automatically find and include packages in the project
    install_requires=[],  # List any dependencies your project needs, e.g., 'numpy'
    classifiers=[
        'Programming Language :: Python :: 3',  # Specify the programming language
        'License :: OSI Approved :: MIT License',  # License type
        'Operating System :: OS Independent',  # OS compatibility
    ],
    python_requires='>=3.6',  # Minimum Python version
)