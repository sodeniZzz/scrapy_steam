# scrapy_steam

Парсим [Steam](https://store.steampowered.com/) с помощью Scrapy!

По запросам "simulator", "cities", "zombie" [вытащены все игры на первых 2 страницах.](https://github.com/sodeniZzz/scrapy_steam/blob/main/items.json)

Для запуска **python3 -m scrapy crawl SteamProductSpider -o items.json** 