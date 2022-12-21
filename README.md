# examtopics_scraper
![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/aserpi/examtopics_scraper)
![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/aserpi/examtopics_scraper/package.yml)
![Python version](https://img.shields.io/badge/python-v3.10+-blue)

_examtopics_scraper_ is a simple scraper for question discussions on ExamTopics.

```
usage: examtopics_scraper [-h] [-e EXAM] [-o OUTPUT] [-v] provider

positional arguments:
provider                    exam provider

options:
-h, --help                  show this help message and exit
-e EXAM, --exam EXAM        exam code
-o OUTPUT, --output OUTPUT  output path for question discussions
-v, --verbose               enable debug logging
```

If an output path is provided, the module creates an HTML file with the question discussions.
The option is not supported when scraping exam codes.
