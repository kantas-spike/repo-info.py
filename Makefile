DST_DIR=${HOME}/bin
SCRIPT_HOME=$(dir $(abspath repo-info.py))


repo-info.sh: repo-info.sh.tmpl
	cat $< | sed -e 's#@@@SCRIPT_HOME_DIR@@@#${SCRIPT_HOME}#' > $@

clean: repo-info.sh
	rm $^

install: repo-info.sh
	mkdir -p ${DST_DIR}
	cp $< ${DST_DIR}
	chmod u+x ${DST_DIR}/$<
