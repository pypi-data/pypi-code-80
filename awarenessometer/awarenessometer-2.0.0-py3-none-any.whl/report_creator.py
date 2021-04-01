import os
from datetime import date
from typing import Dict, Union

from mako.lookup import TemplateLookup

from awarenessometer.labeled_study import LabeledStudy
from awarenessometer.pre_post_study import PrePostStudy

LANGUAGE = os.environ['LANG'].split('.')[0]
if LANGUAGE not in ['de_DE', 'en_US']:
    LANGUAGE = 'en_US'


class ReportCreator:
    def __init__(self, out_file: str):
        self.out_file = out_file
        self.template_names = {
            'pre-post': f'pre_post_template_{LANGUAGE}.md',
            'labeled': f'labeled_template_{LANGUAGE}.md'
        }

    def create_study_report(self, study: Union[LabeledStudy, PrePostStudy], author: str) -> None:
        templates_path = os.path.join(os.path.dirname(__file__), 'templates')

        study.create_plots()
        study_tokens = study.create_tokens()
        extra_tokens = {'author': author, 'date': date.today().isoformat()}
        tokens = {**study_tokens, **extra_tokens}
        template_name = self.template_names[study.type]
        rendered = self._render_report(template_name, templates_path, tokens)
        final_text = rendered.replace(r'\##', '##')
        with open(self.out_file, 'w') as stream:
            stream.writelines(final_text)

    @staticmethod
    def _render_report(filename: str, templates_path: str, tokens: Dict) -> str:
        template_lookup = TemplateLookup(directories=[templates_path])
        tpl = template_lookup.get_template(filename)
        return tpl.render(**tokens)
