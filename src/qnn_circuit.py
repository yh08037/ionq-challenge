import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit import ParameterVector
from qiskit.quantum_info import Statevector

class QnnCircuit:
  def __init__(self, n_qubits: int, n_layers: int) -> None:
    self.n_qubits = n_qubits
    self.n_layers = n_layers
    self._x = ParameterVector("x", n_qubits)
    self._w = ParameterVector("w", n_layers * n_qubits * 3)
    self._embed_layer = None
    self._pqc_layer = None
    self._binded_pqc_layer = None
    self._create_embed_layer()
    self._create_pqc_layer()
    self._initialize_weights()

  def get_circuit(self) -> None:
    assert self._embed_layer is not None
    assert self._pqc_layer is not None
    return self._embed_layer.compose(self._pqc_layer)
  
  def _initialize_weights(self) -> None:
    weight = np.random.random(size=(self.n_layers, self.n_qubits, 3))
    self.set_weights(weight)

  def set_weights(self, w: np.ndarray) -> None:
    assert w.shape == (self.n_layers, self.n_qubits, 3)
    self._binded_pqc_layer = self._pqc_layer.bind_parameters(w.flatten())

  def run(self, x: np.ndarray) -> np.ndarray:
    assert x.size == self.n_qubits
    assert self._binded_pqc_layer is not None
    binded_embed_layer = self._embed_layer.bind_parameters(x.flatten())
    circuit = binded_embed_layer.compose(self._binded_pqc_layer)
    return Statevector(circuit).probabilities()

  def _create_embed_layer(self) -> None:
    self._embed_layer = QuantumCircuit(self.n_qubits)
    for i, theta in enumerate(self._x):
      self._embed_layer.ry(theta, i)
    self._embed_layer.barrier()
    
  def _create_pqc_layer(self) -> None:
    self._pqc_layer = QuantumCircuit(self.n_qubits)
    for layer in range(self.n_layers):
      for qubit in range(self.n_qubits):
        idx = (layer * self.n_qubits + qubit) * 3
        self._pqc_layer.u(*self._w[idx:idx+3], qubit)
      for qubit in range(self.n_qubits - 1):
        self._pqc_layer.cz(qubit, qubit + 1)
      self._pqc_layer.barrier()

if __name__ == '__main__':
  qc = QnnCircuit(4, 3)

  temp = np.array([[1, 2, 3], [3, 2, 1], [5, 4, 6], [2, 6, 4]])
  model_param = np.array([temp, temp, temp])
  qc.set_weights(model_param)
  
  input_vector = np.array([1, 2, 3, 4])
  out = qc.run(input_vector)

  print(out)
