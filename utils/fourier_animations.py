import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation


def square_signal_decomposition(nb_iterations):
    # First set up the figure, the axis, and the plot element we want to animate
    # create a figure with two subplots
    fig, (ax1, ax2) = plt.subplots(1, 2)
    fig.tight_layout(pad=3.0)
    ax2.set_title("Resulting signal")
    fig.dpi = 150

    t_max = 4*np.pi
    line = ax2.plot([], [], lw=2, color='r')
    for ax in [ax1, ax2]:
        ax.set_ylim(-1.5, 1.5)
        ax.set_xlim(0, t_max)
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Amplitude (a.u.)")

    # Animation function.  This is called sequentially
    def animate(i):
        x = np.linspace(0, t_max, 500)
        y = np.zeros(len(x))
        for n in range(1, 2*i+2, 2):
            y = np.vstack((y, 4*np.sin(n * x)/(np.pi*n)))
        ax1.set_title(f"{i+1} summed sinusoids")
        ax1.plot(x.T, y[1:].T, lw=1)
        ax1.set_prop_cycle(None)
        line[0].set_data(x, y[1:].sum(0))
        return line

    # create the animation
    anim_square_signal = animation.FuncAnimation(fig, animate, frames=15, interval=250, blit=True)
    plt.close()
    return anim_square_signal
