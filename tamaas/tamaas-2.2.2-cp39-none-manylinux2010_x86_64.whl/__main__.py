#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# vim: set ft=python:

import sys
import io
import time
import argparse
import tamaas as tm
import numpy as np


__author__ = "Lucas Frérot"
__copyright__ = (
    "Copyright (©) 2019-2021, EPFL (École Polytechnique Fédérale de Lausanne),"
    "\nLaboratory (LSMS - Laboratoire de Simulation en Mécanique des Solides)"
)
__license__ = "AGPL"
__email__ = "lucas.frerot@gmail.com"


def load_stream(stream):
    """
    Load numpy from binary stream (allows piping)

    Code from
    https://gist.github.com/CMCDragonkai/3c99fd4aabc8278b9e17f50494fcc30a
    """
    np_magic = stream.read(6)
    # use the sys.stdin.buffer to read binary data
    np_data = stream.read()
    # read it all into an io.BytesIO object
    return io.BytesIO(np_magic + np_data)


def surface(args):
    if args.generator == 'random_phase':
        generator = tm.SurfaceGeneratorRandomPhase2D(args.sizes)
    elif args.generator == 'filter':
        generator = tm.SurfaceGeneratorFilter2D(args.sizes)
    else:
        raise ValueError('Unknown generator method {}'.format(args.generator))

    generator.spectrum = tm.Isopowerlaw2D()
    generator.spectrum.q0 = args.cutoffs[0]
    generator.spectrum.q1 = args.cutoffs[1]
    generator.spectrum.q2 = args.cutoffs[2]
    generator.spectrum.hurst = args.hurst
    generator.random_seed = args.seed

    surface = generator.buildSurface() / generator.spectrum.rmsSlopes() \
        * args.rms

    output = args.output if args.output is not None else sys.stdout

    np.savetxt(output, surface)


def contact(args):
    from tamaas.dumpers import NumpyDumper

    tm.set_log_level(tm.LogLevel.error)

    if not args.input:
        input = sys.stdin
    else:
        input = args.input

    surface = np.loadtxt(input)

    discretization = surface.shape
    system_size = [1., 1.]

    model = tm.ModelFactory.createModel(tm.model_type.basic_2d,
                                        system_size, discretization)
    solver = tm.PolonskyKeerRey(model, surface, args.tol)

    solver.solve(args.load)

    dumper = NumpyDumper('numpy', 'traction', 'displacement')
    dumper.dump_to_file(sys.stdout.buffer, model)


def plot(args):
    import matplotlib.pyplot as plt

    fig, (ax_traction, ax_displacement) = plt.subplots(1, 2)

    ax_traction.set_title('Traction')
    ax_displacement.set_title('Displacement')

    with load_stream(sys.stdin.buffer) as f_np:
        data = np.load(f_np)
        ax_traction.imshow(data['traction'])
        ax_displacement.imshow(data['displacement'])

    fig.set_size_inches(10, 6)
    fig.tight_layout()

    plt.show()


def main():
    parser = argparse.ArgumentParser(
        prog='tamaas',
        description=("tm.py is a simple utility script for surface generation and,"
                     " elastic contact computation and plotting of contact"
                     " solutions"),
    )

    subs = parser.add_subparsers(title='commands',
                                 description='utility commands')

    # Arguments for surface command
    parser_surface = subs.add_parser(
        'surface', description='Generate a self-affine rough surface')
    parser_surface.add_argument("--cutoffs", "-K",
                                nargs=3,
                                type=int,
                                help="Long, rolloff and short wavelength cutoffs",
                                metavar=('k_l', 'k_r', 'k_s'),
                                required=True)
    parser_surface.add_argument("--sizes",
                                nargs=2,
                                type=int,
                                help="Number of points",
                                metavar=('nx', 'ny'),
                                required=True)
    parser_surface.add_argument("--hurst", "-H",
                                type=float,
                                help="Hurst exponent",
                                required=True)
    parser_surface.add_argument("--rms",
                                type=float,
                                help="Root-mean-square of slopes",
                                default=1.)
    parser_surface.add_argument("--seed",
                                type=int,
                                help="Random seed",
                                default=int(time.time()))
    parser_surface.add_argument("--generator",
                                help="Generation method",
                                choices=('random_phase', 'filter'),
                                default='random_phase')
    parser_surface.add_argument("--output", "-o",
                                help="Output file name (compressed if .gz)")
    parser_surface.set_defaults(func=surface)


    # Arguments for contact command
    parser_contact = subs.add_parser(
        'contact',
        description="Compute the elastic contact solution with a given surface")

    parser_contact.add_argument("--input", "-i",
                                help="Rough surface file (default read from stdin)")
    parser_contact.add_argument("--tol",
                                type=float,
                                default=1e-12,
                                help="Solver tolerance")
    parser_contact.add_argument("load",
                                type=float,
                                help="Applied average pressure")
    parser_contact.set_defaults(func=contact)


    # Arguments for plot command
    parser_plot = subs.add_parser(
        'plot', description='Plot contact solution')
    parser_plot.set_defaults(func=plot)

    args = parser.parse_args()

    try:
        args.func(args)
    except AttributeError:
        parser.print_usage()

if __name__ == '__main__':
    main()
