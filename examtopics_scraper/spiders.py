import re

import scrapy


class ExamtopicsExamsSpider(scrapy.Spider):
    name = "examtopics_exams"

    def __init__(self, provider, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.provider = provider
        self.start_urls = [f"https://www.examtopics.com/exams/{self.provider}/"]

    def parse(self, response, **kwargs):
        for exam in response.css("a.popular-exam-link"):
            yield {
                "code": exam.css("span.popular-exam-code::text").extract_first(),
                "name": exam.xpath("text()").extract_first(),
            }


class ExamtopicsQuestionsSpider(scrapy.Spider):
    name = "examtopics_questions"

    def __init__(self, provider, exam, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.exam = exam
        self.provider = provider
        self.discussion_regex = re.compile(fr"Exam {self.exam} (.*) question (\d+)", re.IGNORECASE)
        self.start_urls = [f"https://www.examtopics.com/discussions/{self.provider}/"]

    def parse(self, response, **kwargs):
        for question in response.css("a.discussion-link"):
            if match := re.search(self.discussion_regex, question.css("::text").extract_first()):
                yield {
                    "question": int(match.group(2)),
                    "topic": match.group(1),
                    "url": response.urljoin(question.attrib["href"]),
                }
        if next_page := response.css("span.pagination-nav>a.btn.btn-sm"):
            yield from response.follow_all(next_page, callback=self.parse)
