from typing import Dict, List, Iterable

import pandas as pd
import numpy as np
from pandas import DataFrame


class DataPreprocessor:
    # pylint:disable=too-many-locals
    @staticmethod
    def get_good_evaluations(reports: Iterable[DataFrame],
                             artifacts: List[str],
                             iv_participants: Iterable[DataFrame]) -> np.array:
        report = pd.concat(reports)
        iv_participants = pd.concat(iv_participants)
        subjects = sorted(list(set(iv_participants['subject'])))
        good_eval_matrix = np.zeros((len(subjects), len(artifacts)))
        for artifact_index, artifact in enumerate(artifacts):  # pylint:disable=unused-variable
            artifact_traces = report.query('recipe == @artifact')
            for subject_index, subject in enumerate(subjects):  # pylint:disable=unused-variable
                good_evaluation = np.nan
                subject_traces = artifact_traces.query('subject_id == @subject')
                scores = set()
                for _, data in subject_traces.iterrows():
                    scores.add(data['score'])
                if scores:
                    good_evaluation = 0
                    if (not any([score < 0 for score in scores]) or
                            any([score > 0 for score in scores])):
                        good_evaluation = 1
                good_eval_matrix[subject_index, artifact_index] = good_evaluation
        return good_eval_matrix

    @staticmethod
    def get_positive_actions(reports: Iterable[DataFrame],
                             artifacts: List[str],
                             iv_participants: Iterable[DataFrame]) -> np.array:
        report = pd.concat(reports)
        iv_participants = pd.concat(iv_participants)
        subjects = sorted(list(set(iv_participants['subject'])))
        positive_action_matrix = np.zeros((len(subjects), len(artifacts)))
        for artifact_index, artifact in enumerate(artifacts):  # pylint:disable=unused-variable
            artifact_traces = report.query('recipe == @artifact')
            for subject_index, subject in enumerate(subjects):  # pylint:disable=unused-variable
                positive_action = np.nan
                subject_traces = artifact_traces.query('subject_id == @subject')
                for _, data in subject_traces.iterrows():
                    if np.isnan(positive_action):
                        positive_action = 0
                    if data['score'] > 0:
                        positive_action = 1
                positive_action_matrix[subject_index, artifact_index] = positive_action
        return positive_action_matrix

    @staticmethod
    def extend_report(report: DataFrame, series_df: DataFrame) -> DataFrame:
        """
        Adds 'armed' traces to the report

        These are generated from the series_df, but also do not reflect
        whether a subject has received an artifact (see #12).
        If #12 is addressed, this method should be changed accordingly!
        """
        tmp: Dict[str, List] = {'subject_id': [], 'recipe': [], 'score': [],
                                'course_of_action': [], 'online_time': []}
        for row in series_df.iterrows():
            if row[1]['armed']:
                tmp['subject_id'].append(row[1]['subject_id'])
                tmp['recipe'].append(row[1]['recipe'])
                tmp['score'].append(0)
                tmp['course_of_action'].append('arm')
                tmp['online_time'].append(0)
        tmp_df = pd.DataFrame(tmp)
        return pd.concat([report, tmp_df], ignore_index=True)

    @staticmethod
    def series_to_df(series: Dict, min_seconds_exposed: int) -> DataFrame:
        headers = ['subject_id', 'season', 'recipe', 'armed']
        data: Dict = {}
        for header in headers:
            data[header] = []

        for season in series['seasons']:
            for episode in season['episodes']:
                data['subject_id'].append(episode['subject_id'])
                data['season'].append(season['id'])
                data['recipe'].append(season['recipe_id'])
                data['armed'].append(episode['seconds_exposed'] >= min_seconds_exposed)
        return DataFrame(data)

    @staticmethod
    def extract_series_data(series: Dict) -> Dict:
        label = series['label']
        start = series['start_date']
        end = series['end_date']
        participants = [episode['subject_id'] for episode in series['seasons'][0]['episodes']]
        artifacts = [season['recipe_id'] for season in series['seasons']]
        data = {
            'label': label,
            'start': start,
            'end': end,
            'participants': participants,
            'artifacts': artifacts
        }
        return data

    @staticmethod
    def compute_pre_post_subject_df(series_pre: DataFrame,  # noqa
                                    series_post: DataFrame,
                                    iv_participants_pre: DataFrame,
                                    iv_participants_post: DataFrame,
                                    report_pre: DataFrame,
                                    report_post: DataFrame,
                                    raw_pseudonym_links: Dict) -> DataFrame:
        pseudonym_links = (
            DataPreprocessor.complete_pseudonym_links(raw_pseudonym_links)
        )
        iv_participants = pd.concat([iv_participants_pre, iv_participants_post])

        data: Dict = {}
        headers = ['internal_id', 'id_pre', 'id_post', 'arms_pre', 'arms_post',
                   'schooled', '#good_evaluation_pre', '#good_evaluation_post',
                   '#bad_evaluation_pre', '#bad_evaluation_post', '#pos_pre',
                   '#pos_post', '#neg_pre', '#neg_post', '#pos_neg_pre',
                   '#pos_neg_post']
        for header in headers:
            data[header] = []

        subjects_pre = series_pre['subject_id'].unique()
        for id_pre in subjects_pre:
            id_post = pseudonym_links.get(id_pre, '')
            # the following call modifies the data dict!
            DataPreprocessor._add_subject_pre_post(data,
                                                   id_pre,
                                                   id_post,
                                                   series_pre,
                                                   series_post,
                                                   iv_participants,
                                                   report_pre,
                                                   report_post)
        subjects_post = series_post['subject_id'].unique()
        for id_post in subjects_post:
            if id_post not in data['id_post']:
                id_pre = pseudonym_links.get(id_post, '')
                # the following call modifies the data dict!
                DataPreprocessor._add_subject_pre_post(data,
                                                       id_pre,
                                                       id_post,
                                                       series_pre,
                                                       series_post,
                                                       iv_participants,
                                                       report_pre,
                                                       report_post)
        return DataFrame(data)

    @staticmethod
    def compute_labeled_subject_df(series: DataFrame,
                                   iv_participants: DataFrame,
                                   report: DataFrame) -> DataFrame:
        headers = ['id', 'arms', 'schooled', '#good_evaluation',
                   '#bad_evaluation', '#pos', '#neg', '#pos_neg']
        data: Dict = {}
        for header in headers:
            data[header] = []

        subjects = series['subject_id'].unique()
        for subject_id in subjects:
            DataPreprocessor._add_subject_labeled(data, subject_id, series, iv_participants, report)
        return DataFrame(data)

    @staticmethod
    def complete_pseudonym_links(raw_pseudonym_links: Dict) -> Dict:
        links = {}
        for key, value in raw_pseudonym_links.items():
            links[value[0]] = key
            links[key] = value[0]
        return links

    @staticmethod
    def _add_subject_pre_post(data: Dict,  # noqa
                              id_pre: str,
                              id_post: str,
                              series_pre: DataFrame,
                              series_post: DataFrame,
                              iv_participants: DataFrame,
                              report_pre: DataFrame,
                              report_post: DataFrame) -> None:
        internal_id = len(data['internal_id'])
        armed_artifacts_pre = set(
            series_pre.query('subject_id == @id_pre & armed == True')['recipe'].unique()
        )
        armed_artifacts_post = set(
            series_post.query('subject_id == @id_post & armed == True')['recipe'].unique()
        )
        negative_actions_pre = set(
            report_pre.query('subject_id == @id_pre & score < 0')['recipe'].unique()
        )
        negative_actions_post = set(
            report_post.query('subject_id == @id_post & score < 0')['recipe'].unique()
        )
        positive_actions_pre = set(
            report_pre.query('subject_id == @id_pre & score > 0')['recipe'].unique()
        )
        positive_actions_post = set(
            report_post.query('subject_id == @id_post & score > 0')['recipe'].unique()
        )

        arms_pre = len(armed_artifacts_pre)
        arms_post = len(armed_artifacts_post)

        schooled = (iv_participants.query('subject == @id_pre | subject == @id_post')
                    .intervention.values[0])

        bad_evaluation_pre = negative_actions_pre - positive_actions_pre
        bad_evaluation_post = negative_actions_post - positive_actions_post
        good_evaluation_pre = armed_artifacts_pre - bad_evaluation_pre
        good_evaluation_post = armed_artifacts_post - bad_evaluation_post
        positive_negative_pre = (positive_actions_pre & negative_actions_pre)
        positive_negative_post = (positive_actions_post & negative_actions_post)

        # changes `data` in place!
        data['internal_id'].append(internal_id)
        data['id_pre'].append(id_pre)
        data['id_post'].append(id_post)
        data['arms_pre'].append(arms_pre)
        data['arms_post'].append(arms_post)
        data['schooled'].append(schooled)
        data['#good_evaluation_pre'].append(len(good_evaluation_pre))
        data['#good_evaluation_post'].append(len(good_evaluation_post))
        data['#bad_evaluation_pre'].append(len(bad_evaluation_pre))
        data['#bad_evaluation_post'].append(len(bad_evaluation_post))
        data['#pos_pre'].append(len(positive_actions_pre))
        data['#pos_post'].append(len(positive_actions_post))
        data['#neg_pre'].append(len(negative_actions_pre))
        data['#neg_post'].append(len(negative_actions_post))
        data['#pos_neg_pre'].append(len(positive_negative_pre))
        data['#pos_neg_post'].append(len(positive_negative_post))

    @staticmethod
    def _add_subject_labeled(data: Dict,  # noqa
                             subject_id: str,
                             series: DataFrame,
                             iv_participants: DataFrame,
                             report: DataFrame) -> None:
        armed_artifacts = set(
            series.query('subject_id == @subject_id & armed == True')['recipe'].unique()
        )
        negative_actions = set(
            report.query('subject_id == @subject_id & score < 0')['recipe'].unique()
        )
        positive_actions = set(
            report.query('subject_id == @subject_id & score > 0')['recipe'].unique()
        )

        arms = len(armed_artifacts)

        schooled = iv_participants.query('subject == @subject_id').intervention.values[0]

        bad_evaluation = negative_actions - positive_actions
        good_evaluation = armed_artifacts - bad_evaluation
        positive_negative = positive_actions & negative_actions

        # changes `data` in place!
        data['id'].append(subject_id)
        data['arms'].append(arms)
        data['schooled'].append(schooled)
        data['#good_evaluation'].append(len(good_evaluation))
        data['#bad_evaluation'].append(len(bad_evaluation))
        data['#pos'].append(len(positive_actions))
        data['#neg'].append(len(negative_actions))
        data['#pos_neg'].append(len(positive_negative))
