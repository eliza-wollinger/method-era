import numpy as np
import matplotlib.pyplot as plt
import json

data = json.load(open('data.json'))

mass_data = data['mass']
damp_data = data['damp']
stif_data = data['stif']

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

stif_matrix = np.array([
                        [stif_data[0]+stif_data[1],        -stif_data[1]     ,             0            ,             0            ,      0       ],
                        [       -stif_data[1]     , stif_data[1]+stif_data[2],        -stif_data[2]     ,             0            ,      0       ],
                        [            0            ,        -stif_data[2]     , stif_data[2]+stif_data[3],        -stif_data[3]     ,      0       ],
                        [            0            ,             0            ,        -stif_data[3]     , stif_data[3]+stif_data[4], -stif_data[4]],
                        [            0            ,             0            ,             0            ,        -stif_data[4]     ,  stif_data[4]]
                        ])

zero_matrix         = np.zeros((5, 5))
identify_matrix     = np.eye(5)
inverse_mass_matrix = np.linalg.inv(mass_matrix)

A = np.block([
              [       zero_matrix              ,          identify_matrix        ],
              [-inverse_mass_matrix@stif_matrix, -inverse_mass_matrix@damp_matrix]
              ])

eigvals, eigvecs  = np.linalg.eig(A)
negative_eigvals  = eigvals[10:0:-2].T
eigvectors        = eigvecs[0:5, 10:0:-2].T

eigvalscut_square = np.abs(negative_eigvals) / (2*np.pi)
sort              = np.argsort(eigvalscut_square)

eigvecs_imag_norm = np.array([eigvectors.imag[i] / eigvectors.imag[i,0] for i in range(5)])
eigvecs_real_norm = np.array([eigvectors.real[i] / eigvectors.real[i,0] for i in range(5)])

mode_shape_imag = np.block([np.zeros((5,1)), eigvecs_imag_norm])
mode_shape_real = np.block([np.zeros((5,1)), eigvecs_real_norm])

np.set_printoptions(precision = 4, suppress = True)

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

# IRF Simulation

noise_amplitude = float(input("Noise amplitude = "))
delta_t         = 0.04
Npt             = 10
t               = np.array(np.arange(0, Npt, 1)*delta_t)


r               = np.array([
                            eigvectors[i, j] * eigvectors[i, 0]
                            for i in range(5)
                            for j in range(5)
                            ])

#h               = np.array([
#                            2*np.real(r[j]@np.exp(eigvectors*t[i])) + np.random.uniform(-noise_amplitude, noise_amplitude)
#                            for i in range(Npt)
#                            for j in range(5)
#                            ])


#print("Mass Matrix = \n", mass_matrix)
#print("\n Damping Matrix = \n", damp_matrix)
#print("\n Stiffness Matrix = \n", stif_matrix)
#print("\n Matrix A = \n", A)
#print("\n eigenvalues = \n", eigvals)
#print("\n eigenvectors = \n", eigvecs)
print("\n r = \n", r)
#print("\n negative aigenvalues = \n", negative_eigvals)

#wn_ST = np.abs(eigvalscut)
#qsi   = -np.real(negative_eigvals) / np.abs(negative_eigvals)