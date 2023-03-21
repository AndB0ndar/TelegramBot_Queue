from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))
# Get the long description from the README file
# long_description = open(here+"/"+"README.md", 'r').read()

if __name__ == "__main__":
	f = open('requirements.txt')
	req = []
	for line in f:
		req.append(line)

	setup(
		name="BotQueueTg",
		version="1.0.0",
		description="Python project implementing a bot queue in the telegram social network",
		packages=find_packages(
			exclude=['venv']
		),
		install_requires=req
	)
