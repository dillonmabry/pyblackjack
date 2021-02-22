from setuptools import setup, find_packages


def readme():
    with open('README.md') as f:
        return f.read()


setup(name='pyblackjack',
      version='0.0.1',
      description='Blackjack Simulator in Python',
      long_description=readme(),
      long_description_content_type='text/markdown',
      license='MIT',
      packages=find_packages(),
      test_suite='tests',
      entry_points={
          'console_scripts': [
              'pyblackjack = flagger.__main__:main'
          ]
      },
      include_package_data=True,
      data_files=[('', [
          'pyblackjack/resources/strategies/basic_strategy.json',
          'pyblackjack/resources/strategies/basic_strategy_alt.json'
      ])],
      zip_safe=False
      )
