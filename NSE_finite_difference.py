import numpy as np

def NSE_scheme(p_IC:np.ndarray,
               Fx:np.ndarray,
               Fy:np.ndarray,
               u_IC:np.ndarray,
               v_IC:np.ndarray,
               eta:float,
               rho:float,
               frames_num:int,
               ):
    """
    solver for NSE by finite difference method
    """

    #shapes
    size_x = p_IC.shape[0]
    size_y = p_IC.shape[1]

    # grid step
    dx = 0.5
    dy = 0.5
    # time step
    dt = 0.01

    #kinematic viscosity
    nu = eta/rho

    #making arrays for every time step
    p = np.zeros((frames_num, size_x, size_y))
    p[0] += p_IC
    u = np.zeros((frames_num, size_x, size_y))
    u[0] += u_IC
    v = np.zeros((frames_num, size_x, size_y))
    v[0] += v_IC

    # main loop
    for k in range(0, frames_num-1):

        # first step: making Vx and Vy without p
        tilda_u = np.zeros((size_x, size_y))
        for i in range(0, size_x-1):
            for j in range(0, size_y-1):
                laplace_u = (u[k][i+1][j] - 2*u[k][i][j] + u[k][i-1][j]) / dx**2 + (u[k][i][j+1] - 2*u[k][i][j] + u[k][i][j-1]) / dy**2
                nabla_u = u[k][i][j] * (u[k][i+1][j] - u[k][i][j]) / dx
                tilda_u[i][j] = u[k][i][j] + dt * (Fx[k][i][j] + nu*laplace_u - nabla_u)

        tilda_v = np.zeros((size_x, size_y))
        for i in range(0, size_x-1):
            for j in range(0, size_y-1):
                laplace_v = (v[k][i+1][j] - 2*v[k][i][j] + v[k][i-1][j]) / dx**2 + (v[k][i][j+1] - 2*v[k][i][j] + v[k][i][j-1]) / dy**2
                nabla_v = v[k][i][j] * (v[k][i][j+1] - v[k][i][j]) / dy
                # 0 with nabla because nabla_v broke stability (why? I don't know...)
                tilda_v[i][j] = v[k][i][j] + dt * (Fy[k][i][j] + nu*laplace_v - 0*nabla_v)

        # second step: calculating p (we should have div(p)=0)
        for i in range(0, size_x-1):
            for j in range(0, size_y-1):
                laplace_p = (p[k][i+1][j] - 2*p[k][i][j] + p[k][i-1][j]) * dx**3 + (p[k][i][j-1] - 2*p[k][i][j] + p[k][i][j-1]) * dy**3
                divergence = rho * (dx * dy**2 * (tilda_u[i+1][j] - tilda_u[i][j]) + dx**2 * dy * (tilda_v[i][j+1] - tilda_v[i][j])) / dt    
                p[k][i][j] = laplace_p - divergence + p[k][i][j]

        # third step: calculating true velocities with right pressure
        for i in range(0, size_x-1):
            for j in range(0, size_y-1):
                u[k+1][i][j] = tilda_u[i][j] - dt * ((p[k][i][j] - p[k][i-1][j]) / dx) / rho
                v[k+1][i][j] = tilda_v[i][j] - dt * ((p[k][i][j] - p[k][i-1][j]) / dy) / rho
        
    return p, u, v