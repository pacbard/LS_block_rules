.PHONY: all
all:
	python2 build_rules.py; \
	git commit -a -m "Rules updated: `date`"; \
	git push

