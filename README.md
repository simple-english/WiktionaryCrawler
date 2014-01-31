Refer to http://www.google-melange.com/gci/task/view/google/gci2013/5591760998760448

# Dependencies

	$ sudo pip install urlnorm

Depending on your language, you may need to install more dependencies.

Here are the list of language specific dependencies:

* **zh** (Chinese, simplified and traditional): `sudo pip install mafan BeautifulSoup4`
* **th** (Thai): `sudo pip install BeautifulSoup4`
* **lo** (Lao): `sudo pip install BeautifulSoup4`

# Running the crawler

	$ python main.py

That's... all you have to do. All configuration is done in `config.py`.

# Stages

The crawler goes through 5 stages.

## Stage 1: Obtaining list of subcategories to crawl.

1) The crawler looks for sub-categories in a starting category (`config.start_cat`) and records them down in `data/site/start_cat/subcats.txt`. Any sub-categories blacklisted will not be included.

2) The crawler looks for sub-categories in those sub-categories and adds them to the list of sub-categories.

## Stage 2: Obtaining list of pages to crawl.

2) The crawler then crawls the sub-categories for pages and records them down in `data/site/start_cat/subcat/pages.txt`. Any pages blacklisted or filtered will not be included.

More information can be found at [Filters](https://github.com/wei2912/WiktionaryCrawler#filters).

3) These pages are then added to a list of pages which will then be crawled at the next stage.

## Stage 3: Crawling all pages in list.

1) The crawler goes through every page in the list and downloads it into `data/pages`.

***NOTE: This stage will take a very long time to complete as the crawler has to abide by crawl delays.***

## Stage 4: Parsing all pages in list.

1) The parser goes through every page in the list and parses it based on the language.

More information can be found at [Parsers](https://github.com/wei2912/WiktionaryCrawler#parsers).

## Stage 5: Writing final results to file.

1) All spelings are written to `data/spelings.txt`

2) The program terminates with statistics.

# Filters

At stage 2, pages can be filtered out by plugins based on language. Here is the list of filters:

* **zh.py** - Chinese (simplified and traditional)
	* Pages are filtered out based on whether the word is simplified, traditional or both.
	* This can be set in `config.py`.
* **th.py** - Thai
	* Nothing to see here, move on.

Filters are stored in `filters/`. Every filter has a test suite which goes by the filename `filter_test.py`. This test suite can be runned to check if the filter has any errors.

# Parsers

At stage 4, pages are parsed based on language. Here is the list of parsers:

* **zh.py** - Chinese (simplified and traditional)
	* Parses pages into the following format: `word ; POS tag ; pinyin ; gloss (meaning)`
* **th.py** - Thai
	* Parses pages into the following format: `word ; romanised ; pinyin ; gloss (meaning)`

The parser is automatically selected based on the language set in `config.py`. More information can be found at [General Config](https://github.com/wei2912/WiktionaryCrawler#general-config)

Parsers are stored in `parsers/`. Every parser has a test suite which goes by the filename `parser_test.py`. This test suite can be runned to check if the parser has any errors.

# General Config

The default `config.py` looks like this:

	# coding=utf8

	start_cat = "Category:Mandarin language"
	api_crawl_delay = 1 # in seconds
	page_crawl_delay = 0.4 # in seconds
	lang = "zh"

	## lang-specific config vals ##
	.
	.
	.
	## lang-specific config vals ##

	## DO NOT MODIFY ##
	.
	.
	.
	## DO NOT MODIFY

The top comment, `# coding=utf8`, is required to set the encoding of the file so that unicode characters can be included in comments, if you ever need to.

## `start_cat`

`start_cat` is the category where the crawler begins crawling for sub-categories.

Here are the following values for different languages:

* **zh** `Category:Mandarin language`
* **th** `Category:Thai parts of speech`

## `api_crawl_delay` and `page_crawl_delay`

`api_crawl_delay` is the time the crawler waits before sending a request to the API while `page_crawl_delay` is the time the crawler waits before crawling the next page. The default delays are fine and you should not set a value lower than the defaults.

The default value of `api_crawl_delay` is 1 second as it is an API request whereas the default value of `page_crawl_delay` is 0.4 seconds as pages are cached.

The crawl delay is in seconds.

## `lang`

`lang` is the language code which will determine the [parser](https://github.com/wei2912/WiktionaryCrawler#parsers) and [filter](https://github.com/wei2912/WiktionaryCrawler#filters) which the program will use.

The following languages are supported:

* **zh** - Chinese (simplified and traditional)
* **th** - Thai
* **lo** - Lao

## Language specific configuration values

The default configuration values parse simplified Chinese text. If you wish to parse another language, please comment out these values and look for your language, then uncomment those config values.

The config values for each language is specified here.

### **zh** - Chinese, simplified and traditional

These values are available:

* `zh_s`: Set to `True` if you wish to crawl only simplified words.
* `zh_t`: Set to `True` if you wish to crawl only traditional words.

Words that are both simplified and traditional will always be parsed if either `zh_s` or `zh_t` is set to `True`.

### **th** - Thai

Nothing to see here, move on.

### **lo** - Lao

Nothing to see here, move on.
