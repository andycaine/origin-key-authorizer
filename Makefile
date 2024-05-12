SHELL := /bin/bash

clean:
	rm -f packaged.yaml
	rm -rf .aws-sam/build

test: oka/app.py tests/test_app.py
	pytest

.aws-sam/build: template.yaml test
	sam build

packaged.yaml: .aws-sam/build
	sam package \
		--resolve-s3 \
		--output-template-file $@

publish: packaged.yaml
	sam publish --template packaged.yaml
