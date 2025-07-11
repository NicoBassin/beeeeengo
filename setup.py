from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="bingo-seguro",
    version="1.0.0",
    author="Tu Nombre",
    author_email="tu@email.com",
    description="Simulador de Bingo Argentino con interfaz gráfica",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tu-usuario/bingo-seguro",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Games/Entertainment",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.7",
    install_requires=[
        "pymysql>=1.0.2",
    ],
    entry_points={
        "console_scripts": [
            "bingo-seguro=app:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)