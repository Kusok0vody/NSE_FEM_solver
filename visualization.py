import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os.path


def plot_result(data,
                data_Vx,
                data_Vy,
                path:str=None,
                name:str=None,
                colour:str='viridis',
                grad_freq:int=5,
                save_picture:bool=False,
                showMe:bool=False):
    """
    Plotting of u(x,y) and V(x,y)
    
    Parameters
    ----------
    data : array_like
        3d array of field data.
    data_x : array_like
        3d array of x-axis values for gradient.
    data_y : array_like
        3d array of x-axis values for gradient.
    path : str, optional
        Path where you want to save gif. If path==None, saves
        to program's directory.
    name : str, optional
        Name for a picture, default name is given by shapes.
    colour: str, optional
        Colour for data field, colour by default is Viridis.
    grad_freq : int, optional
        Gradient's arrows frequency, by default equals 5.
    save_picture : bool, optional
        If True, saves picture in .png format.
    showMe : bool, optional
        If True, show the plot.
    """

    # shapes
    size_x = data[0].shape[0]
    size_y = data[0].shape[1]

    # grid
    X = np.linspace(0,size_x,size_x)
    Y = np.linspace(0,size_y,size_y)

    # making plot
    fig, ax = plt.subplots()
    # show data
    line = plt.imshow(data[:size_x-1, :size_y-1], aspect = 'auto', cmap = colour, extent = [0,size_x,size_y,0])
    plt.colorbar(line, ax=ax)
    # gradient for velocity
    ax.quiver(X[::grad_freq]+1,
              Y[::grad_freq]+1,
              data_Vx[0].T[::grad_freq, ::grad_freq],
              data_Vy[0].T[::grad_freq, ::grad_freq],
              color='red')

    ax.set_xlabel('x, m')
    ax.set_ylabel('y, m')
    ax.set_title('u(x,y) and V(x,y)')

    # show picture
    if showMe == True:
        plt.show()

    # saving picture
    if save_picture == True:
        if name == None:
            if path==None:
                if os.path.exists(f"max_x={size_x}, max_y={size_y}.png")==True:
                    k = 1
                    while os.path.exists(f", max_x={size_x}, max_y={size_y}_{k}.png")==True:
                        k += 1                    
                    plt.savefig(f"max_x={size_x}, max_y={size_y}_{k}.png")
                else:
                    plt.savefig(f"max_x={size_x}, max_y={size_y}.png")
            else:
                if os.path.exists(f"{path}/max_x={size_x}, max_y={size_y}.png")==True:
                    k = 1
                    while os.path.exists(f"{path}/max_x={size_x}, max_y={size_y}_{k}.png")==True:
                        k += 1                    
                    plt.savefig(f"{path}/max_x={size_x}, max_y={size_y}_{k}.png")
                else:
                    plt.savefig(f"{path}/max_x={size_x}, max_y={size_y}.png")
        else:
            if path==None:
                if os.path.exists(f"{name}.png")==True:
                    k = 1
                    while os.path.exists(f"{name}_{k}.png")==True:
                        k += 1                    
                    plt.savefig(f"{name}_{k}.png")
                else:
                    plt.savefig(f"{name}.png")
            else:
                if os.path.exists(f"{path}/{name}.png")==True:
                    k = 1
                    while os.path.exists(f"{path}/{name}_{k}.png")==True:
                        k += 1                    
                    plt.savefig(f"{path}/{name}_{k}.png")
                else:
                    plt.savefig(f"{path}/{name}.png")

def anim_result(data,
                data_x,
                data_y,
                path:str=None,
                name:str=None,
                colour:str='viridis',
                grad_freq:int=5,
                savetogif:bool=False,
                showMe:bool=False,
                ):
    """
    Make animation of u(t,x,y) and V(t,x,y) and, 
    if necessary, save it to gif or show it

    Parameters
    ----------
    data : array_like
        3d array of field data for every frame.
    data_x : array_like
        3d array of x-axis values for gradient for every frame.
    data_y : array_like
        3d array of x-axis values for gradient for every frame.
    path : str, optional
        Path where you want to save gif. If path==None, saves
        to program's directory.
    name : str, optional
        Name for a gif, default name is given by number of frames
        and shapes.
    colour: str, optional
        Colour for data field, colour by default is Viridis.
    grad_freq : int, optional
        Gradient's arrows frequency, by default equals 5.
    savetogif : bool, optional
        If True, saves animation in .gif format.
    showMe : bool, optional
        If True, show the first frame of animation.
    """
    # animate function for animation.FuncAnimation
    def animate(i):
        # change "slice" of data cube
        line.set_array(data[i][:size_x-1, :size_y-1])
        ax.set_title(f'u(x,y,t) and V(x,y,t) at t = {i}')
        q = ax.quiver(X[::grad_freq]+1,
                      Y[::grad_freq]+1,
                      data_x[i].T[::grad_freq, ::grad_freq],
                      data_y[i].T[::grad_freq, ::grad_freq],
                      color='red')
        return line, q
    

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
    line = plt.imshow(data[0][:size_x-1, :size_y-1], aspect = 'auto', cmap = colour, extent = [0,size_x,size_y,0])
    plt.colorbar(line, ax=ax)
    plt.clim(np.min(data), np.max(data))
    # gradient for velocity
    ax.quiver(X[::grad_freq]+1,
              Y[::grad_freq]+1,
              data_x[0].T[::grad_freq, ::grad_freq],
              data_y[0].T[::grad_freq, ::grad_freq],
              color='red')

    ax.set_xlabel('x, m')
    ax.set_ylabel('y, m')
    ax.set_title('u(x,y,t) and V(x,y,t) at t = {t}'.format(t=0))

    # animate
    ani = animation.FuncAnimation(fig, animate, interval=30, blit=True, frames = size_t)

    # show first frame
    if showMe == True:
        plt.show()

    # save to .gif with all specifies
    if savetogif == True:
        if name == None:
            if path==None:
                if os.path.exists(f"t={size_t}, max_x={size_x}, max_y={size_y}.gif")==True:
                    k = 1
                    while os.path.exists(f"t={size_t}, max_x={size_x}, max_y={size_y}_{k}.gif")==True:
                        k += 1                    
                    writer = animation.PillowWriter(
                        fps=120, metadata=dict(artist='Doofenshmirtz Evil Incorporated'), bitrate=1800)
                    ani.save(f"t={size_t}, max_x={size_x}, max_y={size_y}_{k}.gif", writer=writer)
                else:
                    writer = animation.PillowWriter(
                    fps=120, metadata=dict(artist='Doofenshmirtz Evil Incorporated'), bitrate=1800)
                    ani.save(f"t={size_t}, max_x={size_x}, max_y={size_y}.gif", writer=writer)
            else:
                if os.path.exists(f"{path}/t={size_t}, max_x={size_x}, max_y={size_y}.gif")==True:
                    k = 1
                    while os.path.exists(f"{path}/t={size_t}, max_x={size_x}, max_y={size_y}_{k}.gif")==True:
                        k += 1                    
                    writer = animation.PillowWriter(
                        fps=120, metadata=dict(artist='Doofenshmirtz Evil Incorporated'), bitrate=1800)
                    ani.save(f"{path}/t={size_t}, max_x={size_x}, max_y={size_y}_{k}.gif", writer=writer)
                else:
                    writer = animation.PillowWriter(
                    fps=120, metadata=dict(artist='Doofenshmirtz Evil Incorporated'), bitrate=1800)
                    ani.save(f"{path}/t={size_t}, max_x={size_x}, max_y={size_y}.gif", writer=writer)
        else:
            if path==None:
                if os.path.exists(f"{name}.gif")==True:
                    k = 1
                    while os.path.exists(f"{name}_{k}.gif")==True:
                        k += 1                    
                    writer = animation.PillowWriter(
                        fps=120, metadata=dict(artist='Doofenshmirtz Evil Incorporated'), bitrate=1800)
                    ani.save(f"{name}_{k}.gif", writer=writer)
                else:
                    writer = animation.PillowWriter(
                    fps=120, metadata=dict(artist='Doofenshmirtz Evil Incorporated'), bitrate=1800)
                    ani.save(f"{name}.gif", writer=writer)
            else:
                if os.path.exists(f"{path}/{name}.gif")==True:
                    k = 1
                    while os.path.exists(f"{path}/{name}_{k}.gif")==True:
                        k += 1                    
                    writer = animation.PillowWriter(
                        fps=120, metadata=dict(artist='Doofenshmirtz Evil Incorporated'), bitrate=1800)
                    ani.save(f"{path}/{name}_{k}.gif", writer=writer)
                else:
                    writer = animation.PillowWriter(
                    fps=120, metadata=dict(artist='Doofenshmirtz Evil Incorporated'), bitrate=1800)
                    ani.save(f"{path}/{name}.gif", writer=writer)
