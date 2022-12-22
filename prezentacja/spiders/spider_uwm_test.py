import scrapy


class SpiderUWM(scrapy.Spider):
    name = "spider-uwm-test"
    start_url = "http://wmii.uwm.edu.pl/ogloszenia"

    def start_requests(self):
        yield scrapy.Request(url=self.start_url, callback=self.parse)

    def parse(self, response):
        all_links = response.css("div.view-content a")
        for link in all_links:
            url = link.css("::attr(href)").get()
            if self._is_valid_url(url):
                yield response.follow(url=url, callback=self.scrape_announcement)
        # paginacja
        if next_page_url := response.css(
            "a[title='Przejdź do następnej strony']::attr(href)"
        ).get():
            yield response.follow(url=next_page_url, callback=self.parse)

    def scrape_announcement(self, response):
        title = response.css("h1.page-title::text").get()
        # texts_list = response.css("div.node__content ::text").getall()
        # content = "\n".join(texts_list)
        content = response.xpath(
            "string(//div[contains(@class, 'node__content')])"
        ).get()
        source_url = response.url
        yield {
            "title": title,
            "content": content,
            "source_url": source_url,
        }

    @staticmethod
    def _is_valid_url(url):
        if url:
            no_allowed_chars = [".pdf", ".docx", "mailto", ".."]
            is_not_document = not any(char in url for char in no_allowed_chars)
            proper_domain = True
            if url.startswith("http") and not url.startswith("http://wmii.uwm.edu.pl"):
                proper_domain = False
            return all([is_not_document, proper_domain])
