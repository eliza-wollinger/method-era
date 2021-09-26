import numpy as np
import matplotlib.pyplot as plt

np.set_printoptions(precision=7, suppress=True)

data = json.load(open('data.json'))

m = data['m']
k = data['k']
c = data['c']


m_matrix = np.diag(m)
k_matrix = np.array([[k[0]+k[1],   -k[1]  ,     0    ,     0    ,   0  ],
                     [  -k[1]  , k[1]+k[2],   -k[2]  ,     0    ,   0  ],
                     [    0    ,   -k[2]  , k[2]+k[3],   -k[3]  ,   0  ],
                     [    0    ,     0    ,   -k[3]  , k[3]+k[4], -k[4]],
                     [    0    ,     0    ,     0    ,   -k[4]  ,  k[4]]
                     ])
c_matrix = np.array([[c[0]+c[1],   -c[1]  ,     0    ,     0    ,   0  ],
                     [  -c[1]  , c[1]+c[2],   -c[2]  ,     0    ,   0  ],
                     [    0    ,   -c[2]  , c[2]+c[3],   -c[3]  ,   0  ],
                     [    0    ,     0    ,   -c[3]  , c[3]+c[4], -c[4]],
                     [    0    ,     0    ,     0    ,   -c[4]  ,  c[4]]
                     ])

zero_matrix         = np.zeros((5, 5))
identify_matrix     = np.eye(5)
inverse_m_matrix    = np.linalg.inv(m_matrix)

A = np.block([
             [       zero_matrix        ,       identify_matrix     ],
             [-inverse_m_matrix@k_matrix, -inverse_m_matrix@c_matrix]
             ])

eigvals, eigvecs  = np.linalg.eig(A)
eigval             = eigvals[10:0:-2].T
eigvec                = eigvecs[0:5, 10:0:-2].T


fnhertz = np.abs(eigval) / (2*np.pi)
sort    = np.argsort(fnhertz)

eigvecs_imag_norm = np.array([eigvec.T.imag[i] / eigvec.T.imag[i,0] for i in range(5)])
eigvecs_real_norm = np.array([eigvec.T.real[i] / eigvec.T.real[i,0] for i in range(5)])

mode_shape_imag = np.block([np.zeros((5,1)), eigvecs_imag_norm])
mode_shape_real = np.block([np.zeros((5,1)), eigvecs_real_norm])

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

size = 5

def get_residues():
  residue_array = []
  for i in range(size):
    residue = []
    for j in range(size):
      residue.append(np.array(eigvec.T[i][j] * eigvec.T[0][j]))
    residue_array.append(residue)
  return residue_array


# IRF Simulation

points = 10

delta_time = 1/40

def get_time():
  time = []

  for i in range(points):
    time.append(i*delta_time)

  return time

def get_natural_frequency():
  time = get_time()
  residues = get_residues()

  fris = np.zeros((size, points))
  for i in range(size):
    for j in range(points):
      for k in range(size):
        fris[i][j] = fris[i][j] + 2*np.real(np.array(residues[i][k])*np.exp(eigvec[i][k]*time[j]))
  return fris

