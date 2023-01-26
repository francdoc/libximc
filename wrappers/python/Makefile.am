XIGEN = ${top_builddir}/deps/xigen/bin/xigen

$(top_builddir)/wrappers/python/pyximc.py: ${top_srcdir}/libximc/src/protocol.xi $(top_srcdir)/wrappers/python/pyximc-template.py 
	$(XIGEN) --gen-python -w -x $(top_srcdir)/version -i $< -o $@ -t $(top_srcdir)/wrappers/python/pyximc-template.py

BUILT_SOURCES = $(top_builddir)/wrappers/python/pyximc.py

all-local: ${BUILT_SOURCES}

EXTRA_DIST = pyximc-template.py

CLEANFILES = $(top_builddir)/wrappers/python/pyximc.py
