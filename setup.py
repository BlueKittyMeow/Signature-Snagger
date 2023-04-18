from setuptools import setup, find_packages

setup(
    name="signature-snagger",
    version="0.1.0",
    packages=find_packages(),
    python_requires='>=3.6',
    install_requires=[
        "Pillow",
        "pdf2image",
        "img2pdf",
        "pdfrw",
        "watchdog"
    ],
    entry_points={
        "console_scripts": [
            "signature-snagger = main:run",
        ],
    },
)
