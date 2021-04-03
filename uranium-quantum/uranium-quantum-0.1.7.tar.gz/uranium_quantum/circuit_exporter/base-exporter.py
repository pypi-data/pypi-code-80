class ExportException(BaseException):
    pass


class BaseExporter:

    """Base class for exporting circuits from YAML format.
    to Qiskit, OpenQasm, Pyquil, Quil and Cirq."""

    def __init__(self):
        self._qubits = None

    def set_number_qubits(self, qubits):
        """Set the number of qubits in this circuit."""
        self._qubits = qubits

    def set_number_bits(self, bits):
        """Set the number of classical bits in this circuit."""
        self._bits = bits

    def process_step(self, step, add_comments=True):
        """Export gates present in one step from the input YAML file."""
        output = ""
        if "gates" in step:
            for gate in step["gates"]:

                controlstate, controlstate2, root, theta_radians, phi_radians, lambda_radians, bit = (
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None
                )
                if "controlstate" in gate:
                    controlstate = gate["controlstate"]
                if "controlstate2" in gate:
                    controlstate2 = gate["controlstate2"]
                if "root" in gate:
                    root = gate["root"]
                if "theta" in gate:
                    theta_radians = gate["theta"]
                if "phi" in gate:
                    phi_radians = gate["phi"]
                if "lambda" in gate:
                    lambda_radians = gate["lambda"]
                if "bit" in gate:
                    bit = gate["bit"]

                qubits = []
                if "control" in gate:
                    qubits.append(gate["control"])
                if "control2" in gate:
                    qubits.append(gate["control2"])
                qubits.append(gate["target"])
                if "target2" in gate:
                    qubits.append(gate["target2"])

                name = gate["name"]
                output += self.process_gate(
                    name,
                    controlstate,
                    controlstate2,
                    root,
                    theta_radians,
                    phi_radians,
                    lambda_radians,
                    bit,
                    *qubits,
                    add_comments=add_comments,
                )
        return output + "\n"

    def process_gate(
        self,
        name,
        controlstate,
        controlstate2,
        root,
        theta_radians,
        phi_radians,
        lambda_radians,
        bit,
        *qubits,
        add_comments=True,
    ):
        """Create export code corresponding to a gate in yaml circuit."""
        if name == "u3":
            return self._gate_u3(
                qubits[0],
                theta_radians,
                phi_radians,
                lambda_radians,
                add_comments=add_comments,
            )
        elif name == "u2":
            return self._gate_u2(
                qubits[0], phi_radians, lambda_radians, add_comments=add_comments
            )
        elif name == "u1":
            return self._gate_u1(qubits[0], lambda_radians, add_comments=add_comments)
        elif name == "identity":
            return self._gate_identity(qubits[0], add_comments=add_comments)
        elif name == "hadamard":
            return self._gate_hadamard(qubits[0], add_comments=add_comments)
        elif name == "pauli-x":
            return self._gate_pauli_x(qubits[0], add_comments=add_comments)
        elif name == "pauli-y":
            return self._gate_pauli_y(qubits[0], add_comments=add_comments)
        elif name == "pauli-z":
            return self._gate_pauli_z(qubits[0], add_comments=add_comments)
        elif name == "pauli-x-root":
            return self._gate_pauli_x_root(qubits[0], root, add_comments=add_comments)
        elif name == "pauli-y-root":
            return self._gate_pauli_y_root(qubits[0], root, add_comments=add_comments)
        elif name == "pauli-z-root":
            return self._gate_pauli_z_root(qubits[0], root, add_comments=add_comments)
        elif name == "pauli-x-root-dagger":
            return self._gate_pauli_x_root_dagger(
                qubits[0], root, add_comments=add_comments
            )
        elif name == "pauli-y-root-dagger":
            return self._gate_pauli_y_root_dagger(
                qubits[0], root, add_comments=add_comments
            )
        elif name == "pauli-z-root-dagger":
            return self._gate_pauli_z_root_dagger(
                qubits[0], root, add_comments=add_comments
            )
        elif name == "sqrt-not":
            return self._gate_sqrt_not(qubits[0], add_comments=add_comments)
        elif name == "t":
            return self._gate_t(qubits[0], add_comments=add_comments)
        elif name == "t-dagger":
            return self._gate_t_dagger(qubits[0], add_comments=add_comments)
        elif name == "s":
            return self._gate_s(qubits[0], add_comments=add_comments)
        elif name == "s-dagger":
            return self._gate_s_dagger(qubits[0], add_comments=add_comments)
        elif name == "rx-theta":
            return self._gate_rx_theta(
                qubits[0], theta_radians, add_comments=add_comments
            )
        elif name == "ry-theta":
            return self._gate_ry_theta(
                qubits[0], theta_radians, add_comments=add_comments
            )
        elif name == "rz-theta":
            return self._gate_rz_theta(
                qubits[0], theta_radians, add_comments=add_comments
            )
        elif name == "ctrl-u3":
            return self._gate_ctrl_u3(
                qubits[0],
                qubits[1],
                controlstate,
                theta_radians,
                phi_radians,
                lambda_radians,
                add_comments=add_comments,
            )
        elif name == "ctrl-u2":
            return self._gate_ctrl_u2(
                qubits[0],
                qubits[1],
                controlstate,
                phi_radians,
                lambda_radians,
                add_comments=add_comments,
            )
        elif name == "ctrl-u1":
            return self._gate_ctrl_u1(
                qubits[0],
                qubits[1],
                controlstate,
                lambda_radians,
                add_comments=add_comments,
            )
        elif name == "ctrl-hadamard":
            return self._gate_ctrl_hadamard(
                qubits[0], qubits[1], controlstate, add_comments=add_comments
            )
        elif name == "ctrl-pauli-x":
            return self._gate_ctrl_pauli_x(
                qubits[0], qubits[1], controlstate, add_comments=add_comments
            )
        elif name == "ctrl-pauli-y":
            return self._gate_ctrl_pauli_y(
                qubits[0], qubits[1], controlstate, add_comments=add_comments
            )
        elif name == "ctrl-pauli-z":
            return self._gate_ctrl_pauli_z(
                qubits[0], qubits[1], controlstate, add_comments=add_comments
            )
        elif name == "ctrl-pauli-x-root":
            return self._gate_ctrl_pauli_x_root(
                qubits[0], qubits[1], controlstate, root, add_comments=add_comments
            )
        elif name == "ctrl-pauli-y-root":
            return self._gate_ctrl_pauli_y_root(
                qubits[0], qubits[1], controlstate, root, add_comments=add_comments
            )
        elif name == "ctrl-pauli-z-root":
            return self._gate_ctrl_pauli_z_root(
                qubits[0], qubits[1], controlstate, root, add_comments=add_comments
            )
        elif name == "ctrl-pauli-x-root-dagger":
            return self._gate_ctrl_pauli_x_root_dagger(
                qubits[0], qubits[1], controlstate, root, add_comments=add_comments
            )
        elif name == "ctrl-pauli-y-root-dagger":
            return self._gate_ctrl_pauli_y_root_dagger(
                qubits[0], qubits[1], controlstate, root, add_comments=add_comments
            )
        elif name == "ctrl-pauli-z-root-dagger":
            return self._gate_ctrl_pauli_z_root_dagger(
                qubits[0], qubits[1], controlstate, root, add_comments=add_comments
            )
        elif name == "ctrl-sqrt-not":
            return self._gate_ctrl_sqrt_not(
                qubits[0], qubits[1], controlstate, add_comments=add_comments
            )
        elif name == "ctrl-t":
            return self._gate_ctrl_t(
                qubits[0], qubits[1], controlstate, add_comments=add_comments
            )
        elif name == "ctrl-t-dagger":
            return self._gate_ctrl_t_dagger(
                qubits[0], qubits[1], controlstate, add_comments=add_comments
            )
        elif name == "ctrl-s":
            return self._gate_ctrl_s(
                qubits[0], qubits[1], controlstate, add_comments=add_comments
            )
        elif name == "ctrl-s-dagger":
            return self._gate_ctrl_s_dagger(
                qubits[0], qubits[1], controlstate, add_comments=add_comments
            )
        elif name == "ctrl-rx-theta":
            return self._gate_ctrl_rx_theta(
                qubits[0],
                qubits[1],
                controlstate,
                theta_radians,
                add_comments=add_comments,
            )
        elif name == "ctrl-ry-theta":
            return self._gate_ctrl_ry_theta(
                qubits[0],
                qubits[1],
                controlstate,
                theta_radians,
                add_comments=add_comments,
            )
        elif name == "ctrl-rz-theta":
            return self._gate_ctrl_rz_theta(
                qubits[0],
                qubits[1],
                controlstate,
                theta_radians,
                add_comments=add_comments,
            )
        elif name == "swap":
            return self._gate_swap(qubits[0], qubits[1], add_comments=add_comments)
        elif name == "iswap":
            return self._gate_iswap(qubits[0], qubits[1], add_comments=add_comments)
        elif name == "sqrt-swap":
            return self._gate_sqrt_swap(qubits[0], qubits[1], add_comments=add_comments)
        elif name == "swap-phi":
            return self._gate_swap_phi(
                qubits[0], qubits[1], phi_radians, add_comments=add_comments
            )
        elif name == "xx":
            return self._gate_xx(
                qubits[0], qubits[1], theta_radians, add_comments=add_comments
            )
        elif name == "yy":
            return self._gate_yy(
                qubits[0], qubits[1], theta_radians, add_comments=add_comments
            )
        elif name == "zz":
            return self._gate_zz(
                qubits[0], qubits[1], theta_radians, add_comments=add_comments
            )
        elif name == "toffoli":
            return self._gate_toffoli(
                qubits[0], qubits[1], qubits[2], controlstate, controlstate2, add_comments=add_comments
            )
        elif name == "fredkin":
            return self._gate_fredkin(
                qubits[0], qubits[1], qubits[2], controlstate, add_comments=add_comments
            )
        elif name == "measure-x":
            return self._gate_measure_x(qubits[0], bit, add_comments=add_comments)
        elif name == "measure-y":
            return self._gate_measure_y(qubits[0], bit, add_comments=add_comments)
        elif name == "measure-z":
            return self._gate_measure_z(qubits[0], bit, add_comments=add_comments)
        raise ExportException(f"The gate {name} is not implemented in exporter code.")

    @staticmethod
    def _gate_u3(
        target, theta_radians, phi_radians, lambda_radians, add_comments=True
    ):
        return ""

    @staticmethod
    def _gate_u2(target, phi_radians, lambda_radians, add_comments=True):
        return ""

    @staticmethod
    def _gate_u1(target, lambda_radians, add_comments=True):
        return ""

    @staticmethod
    def _gate_identity(target, add_comments=True):
        return ""

    @staticmethod
    def _gate_hadamard(target, add_comments=True):
        return ""

    @staticmethod
    def _gate_pauli_x(target, add_comments=True):
        return ""

    @staticmethod
    def _gate_pauli_y(target, add_comments=True):
        return ""

    @staticmethod
    def _gate_pauli_z(target, add_comments=True):
        return ""

    @staticmethod
    def _gate_pauli_x_root(target, add_comments=True):
        return ""

    @staticmethod
    def _gate_pauli_y_root(target, add_comments=True):
        return ""

    @staticmethod
    def _gate_pauli_z_root(target, add_comments=True):
        return ""

    @staticmethod
    def _gate_pauli_x_root_dagger(target, add_comments=True):
        return ""

    @staticmethod
    def _gate_pauli_y_root_dagger(target, add_comments=True):
        return ""

    @staticmethod
    def _gate_pauli_z_root_dagger(target, add_comments=True):
        return ""

    @staticmethod
    def _gate_sqrt_not(target, add_comments=True):
        return ""

    @staticmethod
    def _gate_t(target, add_comments=True):
        return ""

    @staticmethod
    def _gate_t_dagger(target, add_comments=True):
        return ""

    @staticmethod
    def _gate_rx_theta(target, theta, add_comments=True):
        return ""

    @staticmethod
    def _gate_ry_theta(target, theta, add_comments=True):
        return ""

    @staticmethod
    def _gate_rz_theta(target, theta, add_comments=True):
        return ""

    @staticmethod
    def _gate_s(target, add_comments=True):
        return ""

    @staticmethod
    def _gate_s_dagger(target, add_comments=True):
        return ""

    @staticmethod
    def _gate_swap(target, target2, add_comments=True):
        return ""

    @staticmethod
    def _gate_iswap(target, target2, add_comments=True):
        return ""

    @staticmethod
    def _gate_swap_phi(target, target2, phi, add_comments=True):
        return ""

    @staticmethod
    def _gate_sqrt_swap(target, target2, add_comments=True):
        return ""

    @staticmethod
    def _gate_xx(target, target2, theta, add_comments=True):
        return ""

    @staticmethod
    def _gate_yy(target, target2, theta, add_comments=True):
        return ""

    @staticmethod
    def _gate_zz(target, target2, theta, add_comments=True):
        return ""

    @staticmethod
    def _gate_ctrl_hadamard(control, target, controlstate, add_comments=True):
        return ""

    @staticmethod
    def _gate_ctrl_u3(
        control,
        target,
        controlstate,
        theta_radians,
        phi_radians,
        lambda_radians,
        add_comments=True,
    ):
        return ""

    @staticmethod
    def _gate_ctrl_u2(
        control, target, controlstate, phi_radians, lambda_radians, add_comments=True
    ):
        return ""

    @staticmethod
    def _gate_ctrl_u1(
        control, target, controlstate, lambda_radians, add_comments=True
    ):
        return ""

    @staticmethod
    def _gate_ctrl_t(control, target, controlstate, add_comments=True):
        return ""

    @staticmethod
    def _gate_ctrl_t_dagger(control, target, controlstate, add_comments=True):
        return ""

    @staticmethod
    def _gate_ctrl_pauli_x(control, target, controlstate, add_comments=True):
        return ""

    @staticmethod
    def _gate_ctrl_pauli_y(control, target, controlstate, add_comments=True):
        return ""

    @staticmethod
    def _gate_ctrl_pauli_z(control, target, controlstate, add_comments=True):
        return ""

    @staticmethod
    def _gate_ctrl_sqrt_not(control, target, controlstate, add_comments=True):
        return ""

    @staticmethod
    def _gate_ctrl_rx_theta(control, target, controlstate, theta, add_comments=True):
        return ""

    @staticmethod
    def _gate_ctrl_ry_theta(control, target, controlstate, theta, add_comments=True):
        return ""

    @staticmethod
    def _gate_ctrl_rz_theta(control, target, controlstate, theta, add_comments=True):
        return ""

    @staticmethod
    def _gate_ctrl_s(control, target, controlstate, add_comments=True):
        return ""

    @staticmethod
    def _gate_ctrl_s_dagger(control, target, controlstate, add_comments=True):
        return ""

    @staticmethod
    def _gate_toffoli(control, control2, target, add_comments=True):
        return ""

    @staticmethod
    def _gate_fredkin(control, control2, controlstate, target, add_comments=True):
        return ""

    @staticmethod
    def _gate_measure_x(target, classic_bit, add_comments=True):
        return ""

    @staticmethod
    def _gate_measure_y(target, classic_bit, add_comments=True):
        return ""

    @staticmethod
    def _gate_measure_z(arget, classic_bit, add_comments=True):
        return ""
