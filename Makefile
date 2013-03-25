# Default value for output directory.
OUT_DIR = ./build

# Standard site compilation arguments.
COMPILE = \
	python bin/compile.py

# Static files.
STATIC_SRC = \
             $(wildcard ./*/*.csv) \
             $(wildcard ./*/*.html) \
             $(wildcard ./*/*.jpg) \
             $(wildcard ./*/*.json) \
             $(wildcard ./*/*.png) \
             $(wildcard ./*/*.sql) \
             $(wildcard ./*/*.svg) \
             $(wildcard ./*/*.txt) \
             $(wildcard ./*/*.xml) \
             $(wildcard ./css/*.css) \
             $(wildcard ./css/bootstrap/*.css) \
             $(wildcard ./css/bootstrap/img/*.png)
STATIC_DST = $(subst ./,$(OUT_DIR)/,$(STATIC_SRC))

# Pages to compile.
PAGES_SRC = $(filter-out _%.html,$(wildcard ./*.html))
PAGES_DST = $(subst ./,$(OUT_DIR)/,$(PAGES_SRC))

#------------------------------------------------------------

.default : commands

## commands     : show all commands
commands :
	@grep -E '^##' Makefile | sed -e 's/## //g'

## files        : show filesets
files :
	@echo "PAGES_SRC:" $(PAGES_SRC)
	@echo "PAGES_DST:" $(PAGES_DST)

#------------------------------------------------------------

## check        : rebuild entire site locally for checking purposes.
check : $(STATIC_DST)
	@make check-bare
	@make ascii-chars
	@make check-links

## check-bare   : rebuild entire site locally, but do not validate html 
check-bare: $(STATIC_DST)
	$(COMPILE) $(PAGES_SRC)

## ascii-chars  : check for non-ASCII characters or tab characters.
ascii-chars :
	@python bin/chars.py $(PAGES_DST)

## check-links  : check that local links resolve in generated HTML.
check-links :
	@find $(OUT_DIR) -type f -print | python bin/links.py $(OUT_DIR)

#------------------------------------------------------------

## md-test      : test Markdown conversion
md-test :
	@cat md-header.html > md-test.html
	@pandoc -t html setdict.md >> md-test.html
	@cat md-footer.html >> md-test.html

#------------------------------------------------------------

# Copy static files.
$(OUT_DIR)/% : %
	@mkdir -p $$(dirname $@)
	cp $< $@

#------------------------------------------------------------

## tidy         : clean up local files.
tidy :
	rm -f *~ */*~ */*/*~ */*/*/*~

## clean        : clean up generated files (but not copied files).
clean : tidy
	rm -f $$(find $(OUT_DIR) -name '*.html' -print)

## sterile      : clean up everything.
sterile : tidy
	rm -rf $(OUT_DIR)

