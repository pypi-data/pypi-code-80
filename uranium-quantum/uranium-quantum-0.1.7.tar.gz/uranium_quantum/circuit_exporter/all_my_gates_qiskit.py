import numpy as np
from qiskit import QuantumRegister
from qiskit.circuit import ClassicalRegister
from qiskit import QuantumCircuit, execute, Aer
from qiskit.circuit.library.standard_gates import iswap
from qiskit.circuit.library import RXXGate, RYYGate, RZZGate
from qiskit.quantum_info.operators import Operator
from qiskit.visualization import plot_histogram
cr = ClassicalRegister(3)
qr = QuantumRegister(22)
qc = QuantumCircuit(qr, cr)


############ New circuit step no: 0 ############


# identity gate
qc.id(qr[0])

# u3 gate
qc.u(1.57, 1.57, 1.57, qr[1])

# u2 gate
qc.u(1.5707963267948966, 1.57, 1.57, qr[2])

# u1 gate
qc.p(1.57, qr[3])

# identity gate
qc.id(qr[4])

# hadamard gate
qc.h(qr[5])

# pauli-x gate
qc.x(qr[6])

# pauli-y gate
qc.y(qr[7])

# pauli-z gate
qc.z(qr[8])

# t gate
qc.t(qr[9])

# t-dagger gate
qc.tdg(qr[10])

# rx-theta gate
qc.rx(1.57, qr[11])

# ry-theta gate
qc.ry(1.57, qr[12])

# rz-theta gate
qc.rz(1.57, qr[13])

# s gate
qc.s(qr[14])

# s-dagger gate
qc.sdg(qr[15])

# pauli-x-root gate
pauli_x_root = np.exp(1j * np.pi/(2*2.0)) * Operator([
    [np.cos(np.pi/(2*2.0)), -1j * np.sin(np.pi/(2*2.0))],
    [-1j * np.sin(np.pi/(2*2.0)), np.cos(np.pi/(2*2.0))],
    ])

qc.unitary(pauli_x_root, [16], label='pauli-x-root')

# pauli-y-root gate
pauli_y_root = np.exp(1j * np.pi/(2*(2**7.0))) * Operator([
    [np.cos(np.pi/(2*(2**7.0))), -np.sin(np.pi/(2*(2**7.0)))],
    [np.sin(np.pi/(2*(2**7.0))), np.cos(np.pi/(2*(2**7.0)))],
    ])

qc.unitary(pauli_y_root, [17], label='pauli-y-root')

# pauli-z-root gate
pauli_z_root = np.exp(1j * np.pi/(2**22.0)) * Operator([
    [1, 0],
    [0, np.exp(1j * np.pi/(2**22.0))],
    ])

qc.unitary(pauli_z_root, [18], label='pauli-z-root')

# pauli-x-root-dagger gate
pauli_x_root_dagger = np.exp(-1j * np.pi/(2*(2**29.0))) * Operator([
    [np.cos(np.pi/(2*(2**29.0))), 1j * np.sin(np.pi/(2*(2**29.0)))],
    [1j * np.sin(np.pi/(2*(2**29.0))), np.cos(np.pi/(2*(2**29.0)))],
    ])

qc.unitary(pauli_x_root_dagger, [19], label='pauli-x-root-dagger')

# pauli-y-root-dagger gate
pauli_y_root_dagger = np.exp(-1j * np.pi/(2*(2**8.0))) * Operator([
    [np.cos(np.pi/(2*(2**8.0))), - np.sin(np.pi/(2*(2**8.0)))],
    [np.sin(np.pi/(2*(2**8.0))), np.cos(np.pi/(2*(2**8.0)))],
    ])

qc.unitary(pauli_y_root_dagger, [20], label='pauli-y-root-dagger')

# pauli_z-root-dagger gate
pauli_z_root_dagger = Operator([
    [1, 0],
    [0, np.exp(-1j * np.pi/1.1)],
    ])

qc.unitary(pauli_z_root_dagger, [21], label='pauli-z-root-dagger')



############ New circuit step no: 1 ############


# ctrl-u3 gate
qc.cu(1.57, 1.57, 1.57, 1.5707963267948966, qr[1], qr[2], ctrl_state=1)



############ New circuit step no: 2 ############


# ctrl-u2 gate
qc.cu(1.5707963267948966, 1.57, 1.57, 1.5707963267948966, qr[2], qr[3], ctrl_state=1)



############ New circuit step no: 3 ############


# ctrl-u1 gate
qc.cp(1.57, qr[3], qr[4], ctrl_state=0)



############ New circuit step no: 4 ############


# ctrl-hadamard gate
qc.ch(qr[4], qr[5], ctrl_state=1)



############ New circuit step no: 5 ############


# ctrl-pauli-x gate
qc.cx(qr[5], qr[6], ctrl_state=0)



############ New circuit step no: 6 ############


# ctrl-pauli-y gate
qc.cy(qr[6], qr[7], ctrl_state=1)



############ New circuit step no: 7 ############


# ctrl-pauli-z gate
qc.cz(qr[7], qr[8], ctrl_state=0)



############ New circuit step no: 8 ############


# ctrl-t gate
qc.cp(0.7853981633974483, qr[8], qr[9], ctrl_state=1)



############ New circuit step no: 9 ############


# ctrl-t-dagger gate
qc.cp(-0.7853981633974483, qr[9], qr[10], ctrl_state=0)



############ New circuit step no: 10 ############


# ctrl-rx-theta gate
qc.crx(1.57, qr[10], qr[11], ctrl_state=1)



############ New circuit step no: 11 ############


# ctrl-ry-theta gate
qc.cry(1.57, qr[11], qr[12], ctrl_state=0)



############ New circuit step no: 12 ############


# ctrl-rz-theta gate
qc.crz(1.57, qr[12], qr[13], ctrl_state=1)



############ New circuit step no: 13 ############


# ctrl-s gate
qc.cp(1.5707963267948966, qr[13], qr[14], ctrl_state=0)



############ New circuit step no: 14 ############


# ctrl-s-dagger gate
qc.cp(-1.5707963267948966, qr[14], qr[15], ctrl_state=1)



############ New circuit step no: 15 ############


# ctrl-pauli-x-root gate
ctrl_pauli_x_root = Operator([
    [np.exp(1j * np.pi/(2*2.0)) * np.cos(np.pi/(2*2.0)), 0, -1j * np.exp(1j * np.pi/(2*2.0)) * np.sin(np.pi/(2*2.0)), 0],
    [0, 1, 0, 0],
    [-1j * np.exp(1j * np.pi/(2*2.0)) * np.sin(np.pi/(2*2.0)), 0, np.exp(1j * np.pi/(2*2.0)) * np.cos(np.pi/(2*2.0)), 0],
    [0, 0, 0, 1],
    ])
qc.unitary(ctrl_pauli_x_root, [15, 16], label='ctrl-pauli-x-root')



############ New circuit step no: 16 ############


# ctrl-pauli-y-root gate
ctrl_pauli_y_root = Operator([
    [1, 0, 0, 0],
    [0, np.exp(1j * np.pi/(2*(2**17.0))) * np.cos(np.pi/(2*(2**17.0))), 0, - np.exp(1j * np.pi/(2*(2**17.0))) * np.sin(np.pi/(2*(2**17.0)))],
    [0, 0, 1, 0],
    [0, np.exp(1j * np.pi/(2*(2**17.0))) * np.sin(np.pi/(2*(2**17.0))), 0, np.exp(1j * np.pi/(2*(2**17.0))) * np.cos(np.pi/(2*(2**17.0)))],
    ])
qc.unitary(ctrl_pauli_y_root, [16, 17], label='ctrl-pauli-y-root')



############ New circuit step no: 17 ############


# ctrl-pauli-z-root gate
ctrl_pauli_z_root = Operator([
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, np.exp(1j * np.pi/2.0), 0],
    [0, 0, 0, 1],
    ])
qc.unitary(ctrl_pauli_z_root, [17, 18], label='ctrl-pauli-z-root')



############ New circuit step no: 18 ############


# ctrl-pauli-x-root-dagger gate
ctrl_pauli_x_root_dagger = Operator([
    [np.exp(-1j * np.pi/(2*(2**22.0))) * np.cos(np.pi/(2*(2**22.0))), 0, 1j * np.exp(-1j * np.pi/(2*(2**22.0))) * np.sin(np.pi/(2*(2**22.0))), 0],
    [0, 1, 0, 0],
    [1j * np.exp(-1j * np.pi/(2*(2**22.0))) * np.sin(np.pi/(2*(2**22.0))), 0, np.exp(-1j * np.pi/(2*(2**22.0))) * np.cos(np.pi/(2*(2**22.0))), 0],
    [0, 0, 0, 1],
    ])
qc.unitary(ctrl_pauli_x_root_dagger, [18, 19], label='ctrl-pauli-x-root-dagger')



############ New circuit step no: 19 ############


# ctrl-pauli-y-root-dagger gate
ctrl_pauli_y_root_dagger = Operator([
    [1, 0, 0, 0],
    [0, np.exp(-1j * np.pi/(2*(2**35.0))) * np.cos(np.pi/(2*(2**35.0))), 0, np.exp(-1j * np.pi/(2*(2**35.0))) * np.sin(np.pi/(2*(2**35.0)))],
    [0, 0, 1, 0],
    [0, np.exp(-1j * np.pi/(2*(2**35.0))) * np.sin(np.pi/(2*(2**35.0))), 0, np.exp(-1j * np.pi/(2*(2**35.0))) * np.cos(np.pi/(2*(2**35.0)))],
    ])
qc.unitary(ctrl_pauli_y_root_dagger, [19, 20], label='ctrl-pauli-y-root-dagger')



############ New circuit step no: 20 ############


# ctrl-pauli-z-root-dagger gate
ctrl_pauli_z_root_dagger = Operator([
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, np.exp(-1j * np.pi/2.22), 0],
    [0, 0, 0, 1],
    ])
qc.unitary(ctrl_pauli_z_root_dagger, [20, 21], label='ctrl-pauli-z-root-dagger')



############ New circuit step no: 21 ############


# swap gate
qc.swap(qr[1], qr[2])

# iswap gate
qc.iswap(qr[4], qr[5])

# sqrt-swap gate
qc.u(1.5707963267948966, 1.5707963267948966, -3.141592653589793, qr[6])
qc.u(1.5707963267948966, -1.5707963267948966, 3.141592653589793, qr[7])
qc.cx(qr[6], qr[7])
qc.u(0.7853981633974483, -1.5707963267948966, -1.5707963267948966, qr[6])
qc.u(1.5707963267948966, 0, 5.497787143782138, qr[7])
qc.cx(qr[6], qr[7])
qc.u(0.7853981633974483, -3.141592653589793, -1.5707963267948966, qr[6])
qc.u(1.5707963267948966, 3.141592653589793, 1.5707963267948966, qr[7])
qc.cx(qr[6], qr[7])
qc.u(1.5707963267948966, 0, -4.71238898038469, qr[6])
qc.u(1.5707963267948966, 1.5707963267948966, 0, qr[7])

# swap-phi gate
swap_phi = Operator([
    [1, 0, 0, 0],
    [0, 0,  np.exp(1j * 1.57), 0],
    [0, np.exp(1j * 1.57), 0, 0],
    [0, 0, 0, 1],
    ])
qc.unitary(swap_phi, [9, 10], label='swap-phi')



############ New circuit step no: 22 ############


# xx gate
qc.append(RXXGate(0.5), [1, 2])

# yy gate
qc.append(RYYGate(0.5), [4, 6])

# zz gate
qc.append(RZZGate(0.5), [8, 10])



############ New circuit step no: 23 ############


# toffoli gate
qc.ccx(qr[4], qr[5], qr[6])



############ New circuit step no: 24 ############


# fredkin gate
qc.cswap(qr[7], qr[8], qr[9], ctrl_state=1)



############ New circuit step no: 25 ############


# measure-z gate
qc.measure(qr[2], cr[2])


# Using Aer's qasm_simulator
simulator = Aer.get_backend('qasm_simulator')

# Execute the circuit on the qasm simulator
job = execute(qc, backend=simulator, shots=1000)

# Grab results from the job
result = job.result()

print('Job result status', result.status)
counts = result.get_counts(qc)

# Note: you need to include some measure gates in your circuit in order to see some plots here:
plot_histogram(counts)
