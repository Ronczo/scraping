import scrapy


class SpiderUWM(scrapy.Spider):
    name = "spider-uwm"
    start_url = "http://wmii.uwm.edu.pl/ogloszenia"
    no_allowed_chars = [".pdf", ".docx", "mailto", ".."]

    def start_requests(self):
        yield scrapy.Request(url=self.start_url, callback=self.parse)

    def parse(self, response, **kwargs):
        all_links = response.css("div.view-content a")
        for link in all_links:
            url = link.css("::attr(href)").get()
            if self._is_valid_url(url):
                date = link.css("div.views-field-created::text").get()
                response.meta["date"] = date
                yield response.follow(url=url, callback=self.scrape_announcement, meta=response.meta)
        if next_page_url := response.css("a[title='Przejdź do następnej strony']::attr(href)").get():
            yield response.follow(url=next_page_url, callback=self.parse)

    def scrape_announcement(self, response):
        source_url = response.url
        title = response.css("h1.page-title::text").get()
        content = response.xpath("string(//div[contains(@class, 'node__content')])").get()
        yield {
            "title": title,
            "content": content,
            "source_url": source_url,
            "date": response.meta.get("date")
        }

    def _is_valid_url(self, url):
        if url:
            is_not_document = not any(char in url for char in self.no_allowed_chars)
            proper_domain = True
            if url.startswith("http") and not url.startswith("http://wmii.uwm.edu.pl"):
                proper_domain = False
            return all([is_not_document, proper_domain])
