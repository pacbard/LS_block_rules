.PHONY: all
all:
	python2 build_rules.py; \
	git commit -a -m "Rules updated: `date`"; \
	ssh-agent bash -c 'ssh-add /.ssh/id_rsa; git push'


