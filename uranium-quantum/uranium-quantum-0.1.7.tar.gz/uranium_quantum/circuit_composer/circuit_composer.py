"""A simple API for creating quantum circuits in yaml format using python."""

from typing import Dict, List


class QbitAleadyTaken(Exception):
    """Will be thrown when a gate exist at indicated step and qubit."""

    def __init__(self, qbit, step):
        """Raise exception."""
        super().__init__()
        self.message = (
            f"The position defined by step {step} and qbit {qbit} is already taken."
        )


class QbitIndexLargerThanRegistrySize(Exception):
    """Will throw when the index of the qbit where a gate should be applied is\
 larger than the maximum size limit allowed by the quantum registry."""

    def __init__(self, qbit, step):
        """Raise exception."""
        super().__init__()
        self.message = f"Requested qbit index {qbit} during step {step} is \
larger then the maximum size allowed by quantum registry."


class QuantumRegistry:
    """A quantum registry is basically a collection of qubits where quantum gates
    can be allocated at positions defined by a qbit index and step index."""

    def __init__(self, no_qbits):
        """Intialize a quantum register having a predefined fixed number of qbits."""
        self._no_qbits: int
        self._current_step: int
        self._gates: Dict[int, Dict]
        self._qbits_taken: Dict[int, List]

        self._no_qbits = no_qbits
        self._current_step = 0
        self._gates = {}
        self._qbits_taken = {}

        self._gates[0] = []
        self._qbits_taken[0] = set()

    def increment_step(self):
        """Increment current step index. A step used a to group a collection of \
gates that can be applied in parallel on a quantum registry. Steps is a facility added \
mainly for easier visualisation of the collection of gates applied on a circuit \
in a web browser. Grouping gates in a layout indexed by steps also facilitates \
delivering some of the logic intended by the creator of the circuit."""
        self._current_step += 1
        self._gates[self._current_step] = []
        self._qbits_taken[self._current_step] = set()
        return self

    def _gates_in_current_step(self):
        return self._gates[self._current_step]

    def _check_registry_size(self, target):
        if target >= self._no_qbits:
            raise QbitIndexLargerThanRegistrySize(target, self._current_step)

    def _check_qbit_alocated(self, qbit):
        if qbit in self._qbits_taken[self._current_step]:
            raise QbitAleadyTaken(qbit, self._current_step)

    def _qbits_taken_in_current_step(self):
        return self._qbits_taken[self._current_step]

    def current_step(self):
        """Get number of steps"""
        return self._current_step

    def export(self, name):
        """Export the quantum circuit to a file in YAML format."""
        if not name.endswith(".yaml") and not name.endswith(".yml"):
            name = name + ".yaml"
        with open(name, "w") as yaml_file:
            yaml_file.write("steps:\n")
            for step in range(self._current_step + 1):
                yaml_file.write("  - index: " + str(step) + "\n")
                yaml_file.write("    gates:\n")
                for gate in self._gates[step]:
                    yaml_file.write("      - name: " + gate["name"] + "\n")
                    if "control" in gate:
                        yaml_file.write(
                            "        control: " + str(gate["control"]) + "\n"
                        )
                    if "controlstate" in gate:
                        yaml_file.write(
                            "        controlstate: " + str(gate["controlstate"]) + "\n"
                        )
                    if "control2" in gate:
                        yaml_file.write(
                            "        control2: " + str(gate["control2"]) + "\n"
                        )
                    if "controlstate2" in gate:
                        yaml_file.write(
                            "        controlstate2: "
                            + str(gate["controlstate2"])
                            + "\n"
                        )
                    yaml_file.write("        target: " + str(gate["target"]) + "\n")
                    if "target2" in gate:
                        yaml_file.write(
                            "        target2: " + str(gate["target2"]) + "\n"
                        )
                    if "theta" in gate:
                        yaml_file.write("        theta: " + str(gate["theta"]) + "\n")
                    if "phi" in gate:
                        yaml_file.write("        phi: " + str(gate["phi"]) + "\n")
                    if "lambda" in gate:
                        yaml_file.write("        lambda: " + str(gate["lambda"]) + "\n")
                    if "root-k" in gate:
                        yaml_file.write(
                            "        root: " + f'1/2^{gate["root-k"]}' + "\n"
                        )
                    if "root-t" in gate:
                        yaml_file.write(
                            "        root: " + f'1/{str(gate["root-t"])}' + "\n"
                        )
                    if "bit" in gate:
                        yaml_file.write("        bit: " + str(gate["bit"]) + "\n")

    def setup_new_gate(self, gate, *qbits):
        for qbit in qbits:
            self._check_registry_size(qbit)
            self._check_qbit_alocated(qbit)
        for qbit in range(min(qbits), max(qbits) + 1):
            self._qbits_taken_in_current_step().add(qbit)
        self._gates_in_current_step().append(gate)

    def gate_u1(self, target, lambda_radians):
        """Apply a generic one parameters gate on this target, angle argument is
        specified in radians. This is a generic, one parameter, unitary single
        bit gate and is defined as: u3(0, 0, λ). The "u1" gate acts on a single
        qubit. Leaves the basis state |0⟩ unchanged and map |1⟩ to exp(i*λ)|1⟩.
        The probability of measuring a |0⟩ or |1⟩ is unchanged after applying
        this gate, however it modifies the phase of the quantum state."""
        gate = {}
        gate["name"] = "u1"
        gate["target"] = target
        gate["lambda"] = lambda_radians
        self.setup_new_gate(gate, target)
        return self

    def gate_u2(self, target, phi_radians, lambda_radians):
        """Apply a generic two parameters gate on this target qubit,
        the two rotation arguments are specified in radians. This is a generic,
        two parametric, unitary single bit gate and is defined as: u3(π/2, φ, λ)."""
        gate = {}
        gate["name"] = "u2"
        gate["target"] = target
        gate["phi"] = phi_radians
        gate["lambda"] = lambda_radians
        self.setup_new_gate(gate, target)
        return self

    def gate_u3(self, target, theta_radians, phi_radians, lambda_radians):
        """Apply a generic three parameters gate on this target qubit,
        the three rotation arguments are specified in radians."""
        gate = {}
        gate["name"] = "u3"
        gate["target"] = target
        gate["theta"] = theta_radians
        gate["phi"] = phi_radians
        gate["lambda"] = lambda_radians
        self.setup_new_gate(gate, target)
        return self

    def gate_identity(self, target):
        """Apply an 'identity" gate to this qubit. The "identity" gate acts on a single
        qubit and preserves current state of the qubit it is applied to."""
        gate = {}
        gate["name"] = "identity"
        gate["target"] = target
        self.setup_new_gate(gate, target)
        return self

    def gate_hadamard(self, target):
        """Apply a "hadamard" gate to this qubit. The "hadamard" gate acts on a single
        qubit and is defined as: u2(0, π). This gate creates a superposition by mapping
        |0⟩ to |+⟩ and |1⟩ to |-⟩. It is the combination of two rotations, first a π
        rotation about the Z-axis of the Bloch sphere followed by a π/2 about the Y-axis."""
        gate = {}
        gate["name"] = "hadamard"
        gate["target"] = target
        self.setup_new_gate(gate, target)
        return self

    def gate_pauli_x(self, target):
        """Apply a "pauli-x" gate to this qubit. The "pauli-x" gate acts on a single
        qubit and is defined as: u3(π, 0, π). It is the quantum equivalent of the
        NOT gate for classical computers. This gate, maps |0⟩ to |1⟩ and |1⟩ to |0⟩.
        It is equivalent to a rotation around the X-axis of the Bloch sphere by
        π radians. This gate is also known as CNOT gate."""
        gate = {}
        gate["name"] = "pauli-x"
        gate["target"] = target
        self.setup_new_gate(gate, target)
        return self

    def gate_pauli_y(self, target):
        """Apply a "pauli-y" gate to this qubit. The "pauli-y" gate acts on a single
        qubit and is defined as: u3(π, π/2, π/2). It is equivalent to a rotation around
        the Y-axis of the Bloch sphere by π radians."""
        gate = {}
        gate["name"] = "pauli-y"
        gate["target"] = target
        self.setup_new_gate(gate, target)
        return self

    def gate_pauli_z(self, target):
        """Apply a "pauli-z" gate to this qubit. The "pauli-z" gate acts on a single
        qubit and is defined as: u1(π). It is equivalent to a rotation around the
        Z-axis of the Bloch sphere by π radians. It is a special case of a phase
        shift gate "u1" with λ equal to π. It leaves the basis state |0⟩ unchanged
        and maps |1⟩ to −|1⟩. This gate is also known as CPHASE gate."""
        gate = {}
        gate["name"] = "pauli-z"
        gate["target"] = target
        self.setup_new_gate(gate, target)
        return self

    def gate_pauli_x_root(self, target, t=None, k=None):
        """Apply a "pauli-x-root" gate to this qubit, an operation which amounts to
        aplying a root of the pauli-x gate. The root value is specified either via a
        parameter named 't' which represents the exact root value or via a parameter
        named 'k' which specifies the root value as 2^k. Because non integer powers of
        a matrix are not unique, this gate is defined as a rotation around X-axis of
        the Bloch sphere with an angle given by π/t or π/2^k respectively."""
        assert t or k
        gate = {}
        gate["name"] = "pauli-x-root"
        if k:
            gate["root-k"] = k
        elif t:
            gate["root-t"] = t
        gate["target"] = target
        self.setup_new_gate(gate, target)
        return self

    def gate_pauli_y_root(self, target, t=None, k=None):
        """Apply a "pauli-y-root" gate to this qubit, an operation which amounts to
        aplying a root of the pauli-y gate. The root value is specified either via a
        parameter named 't' which represents the exact root value or via a parameter
        named 'k' which specifies the root value as 2^k. Because non integer powers of
        a matrix are not unique, this gate is defined as a rotation around Y-axis of
        the Bloch sphere with an angle given by π/t or π/2^k respectively."""
        assert t or k
        gate = {}
        gate["name"] = "pauli-y-root"
        if k:
            gate["root-k"] = k
        elif t:
            gate["root-t"] = t
        gate["target"] = target
        self.setup_new_gate(gate, target)
        return self

    def gate_pauli_z_root(self, target, t=None, k=None):
        """Apply a "pauli-z-root" gate to this qubit, an operation which amounts to
        aplying a root of the pauli-z gate. The root value is specified either via a
        parameter named 't' which represents the exact root value or via a parameter
        named 'k' which specifies the root value as 2^k. Because non integer powers of
        a matrix are not unique, this gate is defined as a rotation around Z-axis of
        the Bloch sphere with an angle given by π/t or π/2^k respectively."""
        assert t or k
        gate = {}
        gate["name"] = "pauli-z-root"
        if k:
            gate["root-k"] = k
        elif t:
            gate["root-t"] = t
        gate["target"] = target
        self.setup_new_gate(gate, target)
        return self

    def gate_pauli_x_root_dagger(self, target, t=None, k=None):
        """Apply a "pauli-x-root" gate to this qubit, an operation which amounts to
        aplying a root of the pauli-x gate. The root value is specified either via a
        parameter named 't' which represents the exact root value or via a parameter
        named 'k' which specifies the root value as 2^k. Because non integer powers of
        a matrix are not unique, this gate is defined as a rotation around X-axis of
        the Bloch sphere with an angle given by π/t or π/2^k respectively."""
        assert t or k
        gate = {}
        gate["name"] = "pauli-x-root-dagger"
        if k:
            gate["root-k"] = k
        elif t:
            gate["root-t"] = t
        gate["target"] = target
        self.setup_new_gate(gate, target)
        return self

    def gate_pauli_y_root_dagger(self, target, t=None, k=None):
        """Apply a "pauli-y-root" gate to this qubit, an operation which amounts to
        aplying a root of the pauli-y gate. The root value is specified either via a
        parameter named 't' which represents the exact root value or via a parameter
        named 'k' which specifies the root value as 2^k. Because non integer powers of
        a matrix are not unique, this gate is defined as a rotation around Y-axis of
        the Bloch sphere with an angle given by π/t or π/2^k respectively."""
        assert t or k
        gate = {}
        gate["name"] = "pauli-y-root-dagger"
        if k:
            gate["root-k"] = k
        elif t:
            gate["root-t"] = t
        gate["target"] = target
        self.setup_new_gate(gate, target)
        return self

    def gate_pauli_z_root_dagger(self, target, t=None, k=None):
        """Apply a "pauli-z-root" gate to this qubit, an operation which amounts to
        aplying a root of the pauli-z gate. The root value is specified either via a
        parameter named 't' which represents the exact root value or via a parameter
        named 'k' which specifies the root value as 2^k. Because non integer powers of
        a matrix are not unique, this gate is defined as a rotation around Z-axis of
        the Bloch sphere with an angle given by π/t or π/2^k respectively."""
        assert t or k
        gate = {}
        gate["name"] = "pauli-z-root-dagger"
        if k:
            gate["root-k"] = k
        elif t:
            gate["root-t"] = t
        gate["target"] = target
        self.setup_new_gate(gate, target)
        return self

    def gate_t(self, target):
        """Apply a "t" gate on this qubit. The "t" gate acts on a single qubit and is
        defined as: u1(π/4). Leaves the basis state |0⟩ unchanged and map |1⟩ to
        exp(i*π/4)|1⟩. The probability of measuring a |0⟩ or |1⟩ is unchanged after
        applying this gate, however it modifies the phase of the quantum state. The
        "t" gate is related to "s" gate by the relation: s = t * t."""
        gate = {}
        gate["name"] = "t"
        gate["target"] = target
        self.setup_new_gate(gate, target)
        return self

    def gate_t_dagger(self, target):
        """Apply a "t-dagger" gate on this qubit. The "t-dagger" gate acts on a single
        qubit and is defined as: u1(-π/4). It is the conjugate transpose of "t" gate.
        Leaves the basis state |0⟩ unchanged and map |1⟩ to exp(-i*π/4) |1⟩. The
        probability of measuring a |0⟩ or |1⟩ is unchanged after applying this gate,
        however it modifies the phase of the quantum state."""
        gate = {}
        gate["name"] = "t-dagger"
        gate["target"] = target
        self.setup_new_gate(gate, target)
        return self

    def gate_rx_theta(self, target, theta):
        """Apply a "rx-theta" gate on this target qbit, angle argument is specified
        in radians. The "rx-theta" gate acts on a single qubit and is defined as:
        u3(θ, -π/2, π/2). It is a rotation through angle θ radians around the
        X-axis of the Bloch sphere."""
        gate = {}
        gate["name"] = "rx-theta"
        gate["target"] = target
        gate["theta"] = theta
        self.setup_new_gate(gate, target)
        return self

    def gate_ry_theta(self, target, theta):
        """Apply a "ry-theta" gate on this target qbit, angle argument is specified
        in radians. Controlled gates act on 2 qubits, where first acts as a control
        and the second acts as target. The "ctrl-ry-theta" gate applies the "ry-theta"
        gate on the target qubit only when the control qubit is |1⟩ otherwise leaves
        it unchanged."""
        gate = {}
        gate["name"] = "ry-theta"
        gate["target"] = target
        gate["theta"] = theta
        self.setup_new_gate(gate, target)
        return self

    def gate_rz_theta(self, target, theta):
        """Apply a "rz-theta" gate on this target qbit, angle is specified in radians.
        Controlled gates act on 2 qubits, where first acts as a control and the second
        acts as target. The "ctrl-rz-theta" gate applies the "rz-theta" gate on the
        target qubit only when the control qubit is |1⟩ otherwise leaves it unchanged."""
        gate = {}
        gate["name"] = "rz-theta"
        gate["target"] = target
        gate["theta"] = theta
        self.setup_new_gate(gate, target)
        return self

    def gate_s(self, target):
        """Apply a "s" gate on this qubit. The "s" gate acts on a single qubit and is
        defined as: u1(π/2). It represents as π/2 radians rotation around the Z-axis
        of the Bloch sphere. The "s" gate is related to the "t" gate by the relationship
        s = t * t. It is also the square root of pauli-z gate."""
        gate = {}
        gate["name"] = "s"
        gate["target"] = target
        self.setup_new_gate(gate, target)
        return self

    def gate_s_dagger(self, target):
        """Apply a "s-dagger" gate on this qubit. The "s-dagger" gate acts on a single
        qubit and is defined as: u1(-π/2). It is the conjugate transpose of "s" gate."""
        gate = {}
        gate["name"] = "s-dagger"
        gate["target"] = target
        self.setup_new_gate(gate, target)
        return self

    def gate_xx(self, target, target2, theta):
        """Apply an Ising "xx" gate on these two qbits."""
        assert target != target2
        gate = {}
        gate["name"] = "xx"
        gate["target"] = target
        gate["target2"] = target2
        gate["theta"] = theta
        self.setup_new_gate(gate, target, target2)
        return self

    def gate_yy(self, target, target2, theta):
        """Apply an Ising "yy" gate on these two qbits."""
        assert target != target2
        gate = {}
        gate["name"] = "yy"
        gate["target"] = target
        gate["target2"] = target2
        gate["theta"] = theta
        self.setup_new_gate(gate, target, target2)
        return self

    def gate_zz(self, target, target2, theta):
        """Apply an Ising "zz" gate on these two qbits."""
        assert target != target2
        gate = {}
        gate["name"] = "zz"
        gate["target"] = target
        gate["target2"] = target2
        gate["theta"] = theta
        self.setup_new_gate(gate, target, target2)
        return self

    def gate_swap(self, target, target2):
        """Apply a "swap" gate on these two qbits."""
        assert target != target2
        gate = {}
        gate["name"] = "swap"
        gate["target"] = target
        gate["target2"] = target2
        self.setup_new_gate(gate, target, target2)
        return self

    def gate_iswap(self, target, target2):
        """Apply a "iswap" gate on these two qbits."""
        assert target != target2
        gate = {}
        gate["name"] = "iswap"
        gate["target"] = target
        gate["target2"] = target2
        self.setup_new_gate(gate, target, target2)
        return self

    def gate_swap_phi(self, target, target2, phi):
        """Apply a "swap-phi" gate on these two qbits."""
        assert target != target2
        gate = {}
        gate["name"] = "swap-phi"
        gate["target"] = target
        gate["target2"] = target2
        gate["phi"] = phi
        self.setup_new_gate(gate, target, target2)
        return self

    def gate_sqrt_swap(self, target, target2):
        """Apply a "sqrt-swap" gate on these two qbits."""
        assert target != target2
        gate = {}
        gate["name"] = "sqrt-swap"
        gate["target"] = target
        gate["target2"] = target2
        self.setup_new_gate(gate, target, target2)
        return self

    def gate_ctrl_hadamard(self, control, control_state, target):
        """Apply a controlled "hadamard" gate to these two qbits. Controlled gates act
        on 2 qubits, where first acts as a control and the second acts as target. The
        control state is expressed in computational basis and most often has value 1
        corresponding to |1⟩ state."""
        assert control != target
        gate = {}
        gate["name"] = "ctrl-hadamard"
        gate["target"] = target
        gate["control"] = control
        gate["controlstate"] = control_state
        self.setup_new_gate(gate, control, target)
        return self

    def gate_ctrl_u3(
        self, control, control_state, target, theta_radians, phi_radians, lambda_radians
    ):
        """Apply a controlled generic three parameter gate on these two qbits.
        Controlled gates act on 2 qubits, where first acts as a control and
        the second acts as target. The  control state is expressed in computational
        basis and most often has value 1 corresponding to |1⟩ state."""
        assert control != target
        gate = {}
        gate["name"] = "ctrl-u3"
        gate["target"] = target
        gate["control"] = control
        gate["controlstate"] = control_state
        gate["theta"] = theta_radians
        gate["phi"] = phi_radians
        gate["lambda"] = lambda_radians
        self.setup_new_gate(gate, control, target)
        return self

    def gate_ctrl_u2(self, control, control_state, target, phi_radians, lambda_radians):
        """Apply a controlled generic two parameters gate on these two qbits. Controlled
        gates act on 2 qubits, where first acts as a control and the second acts
        as target. The control state is expressed in computational basis and most often
        has value 1 corresponding to |1⟩ state."""
        assert control != target
        gate = {}
        gate["name"] = "ctrl-u2"
        gate["target"] = target
        gate["control"] = control
        gate["controlstate"] = control_state
        gate["phi"] = phi_radians
        gate["lambda"] = lambda_radians
        self.setup_new_gate(gate, control, target)
        return self

    def gate_ctrl_u1(self, control, control_state, target, lambda_radians):
        """Apply a controlled generic one parameter gate on these two qbits.
        Controlled gates act on 2 qubits, where first acts as a control and
        the second acts as target. The control state is expressed in computational
        basis and most often has value 1 corresponding to |1⟩ state."""
        assert control != target
        gate = {}
        gate["name"] = "ctrl-u1"
        gate["target"] = target
        gate["control"] = control
        gate["controlstate"] = control_state
        gate["lambda"] = lambda_radians
        self.setup_new_gate(gate, control, target)
        return self

    def gate_ctrl_t(self, control, control_state, target):
        """Apply a controlled "t" gate, to these two qbits. Controlled gates act
        on 2 qubits, where first acts as a control and the second acts as target.
        The control state is expressed in computational basis and most often has value
        1 corresponding to |1⟩ state."""
        assert control != target
        gate = {}
        gate["name"] = "ctrl-t"
        gate["target"] = target
        gate["control"] = control
        gate["controlstate"] = control_state
        self.setup_new_gate(gate, control, target)
        return self

    def gate_ctrl_t_dagger(self, control, control_state, target):
        """Apply a controlled "t-dagger" gate to these two qbits. Controlled gates act
        on 2 qubits, where first acts as a control and the second acts as target.
        The control state is expressed in computational basis and most often has value
        1 corresponding to |1⟩ state."""
        assert control != target
        gate = {}
        gate["name"] = "ctrl-t-dagger"
        gate["target"] = target
        gate["control"] = control
        gate["controlstate"] = control_state
        self.setup_new_gate(gate, control, target)
        return self

    def gate_ctrl_pauli_x(self, control, control_state, target):
        """Apply a controlled "pauli-x" gate on these two qbits. Controlled gates act
        on 2 qubits, where first acts as a control and the second acts as target.
        The control state is expressed in computational basis and most often has value
        1 corresponding to |1⟩ state."""
        assert control != target
        gate = {}
        gate["name"] = "ctrl-pauli-x"
        gate["target"] = target
        gate["control"] = control
        gate["controlstate"] = control_state
        self.setup_new_gate(gate, control, target)
        return self

    def gate_ctrl_pauli_y(self, control, control_state, target):
        """Apply a controlled "pauli-y" gate on these two qbits. Controlled gates act
        on 2 qubits, where first acts as a control and the second acts as target.
        The control state is expressed in computational basis and most often has value
        1 corresponding to |1⟩ state."""
        assert control != target
        gate = {}
        gate["name"] = "ctrl-pauli-y"
        gate["target"] = target
        gate["control"] = control
        gate["controlstate"] = control_state
        self.setup_new_gate(gate, control, target)
        return self

    def gate_ctrl_pauli_z(self, control, control_state, target):
        """Apply a controlled "pauli-z" gate on these two qbits. Controlled gates act
        on 2 qubits, where first acts as a control and the second acts as target.
        The control state is expressed in computational basis and most often has value
        1 corresponding to |1⟩ state."""
        assert control != target
        gate = {}
        gate["name"] = "ctrl-pauli-z"
        gate["target"] = target
        gate["control"] = control
        gate["controlstate"] = control_state
        self.setup_new_gate(gate, control, target)
        return self

    def gate_ctrl_pauli_x_root(self, control, control_state, target, t=None, k=None):
        """Apply a "ctrl-pauli-x-root" gate to this qubit, an operation which amounts to
        aplying a root of the pauli-x gate. The root value is specified either via a
        parameter named 't' which represents the exact root value or via a parameter
        named 'k' which specifies the root value as 2^k. Because non integer powers of
        a matrix are not unique, this gate is defined as a rotation around X-axis of
        the Bloch sphere with an angle given by π/t or π/2^k respectively."""
        assert t or k
        assert control != target
        gate = {}
        gate["name"] = "ctrl-pauli-x-root"
        if k:
            gate["root-k"] = k
        elif t:
            gate["root-t"] = t
        gate["target"] = target
        gate["control"] = control
        gate["controlstate"] = control_state
        self.setup_new_gate(gate, control, target)
        return self

    def gate_ctrl_pauli_y_root(self, control, control_state, target, t=None, k=None):
        """Apply a "ctrl-pauli-y-root" gate to this qubit, an operation which amounts to
        aplying a root of the pauli-y gate. The root value is specified either via a
        parameter named 't' which represents the exact root value or via a parameter
        named 'k' which specifies the root value as 2^k. Because non integer powers of
        a matrix are not unique, this gate is defined as a rotation around Y-axis of
        the Bloch sphere with an angle given by π/t or π/2^k respectively."""
        assert t or k
        assert control != target
        gate = {}
        gate["name"] = "ctrl-pauli-y-root"
        if k:
            gate["root-k"] = k
        elif t:
            gate["root-t"] = t
        gate["target"] = target
        gate["control"] = control
        gate["controlstate"] = control_state
        self.setup_new_gate(gate, control, target)
        return self

    def gate_ctrl_pauli_z_root(self, control, control_state, target, t=None, k=None):
        """Apply a "ctrl-pauli-z-root" gate to this qubit, an operation which amounts to
        aplying a root of the pauli-z gate. The root value is specified either via a
        parameter named 't' which represents the exact root value or via a parameter
        named 'k' which specifies the root value as 2^k. Because non integer powers of
        a matrix are not unique, this gate is defined as a rotation around Z-axis of
        the Bloch sphere with an angle given by π/t or π/2^k respectively."""
        assert t or k
        assert control != target
        gate = {}
        gate["name"] = "ctrl-pauli-z-root"
        if k:
            gate["root-k"] = k
        elif t:
            gate["root-t"] = t
        gate["target"] = target
        gate["control"] = control
        gate["controlstate"] = control_state
        self.setup_new_gate(gate, control, target)
        return self

    def gate_ctrl_pauli_x_root_dagger(
        self, control, control_state, target, t=None, k=None
    ):
        """Apply a "ctrl-pauli-x-root" gate to this qubit, an operation which amounts to
        aplying a root of the pauli-x gate. The root value is specified either via a
        parameter named 't' which represents the exact root value or via a parameter
        named 'k' which specifies the root value as 2^k. Because non integer powers of
        a matrix are not unique, this gate is defined as a rotation around X-axis of
        the Bloch sphere with an angle given by π/t or π/2^k respectively."""
        assert t or k
        assert control != target
        gate = {}
        gate["name"] = "ctrl-pauli-x-root-dagger"
        if k:
            gate["root-k"] = k
        elif t:
            gate["root-t"] = t
        gate["target"] = target
        gate["control"] = control
        gate["controlstate"] = control_state
        self.setup_new_gate(gate, control, target)
        return self

    def gate_ctrl_pauli_y_root_dagger(
        self, control, control_state, target, t=None, k=None
    ):
        """Apply a "ctrl-pauli-y-root" gate to this qubit, an operation which amounts to
        aplying a root of the pauli-y gate. The root value is specified either via a
        parameter named 't' which represents the exact root value or via a parameter
        named 'k' which specifies the root value as 2^k. Because non integer powers of
        a matrix are not unique, this gate is defined as a rotation around Y-axis of
        the Bloch sphere with an angle given by π/t or π/2^k respectively."""
        assert t or k
        assert control != target
        gate = {}
        gate["name"] = "ctrl-pauli-y-root-dagger"
        if k:
            gate["root-k"] = k
        elif t:
            gate["root-t"] = t
        gate["target"] = target
        gate["control"] = control
        gate["controlstate"] = control_state
        self.setup_new_gate(gate, control, target)
        return self

    def gate_ctrl_pauli_z_root_dagger(
        self, control, control_state, target, t=None, k=None
    ):
        """Apply a "ctrl-pauli-z-root" gate to this qubit, an operation which amounts to
        aplying a root of the pauli-z gate. The root value is specified either via a
        parameter named 't' which represents the exact root value or via a parameter
        named 'k' which specifies the root value as 2^k. Because non integer powers of
        a matrix are not unique, this gate is defined as a rotation around Z-axis of
        the Bloch sphere with an angle given by π/t or π/2^k respectively."""
        assert t or k
        assert control != target
        gate = {}
        gate["name"] = "ctrl-pauli-z-root-dagger"
        if k:
            gate["root-k"] = k
        elif t:
            gate["root-t"] = t
        gate["target"] = target
        gate["control"] = control
        gate["controlstate"] = control_state
        self.setup_new_gate(gate, control, target)
        return self

    def gate_ctrl_rx_theta(self, control, control_state, target, theta):
        """Apply a controled 'rx-theta" gate to these two qbits, angle is specified
        in radians. Controlled gates act on 2 qubits, where first acts as a control
        and the second acts as target. The control state is expressed in computational
        basis and most often has value 1 corresponding to |1⟩ state."""
        assert control != target
        gate = {}
        gate["name"] = "ctrl-rx-theta"
        gate["target"] = target
        gate["control"] = control
        gate["controlstate"] = control_state
        gate["theta"] = theta
        self.setup_new_gate(gate, control, target)
        return self

    def gate_ctrl_ry_theta(self, control, control_state, target, theta):
        """Apply a controled 'ry-theta" gate to these two qbits, angle is specified
        in radians. Controlled gates act on 2 qubits, where first acts as a control
        and the second acts as target. The control state is expressed in computational
        basis and most often has value 1 corresponding to |1⟩ state."""
        assert control != target
        gate = {}
        gate["name"] = "ctrl-ry-theta"
        gate["target"] = target
        gate["control"] = control
        gate["controlstate"] = control_state
        gate["theta"] = theta
        self.setup_new_gate(gate, control, target)
        return self

    def gate_ctrl_rz_theta(self, control, control_state, target, theta):
        """Apply a controlled "rz-theta" gate to these two qbits, angle is specified
        in radians. Controlled gates act on 2 qubits, where first acts as a control
        and the second acts as target. The control state is expressed in computational
        basis and most often has value 1 corresponding to |1⟩ state."""
        assert control != target
        gate = {}
        gate["name"] = "ctrl-rz-theta"
        gate["target"] = target
        gate["control"] = control
        gate["controlstate"] = control_state
        gate["theta"] = theta
        self.setup_new_gate(gate, control, target)
        return self

    def gate_ctrl_s(self, control, control_state, target):
        """Apply a controlled "s" gate to these two qbits. Controlled gates act
        on 2 qubits, where first acts as a control and the second acts as target.
        The control state is expressed in computational basis and most often has
        value 1 corresponding to |1⟩ state."""
        assert control != target
        gate = {}
        gate["name"] = "ctrl-s"
        gate["target"] = target
        gate["control"] = control
        gate["controlstate"] = control_state
        self.setup_new_gate(gate, control, target)
        return self

    def gate_ctrl_s_dagger(self, control, control_state, target):
        """Apply a controlled "s-dagger" gate to these two qbits. Controlled gates act
        on 2 qubits, where first acts as a control and the second acts as target.
        The control state is expressed in computational basis and most often has value 1
        corresponding to |1⟩ state."""
        assert control != target
        gate = {}
        gate["name"] = "ctrl-s-dagger"
        gate["target"] = target
        gate["control"] = control
        gate["controlstate"] = control_state
        self.setup_new_gate(gate, control, target)
        return self

    def gate_toffoli(self, control, control_state, control2, control_state2, target):
        """Apply a Toffoli gate to these three qbits. Toffoli gate acts on 3
        qubits, where first two acts as a control. The control states are expressed
        in computational basis and most often has value 1 corresponding to |1⟩ state.
        This gate is also known as CCNOT gate."""
        assert control != control2
        assert control != target
        assert control2 != target
        gate = {}
        gate["name"] = "toffoli"
        gate["target"] = target
        gate["control"] = control
        gate["controlstate"] = control_state
        gate["control2"] = control2
        gate["controlstate2"] = control_state2
        self.setup_new_gate(gate, control, control2, target)
        return self

    def gate_fredkin(self, control, control_state, target, target2):
        """Apply a Fredkin (CSWAP) gate to these three qbits. This gate acts on three
        qubits and performs a controlled swap when the control qubit is |1⟩
        otherwise leaves it unchanged. The control state is expressed in computational
        basis and most often has value 1 corresponding to |1⟩ state."""
        assert target != target2
        assert control != target
        assert control != target2
        gate = {}
        gate["name"] = "fredkin"
        gate["target"] = target
        gate["target2"] = target2
        gate["control"] = control
        gate["controlstate"] = control_state
        self.setup_new_gate(gate, control, target, target2)
        return self

    def gate_measure_x(self, target, classic_bit):
        """Measure target bit along the direction given by x axis
        of the Bloch sphere."""
        gate = {}
        gate["name"] = "measure-x"
        gate["target"] = target
        gate["bit"] = classic_bit
        self.setup_new_gate(gate, target)
        return self

    def gate_measure_y(self, target, classic_bit):
        """Measure target bit along the direction given by y axis
        of the Bloch sphere."""
        gate = {}
        gate["name"] = "measure-y"
        gate["target"] = target
        gate["bit"] = classic_bit
        self.setup_new_gate(gate, target)
        return self

    def gate_measure_z(self, target, classic_bit):
        """Measure target along the direction given by z axis
        of the Bloch sphere."""
        gate = {}
        gate["name"] = "measure-z"
        gate["target"] = target
        gate["bit"] = classic_bit
        self.setup_new_gate(gate, target)
        return self
