all: combined.md combined.ipynb
combined.md: [01]*.md combine.py
	python combine.py > $@

%.md: %.md.j2 convert.py $(wildcard codes/*.py)
	python convert.py $< > $@

%.ipynb: %.md md_to_ipynb.py Makefile
	python md_to_ipynb.py $<

clean:
	find . -name "Icon*" -delete
