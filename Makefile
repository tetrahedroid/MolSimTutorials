combined.md: [01]*.md combine.py
	python combine.py > $@

clean:
	find . -name "Icon*" -delete
