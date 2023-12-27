import scrapy
from urllib.parse import urlencode
from spider_steam.items import SpiderSteamItem

queries = ["simulator", "cities", "zombie"]


class SteamproductspiderSpider(scrapy.Spider):
    name = "SteamProductSpider"
    allowed_domains = ["store.steampowered.com"]
    domain_url = "https://store.steampowered.com/"

    def start_requests(self):
        for query in queries:
            for page in ["1", "2"]:
                url = (
                    self.domain_url
                    + "search/?"
                    + urlencode(
                        {"term": query, "ndl": 1, "ignore_preferences": 1, "page": page}
                    )
                )
                yield scrapy.Request(url=url, callback=self.parse_keyword_response)

    def parse_keyword_response(self, response):
        game_links = response.css("a.search_result_row::attr(href)").extract()
        for link in game_links:
            if "agecheck" not in link:
                yield scrapy.Request(url=link, callback=self.parse)

    def parse(self, response):
        items = SpiderSteamItem()
        name = response.xpath('//div[@id="appHubAppName"]//text()').extract()
        category = response.xpath('//div[@class="blockbg"]/a/text()').extract()
        reviews_amount = response.xpath(
            '//input[@id="review_summary_num_reviews"]/@value'
        ).get()
        total_review_grade = response.xpath(
            '//span[starts-with(@class, "game_review_summary")]/text()'
        ).get()
        release_date = response.xpath('//div[@class="date"]/text()').extract()
        developer = response.xpath('//div[@id="developers_list"]/a/text()').extract()
        tags = response.xpath(
            '//div[@class="glance_tags popular_tags"]/a/text()'
        ).extract()
        price = response.xpath(
            '//div[@class="game_purchase_price price"]/text()'
        ).extract()
        platforms = response.xpath('//div[@class="sysreq_tabs"]/div/text()').extract()

        items["name"] = "".join(name)
        items["category"] = "/".join(category[1:])
        items["reviews_amount"] = reviews_amount
        items["total_review_grade"] = total_review_grade
        items["release_date"] = "".join(release_date)
        items["developer"] = ", ".join(developer)
        items["tags"] = ", ".join([tag.strip() for tag in tags])

        if not price:
            items["price"] = "Not available now"
        else:
            items["price"] = price[0].strip()

        if not platforms:
            items["platforms"] = "Windows"
        else:
            items["platforms"] = ", ".join([platform.strip() for platform in platforms])

        if release_date:
            release_year = release_date[0].split()[-1]
            if name != "" and release_year > "2000":
                yield items
