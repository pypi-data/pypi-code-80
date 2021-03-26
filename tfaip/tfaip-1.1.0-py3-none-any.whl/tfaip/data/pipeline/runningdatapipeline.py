# Copyright 2021 The tfaip authors. All Rights Reserved.
#
# This file is part of tfaip.
#
# tfaip is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# tfaip is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along with
# tfaip. If not, see http://www.gnu.org/licenses/.
# ==============================================================================
"""Implementation of the RunningDataPipeline"""
import itertools
import json
from typing import TYPE_CHECKING, Iterable, List, Optional

import numpy as np
import tensorflow as tf
from tensorflow.python.data.experimental import bucket_by_sequence_length

from tfaip import Sample, PipelineMode
from tfaip.util.multiprocessing.parallelmap import tqdm_wrapper

if TYPE_CHECKING:
    from tfaip.data.pipeline.datapipeline import DataPipeline


def compute_limit(limit, batch_size):
    assert limit != 0, 'The limit must not be 0 if calling this method.'
    if limit < 0:
        return limit  # no limit
    else:
        return -(-limit // batch_size)  # ceiled integer div => 1 // 3 = 1; 3 // 3 => 1; 4 // 3 = 2


class RunningDataPipeline:
    """
    The RunningDataPipeline provides the actual methods to obtain and generate samples.
    For the input data using the pre_proc-Pipeline call
    - `generate_input_samples()` to iterate over single (non-batched) samples, the output of the pre-proc-Pipeline
    - `input_dataset()` to obtain a tf.data.Dataset which is batched and padded and ready to use for a `keras.Model`.

    To apply the output pipeline call `process_output`.

    The RunningDataPipeline is created by entering a DataPipeline:
    ```
    with DataPipeline() as running_data_pipeline:
       # running_data_pipeline.generate_input_samples()
       # running_data_pipeline.input_dataset()
    ```
    This ensures that the threads created within the pipelines are joined upon exit.

    See Also:
        - DataPipeline
        - TFDatasetGenerator
    """

    def __init__(self, data_pipeline: 'DataPipeline'):
        self.data_pipeline = data_pipeline
        self.pipeline_params = data_pipeline.pipeline_params
        self.mode = data_pipeline.mode
        self.data_generator = self.data_pipeline.create_data_generator()

    def __len__(self):
        """
        The number of samples produced by the data generator.
        Note that this might not correspond to the number of examples produced by the pre-proc-pipeline if
        `GeneratingDataProcessors` are used.
        """
        real_len = len(self.data_generator)
        if self.pipeline_params.limit > 0:
            return min(self.pipeline_params.limit, real_len)
        return real_len

    def process_output(self, samples: Iterable[Sample]) -> Iterable[Sample]:
        """
        Apply the post-processing pipeline to the given samples.
        """
        output_pipeline = self.data_pipeline.create_output_pipeline()

        def extract_meta(sample: Sample) -> Sample:
            meta = sample.meta or {}
            if 'meta' in sample.inputs:
                input_meta = sample.inputs['meta']
                if isinstance(input_meta, (list, np.ndarray)):
                    assert len(input_meta) == 1, 'This must be one, just be sure'
                    input_meta = input_meta[0]

                meta.update(**json.loads(input_meta))
            return sample.new_meta(meta)

        samples = map(extract_meta, samples)

        if output_pipeline:
            return output_pipeline.apply(samples)
        return samples

    def input_dataset(self, auto_repeat=None) -> Optional['tf.data.Dataset']:
        """
        Obtain the batched, padded, prefetched tf.data.Dataset of the input.
        """
        if len(self) == 0:
            # Empty set
            return None

        tf_dataset_generator = self.data_pipeline.create_tf_dataset_generator()
        dataset = tf_dataset_generator.create(lambda: self.generate_input_samples(auto_repeat))
        return self._wrap_dataset(dataset)

    def preload_input_samples(self, progress_bar=True, non_preloadable_params: Optional[List] = None) -> List[Sample]:
        """
        Applies all pre-proc DataProcessors marked as `preloadable` to the samples of the `DataGenerator` and
        returns a list of the `Samples`. `DataProcessors` that were not applied are added to the
        `non_preloadable_params`.

        See Also:
            `DataPipeline.as_preloaded` uses this to convert the Pipeline to a pipeline with a `RawDataGenerator`
        """
        non_preloadable_params = non_preloadable_params if non_preloadable_params is not None else []
        data_generator = self.data_generator
        old_limit = self.pipeline_params.limit
        self.pipeline_params.limit = len(data_generator)

        # Load the samples
        last_generator = list(tqdm_wrapper(data_generator.generate(), progress_bar=progress_bar,
                                           total=len(data_generator), desc='Loading samples'))
        # Obtain the list of preprocessors that are valid to use (preloadable) and apply them one by one
        processors = self.data_pipeline.flat_input_processors(preload=True,
                                                              non_preloadable_params=non_preloadable_params)
        for processor in processors:
            last_generator = processor.preload(last_generator,
                                               num_processes=self.pipeline_params.num_processes,
                                               progress_bar=progress_bar,
                                               )
            last_generator = list(last_generator)

        self.pipeline_params.limit = old_limit
        return last_generator

    def generate_input_samples(self, auto_repeat=None) -> Iterable[Sample]:
        """
        Obtain the samples after applying the pre-proc pipeline

        Params:
            auto_repeat: if None, auto repeat defaults to True on Training else to False.
        """
        data_generator = self.data_generator
        if auto_repeat is None:
            auto_repeat = self.mode == PipelineMode.TRAINING and self.pipeline_params.limit < 0

        input_pipeline = self.data_pipeline.create_input_pipeline()

        # Do-while-loop required if auto_repeat==True
        while True:
            # get the Iterator[Samples] from the data generator and apply the limit if set
            generate = data_generator.generate()
            if self.data_pipeline.pipeline_params.limit > 0:
                generate = itertools.islice(generate, self.data_pipeline.pipeline_params.limit)

            # Apply the input pipeline
            if input_pipeline:
                for s in input_pipeline.apply(generate):
                    yield s
            else:
                for s in generate:
                    yield s

            if not auto_repeat:
                # Stop of auto repeat is false
                break

    def _wrap_padded_batch(self, dataset: 'tf.data.Dataset') -> 'tf.data.Dataset':
        """
        Pad and batch a tf.data.Dataset
        """
        pipeline_params = self.data_pipeline.pipeline_params
        data = self.data_pipeline.data
        pad_values = data.padding_values()

        def default(dtype):
            if dtype == tf.bool:
                return False
            return '' if dtype == tf.string else 0

        meta_shapes = {k: v.shape for k, v in data.meta_layer_specs().items()}
        meta_values = {k: tf.constant(pad_values.get(k, default(v.dtype)), dtype=v.dtype) for k, v in
                       data.meta_layer_specs().items()}
        if self.mode == PipelineMode.PREDICTION:
            shapes = ({k: v.shape for k, v in data.input_layer_specs().items()}, meta_shapes)
            values = ({k: tf.constant(pad_values.get(k, default(v.dtype)), dtype=v.dtype) for k, v in
                       data.input_layer_specs().items()}, meta_values)
        elif self.mode == PipelineMode.TARGETS:
            shapes = ({k: v.shape for k, v in data.target_layer_specs().items()}, meta_shapes)
            values = ({k: tf.constant(pad_values.get(k, default(v.dtype)), dtype=v.dtype) for k, v in
                       data.target_layer_specs().items()}, meta_values)
        else:
            shapes = (
                {k: v.shape for k, v in data.input_layer_specs().items()},
                {k: v.shape for k, v in data.target_layer_specs().items()},
                meta_shapes,
            )
            values = (
                {k: tf.constant(pad_values.get(k, default(v.dtype)), dtype=v.dtype) for k, v in
                 data.input_layer_specs().items()},
                {k: tf.constant(pad_values.get(k, default(v.dtype)), dtype=v.dtype) for k, v in
                 data.target_layer_specs().items()},
                meta_values,
            )

        if pipeline_params.bucket_boundaries:
            data_elem_len_fn = data.element_length_fn()

            def element_length_func(*args):
                inputs = args[0]
                return data_elem_len_fn(inputs)

            num_buckets = len(pipeline_params.bucket_boundaries) + 1
            bucket_batch_sizes = pipeline_params.bucket_batch_sizes or [pipeline_params.batch_size] * num_buckets
            return dataset.apply(bucket_by_sequence_length(
                element_length_func=element_length_func,
                bucket_batch_sizes=bucket_batch_sizes,
                bucket_boundaries=pipeline_params.bucket_boundaries,
                padded_shapes=shapes,
                padding_values=values,
                drop_remainder=pipeline_params.batch_drop_remainder,
            ))
        else:
            return dataset.padded_batch(pipeline_params.batch_size, shapes, values,
                                        drop_remainder=pipeline_params.batch_drop_remainder)

    def _wrap_dataset(self, dataset: tf.data.Dataset) -> tf.data.Dataset:
        """
        Shuffle, pad, batch, and prefetch a tf.data.Dataset
        """
        pipeline_params = self.data_pipeline.pipeline_params
        if pipeline_params.shuffle_buffer_size > 1:
            dataset = dataset.shuffle(pipeline_params.shuffle_buffer_size)
        if self.data_pipeline.auto_batch:
            dataset = self._wrap_padded_batch(dataset)
        if pipeline_params.prefetch > 0:
            dataset = dataset.prefetch(pipeline_params.prefetch)
        dataset = dataset.take(compute_limit(pipeline_params.limit, pipeline_params.batch_size))
        return dataset
