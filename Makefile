OUTPUTFILE := mpkv
INSTALLLOCATION := ~/.local/bin

$(OUTPUTFILE): code.zip
	echo '#!/usr/bin/env python3' > $(OUTPUTFILE)
	cat code.zip >> $(OUTPUTFILE)
	rm code.zip
	chmod +x $(OUTPUTFILE)

code.zip: __main__.py config.py
	zip code.zip __main__.py config.py
	rm __main__.py

__main__.py: webview.py
	cp webview.py __main__.py

config.py:
	touch config.py

requirements:
	apt-get install zip python3

install: $(OUTPUTFILE)
	mkdir -p $(INSTALLLOCATION)
	cp $(OUTPUTFILE) $(INSTALLLOCATION)/.
