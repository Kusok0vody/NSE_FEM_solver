import numpy as np
from visualization import anim_result, plot_result
from NSE_finite_difference import NSE_scheme

# grid and time step
dx = 0.1
dy = 0.1
dt = 0.01

# size of grid and number of frames (t=dt*frames_num)
n = 50
frames_num = 150

#Initial condition
p_ = 10*np.ones((n, n))
u_ = 0.01*np.ones((n, n))
v_ = np.zeros((n, n))
F_x = np.zeros((frames_num, n, n))
F_y = np.zeros((frames_num, n, n))

# A force that acts half the time
# F_x[0:int(frames_num/2),:,:] -= 0.01

# Pressure to make pipe (you need to change BC in the calculation program)
# for i in range(n):
#     p_[:,i] -= 0.1*i

# A square in the center 
p_[int(n/4):int(3*n/4),int(n/4):int(3*n/4)] += 190

# mayonnaise environment
eta = 63
rho = 941.8

# calculating
p, u, v = NSE_scheme(p_, u_, v_, F_x, F_y, eta, rho, frames_num, dx=dx, dy=dy, dt=dt)

# plot to see IC
plot_result(p[0], u[0], v[0], [dx, dy], path = 'pictures', name='test', grad_freq=2, title='IC', colour='turbo', save_picture=False, showMe=True)

# plot to see last frame
plot_result(p[-1], u[-1], v[-1], [dx, dy], path = 'pictures', name='test', grad_freq=2, title=f't = {frames_num*dt}', colour='turbo', save_picture=False, showMe=True)

anim_result(p, u, v, [dt, dx, dy], path = 'gifs', name='test', title='p', colour='turbo', grad_freq=2, savetogif=False, showMe=True)
anim_result(u, u, v, [dt, dx, dy], path = 'gifs', name='test', title='u', colour='turbo', grad_freq=2, savetogif=False, showMe=True)
anim_result(v, u, v, [dt, dx, dy], path = 'gifs', name='test', title='v', colour='turbo', grad_freq=2, savetogif=False, showMe=True)

# Check div(u)=0 (optional)

# div = np.zeros((frames_num,n,n))
# for k in range(frames_num):
#     for i in range(1,n-1):
#         for j in range(1,n-1):
#             div[k][i][j] = (u[k][i][j+1]-u[k][i][j] + v[k][i+1][j]-u[k][i][j])/dx
# anim_result(div, u, v, path = 'gifs', name='test', title='div', grad_freq=2, savetogif=False, showMe=True)
