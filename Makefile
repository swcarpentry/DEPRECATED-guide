# Default value for output directory.
OUT_DIR = $(PWD)/build

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

# Chapters in book version.
BOOK_STEMS = \
  index \
  intro \
  shell \
  svn \
  python \
  pymedia \
  funclib \
  db \
  numpy \
  quality \
  setdict \
  dev \
  web \
  teach \
  concl \
  ack \
  extras \
  stylesheet \
  bib \
  ref

BOOK_HTML = $(foreach stem,$(BOOK_STEMS),$(stem).html)

#------------------------------------------------------------

.default : commands

## commands     : show all commands
commands :
	@grep -E '^##' Makefile | sed -e 's/## //g'

#------------------------------------------------------------

## check        : rebuild entire site locally for checking purposes.
check : $(STATIC_DST)
	@make ascii-chars
	@make check-bare
	@make check-links
	@make book-figref

## check-bare   : rebuild entire site locally, but do not validate html 
check-bare: $(STATIC_DST)
	$(COMPILE) $(BOOK_HTML)

## check-links  : check that local links resolve in generated HTML.
check-links :
	@find $(OUT_DIR) -type f -print | python bin/links.py $(OUT_DIR)

## ascii-chars  : check for non-ASCII characters or tab characters.
ascii-chars :
	@python bin/chars.py $$(find . -name '*.html' -print)

#------------------------------------------------------------

# Copy static files.
$(STATIC_DST) : $(OUT_DIR)/% : %
	@mkdir -p $$(dirname $@)
	cp $< $@

#------------------------------------------------------------

## book-bib     : check for undefined/unused bibliography references.
book-bib :
	@bin/book.py bibundef $(BOOK_CHAPTERS_HTML)
	@bin/book.py bibunused $(BOOK_CHAPTERS_HTML)

## book-book    : run all checks.
book-book :
	@for i in unknown gloss images source structure bib fig; do \
	  echo '----' $$i '----'; \
	  make book-$$i; \
	done

## book-classes : list all classes used in the generated HTML files.
book-classes :
	@bin/book.py classes $$(find $(OUT_DIR) -name '*.html' -print)

## book-fig     : check figure formatting and for undefined/unused figures.
book-fig :
	@bin/book.py figformat $(BOOK_CHAPTERS_HTML)
	@bin/book.py figundef $(BOOK_CHAPTERS_HTML)
	@bin/book.py figunused $(BOOK_CHAPTERS_HTML)

## book-figref  : patch cross-references in figures
book-figref :
	@python bin/fignumber.py $(BOOK_CHAPTERS_HTML)

## book-fix     : count FIXME markers in files.
book-fix :
	@bin/book.py fix $(BOOK_CHAPTERS_HTML)

## book-gloss   : check glossary formatting and for undefined/unused glossary entries.
book-gloss :
	@bin/book.py glossformat $(BOOK_CHAPTERS_HTML)
	@bin/book.py glossundef $(BOOK_CHAPTERS_HTML)
	@bin/book.py glossunused $(BOOK_CHAPTERS_HTML)

## book-ideas   : extract key ideas.
book-ideas :
	@bin/book.py ideas $(BOOK_CHAPTERS_HTML)

## book-images  : check for undefined/unused images.
book-images :
	@bin/book.py imgundef img $(BOOK_CHAPTERS_HTML)
	@bin/book.py imgunused img $(BOOK_CHAPTERS_HTML)

## book-source  : check for undefined/unused source code fragments.
book-source :
	@bin/book.py srcundef src $(BOOK_CHAPTERS_HTML)
	@bin/book.py srcunused src $(BOOK_CHAPTERS_HTML)

## book-struct  : check overall structure of files.
book-struct :
	@bin/book.py structure $(BOOK_CHAPTERS_HTML)

## book-summary : extract section summaries (learning goals and keypoints).
book-summary :
	@bin/book.py summaries $(BOOK_CHAPTERS_HTML)

## book-unknown : check for unexpected HTML files.
book-unknown :
	@bin/book.py unknown vol1 $(BOOK_CHAPTERS_HTML)

## book-words-a : count words in files (report alphabetically).
book-words-a :
	@bin/book.py words $(BOOK_CHAPTERS_HTML)

## book-words-n : count words in files (report numerically).
book-words-n :
	@bin/book.py words $(BOOK_CHAPTERS_HTML) | sort -n -r -k 2

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

