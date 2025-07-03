.PHONY: all build clean

all: build

build:
	mkdir -p build && pyinstaller main.spec --log-level=DEBUG 2>&1 -y | tee build/debug.log

clean:
	rm -rf build/ dist/

clean-pycache:
	find . -type d -name "__pycache__" -exec rm -rf {} +

update:
	pip install -U akshare
