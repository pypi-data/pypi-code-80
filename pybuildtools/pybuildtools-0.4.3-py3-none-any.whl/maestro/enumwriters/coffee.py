'''
CoffeeScript enum writer

Copyright (c) 2015 - 2021 Rob "N3X15" Nelson <nexisentertainment@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

'''
from buildtools.indentation import IndentWriter
from .enumwriter import EnumWriter

class CoffeeEnumWriter(EnumWriter):
    def __init__(self):
        super().__init__()

    def write(self, w, definition):
        coffeedef = definition.get('coffee',{})
        if coffeedef.get('export', False):
            self.writeForExport(w, definition)
        else:
            self.writeStandard(w, definition)

    def writeStandard(self, w, definition):
        name = definition['name']
        default = definition['default']
        coffeedef = definition.get('coffee',{})

        w.write('\n###')
        if 'notes' in definition:
            for line in definition['notes'].split('\n'):
                w.write('\n# {}'.format(line))
        w.write('\n# @enumdef: {}'.format(definition['name']))
        w.write('\n###')
        w.write('\nclass {}'.format(definition['name']))

        w.write('\n  @_DEFAULT: {}'.format(default))
        w.write('\n  @_ERROR: -1')

        if definition.get('flags', False):
            w.write('\n  @NONE: 0')

        for k,vpak in definition['values'].items():
            v=self._get_value_for(vpak)
            meaning=self._get_meaning_for(vpak)
            padding = '\n  '
            if meaning != '':
                w.write('{PAD}###{PAD}# {MEANING}{PAD}###'.format(PAD=padding, MEANING=meaning))
            w.write('\n  @{}: {}'.format(k,repr(v)))

        if definition.get('flags', False):
            w.write('\n\n  @ValueToStrings: (val) ->')
            w.write('\n    o=[]')
            w.write('\n    for bitidx in [0...{}]'.format(len(definition['values'].keys())))
            w.write('\n      switch((1 << bitidx) & val)')
            written=[]
            for k,vpak in definition['values'].items():
                v=self._get_value_for(vpak)
                if v in written:
                    continue
                written+=[v]
                w.write('\n        when {}'.format(repr(v)))
                w.write('\n          o.push {}'.format(repr(k)))
            w.write('\n    return o')

            w.write('\n\n  @StringsToValue: (valarr) ->')
            w.write('\n    o=0')
            w.write('\n    for flagname in valarr')
            w.write('\n      o |= @StringToValue flagname')
            w.write('\n    return o')

        w.write('\n\n  @ValueToString: (val, sep=", ", start_end="") ->')
        if definition.get('flags', False):
            w.write('\n    o = @ValueToStrings(val).join(sep)')
        else:
            w.write('\n    o=null')
            w.write('\n    switch(val)')
            written=[]
            for k,vpak in definition['values'].items():
                v=self._get_value_for(vpak)
                if v in written:
                    continue
                written+=[v]
                w.write('\n      when {}'.format(repr(v)))
                w.write('\n        o = {}'.format(repr(k)))

        w.write('\n    if start_end.length == 2')
        w.write('\n      o = start_end[0]+o+start_end[1]')
        w.write('\n    return o\n')

        w.write('\n  @StringToValue: (key) ->')
        w.write('\n    switch(key)')
        written=[]
        for k,vpak in definition['values'].items():
            if k in written:
                continue
            written+=[k]
            v=self._get_value_for(vpak)
            w.write('\n      when {}'.format(repr(k)))
            w.write('\n        return {}'.format(repr(v)))
        w.write('\n    return -1;\n')


        w.write('\n  @Keys: ->')
        w.write('\n    return [{}]\n'.format(', '.join([repr(x) for x in definition['values'].keys()])))

        w.write('\n  @Values: ->')
        w.write('\n    return [{}]\n'.format(', '.join([repr(self._get_value_for(x)) for x in definition['values'].values()])))

        w.write('\n  @Count: ->')
        w.write('\n    return {}\n'.format(len(definition['values'].keys())))

        if not definition.get('flags', False):
            w.write('\n  @Min: ->')
            w.write('\n    return {!r}\n'.format(min([self._get_value_for(x) for x in definition['values'].values()])))
            w.write('\n  @Max: ->')
            w.write('\n    return {!r}\n'.format(max([self._get_value_for(x) for x in definition['values'].values()])))
        else:
            allofem=0
            for x in definition['values'].values():
                allofem |= self._get_value_for(x)
            w.write('\n  @All: ->')
            w.write('\n    #  b{0:032b}'.format(allofem))
            w.write('\n    # 0x{0:0X}'.format(allofem))
            w.write('\n    return {}\n'.format(allofem))

    def writeForExport(self, _w, definition) -> None:
            name = definition['name']
            coffeedef = definition.get('coffee',{})
            w = IndentWriter(_w)
            w.writeline('# @generated')
            with w.writeline('export default class {}'.format(name)):
                self._writeStaticConst(w, '__default', definition.get('default',0))
                if definition.get('flags', False):
                    self._writeStaticConst(w, 'NONE', 0)

                if not definition.get('flags', False):
                    self._writeStaticConst(w, '_MIN', min([self.parent._get_value_for(x) for x in definition['values'].values()]))
                    self._writeStaticConst(w, '_MAX', max([self.parent._get_value_for(x) for x in definition['values'].values()]))
                else:
                    allofem=0
                    for x in definition['values'].values():
                        allofem |= self.parent._get_value_for(x)
                    w.writeline( '###')
                    w.writeline(f'#  b{allofem:032b}')
                    w.writeline(f'# 0x{allofem:0X}')
                    w.writeline( '###')
                    self._writeStaticConst(w, 'ALL', allofem)

                for k,vpak in definition['values'].items():
                    v=self.parent._get_value_for(vpak)
                    meaning=self.parent._get_meaning_for(vpak)
                    if meaning and len(meaning) > 0:
                        w.writeline( '###')
                        w.writeline(f'# {meaning}')
                        w.writeline( '###')
                    self._writeStaticConst(w, k, v)

                if definition.get('flags',False):
                    with w.writeline('@ValueToStrings: (val) ->'):
                        w.writeline('o = []')
                        with w.writeline('for bitidx in [0...32]'):
                            with w.writeline('switch (val&(1<<bitidx))'):
                                for k,vpak in definition['values'].items():
                                    v=self.parent._get_value_for(vpak)
                                    with w.writeline(f'when {v!r}'):
                                        w.writeline(f'o.push {k!r}')
                        w.writeline('return o')

                with w.writeline('@ValueToString: (val, sep=",", start_end="") ->'):
                    if not definition.get('flags', False):
                        w.writeline('o = null')
                        with w.writeline('switch (val)'):
                            for k, vpak in definition['values'].items():
                                v=self.parent._get_value_for(vpak)
                                with w.writeline(f'when {v!r}'):
                                    w.writeline(f'o = {k!r}')
                    else:
                        w.writeline(f'o = @ValueToStrings(val).join(sep)')

                    with w.writeline('if start_end.length == 2'):
                        w.writeline('o = start_end.charAt(0) + o + start_end.charAt(1)')
                    w.writeline('return o')


                with w.writeline('@StringToValue: (key) ->'):
                    with w.writeline('switch(key)'):
                        for k,vpak in definition['values'].items():
                            v=self.parent._get_value_for(vpak)
                            with w.writeline(f'when {k!r}'):
                                w.writeline(f'return {v!r}')
                    w.writeline('return -1')


                with w.writeline('@Keys: ->'):
                    w.writeline('return [{}]'.format(', '.join([repr(x) for x in definition['values'].keys()])))

                with w.writeline('@Values: ->'):
                    w.writeline('return [{}]'.format(', '.join([repr(self.parent._get_value_for(x)) for x in definition['values'].values()])))

                with w.writeline('@Count: ->'):
                    w.writeline('return {}'.format(len(definition['values'].keys())))
