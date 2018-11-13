from io import open
from setuptools import setup

setup(
    name='multi-clipboard',
    version='1.3.0',
    url='https://github.com/brentvollebregt/mutli-clipboard',
    license='MIT',
    author='Brent Vollebregt',
    author_email='brent@nitratine.net',
    description='Switch clipboard contents using a simple GUI',
    long_description=''.join(open('README.md', encoding='utf-8').readlines()),
    long_description_content_type='text/markdown',
    keywords=['gui', 'clipboard'],
    packages=['multi_clipboard'],
    include_package_data=True,
    install_requires=['pywin32', 'PyQt5', 'Pillow', 'pynput'],
    python_requires='>=3.5',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Operating System :: Microsoft :: Windows',
    ],
    entry_points={
        'console_scripts': [
            'multi-clipboard=multi_clipboard.__main__:run',
        ],
    },
)
