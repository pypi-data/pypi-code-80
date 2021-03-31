# Copyright 2021 Cambridge Quantum Computing
#
# You may not use this file except in compliance with the Licence.
# You may obtain a copy of the Licence in the LICENCE file accompanying
# these documents or at:
#
#     https://cqcl.github.io/pytket/build/html/licence.html

from typing import Tuple
from pytket.circuit import Circuit  # type: ignore
from pytket.passes import ContextSimp  # type: ignore
from pytket.transform import separate_classical  # type: ignore


def prepare_circuit(circ: Circuit) -> Tuple[Circuit, Circuit]:
    """
    Prepare a circuit for processing by a backend device.

    This method first makes all inputs into Create operations (assuming an initial all-
    zero state) and all outputs into Discard operations (so that the circuit can no
    longer be usefully extended or appended to another circuit). It then attempts to
    apply various simplifications that take advantage of the known initial state and the
    fact that any unmeasured state is discarded. Finally, it separates the circuit into
    two circuits, the first of which is to be run on the backend (after any further
    compilation has been applied), and the second of which is a pure-classical circuit
    (on the same bits) which encodes classical post-processing of the measurement
    results. This post-processing is applied automatically when you pass the classical
    circuit as the `ppcirc` argument to `BackendResult.get_counts()` or
    `BackendResult.get_shots()`.

    :param circ: input circuit
    :return: (c0, ppcirc) where c0 is the simplified circuit and ppcirc should be passed
        to `BackendResult.get_counts()` or `BackendResult.get_shots()` when retrieving
        the final results.
    """
    circ.qubit_create_all()
    circ.qubit_discard_all()
    ContextSimp().apply(circ)
    return separate_classical(circ)  # type: ignore
