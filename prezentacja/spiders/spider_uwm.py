import scrapy


class SpiderUWM(scrapy.Spider):
    name = "spider-uwm-test"
    start_url = "http://wmii.uwm.edu.pl/ogloszenia"
    no_allowed_chars = [".pdf", ".docx", "mailto", ".."]

    # def start_requests(self):

    # def parse():

    # def scrape_announcement(self, response):

    # yield {
    #     "title": title,
    #     "content": content,
    #     "source_url": source_url,
    # }

    def _is_valid_url(self, url):
        if url:
            is_not_document = not any(char in url for char in self.no_allowed_chars)
            proper_domain = (
                True
                if url.startswith("http")
                and not url.startswith("http://wmii.uwm.edu.pl")
                else False
            )
            return is_not_document and proper_domain
