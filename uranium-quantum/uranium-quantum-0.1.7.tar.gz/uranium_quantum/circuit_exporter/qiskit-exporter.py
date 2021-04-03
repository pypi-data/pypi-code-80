import importlib
import math

BaseExporter = importlib.import_module("uranium_quantum.circuit_exporter.base-exporter")


class Exporter(BaseExporter.BaseExporter):
    def start_code(self):
        return f"\
import numpy as np\n\
from qiskit import QuantumRegister\n\
from qiskit.circuit import ClassicalRegister\n\
from qiskit import QuantumCircuit, execute, Aer\n\
from qiskit.circuit.library.standard_gates import iswap\n\
from qiskit.circuit.library import RXXGate, RYYGate, RZZGate\n\
from qiskit.quantum_info.operators import Operator\n\
from qiskit.visualization import plot_histogram\n\
cr = ClassicalRegister({self._bits})\n\
qr = QuantumRegister({self._qubits})\n\
qc = QuantumCircuit(qr, cr)\n\n"

    def end_code(self):
        return f"\
# Using Aer's qasm_simulator\n\
simulator = Aer.get_backend('qasm_simulator')\n\n\
# Execute the circuit on the qasm simulator\n\
job = execute(qc, backend=simulator, shots=1000)\n\n\
# Grab results from the job\n\
result = job.result()\n\n\
print('Job result status', result.status)\n\
counts = result.get_counts(qc)\n\n\
# Note: you need to include some measure gates in your circuit in order to see some plots here:\n\
plot_histogram(counts)\n"

    @staticmethod
    def _gate_u3(
        target, theta_radians, phi_radians, lambda_radians, add_comments=True
    ):
        out = "# u3 gate\n" if add_comments else ""
        out += f"qc.u({theta_radians}, {phi_radians}, {lambda_radians}, qr[{target}])\n\n"
        return out

    @staticmethod
    def _gate_u2(target, phi_radians, lambda_radians, add_comments=True):
        out = "# u2 gate\n" if add_comments else ""
        out += f"qc.u({math.pi/2}, {phi_radians}, {lambda_radians}, qr[{target}])\n\n"
        return out

    @staticmethod
    def _gate_u1(target, lambda_radians, add_comments=True):
        out = "# u1 gate\n" if add_comments else ""
        out += f"qc.p({lambda_radians}, qr[{target}])\n\n"
        return out

    @staticmethod
    def _gate_identity(target, add_comments=True):
        out = "# identity gate\n" if add_comments else ""
        out += f"qc.id(qr[{target}])\n\n"
        return out

    @staticmethod
    def _gate_hadamard(target, add_comments=True):
        out = "# hadamard gate\n" if add_comments else ""
        out += f"qc.h(qr[{target}])\n\n"
        return out

    @staticmethod
    def _gate_pauli_x(target, add_comments=True):
        out = "# pauli-x gate\n" if add_comments else ""
        out += f"qc.x(qr[{target}])\n\n"
        return out

    @staticmethod
    def _gate_pauli_y(target, add_comments=True):
        out = "# pauli-y gate\n" if add_comments else ""
        out += f"qc.y(qr[{target}])\n\n"
        return out

    @staticmethod
    def _gate_pauli_z(target, add_comments=True):
        out = "# pauli-z gate\n" if add_comments else ""
        out += f"qc.z(qr[{target}])\n\n"
        return out

    @staticmethod
    def _gate_pauli_x_root(target, root, add_comments=True):
        root = f"(2**{root[4:]})" if '^' in root else root[2:]
        out = "# pauli-x-root gate\n" if add_comments else ""
        out += f"pauli_x_root = np.exp(1j * np.pi/(2*{root})) * Operator([\n\
    [np.cos(np.pi/(2*{root})), -1j * np.sin(np.pi/(2*{root}))],\n\
    [-1j * np.sin(np.pi/(2*{root})), np.cos(np.pi/(2*{root}))],\n\
    ])\n\n"
        out += f"qc.unitary(pauli_x_root, [{target}], label='pauli-x-root')\n\n"
        return out

    @staticmethod
    def _gate_pauli_y_root(target, root, add_comments=True):
        root = f"(2**{root[4:]})" if '^' in root else root[2:]
        out = "# pauli-y-root gate\n" if add_comments else ""
        out += f"pauli_y_root = np.exp(1j * np.pi/(2*{root})) * Operator([\n\
    [np.cos(np.pi/(2*{root})), -np.sin(np.pi/(2*{root}))],\n\
    [np.sin(np.pi/(2*{root})), np.cos(np.pi/(2*{root}))],\n\
    ])\n\n"
        out += f"qc.unitary(pauli_y_root, [{target}], label='pauli-y-root')\n\n"
        return out

    @staticmethod
    def _gate_pauli_z_root(target, root, add_comments=True):
        root = f"(2**{root[4:]})" if '^' in root else root[2:]
        out = "# pauli-z-root gate\n" if add_comments else ""
        out += f"pauli_z_root = np.exp(1j * np.pi/{root}) * Operator([\n\
    [1, 0],\n\
    [0, np.exp(1j * np.pi/{root})],\n\
    ])\n\n"
        out += f"qc.unitary(pauli_z_root, [{target}], label='pauli-z-root')\n\n"
        return out

    @staticmethod
    def _gate_pauli_x_root_dagger(target, root, add_comments=True):
        root = f"(2**{root[4:]})" if '^' in root else root[2:]
        out = "# pauli-x-root-dagger gate\n" if add_comments else ""
        out += f"pauli_x_root_dagger = np.exp(-1j * np.pi/(2*{root})) * Operator([\n\
    [np.cos(np.pi/(2*{root})), 1j * np.sin(np.pi/(2*{root}))],\n\
    [1j * np.sin(np.pi/(2*{root})), np.cos(np.pi/(2*{root}))],\n\
    ])\n\n"
        out += f"qc.unitary(pauli_x_root_dagger, [{target}], label='pauli-x-root-dagger')\n\n"
        return out

    @staticmethod
    def _gate_pauli_y_root_dagger(target, root, add_comments=True):
        root = f"(2**{root[4:]})" if '^' in root else root[2:]
        out = "# pauli-y-root-dagger gate\n" if add_comments else ""
        out += f"pauli_y_root_dagger = np.exp(-1j * np.pi/(2*{root})) * Operator([\n\
    [np.cos(np.pi/(2*{root})), - np.sin(np.pi/(2*{root}))],\n\
    [np.sin(np.pi/(2*{root})), np.cos(np.pi/(2*{root}))],\n\
    ])\n\n"
        out += f"qc.unitary(pauli_y_root_dagger, [{target}], label='pauli-y-root-dagger')\n\n"
        return out

    @staticmethod
    def _gate_pauli_z_root_dagger(target, root, add_comments=True):
        root = f"(2**{root[4:]})" if '^' in root else root[2:]
        out = "# pauli_z-root-dagger gate\n" if add_comments else ""
        out += f"pauli_z_root_dagger = Operator([\n\
    [1, 0],\n\
    [0, np.exp(-1j * np.pi/{root})],\n\
    ])\n\n"
        out += f"qc.unitary(pauli_z_root_dagger, [{target}], label='pauli-z-root-dagger')\n\n"
        return out

    @staticmethod
    def _gate_sqrt_not(target, add_comments=True):
        out = "# sqrt-not gate\n" if add_comments else ""
        out += f"qc.sx(qr[{target}])\n\n"
        return out

    @staticmethod
    def _gate_t(target, add_comments=True):
        out = "# t gate\n" if add_comments else ""
        out += f"qc.t(qr[{target}])\n\n"
        return out

    @staticmethod
    def _gate_t_dagger(target, add_comments=True):
        out = "# t-dagger gate\n" if add_comments else ""
        out += f"qc.tdg(qr[{target}])\n\n"
        return out

    @staticmethod
    def _gate_rx_theta(target, theta, add_comments=True):
        out = "# rx-theta gate\n" if add_comments else ""
        out += f"qc.rx({theta}, qr[{target}])\n\n"
        return out

    @staticmethod
    def _gate_ry_theta(target, theta, add_comments=True):
        out = "# ry-theta gate\n" if add_comments else ""
        out += f"qc.ry({theta}, qr[{target}])\n\n"
        return out

    @staticmethod
    def _gate_rz_theta(target, theta, add_comments=True):
        out = "# rz-theta gate\n" if add_comments else ""
        out += f"qc.rz({theta}, qr[{target}])\n\n"
        return out

    @staticmethod
    def _gate_s(target, add_comments=True):
        out = "# s gate\n" if add_comments else ""
        out += f"qc.s(qr[{target}])\n\n"
        return out

    @staticmethod
    def _gate_s_dagger(target, add_comments=True):
        out = "# s-dagger gate\n" if add_comments else ""
        out += f"qc.sdg(qr[{target}])\n\n"
        return out

    @staticmethod
    def _gate_swap(target, target2, add_comments=True):
        out = "# swap gate\n" if add_comments else ""
        out += f"qc.swap(qr[{target}], qr[{target2}])\n\n"
        return out

    @staticmethod
    def _gate_iswap(target, target2, add_comments=True):
        out = "# iswap gate\n" if add_comments else ""
        out += f"qc.iswap(qr[{target}], qr[{target2}])\n\n"
        return out

    @staticmethod
    def _gate_swap_phi(target, target2, phi, add_comments=True):
        out = "# swap-phi gate\n" if add_comments else ""
        out += f"swap_phi = Operator([\n\
    [1, 0, 0, 0],\n\
    [0, 0,  np.exp(1j * {phi}), 0],\n\
    [0, np.exp(1j * {phi}), 0, 0],\n\
    [0, 0, 0, 1],\n\
    ])\n"
        out += f"qc.unitary(swap_phi, [{target}, {target2}], label='swap-phi')\n\n"
        return out

    @staticmethod
    def _gate_sqrt_swap(target, target2, add_comments=True):
        out = "# sqrt-swap gate\n" if add_comments else ""
        out += f"qc.u({math.pi/2}, {math.pi/2}, {-math.pi}, qr[{target}])\n"
        out += f"qc.u({math.pi/2}, {-math.pi/2}, {math.pi}, qr[{target2}])\n"
        out += f"qc.cx(qr[{target}], qr[{target2}])\n"
        out += f"qc.u({math.pi/4}, {-math.pi/2}, {-math.pi/2}, qr[{target}])\n"
        out += f"qc.u({math.pi/2}, 0, {1.75 * math.pi}, qr[{target2}])\n"
        out += f"qc.cx(qr[{target}], qr[{target2}])\n"
        out += f"qc.u({math.pi/4}, {-math.pi}, {-math.pi/2}, qr[{target}])\n"
        out += f"qc.u({math.pi/2}, {math.pi}, {math.pi/2}, qr[{target2}])\n"
        out += f"qc.cx(qr[{target}], qr[{target2}])\n"
        out += f"qc.u({math.pi/2}, 0, {-1.5 * math.pi}, qr[{target}])\n"
        out += f"qc.u({math.pi/2}, {math.pi/2}, 0, qr[{target2}])\n\n"
        return out

    @staticmethod
    def _gate_xx(target, target2, theta, add_comments=True):
        out = "# xx gate\n" if add_comments else ""
        out += f"qc.append(RXXGate({theta}), [{target}, {target2}])\n\n"
        return out

    @staticmethod
    def _gate_yy(target, target2, theta, add_comments=True):
        out = "# yy gate\n" if add_comments else ""
        out += f"qc.append(RYYGate({theta}), [{target}, {target2}])\n\n"
        return out

    @staticmethod
    def _gate_zz(target, target2, theta, add_comments=True):
        out = "# zz gate\n" if add_comments else ""
        out += f"qc.append(RZZGate({theta}), [{target}, {target2}])\n\n"
        return out

    @staticmethod
    def _gate_ctrl_hadamard(control, target, controlstate, add_comments=True):
        out = "# ctrl-hadamard gate\n" if add_comments else ""
        out += f"qc.ch(qr[{control}], qr[{target}], ctrl_state={controlstate})\n\n"
        return out

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
        out = "# ctrl-u3 gate\n" if add_comments else ""
        out += f"qc.cu({theta_radians}, {phi_radians}, {lambda_radians}, {math.pi/2}, qr[{control}], qr[{target}], ctrl_state={controlstate})\n\n"
        return out

    @staticmethod
    def _gate_ctrl_u2(
        control, target, controlstate, phi_radians, lambda_radians, add_comments=True
    ):
        out = "# ctrl-u2 gate\n" if add_comments else ""
        out += f"qc.cu({math.pi/2}, {phi_radians}, {lambda_radians}, {math.pi/2}, qr[{control}], qr[{target}], ctrl_state={controlstate})\n\n"
        return out

    @staticmethod
    def _gate_ctrl_u1(
        control, target, controlstate, lambda_radians, add_comments=True
    ):
        out = "# ctrl-u1 gate\n" if add_comments else ""
        out += f"qc.cp({lambda_radians}, qr[{control}], qr[{target}], ctrl_state={controlstate})\n\n"
        return out

    @staticmethod
    def _gate_ctrl_t(control, target, controlstate, add_comments=True):
        out = "# ctrl-t gate\n" if add_comments else ""
        out += f"qc.cp({math.pi/4}, qr[{control}], qr[{target}], ctrl_state={controlstate})\n\n"
        return out

    @staticmethod
    def _gate_ctrl_t_dagger(control, target, controlstate, add_comments=True):
        out = "# ctrl-t-dagger gate\n" if add_comments else ""
        out += f"qc.cp({-math.pi/4}, qr[{control}], qr[{target}], ctrl_state={controlstate})\n\n"
        return out

    @staticmethod
    def _gate_ctrl_pauli_x(control, target, controlstate, add_comments=True):
        out = "# ctrl-pauli-x gate\n" if add_comments else ""
        out += f"qc.cx(qr[{control}], qr[{target}], ctrl_state={controlstate})\n\n"
        return out

    @staticmethod
    def _gate_ctrl_pauli_y(control, target, controlstate, add_comments=True):
        out = "# ctrl-pauli-y gate\n" if add_comments else ""
        out += f"qc.cy(qr[{control}], qr[{target}], ctrl_state={controlstate})\n\n"
        return out

    @staticmethod
    def _gate_ctrl_pauli_z(control, target, controlstate, add_comments=True):
        out = "# ctrl-pauli-z gate\n" if add_comments else ""
        out += f"qc.cz(qr[{control}], qr[{target}], ctrl_state={controlstate})\n\n"
        return out

    @staticmethod
    def _gate_ctrl_pauli_x_root(
        control, target, controlstate, root, add_comments=True
    ):
        root = f"(2**{root[4:]})" if '^' in root else root[2:]
        out = "# ctrl-pauli-x-root gate\n" if add_comments else ""
        if int(controlstate) == 1:
            out += f"ctrl_pauli_x_root = Operator([\n\
    [1, 0, 0, 0],\n\
    [0, np.exp(1j * np.pi/(2*{root})) * np.cos(np.pi/(2*{root})), 0, -1j * np.exp(1j * np.pi/(2*{root})) * np.sin(np.pi/(2*{root}))],\n\
    [0, 0, 1, 0],\n\
    [0, -1j * np.exp(1j * np.pi/(2*{root})) * np.sin(np.pi/(2*{root})), 0, np.exp(1j * np.pi/(2*{root})) * np.cos(np.pi/(2*{root}))],\n\
    ])\n"
        else:
            out += f"ctrl_pauli_x_root = Operator([\n\
    [np.exp(1j * np.pi/(2*{root})) * np.cos(np.pi/(2*{root})), 0, -1j * np.exp(1j * np.pi/(2*{root})) * np.sin(np.pi/(2*{root})), 0],\n\
    [0, 1, 0, 0],\n\
    [-1j * np.exp(1j * np.pi/(2*{root})) * np.sin(np.pi/(2*{root})), 0, np.exp(1j * np.pi/(2*{root})) * np.cos(np.pi/(2*{root})), 0],\n\
    [0, 0, 0, 1],\n\
    ])\n"
        out += f"qc.unitary(ctrl_pauli_x_root, [{control}, {target}], label='ctrl-pauli-x-root')\n\n"
        return out

    @staticmethod
    def _gate_ctrl_pauli_y_root(
        control, target, controlstate, root, add_comments=True
    ):
        root = f"(2**{root[4:]})" if '^' in root else root[2:]
        out = "# ctrl-pauli-y-root gate\n" if add_comments else ""
        if int(controlstate) == 1:
            out += f"ctrl_pauli_y_root = Operator([\n\
    [1, 0, 0, 0],\n\
    [0, np.exp(1j * np.pi/(2*{root})) * np.cos(np.pi/(2*{root})), 0, - np.exp(1j * np.pi/(2*{root})) * np.sin(np.pi/(2*{root}))],\n\
    [0, 0, 1, 0],\n\
    [0, np.exp(1j * np.pi/(2*{root})) * np.sin(np.pi/(2*{root})), 0, np.exp(1j * np.pi/(2*{root})) * np.cos(np.pi/(2*{root}))],\n\
    ])\n"
        else:
            out += f"ctrl_pauli_y_root = Operator([\n\
    [np.exp(1j * np.pi/(2*{root})) * np.cos(np.pi/(2*{root})), 0, - np.exp(1j * np.pi/(2*{root})) * np.sin(np.pi/(2*{root})), 0],\n\
    [0, 1, 0, 0],\n\
    [np.exp(1j * np.pi/(2*{root})) * np.sin(np.pi/(2*{root})), 0, np.exp(1j * np.pi/(2*{root})) * np.cos(np.pi/(2*{root})), 0],\n\
    [0, 0, 0, 1],\n\
    ])\n"
        out += f"qc.unitary(ctrl_pauli_y_root, [{control}, {target}], label='ctrl-pauli-y-root')\n\n"
        return out

    @staticmethod
    def _gate_ctrl_pauli_z_root(
        control, target, controlstate, root, add_comments=True
    ):
        root = f"(2**{root[4:]})" if '^' in root else root[2:]
        out = "# ctrl-pauli-z-root gate\n" if add_comments else ""
        if int(controlstate) == 1:
            out += f"ctrl_pauli_z_root = Operator([\n\
    [1, 0, 0, 0],\n\
    [0, 1, 0, 0],\n\
    [0, 0, 1, 0],\n\
    [0, 0, 0, np.exp(1j * np.pi/{root})],\n\
    ])\n"
        else:
            out += f"ctrl_pauli_z_root = Operator([\n\
    [1, 0, 0, 0],\n\
    [0, 1, 0, 0],\n\
    [0, 0, np.exp(1j * np.pi/{root}), 0],\n\
    [0, 0, 0, 1],\n\
    ])\n"
        out += f"qc.unitary(ctrl_pauli_z_root, [{control}, {target}], label='ctrl-pauli-z-root')\n\n"
        return out

    @staticmethod
    def _gate_ctrl_pauli_x_root_dagger(
        control, target, controlstate, root, add_comments=True
    ):
        root = f"(2**{root[4:]})" if '^' in root else root[2:]
        out = "# ctrl-pauli-x-root-dagger gate\n" if add_comments else ""
        if int(controlstate) == 1:
            out += f"ctrl_pauli_x_root_dagger = Operator([\n\
    [1, 0, 0, 0],\n\
    [0, np.exp(-1j * np.pi/(2*{root})) * np.cos(np.pi/(2*{root})), 0, 1j * np.exp(-1j * np.pi/(2*{root})) * np.sin(np.pi/(2*{root}))],\n\
    [0, 0, 1, 0],\n\
    [0, 1j * np.exp(-1j * np.pi/(2*{root})) * np.sin(np.pi/(2*{root})), 0, np.exp(-1j * np.pi/(2*{root})) * np.cos(np.pi/(2*{root}))],\n\
    ])\n"
        else:
            out += f"ctrl_pauli_x_root_dagger = Operator([\n\
    [np.exp(-1j * np.pi/(2*{root})) * np.cos(np.pi/(2*{root})), 0, 1j * np.exp(-1j * np.pi/(2*{root})) * np.sin(np.pi/(2*{root})), 0],\n\
    [0, 1, 0, 0],\n\
    [1j * np.exp(-1j * np.pi/(2*{root})) * np.sin(np.pi/(2*{root})), 0, np.exp(-1j * np.pi/(2*{root})) * np.cos(np.pi/(2*{root})), 0],\n\
    [0, 0, 0, 1],\n\
    ])\n"
        out += f"qc.unitary(ctrl_pauli_x_root_dagger, [{control}, {target}], label='ctrl-pauli-x-root-dagger')\n\n"
        return out

    @staticmethod
    def _gate_ctrl_pauli_y_root_dagger(
        control, target, controlstate, root, add_comments=True
    ):
        root = f"(2**{root[4:]})" if '^' in root else root[2:]
        out = "# ctrl-pauli-y-root-dagger gate\n" if add_comments else ""
        if int(controlstate) == 1:
            out += f"ctrl_pauli_y_root_dagger = Operator([\n\
    [1, 0, 0, 0],\n\
    [0, np.exp(-1j * np.pi/(2*{root})) * np.cos(np.pi/(2*{root})), 0, np.exp(-1j * np.pi/(2*{root})) * np.sin(np.pi/(2*{root}))],\n\
    [0, 0, 1, 0],\n\
    [0, np.exp(-1j * np.pi/(2*{root})) * np.sin(np.pi/(2*{root})), 0, np.exp(-1j * np.pi/(2*{root})) * np.cos(np.pi/(2*{root}))],\n\
    ])\n"
        else:
            out += f"ctrl_pauli_y_root_dagger = Operator([\n\
    [np.exp(-1j * np.pi/(2*{root})) * np.cos(np.pi/(2*{root})), 0, np.exp(-1j * np.pi/(2*{root})) * np.sin(np.pi/(2*{root})), 0],\n\
    [0, 1, 0, 0],\n\
    [np.exp(-1j * np.pi/(2*{root})) * np.sin(np.pi/(2*{root})), 0, np.exp(-1j * np.pi/(2*{root})) * np.cos(np.pi/(2*{root})), 0],\n\
    [0, 0, 0, 1],\n\
    ])\n"
        out += f"qc.unitary(ctrl_pauli_y_root_dagger, [{control}, {target}], label='ctrl-pauli-y-root-dagger')\n\n"
        return out

    @staticmethod
    def _gate_ctrl_pauli_z_root_dagger(
        control, target, controlstate, root, add_comments=True
    ):
        root = f"(2**{root[4:]})" if '^' in root else root[2:]
        out = "# ctrl-pauli-z-root-dagger gate\n" if add_comments else ""
        if int(controlstate) == 1:
            out += f"ctrl_pauli_z_root_dagger = Operator([\n\
    [1, 0, 0, 0],\n\
    [0, 1, 0, 0],\n\
    [0, 0, 1, 0],\n\
    [0, 0, 0, np.exp(-1j * np.pi/{root})],\n\
    ])\n"
        else:
            out += f"ctrl_pauli_z_root_dagger = Operator([\n\
    [1, 0, 0, 0],\n\
    [0, 1, 0, 0],\n\
    [0, 0, np.exp(-1j * np.pi/{root}), 0],\n\
    [0, 0, 0, 1],\n\
    ])\n"
        out += f"qc.unitary(ctrl_pauli_z_root_dagger, [{control}, {target}], label='ctrl-pauli-z-root-dagger')\n\n"
        return out

    @staticmethod
    def _gate_ctrl_sqrt_not(control, target, controlstate, add_comments=True):
        out = "# ctrl-sqrt-not gate\n" if add_comments else ""
        out += f"qc.csx(qr[{control}], qr[{target}], ctrl_state={controlstate})\n\n"
        return out

    @staticmethod
    def _gate_ctrl_rx_theta(
        control, target, controlstate, theta_radians, add_comments=True
    ):
        out = "# ctrl-rx-theta gate\n" if add_comments else ""
        out += f"qc.crx({theta_radians}, qr[{control}], qr[{target}], ctrl_state={controlstate})\n\n"
        return out

    @staticmethod
    def _gate_ctrl_ry_theta(
        control, target, controlstate, theta_radians, add_comments=True
    ):
        out = "# ctrl-ry-theta gate\n" if add_comments else ""
        out += f"qc.cry({theta_radians}, qr[{control}], qr[{target}], ctrl_state={controlstate})\n\n"
        return out

    @staticmethod
    def _gate_ctrl_rz_theta(
        control, target, controlstate, theta_radians, add_comments=True
    ):
        out = "# ctrl-rz-theta gate\n" if add_comments else ""
        out += f"qc.crz({theta_radians}, qr[{control}], qr[{target}], ctrl_state={controlstate})\n\n"
        return out

    @staticmethod
    def _gate_ctrl_s(control, target, controlstate, add_comments=True):
        out = "# ctrl-s gate\n" if add_comments else ""
        out += f"qc.cp({math.pi/2}, qr[{control}], qr[{target}], ctrl_state={controlstate})\n\n"
        return out

    @staticmethod
    def _gate_ctrl_s_dagger(control, target, controlstate, add_comments=True):
        out = "# ctrl-s-dagger gate\n" if add_comments else ""
        out += f"qc.cp({-math.pi/2}, qr[{control}], qr[{target}], ctrl_state={controlstate})\n\n"
        return out

    @staticmethod
    def _gate_toffoli(
        control, control2, target, controlstate, controlstate2, add_comments=True
    ):
        #controlstate = f"{controlstate}{controlstate2}"
        if (int(controlstate) != 1 or int(controlstate2) != 1):
            raise BaseExporter.ExportException("Due to a bug in current version of Qiskit, Toffoli gate suports only 1 states as control.")
        out = "# toffoli gate\n" if add_comments else ""
        out += f"qc.ccx(qr[{control}], qr[{control2}], qr[{target}])\n\n"
        return out

    @staticmethod
    def _gate_fredkin(control, target, target2, controlstate, add_comments=True):
        out = "# fredkin gate\n" if add_comments else ""
        out += f"qc.cswap(qr[{control}], qr[{target}], qr[{target2}], ctrl_state={controlstate})\n\n"
        return out

    @staticmethod
    def _gate_measure_x(target, classic_bit, add_comments=True):
        raise BaseExporter.ExportException("The measure-x gate is not implemented.")

    @staticmethod
    def _gate_measure_y(target, classic_bit, add_comments=True):
        raise BaseExporter.ExportException("The measure-y gate is not implemented.")

    @staticmethod
    def _gate_measure_z(target, classic_bit, add_comments=True):
        out = "# measure-z gate\n" if add_comments else ""
        out += f"qc.measure(qr[{target}], cr[{classic_bit}])\n\n"
        return out
