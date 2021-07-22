import numpy as np
import matplotlib.pyplot as plt
import json
from math import e

data = json.load(open('data.json'))

m = data['m']
k = data['k']
c = data['c']


def create_matrix(arr):
  size = len(arr)
  lines = []
  for line in range(size):
    columns = []
    for column in range (size):
      current_num = arr[column]
      if line == column:
        if line == 0:
          columns.append(current_num + arr[line+1])
        else:
          columns.append(current_num + arr[line-1])
      elif column == line + 1:
        columns.append(-current_num)
      elif column == line - 1:
        columns.append(-arr[line - 1])
      else:
        columns.append(0)
    lines.append(columns)
  return lines


m_matrix = np.diag(m)
k_matrix = np.array(create_matrix(k))
c_matrix = np.array(create_matrix(c))

zero_matrix         = np.zeros((5, 5))
identify_matrix     = np.eye(5)
inverse_m_matrix    = np.linalg.inv(m_matrix)

A = np.block([
             [       zero_matrix        ,       identify_matrix     ],
             [-inverse_m_matrix@k_matrix, -inverse_m_matrix@c_matrix]
             ])

eigvals, eigvecs  = np.linalg.eig(A)
lambd             = eigvals[10:0:-2]
fi                = eigvecs[0:5, 10:0:-2]

# To make the comparison with the MATLAB program will be using the column view 
# in fi and lambd, but for all accounts, consider the transposed matrix.

fnhertz = np.abs(lambd) / (2*np.pi)
sort    = np.argsort(fnhertz)

eigvecs_imag_norm = np.array([fi.T.imag[i] / fi.T.imag[i,0] for i in range(5)])
eigvecs_real_norm = np.array([fi.T.real[i] / fi.T.real[i,0] for i in range(5)])

mode_shape_imag = np.block([np.zeros((5,1)), eigvecs_imag_norm])
mode_shape_real = np.block([np.zeros((5,1)), eigvecs_real_norm])

np.set_printoptions(precision=4, suppress=True)

mode_shape_imag_plot = [[
                        plt.subplot(511+i), plt.axhline(color = 'darkgray'),\
                        plt.title("Imaginary Parts of Modal Forms") 
                        if i == 0 else None, \
                        plt.plot(mode_shape_imag[sort[i]], color = 'darkorange')]
                        for i in range(5)
                        ]
plt.show()

mode_shape_real_plot = [[
                        plt.subplot(511+i), plt.axhline(color = 'darkgray'), \
                        plt.title("Real Parts of Modal Forms")
                        if i == 0 else None, \
                        plt.plot(mode_shape_real[sort[i]], color = 'darkorange')]
                        for i in range(5)
                        ]
plt.show()

# Residue Calculation

frequency_size = 5

def get_residues():
  residue_array = []
  for i in range(frequency_size):
    residue = []
    for j in range(frequency_size):
      residue.append(np.array(fi[i,j] * fi[0,j]))
    residue_array.append(residue)
  return residue_array


# IRF Simulation

time = 500

def get_natural_frequency():
  residues = get_residues()
  impulse_array = []
  for i in range(time):
    for j in range(frequency_size):
      impulse_array.append(np.array([[2]*np.array(residues[j]) * e**(lambd * i)]))
    return impulse_array

natural_frequencies = get_natural_frequency()
print(natural_frequencies)
