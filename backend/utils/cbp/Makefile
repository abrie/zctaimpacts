download:
	mkdir -p downloads
	(cd downloads; xargs -n 1 curl -O < ../resources.txt)
	find downloads -iname "*.zip" -exec unzip {} -d raw \;
build:
	python -m app
