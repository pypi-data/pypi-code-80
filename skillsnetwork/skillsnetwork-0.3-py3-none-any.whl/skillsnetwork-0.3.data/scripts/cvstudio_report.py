#!python

from datetime import datetime
import skillsnetwork.cvstudio

cvstudio = skillsnetwork.cvstudio.CVStudio()

start_datetime = datetime.now()
end_datetime = datetime.now()
accuracy_list = [0,1,0]
loss_list = [0.5,0.5,0.5]

result = cvstudio.report(start_datetime, end_datetime, { 'accuracy': accuracy_list, 'loss': loss_list })

if result.ok:
    print('Congratulations your results have been reported back to CV Studio!')
else:
    print('Failed to report results.')
