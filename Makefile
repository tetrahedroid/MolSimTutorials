combined.md: [01]*.md combine.py
	python combine.py > $@

%.md: %.md.j2
	python convert.py $< > $@


clean:
	find . -name "Icon*" -delete
