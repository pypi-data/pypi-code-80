import os
from typing import Any, Dict, List

import mpmath
import numpy as np
from pandas import DataFrame

from awarenessometer.stats_helper import collective_awareness
from awarenessometer.stats_helper import artifact_correlations
from awarenessometer.stats_helper import cronbachs_alpha
from awarenessometer.plotter import Plotter


class LabeledStudy:
    def __init__(self,
                 employees_with_vdu: int,
                 series_info: Dict[str, Any],
                 img_dir: str):
        self.type = 'labeled'
        self.employees_with_vdu = employees_with_vdu
        self.series_data: Dict = series_info['series_data']
        self.subjects: DataFrame = series_info['subject_df']
        self.report: DataFrame = series_info['report']
        self.matrices: Dict[str, np.array] = series_info['matrices']
        self.img_dir = img_dir

    def create_tokens(self) -> Dict:
        tokens = {
            'series_info': self._get_series_info(),
            'participation_stats': self._participation_stats(),
            'reaction_stats': self._reaction_stats(),
            'artifacts': self._get_artifacts(),
            'cronbachs_alpha': self._calculate_cronbachs_alphas()
        }
        return tokens

    def _get_artifacts(self) -> List:
        artifacts = []
        images = os.listdir(self.img_dir)
        for artifact in self.series_data['artifacts']:
            artifact_images = sorted([os.path.join('img', img)
                                      for img in images
                                      if img.startswith(artifact)])
            artifact = {'recipe_id': artifact, 'images': artifact_images}
            artifacts.append(artifact)
        return artifacts

    def _get_series_info(self) -> Dict:
        label = self.series_data['label']
        start = self.series_data['start'].strftime('%Y-%m-%d %H:%M:%S')
        end = self.series_data['end'].strftime('%Y-%m-%d %H:%M:%S')
        no_participants = len(self.series_data['participants'])
        no_artifacts = len(self.series_data['artifacts'])
        info = {
            'title': label,
            'start': start,
            'end': end,
            '#participants': no_participants,
            '#artifacts': no_artifacts
        }
        return info

    def _participation_stats(self) -> Dict:
        no_participants = self.subjects.shape[0]
        stats = {}

        no_schooled = self.subjects.query('schooled == 1').shape[0]
        share_schooled = no_schooled / (no_participants / 100)
        stats['#schooled'] = f'{no_schooled} ({share_schooled:.2f}%)'

        no_armed = self.subjects.query('arms >= 1').shape[0]
        share_armed = no_armed / (no_participants / 100)
        stats['#armed'] = f'{no_armed} ({share_armed:.2f}%)'

        no_missed = no_participants - no_armed
        share_missed = no_missed / (no_participants / 100)
        stats['#missed'] = f'{no_missed} ({share_missed:.2f}%)'

        arms = self.subjects['arms']
        stats['#artifacts'] = (f'{arms.mean():.2f} {arms.std():.2f} {arms.min()} {arms.max()}')

        return stats

    # pylint: disable=too-many-locals,too-many-statements
    def _reaction_stats(self) -> Dict:
        stats = {}
        no_arms = self.subjects['arms'].sum()

        # positive and negative actions
        p_pos = self.subjects['#pos'].sum() / no_arms
        p_nopos = 1 - p_pos
        p_pos_neg = self.subjects['#pos_neg'].sum() / no_arms
        # bad_evaluation = neg - pos == nopos_neg
        p_nopos_neg = self.subjects['#bad_evaluation'].sum() / no_arms
        p_pos_noneg = p_pos - p_pos_neg
        p_nopos_noneg = p_nopos - p_nopos_neg

        # class statistics
        armed_subjects = self.subjects.query('arms > 0')
        iv_subjects = armed_subjects.query('schooled == 1')
        noiv_subjects = armed_subjects.query('schooled == 0')
        no_iv_arms = iv_subjects['arms'].sum()
        no_noiv_arms = noiv_subjects['arms'].sum()

        # prefix iv means that the probability is only applied to iv
        # participants, i.e. iv_p_nopos = P(nopos | iv)
        iv_p_nopos = (iv_subjects['arms'] - iv_subjects['#pos']).sum() / no_iv_arms
        noiv_p_nopos = (noiv_subjects['arms'] - noiv_subjects['#pos']).sum() / no_noiv_arms
        iv_p_neg = iv_subjects['#neg'].sum() / no_iv_arms
        noiv_p_neg = noiv_subjects['#neg'].sum() / no_noiv_arms
        iv_p_nopos_neg = iv_subjects['#bad_evaluation'].sum() / no_iv_arms
        noiv_p_nopos_neg = noiv_subjects['#bad_evaluation'].sum() / no_noiv_arms

        # collective and individual awareness
        iv_citsa = collective_awareness(iv_p_nopos_neg, iv_p_nopos, self.employees_with_vdu)
        noiv_citsa = collective_awareness(noiv_p_nopos_neg, noiv_p_nopos, self.employees_with_vdu)
        citsa_increase = mpmath.fdiv(mpmath.fsub(iv_citsa, noiv_citsa), noiv_citsa)

        iv_iitsa = iv_subjects['#good_evaluation'].sum() / no_iv_arms
        noiv_iitsa = noiv_subjects['#good_evaluation'].sum() / no_noiv_arms
        iitsa_increase = (iv_iitsa - noiv_iitsa) / noiv_iitsa

        # more in depth stats
        good_eval_per_artifact = armed_subjects['#good_evaluation'] / armed_subjects['arms']
        bad_eval_per_artifact = armed_subjects['#bad_evaluation'] / armed_subjects['arms']
        good_eval_iv_per_artifact = iv_subjects['#good_evaluation'] / iv_subjects['arms']
        bad_eval_iv_per_artifact = iv_subjects['#bad_evaluation'] / iv_subjects['arms']
        good_eval_noiv_per_artifact = noiv_subjects['#good_evaluation'] / noiv_subjects['arms']
        bad_eval_noiv_per_artifact = noiv_subjects['#bad_evaluation'] / noiv_subjects['arms']

        stats['p_nopos'] = f'{p_nopos:.2%}'
        stats['p_pos_neg'] = f'{p_pos_neg:.2%}'
        stats['p_pos_noneg'] = f'{p_pos_noneg:.2%}'
        stats['p_nopos_neg'] = f'{p_nopos_neg:.2%}'
        stats['p_nopos_noneg'] = f'{p_nopos_noneg:.2%}'

        stats['iv_p_nopos'] = f'{iv_p_nopos:.2%}'
        stats['noiv_p_nopos'] = f'{noiv_p_nopos:.2%}'
        stats['iv_p_neg'] = f'{iv_p_neg:.2%}'
        stats['noiv_p_neg'] = f'{noiv_p_neg:.2%}'
        stats['iv_p_nopos_neg'] = f'{iv_p_nopos_neg:.2%}'
        stats['noiv_p_nopos_neg'] = f'{noiv_p_nopos_neg:.2%}'

        stats['iv_citsa'] = f'{float(iv_citsa):.4f}'
        stats['noiv_citsa'] = f'{float(noiv_citsa):.4f}'
        stats['citsa_increase'] = f'{float(citsa_increase):.2%}'
        stats['iv_iitsa'] = f'{iv_iitsa:.4f}'
        stats['noiv_iitsa'] = f'{noiv_iitsa:.4f}'
        stats['iitsa_increase'] = f'{iitsa_increase:.2%}'

        stats['good_evals_mean'] = f'{good_eval_per_artifact.mean():.2f}'
        stats['good_evals_std'] = f'{good_eval_per_artifact.std():.2f}'
        stats['good_evals_min'] = f'{good_eval_per_artifact.min():.2f}'
        stats['good_evals_max'] = f'{good_eval_per_artifact.max():.2f}'

        stats['bad_evals_mean'] = f'{bad_eval_per_artifact.mean():.2f}'
        stats['bad_evals_std'] = f'{bad_eval_per_artifact.std():.2f}'
        stats['bad_evals_min'] = f'{bad_eval_per_artifact.min():.2f}'
        stats['bad_evals_max'] = f'{bad_eval_per_artifact.max():.2f}'

        stats['good_evals_iv_mean'] = f'{good_eval_iv_per_artifact.mean():.2f}'
        stats['good_evals_iv_std'] = f'{good_eval_iv_per_artifact.std():.2f}'
        stats['good_evals_iv_min'] = f'{good_eval_iv_per_artifact.min():.2f}'
        stats['good_evals_iv_max'] = f'{good_eval_iv_per_artifact.max():.2f}'

        stats['bad_evals_iv_mean'] = f'{bad_eval_iv_per_artifact.mean():.2f}'
        stats['bad_evals_iv_std'] = f'{bad_eval_iv_per_artifact.std():.2f}'
        stats['bad_evals_iv_min'] = f'{bad_eval_iv_per_artifact.min():.2f}'
        stats['bad_evals_iv_max'] = f'{bad_eval_iv_per_artifact.max():.2f}'

        stats['good_evals_noiv_mean'] = f'{good_eval_noiv_per_artifact.mean():.2f}'
        stats['good_evals_noiv_std'] = f'{good_eval_noiv_per_artifact.std():.2f}'
        stats['good_evals_noiv_min'] = f'{good_eval_noiv_per_artifact.min():.2f}'
        stats['good_evals_noiv_max'] = f'{good_eval_noiv_per_artifact.max():.2f}'

        stats['bad_evals_noiv_mean'] = f'{bad_eval_noiv_per_artifact.mean():.2f}'
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
        self._plot_iitsa_kernel_density()
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
        artifacts = list(self.report.query('course_of_action == "arm"')['recipe'].unique())
        no_reactions: Dict[str, List[int]] = {
            'bad': [],
            'good': [],
            'good_and_bad': []
        }
        # pylint: disable=unused-variable
        for artifact in artifacts:
            artifact_traces = self.report.query('recipe == @artifact')
            no_participants = artifact_traces['subject_id'].nunique()
            good_reactions = artifact_traces.query('score > 0')
            bad_reactions = artifact_traces.query('score < 0')
            good_reaction_subjects = set(good_reactions['subject_id'])
            bad_reaction_subjects = set(bad_reactions['subject_id'])
            no_reactions['good'].append(-len(good_reaction_subjects) / no_participants)
            no_reactions['bad'].append(len(bad_reaction_subjects) / no_participants)
            no_reactions['good_and_bad'].append(len(good_reaction_subjects &
                                                    bad_reaction_subjects) / no_participants)

        plt_path = os.path.join(self.img_dir, 'fig_reactions_by_artifact_relative.pdf')
        Plotter.reactions_by_artifact_relative(artifacts, no_reactions, 0, plt_path)

    def _plot_iitsa_kernel_density(self) -> None:
        queries = ['arms > 0 and schooled == 1', 'arms > 0 and schooled == 0']
        iitsas = [self.subjects.query(query)['#good_evaluation'] for query in queries]
        iv_subjects = self.subjects.query(queries[0])
        noiv_subjects = self.subjects.query(queries[1])
        iitsa_iv = iv_subjects['#good_evaluation'] / iv_subjects['arms']
        iitsa_noiv = noiv_subjects['#good_evaluation'] / noiv_subjects['arms']
        plt_path = os.path.join(self.img_dir, 'fig_iitsa_kde.pdf')
        Plotter.iitsa_kde(iitsas, iitsa_iv, iitsa_noiv, plt_path, 0)
