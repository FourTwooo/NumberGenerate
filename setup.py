from setuptools import setup, find_packages

setup(
    name='NumberGenerate',
    version='0.1.1',
    description='CN-NumberGenerate',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='42',
    author_email='1666671111@qq.com',
    url='https://github.com/FourTwooo/NumberGenerate',
    packages=find_packages(),  # 这行会自动找出NumberGenerate作为包
    include_package_data=True,  # 启用包括包数据
    package_data={
        '': ['*.db'],  # 包含所有包中的 .db 文件
    },
    install_requires=open('requirements.txt').read().splitlines(),
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=3.6',
)


# python setup.py sdist bdist_wheel
# twine upload dist/*