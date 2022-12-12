import os

import itemadapter


class ScrapyPipeline:
    """Base Scrapy pipeline item."""

    def process_item(self, item, spider):
        raise NotImplementedError


class ExamtopicsExamsStdoutPipeline(ScrapyPipeline):
    """Stdout exporter for ExamTopics exams."""

    def process_item(self, item, spider):
        dict_item = itemadapter.ItemAdapter(item).asdict()
        print(f"{dict_item['code']}{dict_item['name']}")
        return item


class ExamtopicsQuestionsStdoutPipeline(ScrapyPipeline):
    """Stdout exporter for ExamTopics question discussions."""

    def process_item(self, item, spider):
        print(itemadapter.ItemAdapter(item).asdict()['url'])
        return item


def generate_questions_html_exporter(
        provider: str, exam: str, output: str | bytes | os.PathLike | int) -> type[ScrapyPipeline]:
    class ExamtopicsQuestionsHtmlPipeline(ScrapyPipeline):
        """HTML exporter for ExamTopics question discussions."""

        def __init__(self):
            self.questions = []

        def close_spider(self, spider):
            with open(output, "w") as out:
                print(f"<html><head><title>{provider} {exam}</title>"
                      "<style>table{border-collapse:collapse;font-family:Arial,Helvetica,sans-serif;width:100%}td,th{border:1px solid #ddd;padding:8px}table tr:nth-child(2n){background-color:#f2f2f2}table tr:hover{background-color:#ddd}table th{background-color:#0095eb;color:#fff;padding-bottom:12px;padding-top:12px;text-align:left}</style></head>"
                      f"<body><h1>{provider} {exam}</h1><table><"
                      f"tr><th>Topic</th><th>Question</th></tr>", file=out)
                for question in sorted(self.questions, key=lambda q: (q["topic"], q["question"])):
                    print(f'<tr><td>{question["topic"]}</td><td><a href="{question["url"]}" '
                          f'target="_blank">{question["question"]}</a></td></tr>', file=out)
                print("</table></body></html>", file=out)

        def open_spider(self, spider):
            self.questions = []

        def process_item(self, item, spider):
            # Cannot print one item at a time because questions are sorted
            self.questions.append(itemadapter.ItemAdapter(item).asdict())
            return item

    return ExamtopicsQuestionsHtmlPipeline
