typecheck:
	poetry run mypy src/timekill --ignore-missing-imports

test:
	poetry run pytest

SUBREDDITS := python quantifiedself coolgithubprojects rust programming linux

data: data/feeds

data/feeds: $(patsubst %,data/feeds/reddit/%/top.json,$(SUBREDDITS))

data/feeds/reddit/%/top.json:
	$(eval TARGET := $(patsubst data/feeds/reddit/%,%,$@))
	mkdir -p $(dir data/feeds/reddit/$(TARGET))
	curl --fail -o $@ 'https://www.reddit.com/r/$(TARGET)?limit=100&t=week'

clean:
	rm -rf data/feeds
