from distutils.core import setup

setup(name='pivot',
      version='1.0',
      description='Automated mathematical deduction in python',
      author='Ryan Abrams',
      author_email='rdabrams@gmail.com',
      url='https://github.com/caervs/pivot',
      packages=['pivot',
                'pivot.deduction',
                'pivot.interface',
                'pivot.ontology',
                'pivot.examples',
                'pivot.lexicon',
                'pivot.tests', ])
