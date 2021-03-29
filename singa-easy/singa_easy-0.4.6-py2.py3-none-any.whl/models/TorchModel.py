#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#

from __future__ import division
from __future__ import print_function
import sys
import base64
import abc
import tempfile
import json
from typing import Union, Dict, Optional, Any, List
import traceback
import io
# SINGA-AUTO Dependency

from singa_auto.model import CategoricalKnob, FixedKnob, utils, BaseModel
from singa_auto.model.knob import BaseKnob

# PyTorch Dependency
import torch
import torch.nn as nn
import torch.optim as optim
from torch.optim import lr_scheduler
from torch.autograd import Variable
from torch.utils.data import DataLoader

# Misc Third-party Machine-Learning Dependency
import sklearn.metrics
import numpy
import copy
import numpy as np
from PIL import Image
import matplotlib.cm as mpl_color_map
# singa_easy Modules Dependency
from singa_easy.modules.explanations.lime.lime import Lime
from singa_easy.modules.explanations.gradcam.gradcam import GradCam
from singa_easy.modules.mod_modelslicing.models import create_sr_scheduler, upgrade_dynamic_layers
from singa_easy.modules.mod_gmreg.gm_prior_optimizer_pytorch import GMOptimizer
from singa_easy.modules.mod_driftadapt import LabelDriftAdapter
from singa_easy.modules.mod_spl.spl import SPL
from singa_easy.modules.mod_mcdropout.mc_dropout import update_model
from singa_easy.datasets.TorchImageDataset import TorchImageDataset
# import nni
from datetime import datetime
import gc 
import base64

KnobConfig = Dict[str, BaseKnob]
Knobs = Dict[str, Any]
Params = Dict[str, Union[str, int, float, np.ndarray]]


class SINGAEasyModel(BaseModel):

    def __init__(self, **knobs: Knobs):
        super().__init__(**knobs)

    @abc.abstractmethod
    def local_explain(self, org_imgs, images, params: Params):
        raise NotImplementedError()


class TorchModel(SINGAEasyModel):
    """
    Implementation of PyTorch DenseNet
    """

    def __init__(self, **knobs):
        super().__init__(**knobs)
        self._knobs = knobs

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        # NOTE: should be dumped/loaded in dump_parameter/load_parameter
        self._image_size = 128

        # The following parameters are determined when training dataset is loaded
        self._normalize_mean = []
        self._normalize_std = []
        # self._num_classes = 2
        self.label_mapper = dict()

    def _create_model(self, scratch: bool, num_classes: int):
        raise NotImplementedError

    @staticmethod
    def get_knob_config():
        return {
            'model_class':CategoricalKnob(['TorchModel']),
            # Learning parameters
            'lr': FixedKnob(0.0001),  ### learning_rate
            'weight_decay': FixedKnob(0.0),
            'momentum':FixedKnob(0),
            'drop_rate': FixedKnob(0.0),
            'max_epochs': FixedKnob(1),
            'batch_size': CategoricalKnob([32]),
            'max_iter': FixedKnob(20),
            'optimizer': CategoricalKnob(['adam']),
            'scratch': FixedKnob(True),

            # Data augmentation
            'max_image_size': FixedKnob(32),
            'share_params': CategoricalKnob(['SHARE_PARAMS']),
            'tag': CategoricalKnob(['relabeled']),
            'workers': FixedKnob(8),
            'seed': FixedKnob(123456),
            'scale': FixedKnob(512),
            'horizontal_flip': FixedKnob(True),

            # Self-paced Learning and Loss Revision
            'enable_spl': FixedKnob(True),
            'spl_threshold_init': FixedKnob(16.0),
            'spl_mu': FixedKnob(1.3),
            'enable_lossrevise': FixedKnob(False),
            'lossrevise_slop': FixedKnob(2.0),

            # Label Adaptation
            'enable_label_adaptation': FixedKnob(True),

            # GM Prior Regularization
            'enable_gm_prior_regularization': FixedKnob(False),
            'gm_prior_regularization_a': FixedKnob(0.001),
            'gm_prior_regularization_b': FixedKnob(0.0001),
            'gm_prior_regularization_alpha': FixedKnob(0.5),
            'gm_prior_regularization_num': FixedKnob(4),
            'gm_prior_regularization_lambda': FixedKnob(0.0001),
            'gm_prior_regularization_upt_freq': FixedKnob(100),
            'gm_prior_regularization_param_upt_freq': FixedKnob(50),

            # Explanation
            'enable_explanation': FixedKnob(False),
            'explanation_gradcam': FixedKnob(True),
            'explanation_lime': FixedKnob(True),

            # Model Slicing
            'enable_model_slicing': FixedKnob(False),
            'model_slicing_groups': FixedKnob(0),
            'model_slicing_rate': FixedKnob(1.0),
            'model_slicing_scheduler_type': FixedKnob('randomminmax'),
            'model_slicing_randnum': FixedKnob(1),

            # MC Dropout
            'enable_mc_dropout': FixedKnob(False),
            'mc_trials_n': FixedKnob(10),
            'hidden_size': FixedKnob(512), ### nni
            'no_cuda':FixedKnob(False), ### nni
        }

    def get_peformance_metrics(self,
                               gts: np.ndarray,
                               probabilities: np.ndarray,
                               use_only_index=None):

        def compute_metrics_for_class(i):  # i for each pathology
            p, r, t = sklearn.metrics.precision_recall_curve(
                gts[:, i], probabilities[:, i])
            PR_AUC = sklearn.metrics.auc(r, p)
            ROC_AUC = sklearn.metrics.roc_auc_score(gts[:, i], probabilities[:, i])
            F1 = sklearn.metrics.f1_score(gts[:, i], preds[:, i])
            acc = sklearn.metrics.accuracy_score(gts[:, i], preds[:, i])
            count = np.sum(gts[:, i])
            return PR_AUC, ROC_AUC, F1, acc, count

        PR_AUCs = []
        ROC_AUCs = []
        F1s = []
        accs = []
        counts = []
        preds = probabilities >= 0.5

        classes = [use_only_index] if use_only_index is not None else range(
            self._num_classes)

        for i in classes:
            try:
                PR_AUC, ROC_AUC, F1, acc, count = compute_metrics_for_class(i)
            except ValueError:
                continue
            PR_AUCs.append(PR_AUC)
            ROC_AUCs.append(ROC_AUC)
            F1s.append(F1)
            accs.append(acc)
            counts.append(count)
            # print('Class: {:3d} Count: {:6d} PR AUC: {:.4f} ROC AUC: {:.4f} F1: {:.3f} Acc: {:.3f}'.format(i, count, PR_AUC, ROC_AUC, F1, acc))

        avg_PR_AUC = np.average(PR_AUCs)
        avg_ROC_AUC = np.average(ROC_AUCs, weights=counts)
        avg_F1 = np.average(F1s, weights=counts)

        # print('Avg PR AUC: {:.3f}'.format(avg_PR_AUC))
        # print('Avg ROC AUC: {:.3f}'.format(avg_ROC_AUC))
        # print('Avg F1: {:.3f}'.format(avg_F1))
        return avg_PR_AUC, avg_ROC_AUC, avg_F1, np.mean(accs)

    def train(self,
              dataset_path: str,
              shared_params: Optional[Params] = None,
              **train_args):
        """
        Overide BaseModel.train()
        Train the model with given dataset_path

        parameters:
            dataset_path: path to dataset_path
                type: str
            **kwargs:
                optional arguments

        return:
            nothing
        """
        torch.manual_seed(self._knobs.get("seed"))
        ''''''
        # print ('*********** dataset_path *************',dataset_path)
        # dataset_path='/hdd2/yangnan/Singa/aug-21/data/xray_train.zip'
        ''''''
        dataset = utils.dataset.load_dataset_of_image_files(
            dataset_path,
            min_image_size=32,
            max_image_size=self._knobs.get("max_image_size"),
            mode='RGB')
        self._normalize_mean, self._normalize_std = dataset.get_stat()
        # self._normalize_mean = [0.48233507, 0.48233507, 0.48233507]
        # self._normalize_std = [0.07271624, 0.07271624, 0.07271624]

        self._num_classes = dataset.classes
        self.label_mapper = dataset.label_mapper

        # construct the model
        self._model = self._create_model(scratch=self._knobs.get("scratch"), hidden_size=self._knobs.get("hidden_size"),
                                         num_classes=self._num_classes)
        if self._knobs.get("enable_mc_dropout"):
            self._model = update_model(self._model)

        if self._knobs.get("enable_model_slicing"):
            self._model = upgrade_dynamic_layers(
                model=self._model,
                num_groups=self._knobs.get("model_slicing_groups"),
                sr_in_list=[0.5, 0.75, 1.0])

        if self._knobs.get("enable_gm_prior_regularization"):
            self._gm_optimizer = GMOptimizer()
            for name, f in self._model.named_parameters():
                self._gm_optimizer.gm_register(
                    name,
                    f.data.cpu().numpy(),
                    model_name=self._knobs.get("model_class"),
                    hyperpara_list=[
                        self._knobs.get("gm_prior_regularization_a"),
                        self._knobs.get("gm_prior_regularization_b"),
                        self._knobs.get("gm_prior_regularization_alpha"),
                    ],
                    gm_num=self._knobs.get("gm_prior_regularization_num"),
                    gm_lambda_ratio_value=self._knobs.get(
                        "gm_prior_regularization_lambda"),
                    uptfreq=[
                        self._knobs.get("gm_prior_regularization_upt_freq"),
                        self._knobs.get(
                            "gm_prior_regularization_param_upt_freq")
                    ])

        if self._knobs.get("enable_spl"):
            self._spl = SPL()

        train_dataset = TorchImageDataset(sa_dataset=dataset,
                                          image_scale_size=self._image_size,
                                          norm_mean=self._normalize_mean,
                                          norm_std=self._normalize_std,
                                          is_train=True)
        train_dataloader = DataLoader(train_dataset,
                                      batch_size=self._knobs.get("batch_size"),
                                      shuffle=True)

        #Setup Criterion
        # print("self._num_classes is :   ", self._num_classes)

        self.train_criterion = nn.MultiLabelSoftMarginLoss(
        )  ### type(torch.FloatTensor)

        #Setup Optimizer
        if self._knobs.get("optimizer") == "adam":
            optimizer = optim.Adam(filter(lambda p: p.requires_grad,
                                          self._model.parameters()),
                                   lr=self._knobs.get("lr"),
                                   weight_decay=self._knobs.get("weight_decay")) # Adam does not have momentum parameter
        elif self._knobs.get("optimizer") == "rmsprop":
            optimizer = optim.RMSprop(
                filter(lambda p: p.requires_grad, self._model.parameters()),
                lr=self._knobs.get("lr"),
                weight_decay=self._knobs.get("weight_decay"),
                momentum=self._knobs.get("momentum"))
        elif self._knobs.get("optimizer") == "sgd":
            optimizer = optim.SGD(
                filter(lambda p: p.requires_grad, self._model.parameters()),
                lr=self._knobs.get("lr"),
                weight_decay=self._knobs.get("weight_decay"),
                momentum=self._knobs.get("momentum"))
        else:
            raise NotImplementedError()

        #Setup Learning Rate Scheduler
        scheduler = lr_scheduler.ReduceLROnPlateau(optimizer,
                                                   patience=1,
                                                   threshold=0.001,
                                                   factor=0.1)

        self._model = self._model.to(self.device)

        self._model.train()

        if self._knobs.get("enable_model_slicing"):
            sr_scheduler = create_sr_scheduler(
                scheduler_type=self._knobs.get("model_slicing_scheduler_type"),
                sr_rand_num=self._knobs.get("model_slicing_randnum"),
                sr_list=[0.5, 0.75, 1.0],
                sr_prob=None)
        # utils.logger.define_plot('Loss Over Epochs', ['loss', 'epoch_accuracy'],
                                 # x_axis='epoch')
        # utils.logger.log(loss=0.0, epoch_accuracy=0.0, epoch=0)
        Epoch_gross_timing, Epoch_net_timing= [], []
        Slicng_timing= [] 
        Spl_timing= []
        Gm_timing= []
        epoch_test_val_loss = []
        # for epoch in range(1, self._knobs.get("max_epochs") + 1):
        ''''''
        for epoch in range(1, 101):
            # print("Epoch {}/{}".format(epoch, self._knobs.get("max_epochs")))

            batch_accuracy = []
            batch_losses = []
            slicing_timing = datetime.now()-datetime.now()
            spl_timing= datetime.now()-datetime.now()
            gm_timing= datetime.now()-datetime.now()
            Epoch_starttime = datetime.now()
            ''''''
            for batch_idx, (raw_indices, traindata,
                            batch_classes) in enumerate(train_dataloader):
                # print("Got batch_idx and batchdata", batch_idx)
                inputs, labels = self._transform_data(traindata,
                                                      batch_classes,
                                                      train=True)
                # print("zero the optimizer")
                optimizer.zero_grad()
                if self._knobs.get("enable_model_slicing"):
                    ''''''
                    # print('enable_model_slicing')
                    Slicing_starttime = datetime.now()
                    ''''''
                    for sr_idx in next(sr_scheduler):
                        self._model.update_sr_idx(sr_idx)
                        outputs = self._model(inputs)
                        trainloss = self.train_criterion(outputs, labels)
                        trainloss.backward()
                    ''''''
                    slicing_timing += datetime.now() - Slicing_starttime
                    ''''''
                else:
                    # torch.Size([256, 3, 128, 128])
                    outputs = self._model(inputs)
                    trainloss = self.train_criterion(outputs, labels)
                    # print("doing backward")
                    trainloss.backward()
                if self._knobs.get("enable_gm_prior_regularization"):
                    ''''''
                    # print ('enable_gm_prior_regularization')
                    Gm_starttime = datetime.now()
                    ''''''
                    for name, f in self._model.named_parameters():
                        self._gm_optimizer.apply_GM_regularizer_constraint(
                            labelnum=dataset.classes,
                            trainnum=dataset.size,
                            epoch=epoch,
                            weight_decay=self._knobs.get("weight_decay"),
                            f=f,
                            name=name,
                            step=batch_idx)
                    ''''''
                    gm_timing += datetime.now() - Gm_starttime
                    ''''''

                if self._knobs.get("enable_spl"):
                    ''''''
                    # print ('enable_spl')
                    Spl_starttime = datetime.now()
                    ''''''
                    train_dataset.update_sample_score(
                        raw_indices,
                        trainloss.detach().cpu().numpy())
                    ''''''
                    spl_timing += datetime.now() - Spl_starttime
                    ''''''
                optimizer.step()
                # print("Epoch: {:d} Batch: {:d} Train Loss: {:.6f}".format(
                    # epoch, batch_idx, trainloss.item()))
                # sys.stdout.flush()

                # transfered_labels = torch.max(labels.data, 1)
                # transfered_outpus = torch.max(torch.sigmoid(outputs), 1)
                # batch_accuracy.append(
                    # transfered_labels[1].eq(transfered_outpus[1]).sum().item() /
                    # transfered_labels[1].size(0))
                batch_losses.append(trainloss.item())
            train_loss = np.mean(batch_losses)
            # batch_accuracy_mean = np.mean(batch_accuracy)
            # utils.logger.log(loss=train_loss,
                             # epoch_accuracy=batch_accuracy_mean,
                             # epoch=epoch)
            # print("epoch Training Loss: {:.6f}".format(train_loss))
            if self._knobs.get("enable_spl"):
                ''''''
                # print ('enable_spl--2')
                Spl_starttime = datetime.now()
                ''''''
                train_dataset.update_score_threshold(
                    threshold=self._spl.calculate_threshold_by_epoch(
                        epoch=epoch,
                        threshold_init=self._knobs.get("spl_threshold_init"),
                        mu=self._knobs.get("spl_mu")))
                ''''''
                spl_timing += datetime.now() - Spl_starttime
            epoch_gross_timing = datetime.now() - Epoch_starttime
            Epoch_gross_timing.append(epoch_gross_timing)
            Epoch_net_timing.append(epoch_gross_timing - spl_timing - gm_timing - slicing_timing)
            ''''''
            ### nni epoch val
            self._model.eval()
            ### label drift, label adaptation
            # if self._knobs.get("enable_label_adaptation"):
                # self._label_drift_adapter = LabelDriftAdapter(
                    # model=self._model, num_classes=self._num_classes)

            batch_losses = []
            batch_accuracy =[]
            train_criterion = nn.MultiLabelSoftMarginLoss() ### easy
            val_dataset_path=self._knobs.get("val_dataset_path")
            # val_dataset_path='/hdd2/yangnan/Singa/aug-21/data/xray_test.zip'
            # print ('********** val_dataset_path **********',val_dataset_path)
            val_dataset_ = utils.dataset.load_dataset_of_image_files(
                    val_dataset_path,
                    min_image_size=32,
                    max_image_size=self._knobs.get("max_image_size"),
                    mode='RGB')

            val_dataset = TorchImageDataset(sa_dataset=val_dataset_,
                                                  image_scale_size=self._image_size,
                                                  norm_mean=self._normalize_mean,
                                                  norm_std=self._normalize_std,
                                                  is_train=False)
            val_loader = torch.utils.data.DataLoader(val_dataset,
                batch_size=self._knobs.get('batch_size'))
                # batch_size=1000)
            try:
                with torch.no_grad():
                    for batch_idx, (raw_indices, data, target)in enumerate(val_loader):
                        data, target=self._transform_data(data, target, train=False)
                        data, target = data.to(self.device), target.to(self.device)
                        output = self._model(data)
                        # sum up batch loss
                        loss = train_criterion(output, target) ### easy
                        batch_losses.append(loss.item()) ### easy
                        ### label drift, label adaptation
                        # if self._knobs.get("enable_label_adaptation"):
                            # self._label_drift_adapter.accumulate_c(output, target)
                        # get the index of the max log-probability
                        transfered_labels = torch.max(target.data, 1)
                        transfered_outpus = torch.max(torch.sigmoid(output), 1)
                        batch_accuracy.append(
                                transfered_labels[1].eq(transfered_outpus[1]).sum().item() /
                                transfered_labels[1].size(0))
                valid_loss = np.mean(batch_losses) ### easy
                epoch_test_val_loss.append(valid_loss)
                batch_accuracy_mean = np.mean(batch_accuracy)
                # print (epoch, 'Epoch val Average loss: {:.4f}, Accuracy: {}. epoch val batch size: {} \n'.format(
                    # valid_loss, batch_accuracy_mean, len(val_loader.dataset)))
                print (epoch, 'Epoch val Average loss: {:.4f}, Accuracy: {}. \n'.format(
                    valid_loss, batch_accuracy_mean))
                # gc.collect()
                # torch.cuda.empty_cache()
                ### label drift, label adaptation
                # if self._knobs.get("enable_label_adaptation"):
                    # self._label_drift_adapter.estimate_cinv()
            except:
                print ('********* Val NotImplementedError ***************')
            ''''''
        # print ('batch_losses: \n', epoch_test_val_loss,'\nEpoch_net_timing:\n', Epoch_net_timing, '\nEpoch_gross_timing:\n', Epoch_gross_timing)
        print ('batch_losses: \n', epoch_test_val_loss)
        try: 
            filename='/hdd1/yangnan/Singa/feb-16-easy/singa_easy/models/easy_{}_{}e_{}bs_{}.txt'.format(self._knobs.get("model_class"),self._knobs.get("max_epochs"), self._knobs.get("batch_size"), str(datetime.now().date()))
            geeky_file = open(filename, 'wt') 
            geeky_file.write(str({
                'epoch_test_val_loss': epoch_test_val_loss,'\nEpoch_net_timing': Epoch_net_timing, '\nEpoch_gross_timing': Epoch_gross_timing
                })) 
            geeky_file.close() 
            print ('saved to file', filename)
            sys.stdout.flush()
        except: 
            print("Unable to write to file")

    def evaluate(self, dataset_path, **kargs):
        ''''''
        # print('**************** dataset_path **********', dataset_path)
        # dataset_path='/hdd2/yangnan/Singa/aug-21/data/xray_test.zip'
        ''''''
        dataset = utils.dataset.load_dataset_of_image_files(
            dataset_path,
            min_image_size=32,
            max_image_size=self._knobs.get("max_image_size"),
            mode='RGB')

        torch_dataset = TorchImageDataset(sa_dataset=dataset,
                                          image_scale_size=self._image_size,
                                          norm_mean=self._normalize_mean,
                                          norm_std=self._normalize_std,
                                          is_train=False)

        torch_dataloader = DataLoader(torch_dataset,
                                      batch_size=self._knobs.get("batch_size"))
                                      # batch_size=1000) # set large batch size for evaluation

        self._model.eval()

        if self._knobs.get("enable_label_adaptation"):
            self._label_drift_adapter = LabelDriftAdapter(
                model=self._model, num_classes=self._num_classes)

        # batch_losses = []
        outs = []
        gts = []
        with torch.no_grad():
            for batch_idx, (raw_indices, batch_data,
                            batch_classes) in enumerate(torch_dataloader):
                inputs, labels = self._transform_data(batch_data,
                                                      batch_classes,
                                                      train=False)
                outputs = self._model(inputs)
                loss = self.train_criterion(outputs, labels)
                # batch_losses.append(loss.item())
                outs.extend(torch.sigmoid(outputs).cpu().numpy())
                gts.extend(labels.cpu().numpy())

                if self._knobs.get("enable_label_adaptation"):
                    self._label_drift_adapter.accumulate_c(outputs, labels)

                # print("Batch: {:d}".format(batch_idx))

        if self._knobs.get("enable_label_adaptation"):
            self._label_drift_adapter.estimate_cinv()

        # valid_loss = np.mean(batch_losses)
        # print("Validation Loss: {:.6f}".format(valid_loss))
        gts = np.array(gts)
        outs = np.array(outs)

        # in case that the ground truth has only one dimension
        # i.e. is size of (N,) with integer elements of 0...C-1, where C is the number of classes
        # the ground truth array has to be "one hot" encoded for evaluating the performance metric
        if len(gts.shape) == 1:
            gts = np.eye(self._num_classes)[gts].astype(np.int64)

        pr_auc, roc_auc, f1, acc = self.get_peformance_metrics(
            gts=np.array(gts), probabilities=np.array(outs))

        return f1

    def predict(self, queries: List[Any]) -> List[Any]:
        """
        Overide BaseModel.predict()
        Making prediction using queries

        Parameters:
            queries: list of quries
        Return:
            outs: list of numbers indicating scores of classes
        """
        ''''''
        # queries = utils.dataset.load_images(['/hdd2/yangnan/Singa/aug-21/data/image_classification/xray_1.png'])
        ''''''
        print('Begin to predict')
        ndarray_images, pil_images = utils.dataset.transform_images(
            queries, image_size=self._image_size, mode='RGB')
        (images, _, _) = utils.dataset.normalize_images(ndarray_images,
                                                        self._normalize_mean,
                                                        self._normalize_std)
        print('Using device:', self.device)
        self._model.to(self.device)
        self._model.eval()
        # images are size of (B, W, H, C)
        with torch.no_grad():
            images = torch.FloatTensor(images).permute(0, 3, 1, 2).to(self.device)

            if self._knobs.get("enable_mc_dropout"):
                # print("MC Dropout Enabled")
                trials_n = self._knobs.get("mc_trials_n")
            else:
                trials_n = 1
            outs = list()

            for i in range(trials_n):
                out = self._model(images)
                if self._knobs.get("enable_label_adaptation"):
                    out = self._label_drift_adapter.adapt(out).squeeze()
                else:
                    out = torch.sigmoid(out).cpu().squeeze()
                outs.append(out.cpu().numpy())

        result = dict()
        outs = np.asarray(outs)
        result['outs'] = outs.tolist()
        result['explanations'] = {}
        result['mc_dropout'] = []

        if self._knobs.get("enable_explanation"):
            exp = self.local_explain(org_imgs=pil_images,
                                     images=ndarray_images,
                                     params={})
            if exp:
                result['explanations'] = exp
            import base64
            # print (exp)
            # if self._knobs.get("explanation_lime"):
            ''''''
            try:
                base64_img=exp['lime_img']
                base64_img_bytes = base64_img.encode('utf-8')
                filename='/hdd1/yangnan/Singa/feb-16-easy/singa_easy/models/easy_exp_lime_{}_{}e_{}bs_{}.png'.format(self._knobs.get("model_class"),self._knobs.get("max_epochs"), self._knobs.get("batch_size"),str(datetime.now().date()))
                with open(filename, 'wb') as file_to_save:
                    decoded_image_data = base64.decodebytes(base64_img_bytes)
                    file_to_save.write(decoded_image_data)

            # if self._knobs.get("explanation_gradcam"):
                base64_img=exp['gradcam_img']
                base64_img_bytes = base64_img.encode('utf-8')
                filename='/hdd1/yangnan/Singa/feb-16-easy/singa_easy/models/easy_exp_gradcam_{}_{}e_{}bs_{}.png'.format(self._knobs.get("model_class"),self._knobs.get("max_epochs"), self._knobs.get("batch_size"),str(datetime.now().date()))
                with open(filename, 'wb') as file_to_save:
                    decoded_image_data = base64.decodebytes(base64_img_bytes)
                    file_to_save.write(decoded_image_data)
            except:
                print ('*********** unable save saliency map ********')

            try: 
                filename='/hdd1/yangnan/Singa/feb-16-easy/singa_easy/models/easy_explanation_{}_{}e_{}bs_{}.txt'.format(self._knobs.get("model_class"),self._knobs.get("max_epochs"), self._knobs.get("batch_size"),str(datetime.now().date()))
                geeky_file = open(filename, 'wt') 
                geeky_file.write(str(exp)) 
                geeky_file.close() 
                print ('saved to file', filename)
                sys.stdout.flush()
            except: 
                print("Unable to write to file")
            ''''''

        if self._knobs.get("enable_mc_dropout"):
            mean_var_eles = list()
            # print("mean {}, var {}".format(np.mean(outs, axis=0),
                                           # np.var(outs, axis=0)))
            label_index = 0
            for mean, var in zip(
                    np.mean(outs, axis=0).squeeze().tolist(),
                    np.var(outs, axis=0).squeeze().tolist()):
                mean_var_ele = dict()
                mean_var_ele['label'] = self.label_mapper[str(label_index)] if self.label_mapper.get(str(label_index)) \
                                                                               is not None else str(label_index)
                mean_var_ele['mean'] = mean
                mean_var_ele['std'] = var
                mean_var_eles.append(mean_var_ele)
                label_index += 1

            result['mc_dropout'] = mean_var_eles
        return [result]

    def local_explain(self, org_imgs: Image,
                      images: List[Any],
                      params: Params) -> Dict:
        """
        Parameters:
            org_imgs: list of PIL.image
            images: list of images(ndarray)
            params: parameters

        Return:
            explanations: list of explanations
        """
        print('begin to do the explanations')
        enable_gradcam = self._knobs.get("explanation_gradcam")
        enable_lime = self._knobs.get("explanation_lime")
        # print('Enable gradcam: {}, Enable lime: {} '.format(enable_gradcam, enable_lime))

        explanation = dict()

        if enable_lime:
            try:
                self._lime = Lime(self._model,
                                  self._image_size,
                                  self._normalize_mean,
                                  self._normalize_std,
                                  self.device)

                imgs_explained = self._lime.explain(images)
                imgs_explained = self.convert_img_to_str(imgs_explained)
                explanation['lime_img'] = imgs_explained
            except:
                explanation['lime_img'] = ''
                traceback.print_exc(file=sys.stdout)

        if enable_gradcam:
            if 'densenet' in self._knobs.get("model_class"):
                model_arch = 'densenet'
            elif 'alexnet' in self._knobs.get("model_class"):
                model_arch = 'alexnet'
            elif 'resnet' in self._knobs.get("model_class"):
                model_arch = 'resnet'
            elif 'vgg' in self._knobs.get("model_class"):
                model_arch = 'vgg'
            else:
                raise NameError()
            try:
                GC = GradCam(model=self._model,
                             model_arch=model_arch,
                             target_layer=None,
                             device=self.device)
                (images, _, _) = utils.dataset.normalize_images(
                    images,
                    self._normalize_mean,
                    self._normalize_std)
                images = images.swapaxes(3, 1)
                images = images.swapaxes(2, 3)
                cam = GC.generate_cam(images)
                combined_gradcam = self.combine_images(org_im=org_imgs[0],### only explain the first img
                                                       activation=cam)
                # explanation['gradcam_exp'] = combined_gradcam.tolist()
                combined_gradcam = self.convert_img_to_str(combined_gradcam)
                explanation['gradcam_img'] = combined_gradcam
            except:
                explanation['gradcam_img'] = ''
                traceback.print_exc(file=sys.stdout)

        return explanation

    def dump_parameters(self):
        """
        Override BaseModel.dump_parameters

        Write PyTorch model's state dict to file, then read it back and encode with base64 encoding.
        The encoded model and the other persistent hyperparameters are returned to SINGA-AUTO
        """
        params = {}

        # Save model parameters
        with tempfile.NamedTemporaryFile() as tmp:
            # Save whole model to temp h5 file
            state_dict = self._model.state_dict()
            torch.save(state_dict, tmp.name)

            # Read from temp h5 file & encode it to base64 string
            with open(tmp.name, 'rb') as f:
                h5_model_bytes = f.read()

            params['h5_model_base64'] = base64.b64encode(h5_model_bytes).decode(
                'utf-8')

        # Save pre-processing params
        params['image_size'] = self._image_size
        params['normalize_mean'] = json.dumps(self._normalize_mean.tolist())
        params['normalize_std'] = json.dumps(self._normalize_std.tolist())
        params['num_classes'] = self._num_classes
        params['label_mapper'] = json.dumps(self.label_mapper)

        if self._knobs.get("enable_label_adaptation"):
            params[self._label_drift_adapter.get_mod_name(
            )] = self._label_drift_adapter.dump_parameters()
        # print ('***********************TorchModel DUMP Model *********************')
        # torch.save(self._model, 'test/trained_{}.pt'.format())
        return params

    def load_parameters(self, params):
        """
        Override BaseModel.load_parameters

        Write base64 encoded PyTorch model state dict to temp file and then read it back with torch.load.
        The other persistent hyperparameters are recovered by setting model's private property
        """
        # Load model parameters
        h5_model_base64 = params['h5_model_base64']
        self._image_size = params['image_size']
        self._normalize_mean = np.array(json.loads(params['normalize_mean']))
        self._normalize_std = np.array(json.loads(params['normalize_std']))
        self._num_classes = params['num_classes']
        self.label_mapper = json.loads(params['label_mapper'])

        with tempfile.NamedTemporaryFile() as tmp:
            # Convert back to bytes & write to temp file
            h5_model_bytes = base64.b64decode(h5_model_base64.encode('utf-8'))
            with open(tmp.name, 'wb') as f:
                f.write(h5_model_bytes)

            # Load model from temp file
            self._model = self._create_model(scratch=self._knobs.get("scratch"), hidden_size=self._knobs.get("hidden_size"),
                                             num_classes=self._num_classes)
            if self._knobs.get("enable_mc_dropout"):
                self._model = update_model(self._model)
            if self._knobs.get("enable_model_slicing"):
                self._model = upgrade_dynamic_layers(
                    model=self._model,
                    num_groups=self._knobs.get("model_slicing_groups"),
                    sr_in_list=[0.5, 0.75, 1.0])
            if torch.cuda.is_available() == False:
                # print ('GPU is not available. Model parameters storages are mapped to CPU')
                self._model.load_state_dict(torch.load(tmp.name,map_location=torch.device('cpu')))
            else:
                # print ('GPU is available. Model parameters storages are mapped to GPU')
                self._model.load_state_dict(torch.load(tmp.name))

        if self._knobs.get("enable_label_adaptation"):
            self._label_drift_adapter = LabelDriftAdapter(
                model=self._model, num_classes=self._num_classes)
            self._label_drift_adapter.load_parameters(
                params=params[self._label_drift_adapter.get_mod_name()])

    def _transform_data(self, data, labels, train=False):
        """
        Send data to GPU
        """
        inputs = data
        labels = labels.type(torch.LongTensor)
        one_hot_labels = torch.zeros(labels.shape[0], self._num_classes)
        one_hot_labels[range(one_hot_labels.shape[0]), labels.squeeze()] = 1
        one_hot_labels = one_hot_labels.type(torch.FloatTensor)
        inputs = Variable(inputs, requires_grad=train)
        one_hot_labels = Variable(one_hot_labels, requires_grad=train)

        inputs, one_hot_labels = inputs.to(self.device), one_hot_labels.to(self.device)

        return inputs, one_hot_labels

    def combine_images(self, org_im, activation, colormap_name='hsv'):
        '''
        org_im: PIL.Image, should be the same size with activation
        return:  list
        '''

        color_map = mpl_color_map.get_cmap(colormap_name)
        no_trans_heatmap = color_map(activation)

        heatmap = copy.copy(no_trans_heatmap)
        heatmap[:, :, 3] = 0.4
        heatmap = Image.fromarray((heatmap * 255).astype(np.uint8))
        no_trans_heatmap = Image.fromarray(
            (no_trans_heatmap * 255).astype(np.uint8))

        # Apply heatmap on iamge
        heatmap_on_image = Image.new("RGBA", org_im.size)
        heatmap_on_image = Image.alpha_composite(heatmap_on_image,
                                                 org_im.convert('RGBA'))
        heatmap_on_image = Image.alpha_composite(heatmap_on_image, heatmap)

        return numpy.asarray(heatmap_on_image)

    def convert_img_to_str(self, arr):
        im = Image.fromarray(arr.astype("uint8"))
        rawBytes = io.BytesIO()
        encoding = 'utf-8'
        im.save(rawBytes, "PNG")
        rawBytes.seek(0)
        return base64.b64encode(rawBytes.read()).decode(encoding)
