

class StockGui(object):
    def __init__(self):
        import PySimpleGUI as sg
        self.sg = sg
        self.sg.theme('BlueMono')
        layout = [
            [self.sg.Button('Get Stock Data')],
            [self.sg.Button('Get Good Stocks')],
            [self.sg.Button('Markovitz Portfolio')],
        ]
        self.window = self.sg.Window('Suluoya Stock', layout)
        self.event, self.values = self.window.read()



    def MarkovitzGui(self):
        
        layout = [
            [self.sg.Text('Start Date'), self.sg.Input('2019-01-01')],

            [self.sg.Text(' End Date'), self.sg.Input('2020-01-01')],

            [self.sg.Text('Frequency'),
                self.sg.Radio('day', 'Frequency', default=True), 
                self.sg.Radio('week', 'Frequency', default=False), 
                self.sg.Radio('month', 'Frequency', default=False)],
            
            [self.sg.Text('Stock List')],
            [self.sg.Multiline('贵州茅台\n隆基股份\n五粮液')],

            [self.sg.Text('Holiday Mode')],
            [self.sg.Radio('open', 'Holiday Mode', default=False),
             self.sg.Radio('close', 'Holiday Mode', default=True)],

            [self.sg.Text('Holiday Name')],
            [self.sg.Combo(['国庆节', '中秋节', '春节'], default_value='春节')],

            [self.sg.Text('before')],
            [self.sg.Input('-21')],

            [self.sg.Text('after')],
            [self.sg.Input('21')],

            [self.sg.Text('risk-free interest rate (annually)')],
            [self.sg.Input('0.0185')],

            [self.sg.Text('Calculate Mode')],
            [self.sg.Radio('iteration algorithm', 'Calculate Mode', default=True),
                self.sg.Radio('generate scatters', 'Calculate Mode', default=False), ],

            [self.sg.Text('Scatter Number')],
            [self.sg.Input('500')],

            [self.sg.Button('Start work!')],
        ]

        window = self.sg.Window('Suluoya Markovitz', layout)

        event, values = window.read()
        names = values[5].split('\n')[:-1]
        start_date = values[0]
        end_date = values[1]

        if values[2]:
            frequency = 'd'
        if values[3]:
            frequency = 'w'
        if values[4]:
            frequency = 'm'

        if values[6]:
            holiday = True
        if values[7]:
            holiday = False

        holiday_name = values[8]

        before = values[9]
        after = values[10]

        no_risk_rate = float(values[11])

        if values[12]:
            accurate = True
        if values[13]:
            accurate = False

        number = values[14]

        window.close()

        try:
            from .Markovitz import Markovitz
        except:
            from Markovitz import Markovitz

        Markovitz = Markovitz(names=names,
                              start_date=start_date,
                              end_date=end_date,
                              frequency=frequency,
                              holiday=holiday,
                              holiday_name=holiday_name,
                              before=before, after=after,
                              no_risk_rate=no_risk_rate
                              )
        print(Markovitz.portfolio(accurate=accurate, number=number))

    def MarkovitzWork(self):
        if self.event == 'Markovitz Portfolio':
            self.window.close()
            self.MarkovitzGui()

    def StockDataGui(self):
        layout = [
            [self.sg.Text('Start Date'), self.sg.Input('2019-01-01',key='start_date')],

            [self.sg.Text(' End Date'), self.sg.Input('2020-01-01',key='end_date')],

            [self.sg.Text('Frequency'),
                self.sg.Radio('day', 'Frequency', default=True,key='day'), 
                self.sg.Radio('week', 'Frequency', default=False,key='week'), 
                self.sg.Radio('month', 'Frequency', default=False,key='month')],
            
            [self.sg.Text('Stock List')],
            [self.sg.Multiline('贵州茅台\n隆基股份\n五粮液',key='stock_list')],
            
            [self.sg.Text('Holiday Mode')],
            [self.sg.Radio('open', 'Holiday Mode', default=False,key='open'),
            self.sg.Radio('close', 'Holiday Mode', default=True,key='close')],

            [self.sg.Text('Holiday Name')],
            [self.sg.Combo(['国庆节', '中秋节', '春节'], default_value='春节',key='holiday')],

            [self.sg.Text('before')],
            [self.sg.Input('-21',key='before')],

            [self.sg.Text('after')],
            [self.sg.Input('21',key='after')],
            
            [self.sg.FolderBrowse('choose a folder to save data',key='path')],
            
            [self.sg.Button('Start work!')]
        ]
        window = self.sg.Window('Suluoya Stock Data', layout)
        values = window.read()[1]
        start_date = values['start_date']
        end_date = values['end_date']
        if values['day']:
            frequency = 'd'
        if values['week']:
            frequency = 'w'
        if values['month']:
            frequency = 'm'
        stock_list = values['stock_list'].split('\n')[:-1]
        path = values['path']
        
        
        
        #if values['close']:
        #    holiday=
        

if __name__ == '__main__':
    sg = StockGui()
    sg.StockDataGui()


