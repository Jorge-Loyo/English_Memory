"""
Setup script para English Memory
"""

from setuptools import setup, find_packages
from pathlib import Path

# Leer README
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

setup(
    name='english-memory',
    version='1.2.0',
    author='Agilize Soluciones',
    author_email='administrador@agilizesoluciones.com',
    description='Aplicación educativa para aprender y organizar vocabulario en inglés',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/tu-usuario/english-memory',
    py_modules=['diccionario_gui', 'diccionario'],
    python_requires='>=3.7',
    install_requires=[
        'pyinstaller>=5.13.2',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Education',
        'Topic :: Education',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Operating System :: OS Independent',
        'Natural Language :: Spanish',
    ],
    keywords='education english learning vocabulary spanish',
    project_urls={
        'Bug Reports': 'https://github.com/tu-usuario/english-memory/issues',
        'Source': 'https://github.com/tu-usuario/english-memory',
        'Documentation': 'https://github.com/tu-usuario/english-memory/blob/main/README.md',
    },
)
