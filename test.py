import numpy as np
from visualization import anim_result
from NSE_finite_difference import NSE_scheme

dx = 0.5
dy = 0.5
dt = 0.01

n = 50
frames_num = 120

p_ = np.ones((n, n))
u_ = np.zeros((n, n))
v_ = np.zeros((n, n))
F_x = np.ones((frames_num, n, n))
F_y = np.zeros((frames_num, n, n))

eta = 8.9*1e-4
rho = 1

p, u, v = NSE_scheme(p_, u_, v_, F_x, F_y, eta, rho, frames_num)

anim_result(p, u, v, path = 'gifs', name='test', colour='winter', savetogif=True, showMe=True)