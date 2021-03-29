# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 15:58:36 2020

@author: U550787
"""

import numpy as np
from matplotlib import pyplot as plt
from copy import deepcopy
import sys
#import scipy.stats as s Possible to integrate a minimization of the test plan parameter

if float(sys.version[:3])  >= 3.7 :
    from .Sample import Sample 
    from .TestSample import TestSample
    from .DataTreatment import DataTreatment
else:
    from Sample import Sample 
    from TestSample import TestSample
    from DataTreatment import DataTreatment
    
class PlanEfficiency:
    """
        Testing efficience of one test plan by multiple repetitions.
    
        Parameters
        ----------
        
        sample : Sample instance
            Add sample to the test plan
        
        test : TestSample instance
            Add test method to the test plan
        
        data_treatment : Datatreament instance
            Add the data treatment to the test plan    
            
        n : int
            Number of the define plan test (by the sample, test, and data_treatment) repetition. Accuracy will 
        
        
        Raises
        ----------
        ValueError
            Parameter 'sample' is missing or incorrect. Please enter a Sample instance, for further information go to help(Sample).
        
        ValueError
            Parameter 'test' is missing or incorrect. Please enter a TestSample instance, for further information go to help(TestSample).
        
        ValueError
            Parameter 'data_treatment' is missing or incorrect. Please enter a DataTreatment instance, for further information go to help(DataTreatment).
        
            
        Methods
        ----------
        exec_testplan_efficiency(self)
        indicators_calculation(self)
        update(self, result="models")
        efficiency_visualization(self)
        
    """
    
    
    def __init__(self, **kwargs):
        
        self.GRAPH = True
        
        self.Sample = kwargs.get("sample", None)
        self.TestSample = kwargs.get("test", None)    
        self.DataTreatment = kwargs.get("data_treatment", None)
        
        self.n = kwargs.get("n", 1)
        
        self.estimation_result_efficiency = {"Normal":{}, "Lognormal":{}, "Weibull":{}, "Exponential":{}}
        
        try:
            if not self.Sample and not isinstance(self.Sample, Sample):
                raise ValueError("Parameter 'sample' is missing or incorrect. Please enter a Sample instance, for further information go to help(Sample).")
        except:
            if not self.Sample and not Sample.__name__ in str(type(Sample)):
                raise ValueError("Parameter 'sample' is missing or incorrect. Please enter a Sample instance, for further information go to help(Sample).")
    
        try:
            if not self.TestSample and not isinstance(self.TestSample, TestSample):
                raise ValueError("Parameter 'test' is missing or incorrect. Please enter a Sample instance, for further information go to help(TestSample).")
        except:
            if not self.TestSample and not TestSample.__name__ in str(type(TestSample)):
                raise ValueError("Parameter 'test' is missing or incorrect. Please enter a Sample instance, for further information go to help(TestSample).")
                
        try:
            if not self.DataTreatment and not isinstance(self.DataTreatment, DataTreatment):
                raise ValueError("Parameter 'data_treatment' is missing or incorrect. Please enter a DataTreatment instance, for further information go to help(DataTreatment).")
        except:
            if not self.DataTreatment and not DataTreatment.__name__ in str(type(DataTreatment)):
                raise ValueError("Parameter 'data_treatment' is missing or incorrect. Please enter a DataTreatment instance, for further information go to help(DataTreatment).")
    
        #Desactivate graphical visualization
        self.Sample.GRAPH = False
        self.TestSample.GRAPH = False
        self.DataTreatment.GRAPH = False
        
        self.exec_testplan_efficiency()
        
    def exec_testplan_efficiency(self):
        """
        Main purpose is to repeat the test plan define the first n times, to statistical construe the efficiency of the methods used.
        Mean, standard deviation and variance will be efficiency indicators
        """
        
        #Compute data treatments n times
        self.treatment = [ (lambda x: self.update())(i) if i!=0 else self.DataTreatment.estimation_result for i in range(self.n) ]
        
        self.indicators_calculation()
        
        if self.GRAPH:
            self.efficiency_visualization()
        
    def indicators_calculation(self):
        """
        Compute efficiency indicators
        Mean, standard deviation and variance
        """
            
        #Take each estimation dictionary
        for i, estimation_dict in enumerate(self.treatment):
        
            for m in ["Normal", "Lognormal", "Exponential", "Weibull"]:
                
                if estimation_dict[m] != {}:
                    
                    #For each data treatment result we will calculate the progressive mean, standard variation and variance. 
                    #Example : i = 2  the indicator will be calculate with values 3 values between 0 and 2
                    for name, value in estimation_dict[m].items():
                                    
                        if i==0:
                            self.estimation_result_efficiency[m][name] = {"mean" : [value], "std" : [value], "var" : [value] }
                                
                        else:
                            
                            for indicator in ["mean", "std", "var"]:
                                        
                                temp = self.estimation_result_efficiency[m][name][indicator] + [value]
                                        
                                if indicator == "mean":
                                    self.estimation_result_efficiency[m][name][indicator] += [np.mean(temp)]
                                elif indicator == "std":
                                    self.estimation_result_efficiency[m][name][indicator] += [np.std(temp)]
                                else:
                                    self.estimation_result_efficiency[m][name][indicator] += [np.var(temp)]
                            
    
    def update(self):
        """
        Generate new randoms value following the define Sample instance, re-run the TestSample instance and calculate the new estimation model
        """
        
        self.Sample.exec_sample()
        self.TestSample.exec_test()
        self.DataTreatment.exec_treatment()
        
        #Need to deepcopy the object to make a new object with a new memory adress reference (if not the values will be the same as the last one)
        return deepcopy(self.DataTreatment.estimation_result) 
        
    def efficiency_visualization(self):
        
        ncols = sum([1 for m in ["Normal", "Lognormal", "Exponential", "Weibull"] if self.estimation_result_efficiency[m] != {}])
        
        nrows = len(self.estimation_result_efficiency["Weibull"].values())
        
        fig, axs = plt.subplots(nrows, ncols)
    
        for i, (law, estimation) in enumerate(self.estimation_result_efficiency.items()):
            
            if estimation != {}:
                
                x = np.arange(1, self.n+1, step=1)
                
                for j, (name, value) in enumerate(estimation.items()):
                    
                    for k, indicator in enumerate(["mean", "std", "var"]):
                        axs[j, i].plot(x, value[indicator], color=["red", "green", "blue"][k], label="{} {}".format(name, indicator))
                    
                    axs[j, i].set_title("{} efficiency indocators".format(name))
                    axs[j, i].set_ylabel("Repetition number")
        
        fig.tight_layout() 
        plt.show()
        
        
class TestPlanEfficiency:
    """
        Test Class tests
        Created to test, debug and integrate the PlanEfficiency
    
        Parameters
        ----------
        
        n : int
            Number of the repetetion wanted to our test plan
        
        Raises
        ----------
 
        Methods
        ----------

    """
    def __init__(self, n):
        
        
        self.n = n 
        
        
    def functionnal_test_1(self):
        """
        First test with a sample represent by a Weibull law, a zero failure test and a Johnson rank post data treatment
        """
        
        sample = Sample(name="TestPlanEfficiency",size=10,representation="Random_variates", law="Weibull", scale=19000, param1=1.3)
        test = TestSample(life_objective=20000,sample=sample, test_type="Zero_failure")
        treatment = DataTreatment(method="Johnson_rank", test_result=test)
        
        self.test_plan = PlanEfficiency(sample=sample, test=test, data_treatment=treatment, n=self.n)
        #self.test_plan.efficiency_visualization()
    
    
    def test_testingefficiency_class_algorithm(self):
        """
        Test the algorithm of the TestingEfficiency Class
        Each times we need to update all the Class and check if the ufond dépdate work correctly
        """
        self.t = {"estimation_result": []}
        self.sample = Sample(name="TestPlanEfficiency",size=10, representation="Random_variates", law="Weibull", scale=19000, param1=1.3)
        self.test =  TestSample(life_objective=20000,sample=self.sample, test_type="Zero_failure")
        self.treatment = DataTreatment(method="Johnson_rank", test_result=self.test)
        print(self.sample.sample)
        print(self.test.result)
        print(self.treatment.estimation_result)
        print("----------------\n END FIRST SAMPLES \n----------------")
        self.sample.exec_sample()
        self.test.exec_test()
        self.treatment.exec_treatment()
        print(self.sample.sample)
        print(self.test.result)
        print(self.treatment.estimation_result)
        self.t["estimation_result"].append(deepcopy(self.treatment.estimation_result))
        print("----------------\n END SECOND SAMPLES \n----------------")
        self.sample.exec_sample()
        self.test.exec_test()
        self.treatment.exec_treatment()
        print(self.sample.sample)
        print(self.test.result)
        print(self.treatment.estimation_result)
        print("----------------\n END\n----------------")
        self.t["estimation_result"].append(deepcopy(self.treatment.estimation_result))
        print(self.t)
        
        
    
if __name__ == "__main__": 
    
    test = TestPlanEfficiency(20)
