#!/usr/bin/env python
# -*- coding: latin-1 -*-
#
#   Copyright 2016-2021 Blaise Frederick
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
#
from __future__ import division, print_function

import argparse
import logging
import sys

import nibabel as nib
import numpy as np

import rapidtide.filter as tide_filt
import rapidtide.io as tide_io
import rapidtide.util as tide_util
import rapidtide.workflows.parser_funcs as pf


LGR = logging.getLogger(__name__)


def _get_parser():
    """
    Argument parser for rapidtide
    """
    parser = argparse.ArgumentParser(
        prog="rapidtide",
        description=("Perform a RIPTiDe time delay analysis on a dataset."),
    )

    # Required arguments
    parser.add_argument(
        "in_file",
        type=lambda x: pf.is_valid_file(parser, x),
        help="The input data file (BOLD fMRI file or NIRS text file)",
    )
    parser.add_argument(
        "outputname",
        type=str,
        help=(
            "The root name for the output files.  "
            "For BIDS compliance, this can only contain valid BIDS entities "
            "from the source data."
        ),
    )

    # Analysis types
    analysis_type = parser.add_argument_group(
        title="Analysis type",
        description=(
            "Single arguments that change default values for many "
            "arguments. "
            "Any parameter set by an analysis type can be overridden "
            "by setting that parameter explicitly. "
            "Analysis types are mutually exclusive with one another."
        ),
    ).add_mutually_exclusive_group()
    analysis_type.add_argument(
        "--denoising",
        dest="denoising",
        action="store_true",
        help=(
            "Preset for hemodynamic denoising - this is a macro that "
            "sets lagmin=-15.0, lagmax=15.0, passes=3, despeckle_passes=4, "
            "refineoffset=True, peakfittype=fastquad, doglmfilt=True. "
            "Any of these options can be overridden with the appropriate "
            "additional arguments"
        ),
        default=False,
    )
    analysis_type.add_argument(
        "--delaymapping",
        dest="delaymapping",
        action="store_true",
        help=(
            "Preset for delay mapping analysis - this is a macro that "
            "sets lagmin=-10.0, lagmax=30.0, passes=3, despeckle_passes=4, "
            "refineoffset=True, pickleft=True, limitoutput=True, "
            "doglmfilt=False. "
            "Any of these options can be overridden with the appropriate "
            "additional arguments"
        ),
        default=False,
    )

    # Macros
    macros = parser.add_argument_group(
        title="Macros",
        description=(
            "Single arguments that change default values for many "
            "arguments. "
            "Macros override individually set parameters. "
            "Macros are mutually exclusive with one another."
        ),
    ).add_mutually_exclusive_group()
    macros.add_argument(
        "--venousrefine",
        dest="venousrefine",
        action="store_true",
        help=(
            "This is a macro that sets --lagminthresh=2.5, "
            "--lagmaxthresh=6.0, --ampthresh=0.5, and "
            "--refineupperlag to bias refinement towards "
            "voxels in the draining vasculature for an "
            "fMRI scan."
        ),
        default=False,
    )
    macros.add_argument(
        "--nirs",
        dest="nirs",
        action="store_true",
        help=(
            "This is a NIRS analysis - this is a macro that "
            "sets --nothresh, --preservefiltering, "
            "--refineprenorm=var, --ampthresh=0.7, and "
            "--lagminthresh=0.1. "
        ),
        default=False,
    )

    # Preprocessing options
    preproc = parser.add_argument_group("Preprocessing options")
    realtr = preproc.add_mutually_exclusive_group()
    realtr.add_argument(
        "--datatstep",
        dest="realtr",
        action="store",
        metavar="TSTEP",
        type=lambda x: pf.is_float(parser, x),
        help=(
            "Set the timestep of the data file to TSTEP. "
            "This will override the TR in an "
            "fMRI file. NOTE: if using data from a text "
            "file, for example with NIRS data, using one "
            "of these options is mandatory. "
        ),
        default="auto",
    )
    realtr.add_argument(
        "--datafreq",
        dest="realtr",
        action="store",
        metavar="FREQ",
        type=lambda x: pf.invert_float(parser, x),
        help=(
            "Set the timestep of the data file to 1/FREQ. "
            "This will override the TR in an "
            "fMRI file. NOTE: if using data from a text "
            "file, for example with NIRS data, using one "
            "of these options is mandatory. "
        ),
        default="auto",
    )
    preproc.add_argument(
        "--noantialias",
        dest="antialias",
        action="store_false",
        help="Disable antialiasing filter. ",
        default=True,
    )
    preproc.add_argument(
        "--invert",
        dest="invertregressor",
        action="store_true",
        help=("Invert the sign of the regressor before processing."),
        default=False,
    )
    preproc.add_argument(
        "--interptype",
        dest="interptype",
        action="store",
        type=str,
        choices=["univariate", "cubic", "quadratic"],
        help=(
            "Use specified interpolation type. Options "
            "are 'cubic', 'quadratic', and 'univariate' "
            "(default). "
        ),
        default="univariate",
    )
    preproc.add_argument(
        "--offsettime",
        dest="offsettime",
        action="store",
        type=float,
        metavar="OFFSETTIME",
        help="Apply offset OFFSETTIME to the lag regressors.",
        default=0.0,
    )
    preproc.add_argument(
        "--autosync",
        dest="autosync",
        action="store_true",
        help=(
            "Estimate and apply the initial offsettime of an external "
            "regressor using the global crosscorrelation. "
            "Overrides offsettime if present."
        ),
        default=False,
    )

    # Add filter options
    pf.addfilteropts(parser, "data and regressors", details=True)

    # Add permutation options
    pf.addpermutationopts(parser)

    wfunc = preproc.add_mutually_exclusive_group()
    wfunc.add_argument(
        "--windowfunc",
        dest="windowfunc",
        action="store",
        type=str,
        choices=["hamming", "hann", "blackmanharris", "None"],
        help=(
            "Window function to use prior to correlation. "
            "Options are hamming (default), hann, "
            "blackmanharris, and None."
        ),
        default="hamming",
    )
    wfunc.add_argument(
        "--nowindow",
        dest="windowfunc",
        action="store_const",
        const="None",
        help="Disable precorrelation windowing.",
        default="hamming",
    )

    preproc.add_argument(
        "--detrendorder",
        dest="detrendorder",
        action="store",
        type=int,
        metavar="ORDER",
        help=("Set order of trend removal (0 to disable, " "default is 1 - linear)."),
        default=3,
    )
    preproc.add_argument(
        "--spatialfilt",
        dest="gausssigma",
        action="store",
        type=float,
        metavar="GAUSSSIGMA",
        help=(
            "Spatially filter fMRI data prior to analysis "
            "using GAUSSSIGMA in mm.  Set GAUSSSIGMA negative "
            "to have rapidtide set it to half the mean voxel "
            "dimension (a rule of thumb for a good value)."
        ),
        default=0.0,
    )
    preproc.add_argument(
        "--globalmean",
        dest="useglobalref",
        action="store_true",
        help=(
            "Generate a global mean regressor and use that as the reference "
            "regressor.  If no external regressor is specified, this "
            "is enabled by default."
        ),
        default=False,
    )
    preproc.add_argument(
        "--globalmaskmethod",
        dest="globalmaskmethod",
        action="store",
        type=str,
        choices=["mean", "variance"],
        help=(
            "Select whether to use timecourse mean (default) or variance to "
            "mask voxels prior to generating global mean."
        ),
        default="mean",
    )
    preproc.add_argument(
        "--globalmeaninclude",
        dest="globalmeanincludespec",
        metavar="MASK[:VALSPEC]",
        help=(
            "Only use voxels in mask file NAME for global regressor "
            "generation (if VALSPEC is given, only voxels "
            "with integral values listed in VALSPEC are used)."
        ),
        default=None,
    )
    preproc.add_argument(
        "--globalmeanexclude",
        dest="globalmeanexcludespec",
        metavar="MASK[:VALSPEC]",
        help=(
            "Do not use voxels in mask file NAME for global regressor "
            "generation (if VALSPEC is given, only voxels "
            "with integral values listed in VALSPEC are excluded)."
        ),
        default=None,
    )
    preproc.add_argument(
        "--motionfile",
        dest="motionfilespec",
        metavar="MOTFILE",
        help=(
            "Read 6 columns of motion regressors out of MOTFILE file (.par or BIDS .json) "
            "(with timepoints rows) and regress their derivatives "
            "and delayed derivatives out of the data prior to analysis. "
        ),
        default=None,
    )
    preproc.add_argument(
        "--motpos",
        dest="mot_pos",
        action="store_true",
        help=(
            "Toggle whether displacement regressors will be used in motion "
            "regression. Default is False. "
        ),
        default=False,
    )
    preproc.add_argument(
        "--motderiv",
        dest="mot_deriv",
        action="store_false",
        help=(
            "Toggle whether derivatives will be used in motion regression.  " "Default is True. "
        ),
        default=True,
    )
    preproc.add_argument(
        "--motdelayderiv",
        dest="mot_delayderiv",
        action="store_true",
        help=(
            "Toggle whether delayed derivative regressors will be used in "
            "motion regression.  Default is False. "
        ),
        default=False,
    )
    preproc.add_argument(
        "--globalsignalmethod",
        dest="globalsignalmethod",
        action="store",
        type=str,
        choices=["sum", "meanscale", "pca"],
        help=(
            "The method for constructing the initial global signal regressor - straight summation (default), "
            "mean scaling each voxel prior to summation, or MLE PCA of the voxels in the global signal mask."
        ),
        default="mean",
    )
    preproc.add_argument(
        "--globalpcacomponents",
        dest="globalpcacomponents",
        action="store",
        type=float,
        metavar="VALUE",
        help=(
            "Number of PCA components used for estimating the global signal.  If VALUE >= 1, will retain this"
            "many components.  If "
            "0.0 < VALUE < 1.0, enough components will be retained to explain the fraction VALUE of the "
            "total variance. If VALUE is negative, the number of components will be to retain will be selected "
            "automatically using the MLE method.  Default is 0.8."
        ),
        default=0.8,
    )
    preproc.add_argument(
        "--slicetimes",
        dest="slicetimes",
        action="store",
        type=lambda x: pf.is_valid_file(parser, x),
        metavar="FILE",
        help=("Apply offset times from FILE to each slice in the dataset."),
        default=None,
    )
    preproc.add_argument(
        "--numskip",
        dest="preprocskip",
        action="store",
        type=int,
        metavar="SKIP",
        help=(
            "SKIP TRs were previously deleted during "
            "preprocessing (e.g. if you have done your preprocessing "
            "in FSL and set dummypoints to a nonzero value.) Default is 0. "
        ),
        default=0,
    )
    preproc.add_argument(
        "--timerange",
        dest="timerange",
        action="store",
        nargs=2,
        type=int,
        metavar=("START", "END"),
        help=(
            "Limit analysis to data between timepoints "
            "START and END in the fmri file. If END is set to -1, "
            "analysis will go to the last timepoint.  Negative values "
            "of START will be set to 0. Default is to use all timepoints."
        ),
        default=(-1, -1),
    )
    preproc.add_argument(
        "--nothresh",
        dest="nothresh",
        action="store_true",
        help=("Disable voxel intensity threshold (especially useful for NIRS " "data)."),
        default=False,
    )

    # Correlation options
    corr = parser.add_argument_group("Correlation options")
    corr.add_argument(
        "--oversampfac",
        dest="oversampfactor",
        action="store",
        type=int,
        metavar="OVERSAMPFAC",
        help=(
            "Oversample the fMRI data by the following "
            "integral factor.  Set to -1 for automatic selection (default)."
        ),
        default=-1,
    )
    corr.add_argument(
        "--regressor",
        dest="regressorfile",
        action="store",
        type=lambda x: pf.is_valid_file(parser, x),
        metavar="FILE",
        help=(
            "Read the initial probe regressor from file FILE (if not "
            "specified, generate and use the global regressor)."
        ),
        default=None,
    )

    reg_group = corr.add_mutually_exclusive_group()
    reg_group.add_argument(
        "--regressorfreq",
        dest="inputfreq",
        action="store",
        type=lambda x: pf.is_float(parser, x),
        metavar="FREQ",
        help=(
            "Probe regressor in file has sample "
            "frequency FREQ (default is 1/tr) "
            "NB: --regressorfreq and --regressortstep) "
            "are two ways to specify the same thing."
        ),
        default="auto",
    )
    reg_group.add_argument(
        "--regressortstep",
        dest="inputfreq",
        action="store",
        type=lambda x: pf.invert_float(parser, x),
        metavar="TSTEP",
        help=(
            "Probe regressor in file has sample "
            "frequency FREQ (default is 1/tr) "
            "NB: --regressorfreq and --regressortstep) "
            "are two ways to specify the same thing."
        ),
        default="auto",
    )

    corr.add_argument(
        "--regressorstart",
        dest="inputstarttime",
        action="store",
        type=float,
        metavar="START",
        help=(
            "The time delay in seconds into the regressor "
            "file, corresponding in the first TR of the fMRI "
            "file (default is 0.0)."
        ),
        default=0.0,
    )
    corr.add_argument(
        "--corrweighting",
        dest="corrweighting",
        action="store",
        type=str,
        choices=["None", "phat", "liang", "eckart"],
        help=("Method to use for cross-correlation weighting. " "Default is 'None'."),
        default="None",
    )

    mask_group = corr.add_mutually_exclusive_group()
    mask_group.add_argument(
        "--corrmaskthresh",
        dest="corrmaskthreshpct",
        action="store",
        type=float,
        metavar="PCT",
        help=(
            "Do correlations in voxels where the mean "
            "exceeds this percentage of the robust max "
            "(default is 1.0). "
        ),
        default=1.0,
    )
    mask_group.add_argument(
        "--corrmask",
        dest="corrmaskincludespec",
        metavar="MASK[:VALSPEC]",
        help=(
            "Only do correlations in nonzero voxels in NAME "
            "(if VALSPEC is given, only voxels "
            "with integral values listed in VALSPEC are used). "
        ),
        default=None,
    )
    corr.add_argument(
        "--similaritymetric",
        dest="similaritymetric",
        action="store",
        type=str,
        choices=["correlation", "mutualinfo", "hybrid"],
        help=(
            "Similarity metric for finding delay values.  "
            "Choices are 'correlation' (default), 'mutualinfo', and 'hybrid'."
        ),
        default="correlation",
    )
    corr.add_argument(
        "--mutualinfosmoothingtime",
        dest="smoothingtime",
        action="store",
        type=float,
        metavar="TAU",
        help=(
            "Time constant of a temporal smoothing function to apply to the "
            "mutual information function. "
            "Default is 3.0 seconds.  "
            "TAU <=0.0 disables smoothing."
        ),
        default=3.0,
    )

    # Correlation fitting options
    corr_fit = parser.add_argument_group("Correlation fitting options")

    fixdelay = corr_fit.add_mutually_exclusive_group()
    fixdelay.add_argument(
        "--fixdelay",
        dest="fixeddelayvalue",
        action="store",
        type=float,
        metavar="DELAYTIME",
        help=("Don't fit the delay time - set it to DELAYTIME seconds for all " "voxels."),
        default=None,
    )
    fixdelay.add_argument(
        "--searchrange",
        dest="lag_extrema",
        action=pf.IndicateSpecifiedAction,
        nargs=2,
        type=float,
        metavar=("LAGMIN", "LAGMAX"),
        help=(
            "Limit fit to a range of lags from LAGMIN to "
            "LAGMAX.  Default is -30.0 to 30.0 seconds. "
        ),
        default=(-30.0, 30.0),
    )
    corr_fit.add_argument(
        "--sigmalimit",
        dest="widthlimit",
        action="store",
        type=float,
        metavar="SIGMALIMIT",
        help=("Reject lag fits with linewidth wider than " "SIGMALIMIT Hz. Default is 100.0."),
        default=100.0,
    )
    corr_fit.add_argument(
        "--bipolar",
        dest="bipolar",
        action="store_true",
        help=("Bipolar mode - match peak correlation ignoring sign."),
        default=False,
    )
    corr_fit.add_argument(
        "--nofitfilt",
        dest="zerooutbadfit",
        action="store_false",
        help=("Do not zero out peak fit values if fit fails."),
        default=True,
    )
    corr_fit.add_argument(
        "--peakfittype",
        dest="peakfittype",
        action="store",
        type=str,
        choices=["gauss", "fastgauss", "quad", "fastquad", "COM", "None"],
        help=(
            "Method for fitting the peak of the similarity function "
            "(default is 'gauss'). 'quad' and 'fastquad' use a quadratic fit. "
            "Faster but not as well tested. "
        ),
        default="gauss",
    )
    corr_fit.add_argument(
        "--despecklepasses",
        dest="despeckle_passes",
        action=pf.IndicateSpecifiedAction,
        type=int,
        metavar="PASSES",
        help=(
            "Detect and refit suspect correlations to "
            "disambiguate peak locations in PASSES "
            "passes.  Default is to perform 4 passes. "
            "Set to 0 to disable."
        ),
        default=4,
    )
    corr_fit.add_argument(
        "--despecklethresh",
        dest="despeckle_thresh",
        action="store",
        type=float,
        metavar="VAL",
        help=(
            "Refit correlation if median discontinuity " "magnitude exceeds VAL (default is 5.0s)."
        ),
        default=5.0,
    )

    # Regressor refinement options
    reg_ref = parser.add_argument_group("Regressor refinement options")
    reg_ref.add_argument(
        "--refineprenorm",
        dest="refineprenorm",
        action="store",
        type=str,
        choices=["None", "mean", "var", "std", "invlag"],
        help=(
            "Apply TYPE prenormalization to each "
            "timecourse prior to refinement. Default is 'mean'."
        ),
        default="mean",
    )
    reg_ref.add_argument(
        "--refineweighting",
        dest="refineweighting",
        action="store",
        type=str,
        choices=["None", "NIRS", "R", "R2"],
        help=(
            "Apply TYPE weighting to each timecourse prior "
            "to refinement. Default is 'R2' (r-squared)."
        ),
        default="R2",
    )
    reg_ref.add_argument(
        "--passes",
        dest="passes",
        action="store",
        type=int,
        metavar="PASSES",
        help=("Set the number of processing passes to PASSES.  " "Default is 3."),
        default=3,
    )
    reg_ref.add_argument(
        "--refineinclude",
        dest="refineincludespec",
        metavar="MASK[:VALSPEC]",
        help=(
            "Only use voxels in file MASK for regressor refinement "
            "(if VALSPEC is given, only voxels "
            "with integral values listed in VALSPEC are used). "
        ),
        default=None,
    )
    reg_ref.add_argument(
        "--refineexclude",
        dest="refineexcludespec",
        metavar="MASK[:VALSPEC]",
        help=(
            "Do not use voxels in file MASK for regressor refinement "
            "(if VALSPEC is given, voxels "
            "with integral values listed in VALSPEC are excluded). "
        ),
        default=None,
    )
    reg_ref.add_argument(
        "--lagminthresh",
        dest="lagminthresh",
        action="store",
        metavar="MIN",
        type=float,
        help=("For refinement, exclude voxels with delays " "less than MIN (default is 0.25s). "),
        default=0.5,
    )
    reg_ref.add_argument(
        "--lagmaxthresh",
        dest="lagmaxthresh",
        action="store",
        metavar="MAX",
        type=float,
        help=("For refinement, exclude voxels with delays " "greater than MAX (default is 5s). "),
        default=5.0,
    )
    reg_ref.add_argument(
        "--ampthresh",
        dest="ampthresh",
        action="store",
        metavar="AMP",
        type=float,
        help=(
            "For refinement, exclude voxels with correlation "
            "coefficients less than AMP (default is 0.3).  "
            "NOTE: ampthresh will automatically be set to the p<0.05 "
            "significance level determined by the --numnull option if NREPS "
            "is set greater than 0 and this is not manually specified."
        ),
        default=-1.0,
    )
    reg_ref.add_argument(
        "--sigmathresh",
        dest="sigmathresh",
        action="store",
        metavar="SIGMA",
        type=float,
        help=(
            "For refinement, exclude voxels with widths "
            "greater than SIGMA seconds (default is 100s)."
        ),
        default=100.0,
    )
    reg_ref.add_argument(
        "--norefineoffset",
        dest="refineoffset",
        action="store_false",
        help=("Disable realigning refined regressor to zero lag."),
        default=True,
    )
    reg_ref.add_argument(
        "--psdfilter",
        dest="psdfilter",
        action="store_true",
        help=("Apply a PSD weighted Wiener filter to " "shifted timecourses prior to refinement."),
        default=False,
    )
    reg_ref.add_argument(
        "--pickleft",
        dest="pickleft",
        action="store_true",
        help=("Will select the leftmost delay peak when setting the refine " "offset."),
        default=False,
    )
    reg_ref.add_argument(
        "--pickleftthresh",
        dest="pickleftthresh",
        action="store",
        metavar="THRESH",
        type=float,
        help=(
            "Threshhold value (fraction of maximum) in a histogram "
            "to be considered the start of a peak.  Default is 0.33."
        ),
        default=0.33,
    )

    refine = reg_ref.add_mutually_exclusive_group()
    refine.add_argument(
        "--refineupperlag",
        dest="lagmaskside",
        action="store_const",
        const="upper",
        help=("Only use positive lags for regressor refinement."),
        default="both",
    )
    refine.add_argument(
        "--refinelowerlag",
        dest="lagmaskside",
        action="store_const",
        const="lower",
        help=("Only use negative lags for regressor refinement."),
        default="both",
    )
    reg_ref.add_argument(
        "--refinetype",
        dest="refinetype",
        action="store",
        type=str,
        choices=["pca", "ica", "weighted_average", "unweighted_average"],
        help=("Method with which to derive refined regressor (default is 'pca'"),
        default="pca",
    )
    reg_ref.add_argument(
        "--pcacomponents",
        dest="pcacomponents",
        action="store",
        type=float,
        metavar="VALUE",
        help=(
            "Number of PCA components used for refinement.  If VALUE >= 1, will retain this many components.  If "
            "0.0 < VALUE < 1.0, enough components will be retained to explain the fraction VALUE of the "
            "total variance. If VALUE is negative, the number of components will be to retain will be selected "
            "automatically using the MLE method.  Default is 0.8."
        ),
        default=0.8,
    )
    reg_ref.add_argument(
        "--convergencethresh",
        dest="convergencethresh",
        action="store",
        type=float,
        metavar="THRESH",
        help=(
            "Continue refinement until the MSE between regressors becomes <= THRESH.  "
            "By default, this is not set, so refinement will run for the specified number of passes"
        ),
        default=None,
    )
    reg_ref.add_argument(
        "--maxpasses",
        dest="maxpasses",
        action="store",
        type=int,
        metavar="MAXPASSES",
        help=(
            "Terminate refinement after MAXPASSES passes, whether or not convergence has occured. Default is 15"
        ),
        default=15,
    )

    # Output options
    output = parser.add_argument_group("Output options")
    output.add_argument(
        "--nolimitoutput",
        dest="limitoutput",
        action="store_false",
        help=("Save some of the large and rarely used files."),
        default=True,
    )
    output.add_argument(
        "--savelags",
        dest="savecorrtimes",
        action="store_true",
        help="Save a table of lagtimes used.",
        default=False,
    )
    output.add_argument(
        "--histlen",  # was -h
        dest="histlen",
        action="store",
        type=int,
        metavar="HISTLEN",
        help=("Change the histogram length to HISTLEN (default is 100)."),
        default=100,
    )
    output.add_argument(
        "--glmsourcefile",
        dest="glmsourcefile",
        action="store",
        type=lambda x: pf.is_valid_file(parser, x),
        metavar="FILE",
        help=(
            "Regress delayed regressors out of FILE instead "
            "of the initial fmri file used to estimate "
            "delays."
        ),
        default=None,
    )
    output.add_argument(
        "--noglm",
        dest="doglmfilt",
        action="store_false",
        help=(
            "Turn off GLM filtering to remove delayed "
            "regressor from each voxel (disables output of "
            "fitNorm)."
        ),
        default=True,
    )
    output.add_argument(
        "--preservefiltering",
        dest="preservefiltering",
        action="store_true",
        help="Don't reread data prior to performing GLM.",
        default=False,
    )
    output.add_argument(
        "--saveintermediatemaps",
        dest="saveintermediatemaps",
        action="store_true",
        help="Save lag times, strengths, widths, and mask for each pass.",
        default=False,
    )
    output.add_argument(
        "--legacyoutput",
        dest="bidsoutput",
        action="store_false",
        help=(
            "Use legacy file naming and formats rather than BIDS naming and "
            "format conventions for output files."
        ),
        default=True,
    )
    output.add_argument(
        "--calccoherence",
        dest="calccoherence",
        action="store_true",
        help=("Calculate and save the coherence between the final regressor and the data."),
        default=False,
    )

    # Miscellaneous options
    misc = parser.add_argument_group("Miscellaneous options")
    misc.add_argument(
        "--noprogressbar",
        dest="showprogressbar",
        action="store_false",
        help=("Will disable showing progress bars (helpful if stdout is going " "to a file)."),
        default=True,
    )
    misc.add_argument(
        "--checkpoint",
        dest="checkpoint",
        action="store_true",
        help="Enable run checkpoints.",
        default=False,
    )
    misc.add_argument(
        "--wiener",
        dest="dodeconv",
        action="store_true",
        help=("Do Wiener deconvolution to find voxel transfer function."),
        default=False,
    )
    misc.add_argument(
        "--spcalculation",
        dest="internalprecision",
        action="store_const",
        const="single",
        help=(
            "Use single precision for internal calculations "
            "(may be useful when RAM is limited)."
        ),
        default="double",
    )
    misc.add_argument(
        "--dpoutput",
        dest="outputprecision",
        action="store_const",
        const="double",
        help=("Use double precision for output files."),
        default="single",
    )
    misc.add_argument(
        "--cifti",
        dest="isgrayordinate",
        action="store_true",
        help="Data file is a converted CIFTI.",
        default=False,
    )
    misc.add_argument(
        "--simulate",
        dest="fakerun",
        action="store_true",
        help="Simulate a run - just report command line options.",
        default=False,
    )
    misc.add_argument(
        "--displayplots",
        dest="displayplots",
        action="store_true",
        help="Display plots of interesting timecourses.",
        default=False,
    )
    misc.add_argument(
        "--nonumba",
        dest="nonumba",
        action="store_true",
        help="Disable jit compilation with numba.",
        default=False,
    )
    misc.add_argument(
        "--nosharedmem",
        dest="sharedmem",
        action="store_false",
        help=("Disable use of shared memory for large array storage."),
        default=True,
    )
    misc.add_argument(
        "--memprofile",
        dest="memprofile",
        action="store_true",
        help=("Enable memory profiling for debugging - " "warning: this slows things down a lot."),
        default=False,
    )
    misc.add_argument(
        "--mklthreads",
        dest="mklthreads",
        action="store",
        type=int,
        metavar="MKLTHREADS",
        help=("Use no more than MKLTHREADS worker threads in accelerated numpy " "calls."),
        default=1,
    )
    misc.add_argument(
        "--nprocs",
        dest="nprocs",
        action="store",
        type=int,
        metavar="NPROCS",
        help=(
            "Use NPROCS worker processes for multiprocessing. "
            "Setting NPROCS to less than 1 sets the number of "
            "worker processes to n_cpus - 1."
        ),
        default=1,
    )
    misc.add_argument(
        "--version",
        dest="printversion",
        action="store_true",
        help=("Print version information and exit."),
        default=False,
    )
    misc.add_argument(
        "--debug",
        dest="debug",
        action="store_true",
        help=("Enable additional debugging output."),
        default=False,
    )
    misc.add_argument(
        "--verbose",
        dest="verbose",
        action="store_true",
        help=("Enable additional runtime information output."),
        default=False,
    )

    # Experimental options (not fully tested, may not work)
    experimental = parser.add_argument_group(
        "Experimental options (not fully tested, may not work)"
    )
    experimental.add_argument(
        "--echocancel",
        dest="echocancel",
        action="store_true",
        help=("Attempt to perform echo cancellation."),
        default=False,
    )
    experimental.add_argument(
        "--respdelete",
        dest="respdelete",
        action="store_true",
        help=("Attempt to detect and remove respiratory signal that strays into " "the LFO band."),
        default=False,
    )
    experimental.add_argument(
        "--correlatorhpfreq",
        dest="correlator_hpfreq",
        action="store",
        metavar="HPFREQ",
        type=float,
        help=("High pass filter the correlation function to get rid of baseline " "problems."),
        default=None,
    )
    experimental.add_argument(
        "--cleanrefined",
        dest="cleanrefined",
        action="store_true",
        help=(
            "Perform additional processing on refined "
            "regressor to remove spurious "
            "components."
        ),
        default=False,
    )
    experimental.add_argument(
        "--dispersioncalc",
        dest="dodispersioncalc",
        action="store_true",
        help=("Generate extra data during refinement to " "allow calculation of dispersion."),
        default=False,
    )
    experimental.add_argument(
        "--acfix",
        dest="fix_autocorrelation",
        action="store_true",
        help=("Perform a secondary correlation to " "disambiguate peak location. Experimental."),
        default=False,
    )
    experimental.add_argument(
        "--alwaysmultiproc",
        dest="alwaysmultiproc",
        action="store_true",
        help=("Use the multiprocessing code path even when nprocs=1."),
        default=False,
    )
    experimental.add_argument(
        "--tmask",
        dest="tmaskname",
        action="store",
        type=lambda x: pf.is_valid_file(parser, x),
        metavar="FILE",
        help=(
            "Only correlate during epochs specified "
            "in MASKFILE (NB: each line of FILE "
            "contains the time and duration of an "
            "epoch to include."
        ),
        default=None,
    )

    # Debugging options
    debugging = parser.add_argument_group("Debugging options")
    debugging.add_argument(
        "--singleproc_getNullDist",
        dest="singleproc_getNullDist",
        action="store_true",
        help=("Force single proc path for getNullDist."),
        default=False,
    )
    debugging.add_argument(
        "--singleproc_calcsimilarity",
        dest="singleproc_calcsimilarity",
        action="store_true",
        help=("Force single proc path for calcsimilarity."),
        default=False,
    )
    debugging.add_argument(
        "--singleproc_peakeval",
        dest="singleproc_peakeval",
        action="store_true",
        help=("Force single proc path for peakeval."),
        default=False,
    )
    debugging.add_argument(
        "--singleproc_fitcorr",
        dest="singleproc_fitcorr",
        action="store_true",
        help=("Force single proc path for fitcorr."),
        default=False,
    )
    debugging.add_argument(
        "--singleproc_glm",
        dest="singleproc_glm",
        action="store_true",
        help=("Force single proc path for glm."),
        default=False,
    )

    return parser


def process_args(inputargs=None):
    """
    Compile arguments for rapidtide workflow.
    """
    if inputargs is None:
        LGR.info("processing command line arguments")
        # write out the command used
        try:
            args = vars(_get_parser().parse_args())
            argstowrite = sys.argv
        except SystemExit:
            _get_parser().print_help()
            raise
    else:
        LGR.info("processing passed argument list:")
        LGR.info(inputargs)
        try:
            args = vars(_get_parser().parse_args(inputargs))
            argstowrite = inputargs
        except SystemExit:
            _get_parser().print_help()
            raise

    sh = logging.StreamHandler()
    if args["debug"]:
        logging.basicConfig(level=logging.DEBUG, handlers=[sh])
    else:
        logging.basicConfig(level=logging.INFO, handlers=[sh])

    # save the raw and formatted command lines
    args["commandlineargs"] = argstowrite[1:]
    thecommandline = " ".join(argstowrite)
    tide_io.writevec([thecommandline], args["outputname"] + "_commandline.txt")
    formattedcommandline = []
    for thetoken in argstowrite[0:3]:
        formattedcommandline.append(thetoken)
    for thetoken in argstowrite[3:]:
        if thetoken[0:2] == "--":
            formattedcommandline.append(thetoken)
        else:
            formattedcommandline[-1] += " " + thetoken
    for i in range(len(formattedcommandline)):
        if i > 0:
            prefix = "    "
        else:
            prefix = ""
        if i < len(formattedcommandline) - 1:
            suffix = " \\"
        else:
            suffix = ""
        formattedcommandline[i] = prefix + formattedcommandline[i] + suffix
    tide_io.writevec(formattedcommandline, args["outputname"] + "_formattedcommandline.txt")

    LGR.debug("\nbefore postprocessing:\n{}".format(args))

    # some tunable parameters for internal debugging
    args["dodemean"] = True
    # what fraction of the correlation window to avoid on either end when
    # fitting
    args["edgebufferfrac"] = 0.0
    # only do fits in voxels that exceed threshhold
    args["enforcethresh"] = True
    # if set to the location of the first autocorrelation sidelobe,
    # this will fold back sidelobes
    args["lagmod"] = 1000.0
    # zero out peaks with correlations lower than this value
    args["lthreshval"] = 0.0
    # zero out peaks with correlations higher than this value
    args["uthreshval"] = 1.0
    # width of the reference autocorrelation function
    args["absmaxsigma"] = 10000.0
    # width of the reference autocorrelation function
    args["absminsigma"] = 0.25

    # correlation fitting
    # Peak value must be within specified range.
    # If false, allow max outside if maximum
    # correlation value is that one end of the range.
    args["hardlimit"] = True
    # The fraction of the main peak over which points are included in the peak
    args["searchfrac"] = 0.5
    args["mp_chunksize"] = 50000

    # significance estimation
    args["sighistlen"] = 1000
    args["dosighistfit"] = True

    # output options
    args["savedespecklemasks"] = True
    args["saveglmfiltered"] = True
    args["savemotionfiltered"] = False
    args["savecorrmask"] = True

    # refinement options
    args["filterbeforePCA"] = True
    args["dispersioncalc_step"] = 0.50

    # autocorrelation processing
    args["check_autocorrelation"] = True
    args["acwidth"] = 0.0  # width of the reference autocorrelation function

    # diagnostic information about version
    (
        args["release_version"],
        args["git_longtag"],
        args["git_date"],
        args["git_isdirty"],
    ) = tide_util.version()
    args["python_version"] = str(sys.version_info)

    # configure the filter
    # if arbvec is set, we are going set up an arbpass filter
    if args["arbvec"] is not None:
        if len(args["arbvec"]) == 2:
            args["arbvec"].append(args["arbvec"][0] * 0.95)
            args["arbvec"].append(args["arbvec"][1] * 1.05)
        elif len(args["arbvec"]) != 4:
            raise ValueError("Argument '--arb' must be either two or four " "floats.")
        # NOTE - this vector is LOWERPASS, UPPERPASS, LOWERSTOP, UPPERSTOP
        # setfreqs expects LOWERSTOP, LOWERPASS, UPPERPASS, UPPERSTOP
        theprefilter = tide_filt.noncausalfilter(
            "arb", transferfunc=args["filtertype"], debug=args["debug"]
        )
        theprefilter.setfreqs(
            args["arbvec"][2],
            args["arbvec"][0],
            args["arbvec"][1],
            args["arbvec"][3],
        )
    else:
        theprefilter = tide_filt.noncausalfilter(
            args["filterband"],
            transferfunc=args["filtertype"],
            debug=args["debug"],
        )

    theprefilter.setbutterorder(args["filtorder"])
    (
        args["lowerstop"],
        args["lowerpass"],
        args["upperpass"],
        args["upperstop"],
    ) = theprefilter.getfreqs()

    # Additional argument parsing not handled by argparse
    args["despeckle_passes"] = np.max([args["despeckle_passes"], 0])

    if "lag_extrema_nondefault" in args.keys():
        args["lagmin_nondefault"] = True
        args["lagmax_nondefault"] = True

    args["lagmin"] = args["lag_extrema"][0]
    args["lagmax"] = args["lag_extrema"][1]
    args["startpoint"] = args["timerange"][0]
    if args["timerange"][1] == -1:
        args["endpoint"] = 100000000
    else:
        args["endpoint"] = args["timerange"][1]

    args["offsettime_total"] = args["offsettime"] + 0.0

    reg_ref_used = (
        (args["lagminthresh"] != 0.5)
        or (args["lagmaxthresh"] != 5.0)
        or (args["ampthresh"] != 0.3)
        or (args["sigmathresh"] != 100.0)
        or (args["refineoffset"])
    )
    if reg_ref_used and args["passes"] == 1:
        LGR.warning(
            "One or more arguments have been set that are only "
            "relevant if performing refinement.  "
            "If you want to do refinement, set passes > 1."
        )

    if args["numestreps"] == 0:
        args["ampthreshfromsig"] = False
    else:
        args["ampthreshfromsig"] = True

    if args["ampthresh"] < 0.0:
        args["ampthresh"] = 0.3
        args["ampthreshfromsig"] = True
    else:
        args["ampthreshfromsig"] = False

    if args["despeckle_thresh"] != 5.0 and args["despeckle_passes"] == 0:
        args["despeckle_passes"] = 1

    if args["zerooutbadfit"]:
        args["nohistzero"] = False
    else:
        args["nohistzero"] = True

    if args["fixeddelayvalue"] is not None:
        args["fixdelay"] = True
        args["lag_extrema"] = (
            args["fixeddelayvalue"] - 10.0,
            args["fixeddelayvalue"] + 10.0,
        )
    else:
        args["fixdelay"] = False

    if args["in_file"].endswith("txt") and args["realtr"] == "auto":
        raise ValueError(
            "Either --datatstep or --datafreq must be provided " "if data file is a text file."
        )

    if args["realtr"] != "auto":
        fmri_tr = float(args["realtr"])
    else:
        if tide_io.checkifcifti(args["in_file"]):
            fmri_tr, dummy = tide_io.getciftitr(nib.load(args["in_file"]).header)
        else:
            fmri_tr = nib.load(args["in_file"]).header.get_zooms()[3]
    args["realtr"] = fmri_tr

    if args["inputfreq"] == "auto":
        args["inputfreq"] = 1.0 / fmri_tr

    # mask processing
    if args["corrmaskincludespec"] is not None:
        (args["corrmaskincludename"], args["corrmaskincludevals"],) = tide_io.processnamespec(
            args["corrmaskincludespec"],
            "Including voxels where ",
            "in correlation calculations.",
        )
    else:
        args["corrmaskincludename"] = None

    if args["globalmeanincludespec"] is not None:
        (args["globalmeanincludename"], args["globalmeanincludevals"],) = tide_io.processnamespec(
            args["globalmeanincludespec"], "Including voxels where ", "in global mean."
        )
    else:
        args["globalmeanincludename"] = None

    if args["globalmeanexcludespec"] is not None:
        (args["globalmeanexcludename"], args["globalmeanexcludevals"],) = tide_io.processnamespec(
            args["globalmeanexcludespec"],
            "Excluding voxels where ",
            "from global mean.",
        )
    else:
        args["globalmeanexcludename"] = None

    if args["refineincludespec"] is not None:
        (args["refineincludename"], args["refineincludevals"],) = tide_io.processnamespec(
            args["refineincludespec"], "Including voxels where ", "in refinement."
        )
    else:
        args["refineincludename"] = None

    if args["refineexcludespec"] is not None:
        (args["refineexcludename"], args["refineexcludevals"],) = tide_io.processnamespec(
            args["refineexcludespec"], "Excluding voxels where ", "from refinement."
        )
    else:
        args["refineexcludename"] = None

    # motion processing
    if args["motionfilespec"] is not None:
        (args["motionfilename"], args["motionfilevals"]) = tide_io.processnamespec(
            args["motionfilespec"], "Using columns in ", "as motion regressors."
        )
    else:
        args["motionfilename"] = None

    if args["venousrefine"]:
        LGR.warning("Using 'venousrefine' macro. Overriding any affected arguments.")
        args["lagminthresh"] = 2.5
        args["lagmaxthresh"] = 6.0
        args["ampthresh"] = 0.5
        args["ampthreshfromsig"] = False
        args["lagmaskside"] = "upper"

    if args["nirs"]:
        LGR.warning("Using 'nirs' macro. Overriding any affected arguments.")
        args["nothresh"] = False
        args["preservefiltering"] = True
        args["refineprenorm"] = "var"
        args["ampthresh"] = 0.7
        args["ampthreshfromsig"] = False
        args["lagmaskthresh"] = 0.1

    if args["delaymapping"]:
        pf.setifnotset(args, "despeckle_passes", 4)
        pf.setifnotset(args, "lagmin", -10.0)
        pf.setifnotset(args, "lagmax", 30.0)
        args["passes"] = 3
        args["refineoffset"] = True
        args["pickleft"] = True
        args["limitoutput"] = True
        pf.setifnotset(args, "doglmfilt", False)

    if args["denoising"]:
        pf.setifnotset(args, "despeckle_passes", 4)
        pf.setifnotset(args, "lagmin", -10.0)
        pf.setifnotset(args, "lagmax", 10.0)
        pf.setifnotset(args, "peakfittype", "gauss")
        args["passes"] = 3
        args["refineoffset"] = True
        args["doglmfilt"] = True

    # process limitoutput
    if args["limitoutput"]:
        args["savemovingsignal"] = False
        args["savelagregressors"] = False
    else:
        args["savemovingsignal"] = True
        args["savelagregressors"] = True

    # dispersion calculation
    args["dispersioncalc_lower"] = args["lagmin"]
    args["dispersioncalc_upper"] = args["lagmax"]
    args["dispersioncalc_step"] = np.max(
        [
            (args["dispersioncalc_upper"] - args["dispersioncalc_lower"]) / 25,
            args["dispersioncalc_step"],
        ]
    )

    LGR.debug("\nafter postprocessing\n{}".format(args))

    # start the clock!
    tide_util.checkimports(args)

    return args, theprefilter
