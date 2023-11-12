import numpy as np
import matplotlib.pyplot as plt
import ipywidgets as ipw

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

for i in range(0,120,1):
    u = np.random.uniform(-10,10,(1000,1000))
    vx = np.random.uniform(-200,200,(1000,1000))
    vy = np.random.uniform(-200,200,(1000,1000))
    data_u.append(u)
    data_Vx.append(vx)
    data_Vy.append(vy)

data_u = np.array(data_u)
data_Vx = np.array(data_Vx)
data_Vy = np.array(data_Vy)

def plot_result(ind:int, savepic:bool):
    """
    Plotting of u(t,x,y) and V(t,x,y) at specific time value
    """
    X = np.linspace(0,data_u[T-1].shape[0],data_u[T-1].shape[0])
    Y = np.linspace(0,data_u[T-1].shape[1],data_u[T-1].shape[1])
    fig, ax = plt.subplots()
    plt.imshow(data_u[:,:,ind], aspect = 'auto', cmap = 'Greys', extent = [0,1000,0,1000])
    plt.xlabel('x, m')
    plt.ylabel('y, m')
    plt.title('u(x,y,t) and V(x,y,t) at t = {time_slider}'.format(time_slider=time_slider.value))
    plt.colorbar()
    q = ax.quiver(X[::100], Y[::100], data_Vx[T-1][::100, ::100], data_Vy[T-1][::100, ::100], color='red')
    if savepic==True:
        plt.savefig('u_V_result_t={name}.png'.format(name=ind))
    plt.show()

T = data_u.shape[0]
time_slider = ipw.IntSlider(value=0, min=0, max=T, step=1, description='time')
savepic = ipw.ToggleButton(description='save picture')
ipw.interact(plot_result, ind=time_slider, savepic=savepic)