import numpy as np
import matplotlib.pyplot as plt
import json

data = json.load(open('data.json'))

mass_data = data['mass']
damp_data = data['damp']
hard_data = data['hard']

mass_matrix = np.array([
                        [mass_data[0],     0       ,     0       ,     0       ,     0       ],
                        [    0       , mass_data[1],     0       ,     0       ,     0       ],
                        [    0       ,     0       , mass_data[2],     0       ,     0       ],
                        [    0       ,     0       ,     0       , mass_data[3],     0       ],
                        [    0       ,     0       ,     0       ,     0       , mass_data[4]]
                        ])

damp_matrix = np.array([
                        [damp_data[0]+damp_data[1],        -damp_data[1]     ,             0            ,             0            ,      0       ],
                        [       -damp_data[1]     , damp_data[1]+damp_data[2],        -damp_data[2]     ,             0            ,      0       ],
                        [            0            ,        -damp_data[2]     , damp_data[2]+damp_data[3],        -damp_data[3]     ,      0       ],
                        [            0            ,             0            ,        -damp_data[3]     , damp_data[3]+damp_data[4], -damp_data[4]],
                        [            0            ,             0            ,             0            ,        -damp_data[4]     ,  damp_data[4]]
                        ])

hard_matrix = np.array([
                        [hard_data[0]+hard_data[1],        -hard_data[1]     ,             0            ,             0            ,      0       ],
                        [       -hard_data[1]     , hard_data[1]+hard_data[2],        -hard_data[2]     ,             0            ,      0       ],
                        [            0            ,        -hard_data[2]     , hard_data[2]+hard_data[3],        -hard_data[3]     ,      0       ],
                        [            0            ,             0            ,        -hard_data[3]     , hard_data[3]+hard_data[4], -hard_data[4]],
                        [            0            ,             0            ,             0            ,        -hard_data[4]     ,  hard_data[4]]
                        ])

zero_matrix         = np.zeros((5, 5))
identify_matrix     = np.eye(5)
inverse_mass_matrix = np.linalg.inv(mass_matrix)

A = np.block([[       zero_matrix              ,          identify_matrix        ],
              [-inverse_mass_matrix@damp_matrix, -inverse_mass_matrix@hard_matrix]
              ])

eigvals, eigvecs  = np.linalg.eig(A)
eigvalscut        = eigvals[10:0:-2].T
imaginary_eigvecs = eigvecs[0:5, 10:0:-2].T

eigvalscut_square   = np.abs(eigvalscut) / (2*np.pi)
sort  = np.argsort(eigvalscut_square)

eigvecs_norm = np.array([imaginary_eigvecs.imag[i] / imaginary_eigvecs.imag[i,0] for i in range(5)])

np.set_printoptions(precision = 4, suppress = True)

modal_exact = np.block([np.zeros((5,1)), eigvecs_norm, np.zeros((5,1))])
modal      = [[
             plt.subplot(511+i), plt.axhline(color='darkgray'),\
             plt.title("Modal Forms's Imaginary Parts") if i == 0 else
             None, \
             plt.plot(modal_exact[sort[i]], color='red')] for i in
             range(5)
             ]

plt.show()

#wn_ST = np.abs(eigvalscut)
#qsi   = -np.real(eigvalscut) / np.abs(eigvalscut)

#print("Mass Matrix = \n", mass_matrix)
#print("\n Damping Matrix = \n", damp_matrix)
#print("\n Hardness Matrix = \n", hard_matrix)
#print("\n A_bar = \n", A)
#print("\n eigenvalues = \n", eigvals)
#print("\n eigenvectors = \n", eigvecs)