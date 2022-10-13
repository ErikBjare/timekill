SRCDIR = src/timekill
SOURCES = $(shell find $(SRCDIR) -type f -name '*.py')
# all sources without any __init__.py files
SOURCES_WITHOUT_INIT = $(filter-out %/__init__.py,$(SOURCES))

precommit: lint-fix typecheck test lint

typecheck:
	poetry run mypy $(SRCDIR) --ignore-missing-imports

test:
	poetry run pytest

lint:
	poetry run pylint $(SRCDIR)
	poetry run flake8 $(SRCDIR)
	poetry run bandit -c pyproject.toml -r $(SRCDIR)

lint-fix:
	poetry run autoflake -r $(SRCDIR) --in-place --imports . --remove-unused-variables --ignore-init-module-imports
	poetry run autoimport $(SOURCES_WITHOUT_INIT)
	poetry run reorder-python-imports $(SOURCES) --py310-plus || true
	poetry run isort $(SRCDIR)
	poetry run pyupgrade --py310-plus $(SOURCES)
	poetry run black $(SRCDIR)

.PHONY: docs/_build
docs: docs/_build
docs/_build:
	make -C docs html

SUBREDDITS := python quantifiedself coolgithubprojects rust programming linux

data: data/feeds

data/feeds: $(patsubst %,data/feeds/reddit/%/top.json,$(SUBREDDITS))

data/feeds/reddit/%/top.json:
	$(eval TARGET := $(patsubst data/feeds/reddit/%,%,$@))
	mkdir -p $(dir data/feeds/reddit/$(TARGET))
	curl --fail -o $@ 'https://www.reddit.com/r/$(TARGET)?limit=100&t=week'

package:
	# if macOS
	if [ "$$(uname)" = "Darwin" ]; then \
		make dist/TimeKill.app; \
	fi

media/icon.icns: media/icon.png
	mkdir -p build/MyIcon.iconset
	sips -z 16 16     $< --out build/MyIcon.iconset/icon_16x16.png
	sips -z 32 32     $< --out build/MyIcon.iconset/icon_16x16@2x.png
	sips -z 32 32     $< --out build/MyIcon.iconset/icon_32x32.png
	sips -z 64 64     $< --out build/MyIcon.iconset/icon_32x32@2x.png
	sips -z 128 128   $< --out build/MyIcon.iconset/icon_128x128.png
	sips -z 256 256   $< --out build/MyIcon.iconset/icon_128x128@2x.png
	sips -z 256 256   $< --out build/MyIcon.iconset/icon_256x256.png
	sips -z 512 512   $< --out build/MyIcon.iconset/icon_256x256@2x.png
	sips -z 512 512   $< --out build/MyIcon.iconset/icon_512x512.png
	cp				  $<       build/MyIcon.iconset/icon_512x512@2x.png
	iconutil -c icns build/MyIcon.iconset
	rm -R build/MyIcon.iconset
	mv build/MyIcon.icns $@


dist/TimeKill.app: media/icon.icns
	poetry run pyinstaller --name=TimeKill --onefile --windowed \
		--icon=media/icon.icns --add-data=media:media \
		src/timekill/__main__.py

clean:
	rm -rf data/feeds
