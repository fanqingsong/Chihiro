#! /bin/bash
echo $HOME
date

echo "sleep 60 s"
sleep 60

echo "send command to redis"
redis-cli -h redis -p 6379 lpush QuotesSpider:start_urls http://quotes.toscrape.com/

echo "now crawl"
poetry run scrapy crawl QuotesSpider



