#!/usr/bin/env python
# -*- coding: utf-8 -*-

from booltest.booltest_main import Booltest
import random
import base64
import os
import unittest
import pkg_resources
from booltest import booltest_json


__author__ = 'dusanklinec'

"""
"exp_time": 1553696894,
  "config": {
    "spec": {
      "fnc": "BLOWFISH",
      "params": {
        "block_size": 8,
        "key_size": 16,
        "iv_size": null,
        "rounds": 16,
        "min_rounds": null,
        "in_size": null,
        "out_size": null,
        "fname": null
      },
      "stream_type": 3,
      "data_file": null,
      "data_rounds": 1,
      "rounds": [
        1
      ],
      "c_round": 1,
      "data_size": 10000000,
      "is_egen": true,
      "gen_cfg": {
        "tv_count": 1250000,
        "file_name": "SECMARGINPAPER3_hw_seed_1fe40505e131963c_10MiB__BLOWFISH_r01_b8.bin",
        "seed": "1fe40505e131963c",
        "tv-count": null,
        "notes": "generated by generator.py",
        "stream": {
          "type": "block",
          "key": {
            "type": "pcg32_stream"
          },
          "init_frequency": "only_once",
          "key_size": 32,
          "plaintext-type": {
            "type": "hw_counter",
            "hw": 6
          },
          "iv": {
            "type": "false_stream"
          },
          "round": 1,
          "iv_size": 16,
          "plaintext": {
            "type": "hw_counter",
            "hw": 4
          },
          "block_size": 8,
          "algorithm": "BLOWFISH"
        },
        "tv_size": 8,
        "tv-size": null,
        "stdout": true
      },
      "seed_code": 0,
      "is_randomized": false,
      "strategy": "BLOWFISH-r1-e-cfg1ee9be06eb738259453052904d11"
    },
    "block_size": 128,
    "degree": 2,
    "comb_deg": 2,
    "total_test_idx": 15844,
    "test_desc": "idx: 15844, data: 0010, block: 128, deg: 2, comb-deg: 2, fun: BLOWFISH, round: 1 scode: BLOWFISH-r1-e-cfg1ee9be06eb738259453052904d11, 0",
    "res_file": "BLOWFISH-r1-e-cfg1ee9be06eb738259453052904d11-0010MB-128bl-2deg-2k.json",
    "gen_file": "gen-BLOWFISH-r1-e-cfg1ee9be06eb738259453052904d11-0010MB-0.json",
    "iteration": 0
  },
  "hwanalysis": {
    "term_map": [],
    "term_eval": null,
    "ref_term_eval": null,
    "blocklen": 128,
    "deg": 2,
    "top_k": 128,
    "comb_random": 0,
    "top_comb": 2,
    "zscore_thresh": 1.96,
    "combine_all_deg": false,
    "do_ref": null,
    "no_comb_xor": false,
    "no_comb_and": true,
    "prob_comb": 1.0,
    "skip_print_res": true,
    "do_only_top_comb": true,
    "do_only_top_deg": true,
    "no_term_map": true,
    "use_zscore_heap": true,
    "sort_best_zscores": 256,
    "best_x_combinations": null,
    "total_rounds": 0,
    "total_hws": [],
    "ref_total_hws": [],
    "total_n": 0,
    "last_res": null,
    "all_deg_compute": true,
    "input_poly": [],
    "input_poly_exp": [],
    "input_poly_hws": [],
    "input_poly_ref_hws": [],
    "input_poly_vars": [],
    "input_poly_last_res": null,
    "all_zscore_comp": false,
    "all_zscore_list": null,
    "all_zscore_means": null,
    "comb_res": null,
    "comb_subres": null
  },
  "fidx": 5497,
  "res_file": "/storage/brno3-cerit/home/ph4r05//bool-res/BLOWFISH-r1-e-cfg1ee9be06eb738259453052904d11-0010MB-128bl-2deg-2k.json",
  "gen_file": "/storage/brno3-cerit/home/ph4r05//bool-jobNr44/gen-BLOWFISH-r1-e-cfg1ee9be06eb738259453052904d11-0010MB-0.json",
  "backup_dir": null,
  "skip_finished": false,
  "all_zscores": false
}
"""


class BooltestTest(unittest.TestCase):
    """Simple BoolTest tests"""

    def __init__(self, *args, **kwargs):
        super(BooltestTest, self).__init__(*args, **kwargs)

    def default_config(self, block_size=128, degree=2, comb_deg=2, data_file=None, data_size=1024*1024, halving=False):
        cfg = {
          "config": {
            "spec": {
              "fnc": "test",
              "params": {},
              "data_file": data_file,
              "c_round": 1,
              "data_size": data_size,
              "is_egen": False,
              "gen_cfg": {},
              "seed_code": 0,
              "is_randomized": False,
              "strategy": "test"
            },
            "block_size": block_size,
            "degree": degree,
            "comb_deg": comb_deg,
            "total_test_idx": 0,
            "test_desc": "test",
            "res_file": "test",
            "gen_file": "test",
            "iteration": 0
          },
          "hwanalysis": {
            "term_map": [],
            "term_eval": None,
            "ref_term_eval": None,
            "blocklen": block_size,
            "deg": degree,
            "top_k": 128,
            "comb_random": 0,
            "top_comb": comb_deg,
            "zscore_thresh": 1.96,
            "combine_all_deg": False,
            "do_ref": None,
            "no_comb_xor": False,
            "no_comb_and": True,
            "prob_comb": 1.0,
            "skip_print_res": True,
            "do_only_top_comb": True,
            "do_only_top_deg": True,
            "no_term_map": True,
            "use_zscore_heap": True,
            "sort_best_zscores": 256,
            "best_x_combinations": 256,
            "total_rounds": 0,
            "total_hws": [],
            "ref_total_hws": [],
            "total_n": 0,
            "last_res": None,
            "all_deg_compute": True,
            "input_poly": [],
            "input_poly_exp": [],
            "input_poly_hws": [],
            "input_poly_ref_hws": [],
            "input_poly_vars": [],
            "input_poly_last_res": None,
            "all_zscore_comp": False,
            "all_zscore_list": None,
            "all_zscore_means": None,
            "comb_res": None,
            "comb_subres": None
          },
          "fidx": 0,
          "res_file": None,
          "gen_file": None,
          "backup_dir": None,
          "skip_finished": False,
          "all_zscores": False,
          "halving": halving,
          "halving_top": 5,
        }

        return cfg

    def get_data(self, fname):
        return pkg_resources.resource_string(
          __name__, os.path.join("data", fname)
        )

    def init_booltest(self, blocklen=128, deg=1, comb_deg=1, halving=False):
        cfg = self.default_config(blocklen, deg, comb_deg, halving=halving)
        btest = booltest_json.BooltestJson()
        btest.parse_args([])

        btest.config_data = cfg
        btest.dump_cpu_info = False
        return btest

    def test_prob1_x0(self):
        bin_data = self.get_data('randc_seed1_prob1_x0.data')
        btest = self.init_booltest(128, 1, 1)
        res = btest.work(bin_data)
        best_dists = res['best_dists']

        self.assertTrue(len(best_dists) > 0)
        self.assertEqual(best_dists[0].poly, [[0]])
        self.assertEqual(best_dists[0].expp, 0.5)
        self.assertEqual(best_dists[0].obs_cnt, 0)
        self.assertLess(best_dists[0].zscore, 100)
        for i in range(1, len(best_dists)):
            self.assertGreater(best_dists[i].obs_cnt, 0)

    def test_prob16_x0(self):
        bin_data = self.get_data('randc_seed1_prob16_x0.data')
        btest = self.init_booltest(128, 1, 1)
        res = btest.work(bin_data)
        best_dists = res['best_dists']

        self.assertTrue(len(best_dists) > 0)
        self.assertEqual(best_dists[0].poly, [[0]])
        self.assertEqual(best_dists[0].expp, 0.5)
        self.assertGreater(best_dists[0].obs_cnt, 0)
        self.assertLess(best_dists[0].zscore, -5)
        for i in range(1, len(best_dists)):
            self.assertGreater(best_dists[i].obs_cnt, 0)

    def test_prob1_and_x0_x42(self):
        bin_data = self.get_data('randc_seed1_prob1_and_x0_x42.data')
        btest = self.init_booltest(128, 2, 1)
        res = btest.work(bin_data)
        best_dists = res['best_dists']

        self.assertTrue(len(best_dists) > 0)
        self.assertEqual(best_dists[0].poly, [[0, 42]])
        self.assertEqual(best_dists[0].expp, 0.25)
        self.assertEqual(best_dists[0].obs_cnt, 0)
        self.assertLess(best_dists[0].zscore, -5)

    def test_prob16_and_x0_x42(self):
        bin_data = self.get_data('randc_seed1_prob16_and_x0_x42.data')
        btest = self.init_booltest(128, 2, 1)
        res = btest.work(bin_data)
        best_dists = res['best_dists']

        self.assertTrue(len(best_dists) > 0)
        self.assertEqual(best_dists[0].poly, [[0, 42]])
        self.assertEqual(best_dists[0].expp, 0.25)
        self.assertGreater(best_dists[0].obs_cnt, 0)
        self.assertLess(best_dists[0].zscore, -6)

    def test_prob1_and_x0_x42_x100(self):
        bin_data = self.get_data('randc_seed1_prob1_and_x0_x42_x100.data')
        btest = self.init_booltest(128, 3, 1)
        res = btest.work(bin_data)
        best_dists = res['best_dists']

        self.assertTrue(len(best_dists) > 0)
        self.assertEqual(best_dists[0].poly, [[0, 42, 100]])
        self.assertEqual(best_dists[0].expp, pow(2, -3))
        self.assertEqual(best_dists[0].obs_cnt, 0)
        self.assertLess(best_dists[0].zscore, -5)

    def test_prob1_xor_x0_x42(self):
        bin_data = self.get_data('randc_seed1_prob1_xor_x0_x42.data')
        btest = self.init_booltest(128, 1, 2)
        res = btest.work(bin_data)
        best_dists = res['best_dists']

        self.assertTrue(len(best_dists) > 0)
        self.assertEqual(sorted(best_dists[0].poly), [[0], [42]])
        self.assertEqual(best_dists[0].expp, 0.5)
        self.assertEqual(best_dists[0].obs_cnt, 0)
        self.assertLess(best_dists[0].zscore, -5)

    def test_prob1_xor_x0_x42_x100(self):
        bin_data = self.get_data('randc_seed1_prob1_xor_x0_x42_x100.data')
        btest = self.init_booltest(128, 1, 3)
        res = btest.work(bin_data)
        best_dists = res['best_dists']

        self.assertTrue(len(best_dists) > 0)
        self.assertEqual(sorted(best_dists[0].poly), [[0], [42], [100]])
        self.assertEqual(best_dists[0].expp, 0.5)
        self.assertEqual(best_dists[0].obs_cnt, 0)
        self.assertLess(best_dists[0].zscore, -5)

    def test_prob1_halving_xor_x0_x42_x100(self):
        bin_data = self.get_data('randc_seed1_prob1_xor_x0_x42_x100.data')
        btest = self.init_booltest(128, 1, 3, halving=True)
        res = btest.work(bin_data)
        best_dists = res['best_dists']

        self.assertTrue(len(best_dists) > 0)
        self.assertEqual(best_dists[0][0], ((0,), (42,), (100,)))
        self.assertEqual(best_dists[0][1], 0.5)  # expp
        self.assertEqual(best_dists[0][3], 0)  # obs_cnt
        self.assertLess(best_dists[0][4], -180)  # zscore
        self.assertLess(best_dists[0][6], 5e200)  # pvalue


if __name__ == "__main__":
    unittest.main()  # pragma: no cover


