import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from numpy.fft import *


def square_signal_decomposition():
    """Shows the approximation of a square signal by summing sinusoids"""

    fig, (ax1, ax2) = plt.subplots(2, 1)  # Setting up a figure with 2 subplots
    fig.tight_layout(pad=3.0)
    ax2.set_title("Resulting signal")
    fig.dpi = 150

    t_max = 4 * np.pi  # max time
    t = np.linspace(0, t_max, 500)
    line = ax2.plot([], [], lw=2, color='r')  # Initializing empty plots

    def init():
        ax1.clear()
        for ax in [ax1, ax2]:
            ax.set_ylim(-1.5, 1.5)
            ax.set_xlim(0, t_max)
            ax.set_xlabel("Time (s)")
            ax.set_ylabel("Amplitude (a.u.)")

    # Animation function.  Called sequentially
    def animate(i):

        y = np.zeros(len(t))
        for n in range(1, 2 * i + 2, 2):
            y = np.vstack((y, 4 * np.sin(n * t) / (np.pi * n)))
        ax1.set_title(f"{i + 1} summed sinusoids")
        ax1.plot(t.T, y[1:].T, lw=1)  # plot() allows to display several functions
        ax1.set_prop_cycle(None)  # Colors are always plotted in the same order
        line[0].set_data(t, y[1:].sum(0))  # 2D line will not keep old plots
        return line

    # create the animation
    anim = animation.FuncAnimation(fig, animate, frames=15, init_func=init, interval=250, blit=False)
    plt.close()
    anim.save('./animations/square_signal_decomposition.gif', writer=animation.PillowWriter(fps=5))
    return


def dummy_signal_decomposition():
    fig, (ax1, ax2) = plt.subplots(2, 1)  # Setting up a figure with 2 subplots
    fig.tight_layout(pad=3.0)
    ax2.set_title("Resulting signal")
    fig.dpi = 150

    signal = np.asarray([-9, 5, 20, 20, 0, 5, 10, 15, 10, 5, 5, 15, 20, 5, -7, 15, 5, 10, 10, -5])
    fft_signal = fft(signal)

    line = ax2.plot([], [], lw=2, color='r')  # Initializing empty plots
    t = np.linspace(0, 20, 20)

    def init():
        ax2.plot(t, signal)
        ax1.clear()
        for ax in [ax1, ax2]:
            ax.set_ylim(-10, signal.max() + 1)
            ax.set_xlim(0, 20)
            ax.set_ylabel("Amplitude (a.u.)")

    # Animation function.  Called sequentially
    def animate(i):
        y = np.zeros((len(t), i + 1), dtype=complex)
        for n in range(i + 1):
            temp = np.zeros(len(t), dtype=complex)
            temp[n] = fft_signal[n]
            y[:, n] = ifft(temp)
        ax1.set_title(f"{i + 1} summed sinusoids")
        ax1.plot(t, np.real(y), lw=1)  # plot() allows to display several functions
        ax1.set_prop_cycle(None)  # Colors are always plotted in the same order
        line[0].set_data(t, np.real(y.sum(1)))  # 2D line will not keep old plots
        return line

    # create the animation
    anim = animation.FuncAnimation(fig, animate, frames=len(t), init_func=init, interval=250, blit=False)
    plt.close()
    anim.save('./animations/dummy_signal_decomposition.gif', writer=animation.PillowWriter(fps=10))


def aliasing_1d():
    Fs = 100                                     # Sampling frequency (Hz)
    t_0 = 0                                      # Sampling starting time (s)
    t_max = 1                                    # Sampling ending time (s)
    nb_samples = (t_max - t_0)* Fs               # Number of samples (=500)
    t = np.linspace(t_0, t_max, nb_samples)
    s = np.sin(t * 10 * np.pi) # Creation of the temporal vector (duration: 5 s ; sampling frequency: 100Hz)

    fig, ax = plt.subplots()  # Setting up a figure with 2 subplots
    fig.tight_layout(pad=3.0)
    fig.dpi = 150

    signal = np.asarray([-9, 5, 20, 20, 0, 5, 10, 15, 10, 5, 5, 15, 20, 5, -7, 15, 5, 10, 10, -5])
    fft_signal = fft(signal)

    line = ax.plot([], [], lw=2, color='r')  # Initializing empty plots
    ttl = ax.text(.25, 1.05, '', transform=ax.transAxes)

    def init():
        ax.plot(t, s)
        ax.set_xlim(t_0, t_max)

    # Animation function.  Called sequentially
    def animate(i):
        Fs_undersampled = 20 - i # Sampling frequency
        nb_samples_undersampled = (t_max - t_0)* Fs_undersampled
        t_undersampled = np.linspace(t_0, t_max, nb_samples_undersampled)
        s_undersampled = np.sin(t_undersampled * 10 * np.pi)
        line[0].set_data(t_undersampled, s_undersampled)
        ttl.set_text(f'Sampling frequency: {Fs_undersampled} Hz')

    anim = animation.FuncAnimation(fig, animate, frames=19, init_func=init, interval=500, blit=False)
    plt.close()

    anim.save('./animations/aliasing_1d.gif', writer=animation.PillowWriter(fps=2))
    return
