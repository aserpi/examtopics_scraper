import scrapy


class ExamtopicsExamsSpider(scrapy.Spider):
    name = "examtopics_exams"

    def __init__(self, provider, *args, **kwargs):
        super().__init__(*args, **kwargs)
        raise NotImplementedError


class ExamtopicsQuestionsSpider(scrapy.Spider):
    name = "examtopics_questions"

    def __init__(self, provider, exam, *args, **kwargs):
        super().__init__(*args, **kwargs)
        raise NotImplementedError
