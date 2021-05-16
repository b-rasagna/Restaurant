from setuptools import setup, find_packages

setup(name='restaurant',
      version='1.0.0',
      description='restaurant package',
      author='rasagna',
      author_email='rasagna0609@gmail.com',
      packages=find_packages(),
      package_data={ 
        'restaurant': ["config/*.yaml"]
      },
      scripts=['restaurant/bin/restaurant', 'restaurant/bin/restaurant.bat'],
      install_requires=[
        "bottle==0.12.19"
    ]
)