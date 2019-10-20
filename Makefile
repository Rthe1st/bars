build:
	pyinstaller bars.spec -y

run:
	python -m bars play

run-packaged: build
	./dist/bars/bars.bin

test:
	python -m unittest discover

.PHONY: build run run-packaged test
