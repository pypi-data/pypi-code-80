import importlib
import math

BaseExporter = importlib.import_module("uranium_quantum.circuit_exporter.base-exporter")


class Exporter(BaseExporter.BaseExporter):
    def start_code(self):
        return f'\
OPENQASM 2.0;\n\
include "qelib1.inc";\n\
qreg q0[{self._qubits}];\n\
creg c0[{self._bits}];\n\n\n'

    def end_code(self):
        return out

    @staticmethod
    def _gate_u3(
        target, theta_radians, phi_radians, lambda_radians, add_comments=True
    ):
        out = "# u3 gate\n" if add_comments else ""
        out += f"u({theta_radians}, {phi_radians}, {lambda_radians}) q0[{target}];\n"
        return out

    @staticmethod
    def _gate_u2(target, phi_radians, lambda_radians, add_comments=True):
        out = "# u2 gate\n" if add_comments else ""
        out += f"u({math.pi/2}, {phi_radians}, {lambda_radians}) q0[{target}];\n"
        return out

    @staticmethod
    def _gate_u1(target, lambda_radians, add_comments=True):
        out = "# u1 gate\n" if add_comments else ""
        out += f"p({lambda_radians}) q0[{target}];\n"
        return out

    @staticmethod
    def _gate_identity(target, add_comments=True):
        out = "# identity gate\n" if add_comments else ""
        out += f"q0[{target}];\n"
        return out

    @staticmethod
    def _gate_hadamard(target, add_comments=True):
        out = "# hadamard gate\n" if add_comments else ""
        out += f"h q0[{target}];\n"
        return out

    @staticmethod
    def _gate_pauli_x(target, add_comments=True):
        out = "# pauli-x gate\n" if add_comments else ""
        out += f"x q0[{target}];\n"
        return out

    @staticmethod
    def _gate_pauli_y(target, add_comments=True):
        out = "# pauli-y gate\n" if add_comments else ""
        out += f"y q0[{target}];\n"
        return out

    @staticmethod
    def _gate_pauli_z(target, add_comments=True):
        out = "# pauli-z gate\n" if add_comments else ""
        out += f"z q0[{target}];\n"
        return out

    @staticmethod
    def _gate_pauli_x_root(target, root, add_comments=True):
        # TODO
        root = f"(2**{root[4:]})" if '^' in root else root[2:]
        out = "# pauli-x-root gate\n" if add_comments else ""
        return out

    @staticmethod
    def _gate_pauli_y_root(target, root, add_comments=True):
        # TODO
        root = f"(2**{root[4:]})" if '^' in root else root[2:]
        out = "# pauli-y-root gate\n" if add_comments else ""
        return out

    @staticmethod
    def _gate_pauli_z_root(target, root, add_comments=True):
        # TODO
        root = f"(2**{root[4:]})" if '^' in root else root[2:]
        out = "# pauli-z-root gate\n" if add_comments else ""
        return out

    @staticmethod
    def _gate_pauli_x_root_dagger(target, root, add_comments=True):
        # TODO
        root = f"(2**{root[4:]})" if '^' in root else root[2:]
        out = "# pauli-x-root-dagger gate\n" if add_comments else ""
        return out

    @staticmethod
    def _gate_pauli_y_root_dagger(target, root, add_comments=True):
        # TODO
        root = f"(2**{root[4:]})" if '^' in root else root[2:]
        out = "# pauli-y-root-dagger gate\n" if add_comments else ""
        return out

    @staticmethod
    def _gate_pauli_z_root_dagger(target, root, add_comments=True):
        # TODO
        root = f"(2**{root[4:]})" if '^' in root else root[2:]
        out = "# pauli-z-root-dagger gate\n" if add_comments else ""
        return out

    @staticmethod
    def _gate_sqrt_not(target, add_comments=True):
        out = "# sqrt-not gate\n" if add_comments else ""
        out += f"sx q0[{target}];\n"
        return out

    @staticmethod
    def _gate_t(target, add_comments=True):
        out = "# t gate\n" if add_comments else ""
        out += f"t q0[{target}];\n"
        return out

    @staticmethod
    def _gate_t_dagger(target, add_comments=True):
        out = "# t-dagger gate\n" if add_comments else ""
        out += f"tdg q0[{target}];\n"
        return out

    @staticmethod
    def _gate_rx_theta(target, theta, add_comments=True):
        out = "# rx-theta gate\n" if add_comments else ""
        out += f"rx({theta}) q0[{target}];\n"
        return out

    @staticmethod
    def _gate_ry_theta(target, theta, add_comments=True):
        out = "# ry-theta gate\n" if add_comments else ""
        out += f"ry({theta}) q0[{target}];\n"
        return out

    @staticmethod
    def _gate_rz_theta(target, theta, add_comments=True):
        out = "# rz-theta gate\n" if add_comments else ""
        out += f"rz({theta}) q0[{target}];\n"
        return out

    @staticmethod
    def _gate_s(target, add_comments=True):
        out = "# s gate\n" if add_comments else ""
        out += f"s q0[{target}];\n"
        return out

    @staticmethod
    def _gate_s_dagger(target, add_comments=True):
        out = "# s-dagger gate\n" if add_comments else ""
        out += f"sdg q0[{target}];\n"
        return out

    @staticmethod
    def _gate_swap(target, target2, add_comments=True):
        out = "# swap gate\n" if add_comments else ""
        out += f"swap q0[{target}], q0[{target2}];\n"
        return out

    @staticmethod
    def _gate_iswap(target, target2, add_comments=True):
        out = "# iswap gate\n" if add_comments else ""
        out += f"iswap q0[{target}], q0[{target2}];\n"
        return out

    @staticmethod
    def _gate_swap_phi(target, target2, phi):
        raise BaseExporter.ExportException("The swap-phi gate is not implemented.")

    @staticmethod
    def _gate_sqrt_swap(target, target2, add_comments=True):
        out = "# sqrt-swap gate\n" if add_comments else ""
        out += f"u({math.pi/2}, {math.pi/2}, {-math.pi}) q0[{target}];\n"
        out += f"u({math.pi/2}, {-math.pi/2}, {math.pi}) q0[{target2}];\n"
        out += f"cx q0[{target}], q0[{target2}];\n"
        out += f"u({math.pi/4}, {-math.pi/2}, {-math.pi/2}) q0[{target}];\n"
        out += f"u({math.pi/2}, 0, {1.75 * math.pi}) q0[{target2}];\n"
        out += f"cx q0[{target}], q0[{target2}];\n"
        out += f"u({math.pi/4}, {-math.pi}, {-math.pi/2}) q0[{target}];\n"
        out += f"u({math.pi/2}, {math.pi}, {math.pi/2}) q0[{target2}];\n"
        out += f"cx q0[{target}], q0[{target2}];\n"
        out += f"u({math.pi/2}, 0, {-1.5 * math.pi}) q0[{target}];\n"
        out += f"u({math.pi/2}, {math.pi/2}, 0) q0[{target2}];\n"
        return out

    @staticmethod
    def _gate_xx(target, target2, theta, add_comments=True):
        # TODO
        root = f"(2**{root[4:]})" if '^' in root else root[2:]
        out = "# xx gate\n" if add_comments else ""
        return out

    @staticmethod
    def _gate_yy(target, target2, theta, add_comments=True):
        # TODO
        root = f"(2**{root[4:]})" if '^' in root else root[2:]
        out = "# yy gate\n" if add_comments else ""
        return out

    @staticmethod
    def _gate_zz(target, target2, theta, add_comments=True):
        # TODO
        root = f"(2**{root[4:]})" if '^' in root else root[2:]
        out = "# zz gate\n" if add_comments else ""
        return out

    @staticmethod
    def _gate_ctrl_hadamard(control, target, controlstate, add_comments=True):
        out = "# ctrl-hadamard gate\n" if add_comments else ""
        out += f"ch q[{control}], q[{target}];\n"
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
        out += f"cu({theta_radians}, {phi_radians}, {lambda_radians}, {math.pi/2}) q0[{control}], q0[{target}];\n"
        return out

    @staticmethod
    def _gate_ctrl_u2(
        control, target, controlstate, phi_radians, lambda_radians, add_comments=True
    ):
        out = "# ctrl-u2 gate\n" if add_comments else ""
        out += f"cu({math.pi/2}, {phi_radians}, {lambda_radians}, {math.pi/2}) q0[{control}], q0[{target}];\n"
        return out

    @staticmethod
    def _gate_ctrl_u1(
        control, target, controlstate, lambda_radians, add_comments=True
    ):
        out = "# ctrl-u1 gate\n" if add_comments else ""
        out += f"cp({lambda_radians}) q0[{control}], q0[{target}];\n"
        return out

    @staticmethod
    def _gate_ctrl_t(control, target, controlstate, add_comments=True):
        out = "# ctrl-t gate\n" if add_comments else ""
        out += f"cp({math.pi/4}) q0[{control}], q0[{target}];\n"
        return out

    @staticmethod
    def _gate_ctrl_t_dagger(control, target, controlstate, add_comments=True):
        out = "# ctrl-t-dagger gate\n" if add_comments else ""
        out += f"cp({-math.pi/4}) q0[{control}], q0[{target}];\n"
        return out

    @staticmethod
    def _gate_ctrl_pauli_x(control, target, controlstate, add_comments=True):
        out = "# ctrl-pauli-x gate\n" if add_comments else ""
        out += f"cx q0[{control}], q0[{target}];\n"
        return out

    @staticmethod
    def _gate_ctrl_pauli_y(control, target, controlstate, add_comments=True):
        out = "# ctrl-pauli-y gate\n" if add_comments else ""
        out += f"cy q0[{control}], q0[{target}];\n"
        return out

    @staticmethod
    def _gate_ctrl_pauli_z(control, target, controlstate, add_comments=True):
        out = "# ctrl-pauli-z gate\n" if add_comments else ""
        out += f"cz q0[{control}], q0[{target}];\n"
        return out

    @staticmethod
    def _gate_ctrl_pauli_x_root(
        control, target, controlstate, root, add_comments=True
    ):
        # TODO
        root = f"(2**{root[4:]})" if '^' in root else root[2:]
        out = "# ctrl-pauli-x-root gate\n" if add_comments else ""
        return out

    @staticmethod
    def _gate_ctrl_pauli_y_root(
        control, target, controlstate, root, add_comments=True
    ):
        # TODO
        root = f"(2**{root[4:]})" if '^' in root else root[2:]
        out = "# ctrl-pauli-y-root gate\n" if add_comments else ""
        return out

    @staticmethod
    def _gate_ctrl_pauli_z_root(
        control, target, controlstate, root, add_comments=True
    ):
        # TODO
        root = f"(2**{root[4:]})" if '^' in root else root[2:]
        out = "# ctrl-pauli-z-root gate\n" if add_comments else ""
        return out

    @staticmethod
    def _gate_ctrl_pauli_x_root_dagger(
        control, target, controlstate, root, add_comments=True
    ):
        # TODO
        root = f"(2**{root[4:]})" if '^' in root else root[2:]
        out = "# ctrl-pauli-x-root-dagger gate\n" if add_comments else ""
        return out

    @staticmethod
    def _gate_ctrl_pauli_y_root_dagger(
        control, target, controlstate, root, add_comments=True
    ):
        # TODO
        root = f"(2**{root[4:]})" if '^' in root else root[2:]
        out = "# ctrl-pauli-y-root-dagger gate\n" if add_comments else ""
        return out

    @staticmethod
    def _gate_ctrl_pauli_z_root_dagger(
        control, target, controlstate, root, add_comments=True
    ):
        # TODO
        root = f"(2**{root[4:]})" if '^' in root else root[2:]
        out = "# ctrl-pauli-z-root-dagger gate\n" if add_comments else ""
        return out

    @staticmethod
    def _gate_ctrl_sqrt_not(control, target, controlstate, add_comments=True):
        out = "# ctrl-sqrt-not gate\n" if add_comments else ""
        out += f"csx q0[{control}], q0[{target}];\n"
        return out

    @staticmethod
    def _gate_ctrl_rx_theta(
        control, target, controlstate, theta_radians, add_comments=True
    ):
        out = "# ctrl-rx-theta gate\n" if add_comments else ""
        out += f"crx({theta_radians}) q0[{control}], q0[{target}];\n"
        return out

    @staticmethod
    def _gate_ctrl_ry_theta(
        control, target, controlstate, theta_radians, add_comments=True
    ):
        out = "# ctrl-ry-theta gate\n" if add_comments else ""
        out += f"cry({theta_radians}) q0[{control}], q0[{target}];\n"
        return out

    @staticmethod
    def _gate_ctrl_rz_theta(
        control, target, controlstate, theta_radians, add_comments=True
    ):
        out = "# ctrl-rz-theta gate\n" if add_comments else ""
        out += f"crz({theta_radians}) q0[{control}], q0[{target}];\n"
        return out

    @staticmethod
    def _gate_ctrl_s(control, target, controlstate, add_comments=True):
        out = "# ctrl-s gate\n" if add_comments else ""
        out += f"cp({math.pi/2}) q0[{control}], q0[{target}];\n"
        return out

    @staticmethod
    def _gate_ctrl_s_dagger(control, target, controlstate, add_comments=True):
        out = "# ctrl-s-dagger gate\n" if add_comments else ""
        out += f"cp({-math.pi/2}) q0[{control}], q0[{target}];\n"
        return out

    @staticmethod
    def _gate_toffoli(
        control, control2, target, controlstate, controlstate2, add_comments=True
    ):
        out = "# toffoli gate\n" if add_comments else ""
        out += f"ccx q0[{control}], q0[{control2}], q0[{target}];\n"
        return out

    @staticmethod
    def _gate_fredkin(control, target, target2, controlstate, add_comments=True):
        out = "# fredkin gate\n" if add_comments else ""
        out += f"cswap q0[{control}], q0[{target}], q0[{target2}];\n"
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
        out += f"measure q0[{target}] -> c0[{classic_bit}];\n"
        return out
