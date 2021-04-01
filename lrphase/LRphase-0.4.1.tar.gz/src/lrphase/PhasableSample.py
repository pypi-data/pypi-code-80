# coding=utf-8
import time
from typing import Any, Iterator, Optional, Dict, List, Union
import os
import pysam
from lrphase import SimulatePhasedData
import pyliftover


class PhasableSample:
    """

    """

    # haplotype_reference_sequences: Dict[int, object]
    # bam_files: object
    # reference_sequence_paths: Optional[object]

    # RG_ID_dict: object

    def __init__(
            self,
            sample: str,
            vcf_file_path: str,
            ignore_phase_sets: bool = False,
            alignment_file_paths: list = None,
            RG_ID_dict: dict = None,
            reference_sequence_names: list = None,
            reference_sequence_paths: list = None,
            simulate_haplotypes: bool = False,
            output_directory_path: str = None,
            only_autosomal: bool = False,
            regions: list = None,
            ploidy: int = None
    ) -> None:
        """

        Args:
            sample:
            vcf_file_path:
            ignore_phase_sets:
            alignment_file_paths:
            RG_ID_dict (object):
            reference_sequence_names:
            reference_sequence_paths:
            simulate_haplotypes:
            output_directory_path:
            only_autosomal:
            regions:
            ploidy:

        Returns:
            None:
        """
        self.simulate_haplotypes = simulate_haplotypes
        self.haplotype_simulated_reads = {}
        self.sample = sample

        self.vcf_file = pysam.VariantFile(vcf_file_path)
        self.vcf_file_path = vcf_file_path
        self.ignore_phase_sets = ignore_phase_sets

        self.alignment_file_paths = []
        self.RG_ID_dict = RG_ID_dict
        self.use_RG_tag = {}

        for alignment_file_path in alignment_file_paths:
            self.alignment_file_paths.append(str(alignment_file_path))
            self.use_RG_tag[str(alignment_file_path)] = alignment_file_paths[str(alignment_file_path)]

        self.reference_sequence_names = reference_sequence_names
        self.reference_sequence_paths = reference_sequence_paths
        self.reference_sequences_in_VCF = list(self.vcf_file.index)
        self.only_autosomal = only_autosomal
        self.regions = regions
        self.ploidy = ploidy

        if output_directory_path is None:
            self.output_directory = os.path.abspath('%s/%s' % (os.path.dirname(self.vcf_file_path), str(self.sample)))
        else:
            self.output_directory = os.path.abspath(output_directory_path)

        if not os.path.exists(self.output_directory):
            os.mkdir(self.output_directory)

        if self.simulate_haplotypes:
            self.haplotype_structure_file_path = self.simulate_sample()

    def _pysam_bam_files_initialize(self) -> List[Iterator]:
        """

        Returns:
            object:
        """
        bam_files = []
        for alignment_file_path in self.alignment_file_paths:
            bam_files.append(iter(pysam.AlignmentFile(alignment_file_path, 'rb')))
        return bam_files

    def __iter__(self):
        print('Alignments for sample %s' % str(self.sample))
        self.bam_files = self._pysam_bam_files_initialize()
        # self._initialize_alignment_counter()
        self.alignment_files_processed_count = 0
        self.alignments_processed_count = 0
        self.alignment_files_alignment_counts = []
        bam_file: pysam.AlignmentFile
        for bam_file in self.bam_files:
            self.alignment_files_alignment_counts.append(bam_file.mapped + bam_file.unmapped)
        self.total_alignments = sum(self.alignment_files_alignment_counts)
        self.alignment_file_pysam = self.bam_files[self.alignment_files_processed_count]
        self.start_process_time = time.time()
        self.unique_read_names = set()
        return self

    def __next__(self) -> pysam.AlignedSegment:
        """

        Returns:
            pysam.AlignedSegment:

        """
        alignment = next(self.alignment_file_pysam)
        if alignment.query_name not in self.unique_read_names:
            self.unique_read_names.add(alignment.query_name)
        # read = self._evaluate_alignment(read)
        #id_RG = self._get_RG_info_for_alignment(alignment, self.alignment_file_pysam)
        alignment.set_tag(tag='RG', value=str(self._get_RG_info_for_alignment(alignment, self.alignment_file_pysam)), value_type='Z', replace=True)
        # if str(RG_info[2])[0:3] == 'SIM':
        # read.set_tag(tag='oa', value=str(RG_info[2][3]), value_type='Z', replace=True)
        #alignment.set_tag(tag='RG', value=str(RG_info[1]), value_type='Z', replace=True)
        self.alignment_files_alignment_counts[self.alignment_files_processed_count] -= 1
        if self.alignment_files_alignment_counts[self.alignment_files_processed_count] == 0:
            self.alignment_files_processed_count += 1
            if self.alignment_files_processed_count == len(self.alignment_file_paths):
                raise StopIteration()
            self.alignment_file_pysam = self.bam_files[self.alignment_files_processed_count]
        self.alignments_processed_count += 1
        if self.alignments_processed_count % 2000 == 0:
            print(
                'Processing %s alignments per second' % str(
                    round(self.alignments_processed_count / (time.time() - self.start_process_time), 2)
                )
            )
            print(
                'Processed %s alignments (%s percent complete)' % (str(self.alignments_processed_count), str(
                    round(100 * (self.alignments_processed_count / self.total_alignments), 2)
                ))
            )
            print(
                'Processing sample %s will finish in %s seconds' % (str(self.sample), str(
                    round(
                        (self.total_alignments - self.alignments_processed_count) / (
                                self.alignments_processed_count / (time.time() - self.start_process_time)),
                        1
                    )
                ))
            )
        return alignment

    def __repr__(self):
        return f'Sample: {self.sample}\n' \
               f'Haplotype Information: {self.vcf_file_path}\n' \
               f'Alignment Files: {str(self.alignment_file_paths)}\n' \
               f'Total alignment files processed: {self.alignment_files_processed_count}\n' \
               f'Total alignments: {self.total_alignments}\n' \
               f'Total alignments processed: {self.alignments_processed_count}\n' \
               f'Total unique reads observed: {len(self.unique_read_names)}'

    def _get_RG_info_for_alignment(self, alignment: pysam.AlignedSegment, alignment_file: Union[pysam.AlignmentFile, str]) -> None:

        """

        Args:
            alignment(pysam.AlignedSegment):
            alignment_file (Union[pysam.AlignmentFile, str]):

        Returns:
            object:

        """
        alignment_file_path = ''
        if isinstance(alignment_file, pysam.AlignmentFile):
            if str(alignment_file.filename.decode()) in self.alignment_file_paths:
                alignment_file_path = str(alignment_file.filename.decode())
            else:
                return
        elif str(alignment_file) in self.alignment_file_paths:
            alignment_file_path = str(alignment_file)
        else:
            return
        if alignment_file_path in self.use_RG_tag.keys():
            use_RG_tag = self.use_RG_tag[alignment_file_path]
            if use_RG_tag:
                if str(alignment.get_tag('RG')) in self.RG_ID_dict[alignment_file_path]:
                    if self.RG_ID_dict[alignment_file_path][str(alignment.get_tag('RG'))]['SM'] == self.sample:
                        ID = str(alignment.get_tag('RG'))
                        outputID = self.RG_ID_dict[alignment_file_path][str(alignment.get_tag('RG'))]['outputID']
                        sample_description = self.RG_ID_dict[alignment_file_path][str(alignment.get_tag('RG'))]['DS']
                        return #ID, outputID, sample_description, use_RG_tag
            else:
                ID = list(self.RG_ID_dict[alignment_file_path].keys())[0]
                outputID = self.RG_ID_dict[alignment_file_path][ID]['outputID']
                sample_description = self.RG_ID_dict[alignment_file_path][ID]['DS']

                return #ID, outputID, sample_description, use_RG_tag

    def simulate_sample(self, simulated_directory: str = None) -> str:
        """

        Args:
            simulated_directory:
            self:
        """
        if simulated_directory is None:
            simulated_directory = self.output_directory + '/simulated'
        if not os.path.exists(simulated_directory):
            os.mkdir(simulated_directory)

        haplotype_structure_file_path = simulated_directory + '/haplotype_structure.txt'
        reference_sequence_path = simulated_directory + '/reference_sequence.fa'
        reference_sequence_list = []
        for i, reference_sequence in enumerate(self.reference_sequence_paths):
            reference_sequence_list.append(
                SimulatePhasedData.create_fasta_file(input_fasta_file_path=reference_sequence,
                                                     output_fasta_file_path=str(os.path.abspath(
                                                         self.output_directory)) + '/reference_sequences' + str(
                                                         i) + '.fa', regions=self.regions,
                                                     only_autosomal=self.only_autosomal))

        with open(self.reference_sequence_path, 'a') as outfile:
            for file in reference_sequence_list:
                with open(file, 'r') as infile:
                    outfile.write(infile.read())

        SimulatePhasedData.index_fasta_file(self.reference_sequence_path)

        self.haplotype_reference_sequences = {}
        self.haplotype_chain_files = {}
        self.haplotype_liftover_converters = {}
        for j in range(1, self.ploidy + 1):
            self.haplotype_reference_sequences[j], self.haplotype_chain_files[
                j] = SimulatePhasedData.generate_haplotype_specific_fasta(j, self.sample,
                                                                          self.reference_sequence_path,
                                                                          self.vcf_file_path,
                                                                          output_reference_sequence_path=str(
                                                                              os.path.abspath(
                                                                                  self.output_directory)) + '/haplotype' + str(
                                                                              j) + '_reference_sequence.fa',
                                                                          chain_file_path=str(os.path.abspath(
                                                                              self.output_directory)) + '/haplotype' + str(
                                                                              j) + '_reference_sequence.chain')
            self.haplotype_liftover_converters[j] = pyliftover.LiftOver(self.haplotype_chain_files[j])
        return haplotype_structure_file_path

    # def __repr__(self):
    #     return f'Sample: {self.sample}\n' \
    #            f'Haplotype Information File Path: {self.vcf_file_path}\n' \
    #            f'Reference Sequence Path: {str(self.reference_sequence_paths)}\n' \
    #            f'Total sequences in reference files: {len(self.reference_sequence_names)}\n' \
    #            f'Total Reference sequences in VCF: {len(self.reference_sequences_in_VCF)}\n' \
    #            f'Alignment Files: {str(self.alignment_file_paths)}\n' \
    #            f'Total alignment files processed: {self.alignment_files_processed_count}\n' \
    #            f'Total alignments: {self.total_alignments}\n' \
    #            f'Total alignments processed: {self.alignments_processed_count}\n' \
    #            f'Total unique reads observed: {len(self.unique_read_names)}'

    def simulate_reads(self, path_to_pbsim='pbsim', depth=1,
                       simulation_mode='pbsim2/data/R103.model',
                       difference_ratio='23:31:46', length_mean=20000,
                       length_max=1000000, length_min=100,
                       length_sd=15000, accuracy_min=0.01,
                       accuracy_max=1.00, accuracy_mean=0.80,
                       prefix=None, id_prefix='S', output_directory=None, sample=None,
                       haplotypes=[1, 2]):
        """

        Args:
            path_to_pbsim:
            depth:
            simulation_mode:
            difference_ratio:
            length_mean:
            length_max:
            length_min:
            length_sd:
            accuracy_min:
            accuracy_max:
            accuracy_mean:
            prefix:
            id_prefix:
            output_directory:
            sample:
            haplotypes:
        """
        for haplotype in haplotypes:
            self.haplotype_simulated_reads[haplotype] = SimulatePhasedData.simulate_reads_pbsim2(
                self.haplotype_reference_sequences[haplotype], path_to_pbsim=path_to_pbsim, depth=depth,
                simulation_mode=simulation_mode,
                difference_ratio=difference_ratio, length_mean=length_mean,
                length_max=length_max, length_min=length_min,
                length_sd=length_sd, accuracy_min=accuracy_min,
                accuracy_max=accuracy_max, accuracy_mean=accuracy_mean,
                prefix=prefix, id_prefix=id_prefix, output_directory=self.output_directory + '/simulated',
                sample=self.sample,
                haplotype=haplotype)
