.PHONY: build

dev:
	pip install pipenv==2024.0.1
	pipenv install --dev

p:
	pipenv run pylint --output-format=colorized ./ --jobs=0

b:
	pipenv run black ./

f:
	pipenv run flake8 ./ --config setup.cfg

i:
	pipenv run isort ./

m:
	pipenv run mypy ./ --config setup.cfg

c:
	echo "Check repo is clean"
	git status -s
	git diff
	git diff-index --quiet HEAD --

l: f p m
alf: b i f p m
