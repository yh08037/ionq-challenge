from telnetlib import SGA
import numpy as np

def check_shape(array: np.ndarray) -> bool:
  n = array.shape[0]
  flag = (
    (array.ndim == 2)
    and (n == array.shape[1])
    and ((n & (n-1) == 0) and n != 0)
  )
  return flag

def flip_msb(array: np.ndarray) -> np.ndarray:
  assert check_shape(array)
  n = array.shape[0]
  idx = [int(format(i, '0%db' % int(np.sqrt(n)))[::-1], 2)
         for i in range(n)]
  x, y = np.meshgrid(idx, idx)
  return array[x, y]


def make_conditional(array: np.ndarray) -> np.ndarray:
  assert check_shape(array)
  n = array.shape[0]
  conditoned = np.block([[np.eye(n), np.zeros((n, n))],
                         [np.zeros((n, n)), array]])
  return conditoned

def get_qft_array(n: int):
  N = 2 ** n
  qft = np.ones((N, N), dtype=complex)
  for i in range(1, N):
    for j in range(1, N):
      qft[i, j] = np.exp(2j * np.pi * i * j / N)
  return qft


class QPE:
  def __init__(self, unitary, precision):
    self.unitary = unitary
    self.precision = precision  


def get_unitary_power_list(array: np.ndarray, n: int) -> list[np.ndarray]:
  assert check_shape(array)
  power_array = array
  array_list = [array]
  for _ in range(1, n):
    power_array = power_array @ array 
    array_list.append(power_array)
  return array_list



if __name__ == '__main__':
  import matplotlib.pyplot as plt
  from qiskit import QuantumCircuit, QuantumRegister
  from qiskit.extensions import UnitaryGate
  from qiskit.circuit.library import SGate, QFT
  from qiskit.quantum_info import Statevector
  
  precision = 3

  arr = SGate().to_matrix()

  arr_list = get_unitary_power_list(arr, precision)

  gate_list = [
    UnitaryGate(m, label=f'U^{2**i}').control() 
    for i, m in enumerate(arr_list)
  ]
  
  iqft_circuit = QFT(precision, inverse=True)

  ancilla = QuantumRegister(precision, 'q')
  eigen = QuantumRegister(1, 'v')

  circuit = QuantumCircuit(ancilla, eigen)
  circuit.x(precision + 0)
  circuit.barrier()
  circuit.h(range(precision))
  circuit.barrier()
  for i, gate in enumerate(gate_list):
    circuit.append(gate, [i, 3])
  circuit.barrier()
  circuit.compose(iqft_circuit, range(precision), inplace=True)
  circuit.barrier()
  
  print(Statevector(circuit).probabilities())

  circuit.draw('mpl')
  plt.show()


  
