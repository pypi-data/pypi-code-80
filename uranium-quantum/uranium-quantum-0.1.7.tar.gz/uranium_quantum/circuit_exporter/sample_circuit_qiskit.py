from qiskit import QuantumRegister
from qiskit.circuit import ClassicalRegister
from qiskit import QuantumCircuit, execute, Aer
from qiskit.circuit.library.standard_gates import iswap
from qiskit.circuit.library import RXXGate, RYYGate, RZZGate
from qiskit.quantum_info.operators import Operator
cr = ClassicalRegister(4)
qr = QuantumRegister(17)
qc = QuantumCircuit(qr, cr)



# New circuit step no: 0 


# identity gate
qc.id(qr[0])


# New circuit step no: 1 


# u3 gate
qc.u(1.57, 1.57, 1.57, qr[1])


# New circuit step no: 2 


# u2 gate
qc.u(1.5707963267948966, 1.57, 1.57, qr[2])


# New circuit step no: 3 


# u1 gate
qc.p(1.57, qr[3])


# New circuit step no: 4 


# hadamard gate
qc.h(qr[4])


# New circuit step no: 5 


# pauli-x gate
qc.x(qr[5])


# New circuit step no: 6 


# pauli-y gate
qc.y(qr[6])


# New circuit step no: 7 


# pauli-z gate
qc.z(qr[7])


# New circuit step no: 8 


# sqrt-not gate
qc.sx(qr[8])


# New circuit step no: 9 


# t gate
qc.t(qr[9])


# New circuit step no: 10 


# t-dagger gate
qc.tdg(qr[10])


# New circuit step no: 11 


# rx-theta gate
qc.rx(1.57, qr[11])


# New circuit step no: 12 


# ry-theta gate
qc.ry(1.57, qr[12])


# New circuit step no: 13 


# rz-theta gate
qc.rz(1.57, qr[13])


# New circuit step no: 14 


# s gate
qc.s(qr[14])


# New circuit step no: 15 


# s-dagger gate
qc.sdg(qr[15])


# New circuit step no: 16 


# ctrl-u3 gate
qc.cu(1.57, 1.57, 1.57, 1.5707963267948966, qr[1], qr[2])


# New circuit step no: 17 


# ctrl-u2 gate
qc.cu(1.5707963267948966, 1.57, 1.57, 1.5707963267948966, qr[2], qr[3])


# New circuit step no: 18 


# ctrl-u1 gate
qc.cp(1.57, qr[3], qr[4])


# New circuit step no: 19 


# hadamard gate
qc.h(qr[5])


# New circuit step no: 20 


# ctrl-pauli-x gate
qc.cx(qr[5], qr[6])


# New circuit step no: 21 


# ctrl-pauli-y gate
qc.cy(qr[6], qr[7])


# New circuit step no: 22 


# ctrl-pauli-z gate
qc.cz(qr[7], qr[8])


# New circuit step no: 23 


# ctrl-sqrt-not gate
qc.csx(qr[8], qr[9])


# New circuit step no: 24 


# ctrl-t gate
qc.cp(0.7853981633974483, qr[9], qr[10])


# New circuit step no: 25 


# ctrl-t-dagger gate
qc.cp(-0.7853981633974483, qr[10], qr[11])


# New circuit step no: 26 


# ctrl-rx-theta gate
qc.crx(1.57, qr[11], qr[12])


# New circuit step no: 27 


# ctrl-ry-theta gate
qc.cry(1.57, qr[12], qr[13])


# New circuit step no: 28 


# ctrl-rz-theta gate
qc.crz(1.57, qr[13], qr[14])


# New circuit step no: 29 


# ctrl-s gate
qc.cp(1.5707963267948966, qr[14], qr[15])


# New circuit step no: 30 


# ctrl-s-dagger gate
qc.cp(-1.5707963267948966, qr[15], qr[16])


# New circuit step no: 31 


# swap gate
qc.swap(qr[1], qr[2])


# New circuit step no: 32 


# iswap gate
qc.iswap(qr[2], qr[3])


# New circuit step no: 33 


# sqrt-swap gate
qc.u(1.5707963267948966, 1.5707963267948966, -3.141592653589793, qr[3])
qc.u(1.5707963267948966, -1.5707963267948966, 3.141592653589793, qr[4])
qc.cx(qr[3], qr[4])
qc.u(0.7853981633974483, -1.5707963267948966, -1.5707963267948966, qr[3])
qc.u(1.5707963267948966, 0, 5.497787143782138, qr[4])
qc.cx(qr[3], qr[4])
qc.u(0.7853981633974483, -3.141592653589793, -1.5707963267948966, qr[3])
qc.u(1.5707963267948966, 3.141592653589793, 1.5707963267948966, qr[4])
qc.cx(qr[3], qr[4])
qc.u(1.5707963267948966, 0, -4.71238898038469, qr[3])
qc.u(1.5707963267948966, 1.5707963267948966, 0, qr[4])


# New circuit step no: 35 


# toffoli gate
qc.ccx(qr[4], qr[5], qr[6])


# New circuit step no: 36 


# fredkin gate
qc.cswap(qr[7], qr[8], qr[9])


# New circuit step no: 39 


# measure-z gate
qc.measure(qr[3], cr[3])

simulator = Aer.get_backend('qasm_simulator')
job = execute(qc, backend=simulator, shots=10)
job_result = job.result()
print(job_result.status)
