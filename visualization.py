import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# The whole program will be just functions later

# Importing data
# u_path = input("path to file with  data: ")
# data_u = np.load(u_path)

# Vx_path = input("path to file with velocity data: ")
# data_Vx = np.load(Vx_path)

# Vy_path = input("path to file with velocity data: ")
# data_Vy = np.load(Vy_path)

# Random values (temporally)
data_u = []
data_Vx = []
data_Vy = []

for t in range(0,120,1):
    # u = [[np.sin(i/5) for j in range(0,100)] for k in range(0,100)]
    u = np.random.uniform(-10,10,(100,100))
    vx = np.cos(t/10)*np.ones((100,100))
    vy = np.sin(t/10)*np.ones((100,100))
    data_u.append(u)
    data_Vx.append(vx)
    data_Vy.append(vy)

data_u = np.array(data_u)
data_Vx = np.array(data_Vx)
data_Vy = np.array(data_Vy)

def plot_result(data_u:np.ndarray, data_Vx:np.ndarray, data_Vy:np.ndarray, time:int, picture:bool, showMe:bool):
    """
    Plotting of u(t,x,y) and V(t,x,y) at a specific point in time
    """

    X = np.linspace(0,data_u[0].shape[0],data_u[0].shape[0])                                            # our grid
    Y = np.linspace(0,data_u[0].shape[1],data_u[0].shape[1])
    
    fig, ax = plt.subplots()
    line = plt.imshow(data_u[time], aspect = 'auto', cmap = 'Greys_r', extent = [0,100,0,100])          # u slice
    plt.colorbar(line, ax=ax)                                                                   
    q = ax.quiver(X[::10], Y[::10], data_Vx[time][::10, ::10], data_Vy[time][::10, ::10], color='red')  # gradient for V

    ax.set_xlabel('x, m')
    ax.set_ylabel('y, m')
    ax.set_title('u(x,y,t) and V(x,y,t) at t = {t}'.format(t=0))

    if showMe == True:
        plt.show()

    if picture == True:
        plt.savefig(f"t={data_u.shape[0]}, max_x={X.shape[0]}, max_y={Y.shape[0]},.png")                # saving picture




def anim_result(data_u:np.ndarray, data_Vx:np.ndarray, data_Vy:np.ndarray, picture:bool, showMe:bool):
    """
    Make animation of u(t,x,y) and V(t,x,y) and save it to gif
    """


    def animate(i):                                                                                     # animate function for animation.FuncAnimation
        line.set_array(data_u[i])                                                                       # change "slice" of u cube
        ax.set_title(f'u(x,y,t) and V(x,y,t) at t = {i}')                                               # also change quiver
        q.set_UVC(data_Vx[i][::10, ::10], data_Vy[i][::10, ::10])       
        return line, q
    

    X = np.linspace(0,data_u[0].shape[0],data_u[0].shape[0])                                            # our grid
    Y = np.linspace(0,data_u[0].shape[1],data_u[0].shape[1])
    
    fig, ax = plt.subplots()
    line = plt.imshow(data_u[0], aspect = 'auto', cmap = 'Greys_r', extent = [0,100,0,100])             # u slice
    plt.colorbar(line, ax=ax)                                                                   
    q = ax.quiver(X[::10], Y[::10], data_Vx[0][::10, ::10], data_Vy[0][::10, ::10], color='red')        # gradient for V

    ax.set_xlabel('x, m')
    ax.set_ylabel('y, m')
    ax.set_title('u(x,y,t) and V(x,y,t) at t = {t}'.format(t=0))

    ani = animation.FuncAnimation(                                                                      # animate
    fig, animate, interval=60, blit=True, frames = data_u.shape[0])

    if showMe == True:
        plt.show()

    if picture == True:
        writer = animation.PillowWriter(                                                                # saving picture
            fps=30, metadata=dict(artist='Doofenshmirtz Evil Incorporated'), bitrate=1800)
        ani.save(f"t={data_u.shape[0]}, max_x={X.shape[0]}, max_y={Y.shape[0]},.gif", writer=writer)


# plot_result(data_u, data_Vx, data_Vy, time = 60, picture=True, showMe=True)

anim_result(data_u, data_Vx, data_Vy, picture=True, showMe=True)
