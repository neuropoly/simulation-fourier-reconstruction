import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation


def square_signal_decomposition(nb_iterations):
    """Shows the approximation of a square signal by summing sinusoids"""

    fig, (ax1, ax2) = plt.subplots(1, 2)  # Setting up a figure with 2 subplots
    fig.tight_layout(pad=3.0)
    ax2.set_title("Resulting signal")
    fig.dpi = 150

    t_max = 4*np.pi  # max time
    line = ax2.plot([], [], lw=2, color='r')  # Initializing empty plots
    for ax in [ax1, ax2]:
        ax.set_ylim(-1.5, 1.5)
        ax.set_xlim(0, t_max)
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Amplitude (a.u.)")

    # Animation function.  Called sequentially
    def animate(i):
        x = np.linspace(0, t_max, 500)
        y = np.zeros(len(x))
        for n in range(1, 2*i+2, 2):
            y = np.vstack((y, 4*np.sin(n * x)/(np.pi*n)))
        ax1.set_title(f"{i+1} summed sinusoids")
        ax1.plot(x.T, y[1:].T, lw=1)  # plot() allows to display several functions
        ax1.set_prop_cycle(None)  # Colors are always plotted in the same order
        line[0].set_data(x, y[1:].sum(0))  # 2D line will not keep old plots
        return line

    # create the animation
    anim_square_signal = animation.FuncAnimation(fig, animate, frames=15, interval=250, blit=True)
    plt.close()
    return anim_square_signal
