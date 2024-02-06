import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation



def plot_result(data:np.ndarray, data_Vx:np.ndarray, data_Vy:np.ndarray, time:int, picture:bool, showMe:bool):
    """
    Plotting of u(t,x,y) and V(t,x,y) at a specific point in time
    """

    # frequency for quivers
    m = 5
    # shapes
    size_x = data[0].shape[0]
    size_y = data[0].shape[1]

    # grid
    X = np.linspace(0,size_x,size_x)
    Y = np.linspace(0,size_y,size_y)

    # making plot
    fig, ax = plt.subplots()
    # show data
    line = plt.imshow(data[:size_x-1, :size_y-1], aspect = 'auto', cmap = 'turbo', extent = [0,size_x,size_y,0])
    plt.colorbar(line, ax=ax)
    # gradient for velocity
    ax.quiver(X[::m]+1, Y[::m]+1, data_Vx[0].T[::m, ::m], data_Vy[0].T[::m, ::m], color='red')

    ax.set_xlabel('x, m')
    ax.set_ylabel('y, m')
    ax.set_title('u(x,y) and V(x,y)')

    # show picture
    if showMe == True:
        plt.show()

    # saving picture
    if picture == True:
        plt.savefig(f"max_x={X.shape[0]}, max_y={Y.shape[0]},.png")


def anim_result(data:np.ndarray, data_Vx:np.ndarray, data_Vy:np.ndarray, picture:bool, showMe:bool):
    """
    Make animation of u(t,x,y) and V(t,x,y) and save it to gif
    """

    # animate function for animation.FuncAnimation
    def animate(i):
        # change "slice" of data cube
        line.set_array(data[i][:size_x-1, :size_y-1])
        ax.set_title(f'u(x,y,t) and V(x,y,t) at t = {i}')
        q = ax.quiver(X[::m]+1, Y[::m]+1, data_Vx[i].T[::m, ::m], data_Vy[i].T[::m, ::m], color='red')
        return line, q
    

    # frequency for quivers
    m = 5
    # shapes
    size_t = data.shape[0]
    size_x = data[0].shape[0]
    size_y = data[0].shape[1]

    # grid
    X = np.linspace(0,size_x,size_x)
    Y = np.linspace(0,size_y,size_y)
    
    # making first plot
    fig, ax = plt.subplots()
    # first slice of data
    line = plt.imshow(data[0][:size_x-1, :size_y-1], aspect = 'auto', cmap = 'turbo', extent = [0,size_x,size_y,0])
    plt.colorbar(line, ax=ax)
    plt.clim(np.min(data), np.max(data))
    # gradient for velocity
    ax.quiver(X[::m]+1, Y[::m]+1, data_Vx[0].T[::m, ::m], data_Vy[0].T[::m, ::m], color='red')

    ax.set_xlabel('x, m')
    ax.set_ylabel('y, m')
    ax.set_title('u(x,y,t) and V(x,y,t) at t = {t}'.format(t=0))

    # animate
    ani = animation.FuncAnimation(fig, animate, interval=30, blit=True, frames = size_t)

    # show first frame
    if showMe == True:
        plt.show()

    # save to .gif
    if picture == True:
        writer = animation.PillowWriter(
            fps=120, metadata=dict(artist='Doofenshmirtz Evil Incorporated'), bitrate=1800)
        ani.save(f"t={size_t}, max_x={size_x}, max_y={size_y},.gif", writer=writer)
