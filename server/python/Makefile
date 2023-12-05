
put:
	rsync -uvrzl --exclude __pycache__ *.py 3ddata.txt xmaslights.service .htaccess web videos animations_available animations_enabled ef:python/.

getvids:
	rsync -uvrzl ef:python/videos .

putclean:
	rsync -uvrzl --delete --exclude __pycache__ *.py 3ddata.txt xmaslights.service .htaccess web videos animations_available animations_enabled ef:python/.

