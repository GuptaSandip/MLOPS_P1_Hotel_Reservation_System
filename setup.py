from setuptools import setup,find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()


setup(
    name = "mlops_p1_hotel_reservation_system",
    version="0.1",
    author= "Sandip Gupta",
    packages=find_packages(),
    install_requires = requirements,
    
)