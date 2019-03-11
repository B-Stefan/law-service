import re
from typing import Dict, List

import scrapy

from law.crawler.text_analysis.keywords import get_keywords
from law.service.law_service import LawService

from law.models.domain import Law, LawParagraph, TextParagraph
from law.utils import get_neo4j_driver_instance


class LawCrawler(scrapy.Spider):
    db_service = LawService(get_neo4j_driver_instance())
    laws: Dict[str, Law] = {}
    name = 'law_crawler'
    start_urls = ['https://www.gesetze-im-internet.de/bgb/']
    allowed_domains = ["www.gesetze-im-internet.de", "gesetze-im-internet.de"]

    def get_law(self, response) -> Law:

        parts = response.request.url.split("/")

        if len(parts) < 4:
            raise RuntimeError("Can't find law descriptions url format wrong")

        return Law(id=parts[3])

    def get_law_paragraph(self, response):

        law_sec = response.css('h1 > span::text').extract()

        if len(law_sec) is not 2:
            return None

        number = law_sec[0].strip().replace(" ", "")
        return LawParagraph(name=law_sec[1], number=number)

    def get_text_paragraphs(self, response):
        text_parts = response.css(".jurAbsatz::text").extract()

        texts: list(TextParagraph) = []
        for line in text_parts:

            match = re.search('^\(([0-9]+)\).(.*)', line)
            if match:
                number = match.group(1)
                text = match.group(2)
                texts.append(TextParagraph(number=number, text=text))
            else:
                print("Not found" + line)
                texts.append(TextParagraph(text=line, number=None))

        return texts

    def get_keywords(self, response) -> List[str]:
        text_parts = response.css(".jurAbsatz::text").extract()
        text = '.'.join(text_parts)
        return get_keywords(text)

    def parse(self, response):
        try:
            new_law = self.get_law(response)
            law = self.laws.get(new_law.id, None)
            if law is None:
                self.laws.update({new_law.id: new_law})

            law_paragraph = self.get_law_paragraph(response)
            keywords = self.get_keywords(response)

            if law_paragraph is not None:
                law.add_law_paragraph(law_paragraph)

                texts = self.get_text_paragraphs(response)

                law_paragraph.add_text_paragraphs(texts)
                for text in texts:
                    self.db_service.merge_text_paragraph(text)
            self.db_service.merge_keywords(law_paragraph, keywords)

        except Exception as e:
            print(e)

        # Scrape all pages
        for next_page in response.css('a[href]::attr(href)'):
            relative_url = next_page.extract()
            absolute_url = response.urljoin(relative_url)
            print("Visited: %s", absolute_url)
            yield response.follow(next_page, self.parse)
