from setuptools import setup, find_packages

setup(
    name="nosdonnees",
    version="1.0.0",
    description="Plateforme de partage de bases de données",
    author="Nosdonnées Team",
    packages=find_packages(),
    install_requires=[
        "Django>=4.2.0,<5.0",
        "Pillow>=10.0.0",
        "python-decouple>=3.8",
    ],
) 