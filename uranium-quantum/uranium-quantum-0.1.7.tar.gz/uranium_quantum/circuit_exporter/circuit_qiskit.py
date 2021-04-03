from qiskit import QuantumRegister
from qiskit.circuit import ClassicalRegister
from qiskit import QuantumCircuit, execute, Aer
from qiskit.circuit.library.standard_gates import iswap
from qiskit.circuit.library import RXXGate, RYYGate, RZZGate
from qiskit.quantum_info.operators import Operator
cr = ClassicalRegister(0)
qr = QuantumRegister(12)
qc = QuantumCircuit(qr, cr)



# New circuit step no: 0 


# xx gate
qc.append(RXXGate(0), [0, 1])

# yy gate
qc.append(RYYGate(0), [2, 3])

# zz gate
qc.append(RZZGate(0), [4, 5])



# New circuit step no: 1 


# pauli-x-root gate
pauli_x_root = np.exp(1j * np.pi/3) * Operator([
    [cos(np.pi/3), -1j * sin(np.pi/3)],
    [-1j * sin(np.pi/3), cos(np.pi/3)],
    ])
qc.unitary(pauli_x_root, [0], label='pauli-x-root')

# pauli-y-root gate
pauli_y_root = np.exp(1j * np.pi/3) * Operator([
    [cos(np.pi/3), -sin(np.pi/3)],
    [-sin(np.pi/3), cos(np.pi/3)],
    ])
qc.unitary(pauli_y_root, [1], label='pauli-y-root')

# pauli-z-root gate
pauli_z_root = np.exp(1j * np.pi/3) * Operator([
    [1, 0],
    [0, exp(1j * 2 * np.pi/3)],
    ])
qc.unitary(pauli_z_root, [2], label='pauli-z-root')

# pauli-x-root gate
pauli_x_root = np.exp(1j * np.pi/(2**2)) * Operator([
    [cos(np.pi/(2**2)), -1j * sin(np.pi/(2**2))],
    [-1j * sin(np.pi/(2**2)), cos(np.pi/(2**2))],
    ])
qc.unitary(pauli_x_root, [3], label='pauli-x-root')

# pauli-y-root gate
pauli_y_root = np.exp(1j * np.pi/(2**2)) * Operator([
    [cos(np.pi/(2**2)), -sin(np.pi/(2**2))],
    [-sin(np.pi/(2**2)), cos(np.pi/(2**2))],
    ])
qc.unitary(pauli_y_root, [4], label='pauli-y-root')

# pauli-z-root gate
pauli_z_root = np.exp(1j * np.pi/(2**2)) * Operator([
    [1, 0],
    [0, exp(1j * 2 * np.pi/(2**2))],
    ])
qc.unitary(pauli_z_root, [5], label='pauli-z-root')



# New circuit step no: 2 


# pauli-x-root-dagger gate
pauli_x_root_dagger = np.exp(-1j * np.pi/2) * Operator([
    [cos(np.pi/2), 1j * sin(np.pi/2)],
    [1j * sin(np.pi/2), cos(np.pi/2)],
    ])
qc.unitary(pauli_x_root_dagger, [0], label='pauli-x-root-dagger')

# pauli-y-root-dagger gate
pauli_y_root_dagger = np.exp(-1j * np.pi/2) * Operator([
    [cos(np.pi/2), sin(np.pi/2)],
    [sin(np.pi/2), cos(np.pi/2)],
    ])
qc.unitary(pauli_y_root_dagger, [1], label='pauli-y-root-dagger')

# pauli_z-root-dagger gate
pauli_z_root_dagger = Operator([
    [1, 0],
    [0, exp(-1j * 2 * np.pi/2)],
    ])
qc.unitary(pauli_z_root_dagger, [2], label='pauli-z-root-dagger')

# pauli-x-root-dagger gate
pauli_x_root_dagger = np.exp(-1j * np.pi/(2**5)) * Operator([
    [cos(np.pi/(2**5)), 1j * sin(np.pi/(2**5))],
    [1j * sin(np.pi/(2**5)), cos(np.pi/(2**5))],
    ])
qc.unitary(pauli_x_root_dagger, [3], label='pauli-x-root-dagger')

# pauli-y-root-dagger gate
pauli_y_root_dagger = np.exp(-1j * np.pi/(2**5)) * Operator([
    [cos(np.pi/(2**5)), sin(np.pi/(2**5))],
    [sin(np.pi/(2**5)), cos(np.pi/(2**5))],
    ])
qc.unitary(pauli_y_root_dagger, [4], label='pauli-y-root-dagger')

# pauli_z-root-dagger gate
pauli_z_root_dagger = Operator([
    [1, 0],
    [0, exp(-1j * 2 * np.pi/(2**5))],
    ])
qc.unitary(pauli_z_root_dagger, [5], label='pauli-z-root-dagger')



# New circuit step no: 3 


# ctrl-pauli-x-root gate
ctrl_pauli_x_root = Operator([
    [1, 0, 0, 0],
    [0, cos(np.pi/1), 0, -1j * sin(np.pi/1)],
    [0, 0, 1, 0],
    [0, -1j * sin(np.pi/1), 0, cos(np.pi/1)],
    ])
qc.unitary(ctrl_pauli_x_root, [0], label='ctrl-pauli-x-root')

# ctrl-pauli-y-root gate
ctrl_pauli_y_root = Operator([
    [1, 0, 0, 0],
    [0, cos(np.pi/1), 0, -sin(np.pi/1)],
    [0, 0, 1, 0],
    [0, -sin(np.pi/1), 0, cos(np.pi/1)],
    ])
qc.unitary(ctrl_pauli_y_root, [2], label='ctrl-pauli-y-root')

# ctrl-pauli-z-root gate
ctrl_pauli_z_root = Operator([
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, exp(1j * 2 * np.pi/1)],
    ])
qc.unitary(ctrl_pauli_z_root, [4], label='ctrl-pauli-z-root')

# ctrl-pauli-x-root gate
ctrl_pauli_x_root = Operator([
    [1, 0, 0, 0],
    [0, cos(np.pi/(2**3)), 0, -1j * sin(np.pi/(2**3))],
    [0, 0, 1, 0],
    [0, -1j * sin(np.pi/(2**3)), 0, cos(np.pi/(2**3))],
    ])
qc.unitary(ctrl_pauli_x_root, [6], label='ctrl-pauli-x-root')

# ctrl-pauli-y-root gate
ctrl_pauli_y_root = Operator([
    [1, 0, 0, 0],
    [0, cos(np.pi/(2**3)), 0, -sin(np.pi/(2**3))],
    [0, 0, 1, 0],
    [0, -sin(np.pi/(2**3)), 0, cos(np.pi/(2**3))],
    ])
qc.unitary(ctrl_pauli_y_root, [8], label='ctrl-pauli-y-root')

# ctrl-pauli-z-root gate
ctrl_pauli_z_root = Operator([
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, exp(1j * 2 * np.pi/(2**3))],
    ])
qc.unitary(ctrl_pauli_z_root, [10], label='ctrl-pauli-z-root')



# New circuit step no: 4 


# ctrl-pauli-x-root-dagger gate
ctrl_pauli_x_root_dagger = Operator([
    [1, 0, 0, 0],
    [0, cos(np.pi/1), 0, 1j * sin(np.pi/1)],
    [0, 0, 1, 0],
    [0, 1j * sin(np.pi/1), 0, cos(np.pi/1)],
    ])
qc.unitary(ctrl_pauli_x_root_dagger, [0], label='ctrl-pauli-x-root-dagger')

# ctrl-pauli-y-root-dagger gate
ctrl_pauli_y_root_dagger = Operator([
    [1, 0, 0, 0],
    [0, cos(np.pi/1), 0, sin(np.pi/1)],
    [0, 0, 1, 0],
    [0, sin(np.pi/1), 0, cos(np.pi/1)],
    ])
qc.unitary(ctrl_pauli_y_root_dagger, [2], label='ctrl-pauli-y-root-dagger')

# ctrl-pauli-z-root-dagger gate
ctrl_pauli_z_root_dagger = Operator([
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, exp(-1j * 2 * np.pi/1)],
    ])
qc.unitary(ctrl_pauli_z_root_dagger, [4], label='ctrl-pauli-z-root-dagger')

# ctrl-pauli-x-root-dagger gate
ctrl_pauli_x_root_dagger = Operator([
    [1, 0, 0, 0],
    [0, cos(np.pi/(2**4)), 0, 1j * sin(np.pi/(2**4))],
    [0, 0, 1, 0],
    [0, 1j * sin(np.pi/(2**4)), 0, cos(np.pi/(2**4))],
    ])
qc.unitary(ctrl_pauli_x_root_dagger, [6], label='ctrl-pauli-x-root-dagger')

# ctrl-pauli-y-root-dagger gate
ctrl_pauli_y_root_dagger = Operator([
    [1, 0, 0, 0],
    [0, cos(np.pi/(2**4)), 0, sin(np.pi/(2**4))],
    [0, 0, 1, 0],
    [0, sin(np.pi/(2**4)), 0, cos(np.pi/(2**4))],
    ])
qc.unitary(ctrl_pauli_y_root_dagger, [8], label='ctrl-pauli-y-root-dagger')

# ctrl-pauli-z-root-dagger gate
ctrl_pauli_z_root_dagger = Operator([
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, exp(-1j * 2 * np.pi/(2**4))],
    ])
qc.unitary(ctrl_pauli_z_root_dagger, [10], label='ctrl-pauli-z-root-dagger')


simulator = Aer.get_backend('qasm_simulator')
job = execute(qc, backend=simulator, shots=10)
job_result = job.result()
print(job_result.status)
