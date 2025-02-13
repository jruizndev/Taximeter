from setuptools import setup, find_packages

setup(
    name="taximeter",
    version="0.1",
    packages=find_packages(exclude=['tests*']),  
    install_requires=[
        'mysql-connector-python',
        'python-dotenv',
        'bcrypt'
    ],
    python_requires='>=3.6',  
    include_package_data=True,  
    author="Pepe", 
    description="Sistema de taxímetro digital",  
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)