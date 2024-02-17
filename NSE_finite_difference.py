import numpy as np

def NSE_scheme(p_initial,
               u_initial,
               v_initial,
               Force_x,
               Force_y,
               kinematic_viscosity:float,
               density:float,
               frames_num:int,
               dx:int,
               dy:int,
               dt:int,
               ):
    """
    Solver for NSE by finite difference method.

    Parameters
    ----------
    p_initial : array-like
        2d array of initial values of pressure.
    u_initial : array-like
        2d array of initial x-axis values of velocity.
    v_initial : array-like
        2d array of initial y-axis values of velocity.
    Force_x : array-like
        3d array of x-axis values of force for every frame.
    Force_y : array-like
        3d array of y-axis values of force for every frame.
    kinematic_viscosity : float
        A value of kinematic_viscosity.
    density : float
        A value of density.
    frames_num : int
        A number of frames.
    
    Returns
    -------
    p : ndarray
        A 3d array of pressure for every frame.
    u : ndarray
        A 3d array of x-axis velocity for every frame.
    v : ndarray
        A 3d array of y-axis velocity for every frame.
    """
    # shapes
    size_x = p_initial.shape[0]
    size_y = p_initial.shape[1]

    # kinematic viscosity
    nu = kinematic_viscosity/density

    # making arrays for every time step
    p = np.zeros((frames_num, size_x, size_y))
    p[0] += p_initial
    u = np.zeros((frames_num, size_x, size_y))
    u[0] += u_initial
    v = np.zeros((frames_num, size_x, size_y))
    v[0] += v_initial
    
    # main loop
    for k in range(0, frames_num-1):

                # Dirichlet BC
        u[:,0,:] = u[:,1,:]
        u[:,-1,:] = u[:,-2,:]
        u[:,:,0] = u[:,:,1]
        u[:,:,-1] = u[:,:,-2]

        v[:,0,:] = v[:,1,:]
        v[:,-1,:] = v[:,-2,:]
        v[:,:,0] = v[:,:,1]
        v[:,:,-1] = v[:,:,-2]

        # Dirichlet BC for pressure: equals IC
        p[:,0,:] = p_initial[0,:]
        p[:,-1,:] = p_initial[-1,:]
        p[:,:,0] = p_initial[:,0]
        p[:,:,-1] = p_initial[:,-1]

        # Neumann BC
        # p[:,0,:] = p[:,1,:]
        # p[:,-1,:] = p[:,-2,:]
        # p[:,:,0] = p[:,:,1]
        # p[:,:,-1] = p[:,:,-2]
        
        # first step: making u and v without pressure
        tilda_u = np.zeros((size_x, size_y))
        for i in range(1, size_x-1):
            for j in range(1, size_y-1):
                laplace_u = (u[k][i][j+1] - 2*u[k][i][j] + u[k][i][j-1]) / dx**2 + (u[k][i+1][j] - 2*u[k][i][j] + u[k][i-1][j]) / dy**2
                nabla_u = (2 * u[k][i][j] * (u[k][i][j+1] - u[k][i][j]) / dx 
                + v[k][i][j] * (u[k][i+1][j] - u[k][i][j]) / dy 
                + u[k][i][j] * (v[k][i+1][j] - v[k][i][j]) / dy)
                tilda_u[i][j] = u[k][i][j] + dt * (Force_x[k][i][j] + nu*laplace_u - nabla_u)

        tilda_v = np.zeros((size_x, size_y))
        for i in range(1, size_x-1):
            for j in range(1, size_y-1):
                laplace_v = (v[k][i][j+1] - 2*v[k][i][j] + v[k][i][j-1]) / dx**2 + (v[k][i+1][j] - 2*v[k][i][j] + v[k][i-1][j]) / dy**2
                nabla_v = (2 * v[k][i][j] * (v[k][i+1][j] - v[k][i][j]) / dy 
                + v[k][i][j] * (u[k][i][j+1] - u[k][i][j]) / dx 
                + u[k][i][j] * (v[k][i][j+1] - v[k][i][j]) / dx)
                tilda_v[i][j] = v[k][i][j] + dt * (Force_y[k][i][j] + nu*laplace_v - nabla_v)

        # second step: calculating p (uses heat equation instead of Poisson assuming that pressure doesn't change)
        for i in range(1, size_x-1):
            for j in range(1, size_y-1):
                laplace_p = (p[k][i][j+1] - 2*p[k][i][j] + p[k][i][j-1]) / dx**2 + (p[k][i+1][j] - 2*p[k][i][j] + p[k][i-1][j]) / dy**2
                divergence = (tilda_u[i][j+1] - tilda_u[i][j]) / dx + (tilda_v[i+1][j] - tilda_v[i][j]) / dy
                p[k+1][i][j] = dt / density * laplace_p - divergence + p[k][i][j]

        # third step: calculating true velocities with right pressure
        for i in range(1, size_x-1):
            for j in range(1, size_y-1):
                u[k+1][i][j] = np.round(tilda_u[i][j] - dt * ((p[k+1][i][j+1] - p[k+1][i][j]) / dx) / density,5)
                v[k+1][i][j] = np.round(tilda_v[i][j] - dt * ((p[k+1][i+1][j] - p[k+1][i][j]) / dy) / density,5)
        
    return p, u, v

