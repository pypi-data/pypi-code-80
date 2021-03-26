#Test evaluate
#Test IoU
from .conftest import download_release
from deepforest import evaluate
from deepforest import main
from deepforest import get_data
import os
import pytest
import pandas as pd

@pytest.fixture()
def m(download_release):
    m = main.deepforest()
    m.use_release()
    
    return m
    
def test_evaluate_image(m):
    csv_file = get_data("OSBS_029.csv")
    predictions = m.predict_file(csv_file=csv_file, root_dir=os.path.dirname(csv_file))
    ground_truth = pd.read_csv(csv_file)
    
    result = evaluate.evaluate_image(predictions=predictions, ground_df=ground_truth, show_plot=True, root_dir=os.path.dirname(csv_file), savedir=None)     
        
    assert result.shape[0] == ground_truth.shape[0]
    assert sum(result.IoU) > 10 

def test_evaluate(m):
    csv_file = get_data("OSBS_029.csv")
    predictions = m.predict_file(csv_file=csv_file, root_dir=os.path.dirname(csv_file))
    ground_truth = pd.read_csv(csv_file)
    
    results = evaluate.evaluate(predictions=predictions, ground_df=ground_truth, show_plot=True, root_dir=os.path.dirname(csv_file), savedir=None)     
        
    assert results["results"].shape[0] == ground_truth.shape[0]
    assert results["box_recall"] > 0.5
    assert results["class_recall"].shape == (1,4)
    assert results["results"].true_label.unique() == "Tree"

def test_evaluate_multi(m):
    csv_file = get_data("testfile_multi.csv")
    m = main.deepforest(num_classes=2,label_dict={"Alive":0,"Dead":1})
    ground_truth = pd.read_csv(csv_file)
    
    results = evaluate.evaluate(predictions=ground_truth, ground_df=ground_truth, show_plot=True, root_dir=os.path.dirname(csv_file), savedir=None)     
        
    assert results["results"].shape[0] == ground_truth.shape[0]
    assert results["class_recall"].shape == (2,4)
    assert all(results['class_recall'].recall == pd.Series([1,1]))

#def test_evaluate_benchmark(m):
    #csv_file = "/Users/benweinstein/Documents/NeonTreeEvaluation/evaluation/RGB/benchmark_annotations.csv"
    #predictions = m.predict_file(csv_file=csv_file, root_dir=os.path.dirname(csv_file))
    #ground_truth = pd.read_csv(csv_file)
    
    #results = evaluate.evaluate(predictions=predictions, ground_df=ground_truth, show_plot=False, root_dir=os.path.dirname(csv_file), savedir=None)     
        
    #assert results["results"].shape[0] == ground_truth.shape[0]
    #assert results["class_recall"].shape == (2,4)