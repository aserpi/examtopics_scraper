class ExamtopicsExamsExportPipeline:
    def process_item(self, item, spider):
        raise NotImplementedError


class ExamtopicsQuestionsExportPipeline:
    def process_item(self, item, spider):
        raise NotImplementedError


def generate_questions_html_exporter(provider: str, exam: str, output: str):
    raise NotImplementedError
