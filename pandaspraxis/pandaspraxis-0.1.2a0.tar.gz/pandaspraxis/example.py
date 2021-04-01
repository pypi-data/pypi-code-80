import ipywidgets as widgets
from traitlets import Unicode
from .Translator import *

# See js/lib/example.js for the frontend counterpart to this file.

@widgets.register
class PandasPraxis(widgets.DOMWidget):
    """An example widget."""

    # Name of the widget view class in front-end
    _view_name = Unicode('HelloView').tag(sync=True)

    # Name of the widget model class in front-end
    _model_name = Unicode('HelloModel').tag(sync=True)

    # Name of the front-end module containing widget view
    _view_module = Unicode('pandaspraxis').tag(sync=True)

    # Name of the front-end module containing widget model
    _model_module = Unicode('pandaspraxis').tag(sync=True)

    # Version of the front-end module containing widget view
    _view_module_version = Unicode('^0.1.2').tag(sync=True)
    # Version of the front-end module containing widget model
    _model_module_version = Unicode('^0.1.2').tag(sync=True)

    # Widget specific property.
    # Widget properties are defined as traitlets. Any property tagged with `sync=True`
    # is automatically synced to the frontend *any* time it changes in Python.
    # It is synced back to Python from the frontend *any* time the model is touched.
    value = Unicode('SELECT a FROM z').tag(sync=True)

    def __init__(self, **kwargs):
        super(PandasPraxis, self).__init__(**kwargs)
        self.on_msg(self.handle_event)

    def handle_event(self, _, content, buffers):
        message = content.get('message', '')
        try:
            translation_list = translate_real(message)
            translation_html = self.create_result(translation_list)
        except KeyError as e: 
            translation_html = str(e)
            
        self.send({'msg': translation_html})

    def create_result(self, translation_list):
        explanations = [] # explanations for each line are stored in a separate div;
        lines = []        # they stay above the table that holds the lines 

        for i, line in enumerate(translation_list):
            if 'other_options' in line:
                explanations.append(self.explanation(i, line))
                lines.append(self.create_or_line(i, line))
            else:
                lines.append(self.create_not_or_line(i, line))
        return ''.join(explanations) + '<table id="pp-response-table"><tbody>' + ''.join(lines) + '</tbody></table>'

    def explanation(self, i, line):
        return '''<div class="pp-line-exp" id="pp-line-exp-{0}">
                    Alternative: <br>
                    <span class="code" id="pp-line-alt-{0}">{1}</span> <br>
                    {2} (click to switch!)
                </div>'''.format(i, ', '.join(line['other_options']), line['tooltip'])

    def create_not_or_line(self, i, line):
        item = line['first_choice'] # only one choice
        return '''<tr>
                    <td></td>
                    <td>
                        <span class="code" id="pp-line-{0}" data-pos1="[{1}, {2}]" data-pos2='"*"'
                            onmouseover="pair_emphasize('pp-line-{0}', 'pp-query', 'pp-line-{0}', 'pp-highlight')" 
                            onmouseout="pair_deemphasize('pp-line-{0}', 'pp-query', 'pp-line-{0}', 'pp-highlight')">{3}</span>
                    </td>
                </tr>'''.format(i, item.column-1, item.end_column-1, item)

    def create_or_line(self, i, line):
        item = line['first_choice']
        other_item = line['other_options'][0] # assuming only one other option
        return '''<tr>
                    <td><i class="far fa-question-circle pp-or-button" 
                        id="pp-line-switch-{0}" data-pos1='[{1}, {2}]' data-pos2='[{3}, {4}]'
                        onmouseover="open_sidebar({0});pair_emphasize('pp-line-switch-{0}', 'pp-line-{0}', 'pp-below-txt-{0}', 'pp-box')" 
                        onmouseout="close_sidebar({0});pair_deemphasize('pp-line-switch-{0}', 'pp-line-{0}', 'pp-below-txt-{0}', 'pp-box')"
                        onclick="pair_deemphasize('pp-line-switch-{0}', 'pp-line-{0}', 'pp-below-txt-{0}', 'pp-box');
                        switch_or({0});pair_emphasize('pp-line-switch-{0}', 'pp-line-{0}', 'pp-below-txt-{0}', 'pp-box')">
                    </i></td>
                    <td>
                        <div class="pp-or code" id="pp-line-{0}" data-or="{7}" 
                        data-pos1='[{5}, {6}]' data-pos2='"*"'
                        onmouseover="pair_emphasize('pp-line-{0}', 'pp-query', 'pp-line-{0}', 'pp-highlight')" 
                        onmouseout="pair_deemphasize('pp-line-{0}', 'pp-query', 'pp-line-{0}', 'pp-highlight')">{8}
                        </div>
                    </td>
                </tr>
                <tr class="pp-below code" id="pp-below-{0}">
                    <td></td>
                    <td id="pp-below-txt-{0}">{7}</td>
                </tr>'''.format(i, item.pos_in_stream, item.end_pos, other_item.pos_in_stream, other_item.end_pos, 
                        item.column-1, item.end_column-1, ', '.join(line['other_options']), item)

                        #id="pp-line-switch-{0}" data-pos1="[{1}, {2}]" data-pos2='[{3}, {4}]'
                        
                        #data-pos1="[{5}, {6}]" data-pos2='"*"'