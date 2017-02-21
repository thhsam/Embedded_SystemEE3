from setuptools import setup

setup(name='TheATeamChess',
      version='0.1',
      description='Code for beta server side',
      url='https://github.com/thhsam/Embedded_SystemEE3',
      author='lmp3000',
      author_email='lmpmax3000@gmail.com',
      license='MIT',
      packages=['TheATeamChess'],
      install_requires=[
          'Tkinter',
          'paho.mqtt.client',
          'cb',
          'PIL'
      ],
      zip_safe=False)
