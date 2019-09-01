build:
	pyinstaller bars.spec -y

run:
	python -m bars

run-packaged: build
	./dist/bars/bars.bin

.PHONY: build run run-packaged
