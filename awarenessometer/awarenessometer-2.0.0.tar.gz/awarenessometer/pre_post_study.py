import os
from typing import Any, Dict, List

import mpmath
import numpy as np
import pandas as pd
from pandas import DataFrame

from awarenessometer.stats_helper import collective_awareness
from awarenessometer.stats_helper import artifact_correlations
from awarenessometer.stats_helper import cronbachs_alpha
from awarenessometer.plotter import Plotter


class PrePostStudy:  # pylint:disable=too-many-instance-attributes
    def __init__(self,
                 employees_with_vdu: int,
                 series_info: Dict[str, Any],
                 img_dir: str):
        self.type = 'pre-post'
        self.employees_with_vdu = employees_with_vdu
        self.series_pre_data = series_info['series_data']['pre']
        self.series_post_data = series_info['series_data']['post']
        self.subjects = series_info['subject_df']
        self.reports = series_info['reports']
        self.matrices: Dict[str, np.array] = series_info['matrices']
        self.img_dir = img_dir

    def create_tokens(self) -> Dict:
        tokens = {
            'series_pre_info': self._get_series_info(self.series_pre_data),
            'artifacts_pre': self._get_artifact_info(self.series_pre_data),
            'series_post_info': self._get_series_info(self.series_post_data),
            'artifacts_post': self._get_artifact_info(self.series_post_data),
            'participation_stats': self._participation_stats(),
            'reaction_stats': self._reaction_stats(),
            'cronbachs_alpha': self._calculate_cronbachs_alphas()
        }
        return tokens

    def _get_artifact_info(self, series: Dict) -> List:
        artifacts = []
        images = os.listdir(self.img_dir)
        for artifact in series['artifacts']:
            artifact_images = sorted([os.path.join('img', img)
                                      for img in images
                                      if img.startswith(artifact)])
            artifact_data = {'recipe_id': artifact, 'images': artifact_images}
            artifacts.append(artifact_data)
        return artifacts

    @staticmethod
    def _get_series_info(series: Dict) -> Dict:
        label = series['label']
        start = series['start'].strftime('%Y-%m-%d %H:%M:%S')
        end = series['end'].strftime('%Y-%m-%d %H:%M:%S')
        no_participants = len(series['participants'])
        no_artifacts = len(series['artifacts'])
        info = {
            'title': label,
            'start': start,
            'end': end,
            '#participants': no_participants,
            '#artifacts': no_artifacts
        }
        return info

    def _participation_stats(self) -> Dict:  # pylint: disable=too-many-locals
        subjects = self.subjects
        no_participants = subjects.shape[0]
        subjects_pre = subjects.query('id_pre != ""')
        subjects_post = subjects.query('id_post != ""')
        subjects_pre_and_post = subjects.query('id_pre != "" & id_post != ""')
        stats = {}

        # general info
        no_pre_participants = subjects_pre.shape[0]
        stats['#pre_participants'] = no_pre_participants

        no_post_participants = subjects_post.shape[0]
        stats['#post_participants'] = no_post_participants

        no_intersection = subjects_pre_and_post.shape[0]
        stats['#pre_x_post'] = no_intersection

        no_pre_only = no_pre_participants - no_intersection
        share_pre_only = no_pre_only / (no_pre_participants / 100)
        stats['#pre_only'] = f'{no_pre_only} ({share_pre_only:.2f}%)'

        no_post_only = no_post_participants - no_intersection
        share_post_only = no_post_only / (no_post_participants / 100)
        stats['#post_only'] = f'{no_post_only} ({share_post_only:.2f}%)'

        # class
        no_schooled = subjects.query('schooled == 1').shape[0]
        share_schooled = no_schooled / (no_participants / 100)
        stats['#schooled'] = f'{no_schooled} ({share_schooled:.2f}%)'

        no_schooled_pre = subjects_pre.query('schooled == 1').shape[0]
        share_schooled_pre = no_schooled_pre / (no_pre_participants / 100)
        stats['#schooled_pre'] = (f'{no_schooled_pre} ({share_schooled_pre:.2f}%)')

        no_schooled_post = subjects_post.query('schooled == 1').shape[0]
        share_schooled_post = no_schooled_post / (no_post_participants / 100)
        stats['#schooled_post'] = (f'{no_schooled_post} ({share_schooled_post:.2f}%)')

        no_schooled_pre_and_post = (subjects_pre_and_post.query('schooled == 1').shape[0])
        share_schooled_pre_and_post = no_schooled_pre_and_post / (no_intersection / 100)
        stats['#schooled_pre_post'] = (f'{no_schooled_pre_and_post} '
                                       f'({share_schooled_pre_and_post:.2f}%)')

        # phase 1
        no_missed_pre = subjects_pre.query('arms_pre == 0').shape[0]
        share_missed_pre = no_missed_pre / (no_pre_participants / 100)
        stats['#missed_pre'] = f'{no_missed_pre} ({share_missed_pre:.2f}%)'

        no_armed_pre = no_pre_participants - no_missed_pre
        share_armed_pre = 100 - share_missed_pre
        stats['#armed_pre'] = f'{no_armed_pre} ({share_armed_pre:.2f}%)'

        pre_arms = subjects_pre['arms_pre']
        stats['#pre_artifacts'] = (f'{pre_arms.mean():.2f} '
                                   f'{pre_arms.std():.2f} '
                                   f'{pre_arms.min():.2f} '
                                   f'{pre_arms.max():.2f}')

        # phase 2
        no_missed_post = subjects_post.query('arms_post == 0').shape[0]
        share_missed_post = no_missed_post / (no_post_participants / 100)
        stats['#missed_post'] = f'{no_missed_post} ({share_missed_post:.2f}%)'

        no_armed_post = no_post_participants - no_missed_post
        share_armed_post = 100 - share_missed_post
        stats['#armed_post'] = f'{no_armed_post} ({share_armed_post:.2f}%)'

        post_arms = subjects_post['arms_post']
        stats['#post_artifacts'] = (f'{post_arms.mean():.2f} '
                                    f'{post_arms.std():.2f} '
                                    f'{post_arms.min():.2f} '
                                    f'{post_arms.max():.2f}')
        return stats

    # pylint: disable=too-many-locals,too-many-statements
    def _reaction_stats(self) -> Dict:
        stats = {}
        no_arms_pre = self.subjects['arms_pre'].sum()
        no_arms_post = self.subjects['arms_post'].sum()
        no_arms = no_arms_pre + no_arms_post

        # positive and negative actions
        p_pos_pre = self.subjects['#pos_pre'].sum() / no_arms_pre
        p_pos_post = self.subjects['#pos_post'].sum() / no_arms_post
        p_pos = (self.subjects['#pos_pre'].sum() + self.subjects['#pos_post'].sum()) / no_arms
        p_nopos_pre = 1 - p_pos_pre
        p_nopos_post = 1 - p_pos_post
        p_nopos = 1 - p_pos
        p_pos_neg_pre = self.subjects['#pos_neg_pre'].sum() / no_arms_pre
        p_pos_neg_post = self.subjects['#pos_neg_post'].sum() / no_arms_post
        p_pos_neg = (self.subjects['#pos_neg_pre'] + self.subjects['#pos_neg_post']).sum() / no_arms
        p_nopos_neg_pre = self.subjects['#bad_evaluation_pre'].sum() / no_arms_pre
        p_nopos_neg_post = self.subjects['#bad_evaluation_post'].sum() / no_arms_post
        p_nopos_neg = (self.subjects['#bad_evaluation_pre'] +
                       self.subjects['#bad_evaluation_post']).sum() / no_arms
        p_pos_noneg_pre = p_pos_pre - p_pos_neg_pre
        p_pos_noneg_post = p_pos_post - p_pos_neg_post
        p_pos_noneg = p_pos - p_pos_neg
        p_nopos_noneg_pre = p_nopos_pre - p_nopos_neg_pre
        p_nopos_noneg_post = p_nopos_post - p_nopos_neg_post
        p_nopos_noneg = p_nopos - p_nopos_neg

        # class statistics
        armed_subjects_pre = self.subjects.query('arms_pre > 0')
        armed_subjects_post = self.subjects.query('arms_post > 0')
        armed_subjects = self.subjects.query('arms_pre > 0 | arms_post > 0')
        iv_subjects_pre = armed_subjects_pre.query('schooled == 1')
        iv_subjects_post = armed_subjects_post.query('schooled == 1')
        iv_subjects = armed_subjects.query('schooled == 1')
        noiv_subjects_pre = armed_subjects_pre.query('schooled == 0')
        noiv_subjects_post = armed_subjects_post.query('schooled == 0')
        noiv_subjects = armed_subjects.query('schooled == 0')
        no_iv_arms_pre = iv_subjects_pre['arms_pre'].sum()
        no_iv_arms_post = iv_subjects_post['arms_post'].sum()
        no_iv_arms = no_iv_arms_pre + no_iv_arms_post
        no_noiv_arms_pre = noiv_subjects_pre['arms_pre'].sum()
        no_noiv_arms_post = noiv_subjects_post['arms_post'].sum()
        no_noiv_arms = no_noiv_arms_pre + no_noiv_arms_post

        # prefix iv means that the probability is only applied to iv
        # participants, i.e. iv_p_nopos = P(nopos | iv)
        iv_p_nopos_pre = (iv_subjects_pre['arms_pre'] -
                          iv_subjects_pre['#pos_pre']).sum() / no_iv_arms_pre
        iv_p_nopos_post = ((iv_subjects_post['arms_post'] - iv_subjects_post['#pos_post']).sum() /
                           no_iv_arms_post)
        iv_p_nopos = (((iv_subjects_pre['arms_pre'] - iv_subjects_pre['#pos_pre']).sum() +
                       (iv_subjects_post['arms_post'] - iv_subjects_post['#pos_post']).sum()) /
                      no_iv_arms)
        noiv_p_nopos_pre = ((noiv_subjects_pre['arms_pre'] - noiv_subjects_pre['#pos_pre']).sum() /
                            no_noiv_arms_pre)
        noiv_p_nopos_post = ((noiv_subjects_post['arms_post'] -
                              noiv_subjects_post['#pos_post']).sum() /
                             no_noiv_arms_post)
        noiv_p_nopos = (((noiv_subjects_pre['arms_pre'] - noiv_subjects_pre['#pos_pre']).sum() +
                         (noiv_subjects_post['arms_post'] -
                          noiv_subjects_post['#pos_post']).sum()) /
                        no_noiv_arms)
        iv_p_neg_pre = iv_subjects_pre['#neg_pre'].sum() / no_iv_arms_pre
        iv_p_neg_post = iv_subjects_post['#neg_post'].sum() / no_iv_arms_post
        iv_p_neg = (iv_subjects['#neg_pre'].sum() + iv_subjects['#neg_post'].sum()) / no_iv_arms
        noiv_p_neg_pre = noiv_subjects_pre['#neg_pre'].sum() / no_noiv_arms_pre
        noiv_p_neg_post = noiv_subjects_post['#neg_post'].sum() / no_noiv_arms_post
        noiv_p_neg = ((noiv_subjects['#neg_pre'].sum() + noiv_subjects['#neg_post'].sum()) /
                      no_noiv_arms)
        iv_p_nopos_neg_pre = iv_subjects_pre['#bad_evaluation_pre'].sum() / no_iv_arms_pre
        iv_p_nopos_neg_post = iv_subjects_post['#bad_evaluation_post'].sum() / no_iv_arms_post
        iv_p_nopos_neg = ((iv_subjects_pre['#bad_evaluation_pre'].sum() +
                           iv_subjects_post['#bad_evaluation_post'].sum()) /
                          no_iv_arms)
        noiv_p_nopos_neg_pre = noiv_subjects_pre['#bad_evaluation_pre'].sum() / no_noiv_arms_pre
        noiv_p_nopos_neg_post = noiv_subjects_post['#bad_evaluation_post'].sum() / no_noiv_arms_post
        noiv_p_nopos_neg = (
            (noiv_subjects_pre['#bad_evaluation_pre'].sum() +
             noiv_subjects_post['#bad_evaluation_post'].sum()) /
            no_noiv_arms
        )
        # collective and individual awareness
        iv_citsa_pre = collective_awareness(iv_p_nopos_neg_pre,
                                            iv_p_nopos_pre,
                                            self.employees_with_vdu)
        iv_citsa_post = collective_awareness(iv_p_nopos_neg_post,
                                             iv_p_nopos_post,
                                             self.employees_with_vdu)
        iv_citsa = collective_awareness(iv_p_nopos_neg, iv_p_nopos, self.employees_with_vdu)
        noiv_citsa_pre = collective_awareness(noiv_p_nopos_neg_pre,
                                              noiv_p_nopos_pre,
                                              self.employees_with_vdu)
        noiv_citsa_post = collective_awareness(noiv_p_nopos_neg_post,
                                               noiv_p_nopos_post,
                                               self.employees_with_vdu)
        noiv_citsa = collective_awareness(noiv_p_nopos_neg, noiv_p_nopos, self.employees_with_vdu)
        citsa_increase_pre = mpmath.fdiv(mpmath.fsub(iv_citsa_pre, noiv_citsa_pre), noiv_citsa_pre)
        citsa_increase_post = mpmath.fdiv(mpmath.fsub(iv_citsa_post, noiv_citsa_post),
                                          noiv_citsa_post)
        citsa_increase = mpmath.fdiv(mpmath.fsub(iv_citsa, noiv_citsa), noiv_citsa)

        iv_iitsa_pre = iv_subjects_pre['#good_evaluation_pre'].sum() / no_iv_arms_pre
        iv_iitsa_post = iv_subjects_post['#good_evaluation_post'].sum() / no_iv_arms_post
        iv_iitsa = ((iv_subjects_pre['#good_evaluation_pre'].sum() +
                     iv_subjects_post['#good_evaluation_post'].sum()) /
                    no_iv_arms)
        noiv_iitsa_pre = noiv_subjects_pre['#good_evaluation_pre'].sum() / no_noiv_arms_pre
        noiv_iitsa_post = noiv_subjects_post['#good_evaluation_post'].sum() / no_noiv_arms_post
        noiv_iitsa = ((noiv_subjects_pre['#good_evaluation_pre'].sum() +
                       noiv_subjects_post['#good_evaluation_post'].sum()) /
                      no_noiv_arms)
        iitsa_increase_pre = (iv_iitsa_pre - noiv_iitsa_pre) / noiv_iitsa_pre
        iitsa_increase_post = (iv_iitsa_post - noiv_iitsa_post) / noiv_iitsa_post
        iitsa_increase = (iv_iitsa - noiv_iitsa) / noiv_iitsa

        # more in depth stats
        good_eval_per_artifact_pre = (
            armed_subjects_pre['#good_evaluation_pre'] / armed_subjects_pre['arms_pre']
        )
        good_eval_per_artifact_post = (
            armed_subjects_post['#good_evaluation_post'] / armed_subjects_post['arms_post']
        )
        good_eval_per_artifact = ((armed_subjects['#good_evaluation_pre'] +
                                   armed_subjects['#good_evaluation_post']) /
                                  (armed_subjects['arms_pre'] +
                                   armed_subjects['arms_post']))
        bad_eval_per_artifact_pre = (
            armed_subjects_pre['#bad_evaluation_pre'] / armed_subjects_pre['arms_pre']
        )
        bad_eval_per_artifact_post = (
            armed_subjects_post['#bad_evaluation_post'] / armed_subjects_post['arms_post']
        )
        bad_eval_per_artifact = ((armed_subjects['#bad_evaluation_pre'] +
                                  armed_subjects['#bad_evaluation_post']) /
                                 (armed_subjects['arms_pre'] +
                                  armed_subjects['arms_post']))

        good_eval_iv_per_artifact_pre = (
            iv_subjects_pre['#good_evaluation_pre'] / iv_subjects_pre['arms_pre']
        )
        good_eval_iv_per_artifact_post = (
            iv_subjects_post['#good_evaluation_post'] / iv_subjects_post['arms_post']
        )
        good_eval_iv_per_artifact = ((iv_subjects['#good_evaluation_pre'] +
                                      iv_subjects['#good_evaluation_post']) /
                                     (iv_subjects['arms_pre'] +
                                      iv_subjects['arms_post']))
        bad_eval_iv_per_artifact_pre = (
            iv_subjects_pre['#bad_evaluation_pre'] / iv_subjects_pre['arms_pre']
        )
        bad_eval_iv_per_artifact_post = (
            iv_subjects_post['#bad_evaluation_post'] / iv_subjects_post['arms_post']
        )
        bad_eval_iv_per_artifact = ((iv_subjects['#bad_evaluation_pre'] +
                                     iv_subjects['#bad_evaluation_post']) /
                                    (iv_subjects['arms_pre'] +
                                     iv_subjects['arms_post']))

        good_eval_noiv_per_artifact_pre = (
            noiv_subjects_pre['#good_evaluation_pre'] / noiv_subjects_pre['arms_pre']
        )
        good_eval_noiv_per_artifact_post = (
            noiv_subjects_post['#good_evaluation_post'] / noiv_subjects_post['arms_post']
        )
        good_eval_noiv_per_artifact = (
            (noiv_subjects['#good_evaluation_pre'] +
             noiv_subjects['#good_evaluation_post']) /
            (noiv_subjects['arms_pre'] +
             noiv_subjects['arms_post'])
        )
        bad_eval_noiv_per_artifact_pre = (
            noiv_subjects_pre['#bad_evaluation_pre'] / noiv_subjects_pre['arms_pre']
        )
        bad_eval_noiv_per_artifact_post = (
            noiv_subjects_post['#bad_evaluation_post'] / noiv_subjects_post['arms_post']
        )
        bad_eval_noiv_per_artifact = (
            (noiv_subjects['#bad_evaluation_pre'] +
             noiv_subjects['#bad_evaluation_post']) /
            (noiv_subjects['arms_pre'] +
             noiv_subjects['arms_post'])
        )

        stats['p_nopos_pre'] = f'{p_nopos_pre:.2%}'
        stats['p_nopos_post'] = f'{p_nopos_post:.2%}'
        stats['p_nopos'] = f'{p_nopos:.2%}'
        stats['p_pos_neg_pre'] = f'{p_pos_neg_pre:.2%}'
        stats['p_pos_neg_post'] = f'{p_pos_neg_post:.2%}'
        stats['p_pos_neg'] = f'{p_pos_neg:.2%}'
        stats['p_pos_noneg_pre'] = f'{p_pos_noneg_pre:.2%}'
        stats['p_pos_noneg_post'] = f'{p_pos_noneg_post:.2%}'
        stats['p_pos_noneg'] = f'{p_pos_noneg:.2%}'
        stats['p_nopos_neg_pre'] = f'{p_nopos_neg_pre:.2%}'
        stats['p_nopos_neg_post'] = f'{p_nopos_neg_post:.2%}'
        stats['p_nopos_neg'] = f'{p_nopos_neg:.2%}'
        stats['p_nopos_noneg_pre'] = f'{p_nopos_noneg_pre:.2%}'
        stats['p_nopos_noneg_post'] = f'{p_nopos_noneg_post:.2%}'
        stats['p_nopos_noneg'] = f'{p_nopos_noneg:.2%}'

        stats['iv_p_nopos_pre'] = f'{iv_p_nopos_pre:.2%}'
        stats['iv_p_nopos_post'] = f'{iv_p_nopos_post:.2%}'
        stats['iv_p_nopos'] = f'{iv_p_nopos:.2%}'
        stats['noiv_p_nopos_pre'] = f'{noiv_p_nopos_pre:.2%}'
        stats['noiv_p_nopos_post'] = f'{noiv_p_nopos_post:.2%}'
        stats['noiv_p_nopos'] = f'{noiv_p_nopos:.2%}'
        stats['iv_p_neg_pre'] = f'{iv_p_neg_pre:.2%}'
        stats['iv_p_neg_post'] = f'{iv_p_neg_post:.2%}'
        stats['iv_p_neg'] = f'{iv_p_neg:.2%}'
        stats['noiv_p_neg_pre'] = f'{noiv_p_neg_pre:.2%}'
        stats['noiv_p_neg_post'] = f'{noiv_p_neg_post:.2%}'
        stats['noiv_p_neg'] = f'{noiv_p_neg:.2%}'
        stats['iv_p_nopos_neg_pre'] = f'{iv_p_nopos_neg_pre:.2%}'
        stats['iv_p_nopos_neg_post'] = f'{iv_p_nopos_neg_post:.2%}'
        stats['iv_p_nopos_neg'] = f'{iv_p_nopos_neg:.2%}'
        stats['noiv_p_nopos_neg_pre'] = f'{noiv_p_nopos_neg_pre:.2%}'
        stats['noiv_p_nopos_neg_post'] = f'{noiv_p_nopos_neg_post:.2%}'
        stats['noiv_p_nopos_neg'] = f'{noiv_p_nopos_neg:.2%}'

        stats['iv_citsa_pre'] = f'{float(iv_citsa_pre):.4f}'
        stats['iv_citsa_post'] = f'{float(iv_citsa_post):.4f}'
        stats['iv_citsa'] = f'{float(iv_citsa):.4f}'
        stats['noiv_citsa_pre'] = f'{float(noiv_citsa_pre):.4f}'
        stats['noiv_citsa_post'] = f'{float(noiv_citsa_post):.4f}'
        stats['noiv_citsa'] = f'{float(noiv_citsa):.4f}'
        stats['citsa_increase_pre'] = f'{float(citsa_increase_pre):.2%}'
        stats['citsa_increase_post'] = f'{float(citsa_increase_post):.2%}'
        stats['citsa_increase'] = f'{float(citsa_increase):.2%}'
        stats['iv_iitsa_pre'] = f'{iv_iitsa_pre:.4f}'
        stats['iv_iitsa_post'] = f'{iv_iitsa_post:.4f}'
        stats['iv_iitsa'] = f'{iv_iitsa:.4f}'
        stats['noiv_iitsa_pre'] = f'{noiv_iitsa_pre:.4f}'
        stats['noiv_iitsa_post'] = f'{noiv_iitsa_post:.4f}'
        stats['noiv_iitsa'] = f'{noiv_iitsa:.4f}'
        stats['iitsa_increase_pre'] = f'{iitsa_increase_pre:.2%}'
        stats['iitsa_increase_post'] = f'{iitsa_increase_post:.2%}'
        stats['iitsa_increase'] = f'{iitsa_increase:.2%}'

        stats['good_evals_pre_mean'] = (
            f'{good_eval_per_artifact_pre.mean():.2f}'
        )
        stats['good_evals_pre_std'] = f'{good_eval_per_artifact_pre.std():.2f}'
        stats['good_evals_pre_min'] = f'{good_eval_per_artifact_pre.min():.2f}'
        stats['good_evals_pre_max'] = f'{good_eval_per_artifact_pre.max():.2f}'
        stats['good_evals_post_mean'] = (
            f'{good_eval_per_artifact_post.mean():.2f}'
        )
        stats['good_evals_post_std'] = (
            f'{good_eval_per_artifact_post.std():.2f}'
        )
        stats['good_evals_post_min'] = (
            f'{good_eval_per_artifact_post.min():.2f}'
        )
        stats['good_evals_post_max'] = (
            f'{good_eval_per_artifact_post.max():.2f}'
        )
        stats['good_evals_mean'] = f'{good_eval_per_artifact.mean():.2f}'
        stats['good_evals_std'] = f'{good_eval_per_artifact.std():.2f}'
        stats['good_evals_min'] = f'{good_eval_per_artifact.min():.2f}'
        stats['good_evals_max'] = f'{good_eval_per_artifact.max():.2f}'

        stats['bad_evals_pre_mean'] = f'{bad_eval_per_artifact_pre.mean():.2f}'
        stats['bad_evals_pre_std'] = f'{bad_eval_per_artifact_pre.std():.2f}'
        stats['bad_evals_pre_min'] = f'{bad_eval_per_artifact_pre.min():.2f}'
        stats['bad_evals_pre_max'] = f'{bad_eval_per_artifact_pre.max():.2f}'
        stats['bad_evals_post_mean'] = (
            f'{bad_eval_per_artifact_post.mean():.2f}'
        )
        stats['bad_evals_post_std'] = f'{bad_eval_per_artifact_post.std():.2f}'
        stats['bad_evals_post_min'] = f'{bad_eval_per_artifact_post.min():.2f}'
        stats['bad_evals_post_max'] = f'{bad_eval_per_artifact_post.max():.2f}'
        stats['bad_evals_mean'] = f'{bad_eval_per_artifact.mean():.2f}'
        stats['bad_evals_std'] = f'{bad_eval_per_artifact.std():.2f}'
        stats['bad_evals_min'] = f'{bad_eval_per_artifact.min():.2f}'
        stats['bad_evals_max'] = f'{bad_eval_per_artifact.max():.2f}'

        stats['good_evals_iv_pre_mean'] = (
            f'{good_eval_iv_per_artifact_pre.mean():.2f}'
        )
        stats['good_evals_iv_pre_std'] = (
            f'{good_eval_iv_per_artifact_pre.std():.2f}'
        )
        stats['good_evals_iv_pre_min'] = (
            f'{good_eval_iv_per_artifact_pre.min():.2f}'
        )
        stats['good_evals_iv_pre_max'] = (
            f'{good_eval_iv_per_artifact_pre.max():.2f}'
        )
        stats['good_evals_iv_post_mean'] = (
            f'{good_eval_iv_per_artifact_post.mean():.2f}'
        )
        stats['good_evals_iv_post_std'] = (
            f'{good_eval_iv_per_artifact_post.std():.2f}'
        )
        stats['good_evals_iv_post_min'] = (
            f'{good_eval_iv_per_artifact_post.min():.2f}'
        )
        stats['good_evals_iv_post_max'] = (
            f'{good_eval_iv_per_artifact_post.max():.2f}'
        )
        stats['good_evals_iv_mean'] = f'{good_eval_iv_per_artifact.mean():.2f}'
        stats['good_evals_iv_std'] = f'{good_eval_iv_per_artifact.std():.2f}'
        stats['good_evals_iv_min'] = f'{good_eval_iv_per_artifact.min():.2f}'
        stats['good_evals_iv_max'] = f'{good_eval_iv_per_artifact.max():.2f}'

        stats['bad_evals_iv_pre_mean'] = (
            f'{bad_eval_iv_per_artifact_pre.mean():.2f}'
        )
        stats['bad_evals_iv_pre_std'] = (
            f'{bad_eval_iv_per_artifact_pre.std():.2f}'
        )
        stats['bad_evals_iv_pre_min'] = (
            f'{bad_eval_iv_per_artifact_pre.min():.2f}'
        )
        stats['bad_evals_iv_pre_max'] = (
            f'{bad_eval_iv_per_artifact_pre.max():.2f}'
        )
        stats['bad_evals_iv_post_mean'] = (
            f'{bad_eval_iv_per_artifact_post.mean():.2f}'
        )
        stats['bad_evals_iv_post_std'] = (
            f'{bad_eval_iv_per_artifact_post.std():.2f}'
        )
        stats['bad_evals_iv_post_min'] = (
            f'{bad_eval_iv_per_artifact_post.min():.2f}'
        )
        stats['bad_evals_iv_post_max'] = (
            f'{bad_eval_iv_per_artifact_post.max():.2f}'
        )
        stats['bad_evals_iv_mean'] = f'{bad_eval_iv_per_artifact.mean():.2f}'
        stats['bad_evals_iv_std'] = f'{bad_eval_iv_per_artifact.std():.2f}'
        stats['bad_evals_iv_min'] = f'{bad_eval_iv_per_artifact.min():.2f}'
        stats['bad_evals_iv_max'] = f'{bad_eval_iv_per_artifact.max():.2f}'

        stats['good_evals_noiv_pre_mean'] = (
            f'{good_eval_noiv_per_artifact_pre.mean():.2f}'
        )
        stats['good_evals_noiv_pre_std'] = (
            f'{good_eval_noiv_per_artifact_pre.std():.2f}'
        )
        stats['good_evals_noiv_pre_min'] = (
            f'{good_eval_noiv_per_artifact_pre.min():.2f}'
        )
        stats['good_evals_noiv_pre_max'] = (
            f'{good_eval_noiv_per_artifact_pre.max():.2f}'
        )
        stats['good_evals_noiv_post_mean'] = (
            f'{good_eval_noiv_per_artifact_post.mean():.2f}'
        )
        stats['good_evals_noiv_post_std'] = (
            f'{good_eval_noiv_per_artifact_post.std():.2f}'
        )
        stats['good_evals_noiv_post_min'] = (
            f'{good_eval_noiv_per_artifact_post.min():.2f}'
        )
        stats['good_evals_noiv_post_max'] = (
            f'{good_eval_noiv_per_artifact_post.max():.2f}'
        )
        stats['good_evals_noiv_mean'] = (
            f'{good_eval_noiv_per_artifact.mean():.2f}'
        )
        stats['good_evals_noiv_std'] = (
            f'{good_eval_noiv_per_artifact.std():.2f}'
        )
        stats['good_evals_noiv_min'] = (
            f'{good_eval_noiv_per_artifact.min():.2f}'
        )
        stats['good_evals_noiv_max'] = (
            f'{good_eval_noiv_per_artifact.max():.2f}'
        )

        stats['bad_evals_noiv_pre_mean'] = (
            f'{bad_eval_noiv_per_artifact_pre.mean():.2f}'
        )
        stats['bad_evals_noiv_pre_std'] = (
            f'{bad_eval_noiv_per_artifact_pre.std():.2f}'
        )
        stats['bad_evals_noiv_pre_min'] = (
            f'{bad_eval_noiv_per_artifact_pre.min():.2f}'
        )
        stats['bad_evals_noiv_pre_max'] = (
            f'{bad_eval_noiv_per_artifact_pre.max():.2f}'
        )
        stats['bad_evals_noiv_post_mean'] = (
            f'{bad_eval_noiv_per_artifact_post.mean():.2f}'
        )
        stats['bad_evals_noiv_post_std'] = (
            f'{bad_eval_noiv_per_artifact_post.std():.2f}'
        )
        stats['bad_evals_noiv_post_min'] = (
            f'{bad_eval_noiv_per_artifact_post.min():.2f}'
        )
        stats['bad_evals_noiv_post_max'] = (
            f'{bad_eval_noiv_per_artifact_post.max():.2f}'
        )
        stats['bad_evals_noiv_mean'] = (
            f'{bad_eval_noiv_per_artifact.mean():.2f}'
        )
        stats['bad_evals_noiv_std'] = f'{bad_eval_noiv_per_artifact.std():.2f}'
        stats['bad_evals_noiv_min'] = f'{bad_eval_noiv_per_artifact.min():.2f}'
        stats['bad_evals_noiv_max'] = f'{bad_eval_noiv_per_artifact.max():.2f}'

        return stats

    def _calculate_cronbachs_alphas(self) -> Dict[str, str]:
        good_eval_matrix = self.matrices['good_evals']
        good_eval_correlations = artifact_correlations(good_eval_matrix)
        positive_action_matrix = self.matrices['positive_actions']
        positive_action_correlations = artifact_correlations(positive_action_matrix)
        positive_action_alpha = cronbachs_alpha(positive_action_correlations)
        good_eval_alpha = cronbachs_alpha(good_eval_correlations)
        return {'good_eval': f'{good_eval_alpha:.2f}',
                'positive_action': f'{positive_action_alpha:.2f}'}

    def create_plots(self) -> None:
        self._plot_reactions_by_artifact_relative()
        self._plot_iitsa_kernel_density('pre')
        self._plot_iitsa_kernel_density('post')
        self._plot_good_eval_correlations()
        self._plot_positive_action_correlations()

    def _plot_good_eval_correlations(self) -> None:
        good_eval_matrix = self.matrices['good_evals']
        correlations = artifact_correlations(good_eval_matrix)
        plt_path = os.path.join(self.img_dir, 'fig_good_eval_correlation_distplot.pdf')
        Plotter.distplot(correlations, plt_path)

    def _plot_positive_action_correlations(self) -> None:
        positive_action_matrix = self.matrices['positive_actions']
        correlations = artifact_correlations(positive_action_matrix)
        plt_path = os.path.join(self.img_dir, 'fig_positive_action_correlation_distplot.pdf')
        Plotter.distplot(correlations, plt_path)

    def _plot_reactions_by_artifact_relative(self) -> None:
        def query_reports(query: str) -> DataFrame:
            results_pre = self.reports['pre'].query(query)
            results_post = self.reports['post'].query(query)
            return pd.concat([results_pre, results_post], sort=False)

        artifacts = list(query_reports('course_of_action == "arm"')['recipe'].unique())
        no_reactions: Dict[str, List[int]] = {
            'good': [],
            'bad': [],
            'good_and_bad': []
        }
        for artifact in artifacts:
            artifact_traces = query_reports(f'recipe == "{artifact}"')
            no_participants = artifact_traces['subject_id'].nunique()
            good_reactions = artifact_traces.query('score > 0')
            bad_reactions = artifact_traces.query('score < 0')
            good_reaction_subjects = set(good_reactions['subject_id'])
            bad_reaction_subjects = set(bad_reactions['subject_id'])
            no_reactions['good'].append(-len(good_reaction_subjects) / no_participants)
            no_reactions['bad'].append(len(bad_reaction_subjects) / no_participants)
            no_reactions['good_and_bad'].append(len(good_reaction_subjects &
                                                    bad_reaction_subjects) /
                                                no_participants)

        plt_path = os.path.join(self.img_dir, 'fig_reactions_by_artifact_relative.pdf')
        phase1_artifact_amount = len(self.series_pre_data['artifacts'])
        Plotter.reactions_by_artifact_relative(artifacts,
                                               no_reactions,
                                               phase1_artifact_amount,
                                               plt_path)

    def _plot_iitsa_kernel_density(self, phase: str) -> None:
        queries = [f'arms_{phase} > 0 and schooled == 1',
                   f'arms_{phase} > 0 and schooled == 0']
        iitsas = [self.subjects.query(query)[f'#good_evaluation_{phase}'] for query in queries]
        iv_subjects = self.subjects.query(queries[0])
        noiv_subjects = self.subjects.query(queries[1])
        iitsa_iv = (iv_subjects[f'#good_evaluation_{phase}'] /
                    iv_subjects[f'arms_{phase}'])
        iitsa_noiv = (noiv_subjects[f'#good_evaluation_{phase}'] /
                      noiv_subjects[f'arms_{phase}'])
        phase_no = 1 if phase == 'pre' else 2
        plt_path = os.path.join(self.img_dir, f'fig_phase_{phase_no}_iitsa_kde.pdf')
        Plotter.iitsa_kde(iitsas, iitsa_iv, iitsa_noiv, plt_path, phase_no)
