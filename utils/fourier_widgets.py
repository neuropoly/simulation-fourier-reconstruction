import numpy as np
import ipywidgets
from ipywidgets import interact, Layout
from numpy.fft import *
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, CustomJS, Slider, Title
from bokeh.plotting import Figure, output_file, show
from bokeh.io import push_notebook, output_notebook
from bokeh.palettes import Blues


def aliasing_widget():
    output_notebook()
    x = np.arange(0, 1.01, 0.01)
    y = np.sin(10 * np.pi * x)
    Fs_init = 25
    x_undersampled_init = np.arange(0, 1.01, 1 / Fs_init)
    y_undersampled_init = np.sin(10 * np.pi * x_undersampled_init)

    source1 = ColumnDataSource(data=dict(x=x, y=y))
    source2 = ColumnDataSource(data=dict(x_undersampled=x_undersampled_init, y_undersampled=y_undersampled_init))

    plot = Figure(plot_width=900, plot_height=300)
    plot.line('x', 'y', source=source1, line_width=5, line_color='#04aa6d', legend_label="original")
    plot.line('x_undersampled', 'y_undersampled', source=source2, line_width=5, line_color='#5a9bc7',
              legend_label="sampled")
    plot.circle('x_undersampled', 'y_undersampled', source=source2, fill_color="#5a9bc7", line_color=None, size=15)
    plot.title.text = "Aliasing of a 5Hz signal"
    plot.title.align = "center"
    plot.title.text_color = '#5a9bc7'
    plot.title.text_font_size = "25px"
    plot.add_layout(Title(text="Time (s)", align="center"), "below")
    plot.yaxis.visible = False
    plot.xaxis.minor_tick_line_color = None
    plot.yaxis.minor_tick_line_color = None

    def update_aliasing(Fs):
        x_undersampled = np.arange(0, 1.01, 1/Fs)
        y_undersampled = np.sin(10 * np.pi * x_undersampled)

        source2.data = {'x_undersampled': x_undersampled,
                        'y_undersampled': y_undersampled}
        push_notebook()

    layout = plot
    show(layout, notebook_handle=True)

    style = {'description_width': 'initial', 'handle_color': '#5a9bc7'}
    interact(update_aliasing, Fs=ipywidgets.IntSlider(min=1, max=50, step=1, value=Fs_init,
                                                      description='Sampling frequency:', layout=Layout(width='95%'),
                                                      style=style))


def square_signal_decomposition_widget():
    output_notebook()
    nb_points = 100
    x = np.linspace(0, 1, nb_points)
    xs = []
    ys = []

    nb_sin_max = 33

    for n in range(nb_sin_max):  # We will limit the max number of sinusoids to 33 (for clarity + speed)
        xs.append(x)
        ys.append(4 / np.pi * np.sin(3 * np.pi * (2 * n + 1) * x) / (
                2 * n + 1))  # Approximation of square signal with sinusoids

    nb_sin_init = 10

    color_palette = Blues[256][0:256:256 // nb_sin_max]
    width_palette = np.linspace(5, 1, nb_sin_max)

    source1 = ColumnDataSource(data=dict(x_display=xs[:nb_sin_init],
                                         y_display=ys[:nb_sin_init],
                                         color=color_palette[:nb_sin_init],
                                         width=width_palette[:nb_sin_init]))
    source2 = ColumnDataSource(data=dict(x=x,
                                         y_sum=sum(ys)))

    s1 = Figure(plot_width=900, plot_height=300)
    s1.multi_line(xs='x_display', ys='y_display', source=source1, color='color', line_width='width')
    s1.title.text = "Fourier decomposition of a square signal"
    s1.title.align = "center"
    s1.title.text_color = '#2171b5'
    s1.title.text_font_size = "25px"
    s1.add_layout(Title(text="Time (s)", align="center"), "below")
    s1.xaxis.minor_tick_line_color = None
    s1.yaxis.minor_tick_line_color = None

    s2 = Figure(plot_width=900, plot_height=300)
    s2.line('x', 'y_sum', source=source2, line_width=5, line_color='#2171b5')
    s2.xaxis.minor_tick_line_color = None
    s2.yaxis.minor_tick_line_color = None
    s2.title.text = "Resulting signal (sum of the sinusoids)"
    s2.title.align = "center"
    s2.title.text_color = '#2171b5'
    s2.title.text_font_size = "25px"
    s2.add_layout(Title(text="Time (s)", align="center"), "below")

    def update_square(nb_sin):
        source1.data = {'x_display': xs[:nb_sin],
                        'y_display': ys[:nb_sin],
                        'color': color_palette[:nb_sin],
                        'width': width_palette[:nb_sin]}

        source2.data = {'x': x,
                        'y_sum': sum(ys[:nb_sin])}
        push_notebook()

    layout = column(s1, s2)
    show(layout, notebook_handle=True)
    style = {'description_width': 'initial', 'handle_color': '#2171b5'}

    interact(update_square, nb_sin=ipywidgets.IntSlider(min=1, max=nb_sin_max, step=1, value=nb_sin_init,
                                                        description='Number of sinusoids:', layout=Layout(width='95%'),
                                                        style=style))


def random_signal_decomposition_widget():
    output_notebook()
    nb_points = 50
    signal = np.asarray(np.random.rand(nb_points))  # Generating a random signal composed of nb_points samples
    fft_signal = fft(signal)

    x = np.linspace(0, nb_points, nb_points)  # Time vector
    xs = []  # Will be used to store several time vector (for multi-line plots)
    ys = []  # Will be used to store the different sinusoids

    for n in range(0, nb_points):
        temp = np.zeros(len(x), dtype=complex)
        temp[n] = fft_signal[n]
        y = np.real(ifft(temp))
        xs.append(x)
        ys.append(y)

    nb_sin_init = 10

    color_palette = Blues[256][0:256:256 // nb_points]
    width_palette = np.linspace(5, 1, nb_points)

    source1 = ColumnDataSource(
        data=dict(x_display=xs[:nb_sin_init], y_display=ys[:nb_sin_init], color=color_palette[:nb_sin_init],
                  width=width_palette[:nb_sin_init]))

    source2 = ColumnDataSource(data=dict(x=x, y_sum=sum(ys), signal=signal))

    s1 = Figure(plot_width=900, plot_height=300)
    s1.multi_line(xs='x_display', ys='y_display', source=source1, color='color', line_width='width')
    s1.title.text = "Fourier decomposition of a random signal"
    s1.title.align = "center"
    s1.title.text_color = '#2171b5'
    s1.title.text_font_size = "25px"
    s1.add_layout(Title(text="Time (s)", align="center"), "below")
    s1.xaxis.minor_tick_line_color = None
    s1.yaxis.minor_tick_line_color = None

    s2 = Figure(plot_width=900, plot_height=300)
    s2.line('x', 'signal', source=source2, line_width=5, line_color='#aaaaaa', legend_label='original signal')
    s2.line('x', 'y_sum', source=source2, line_width=5, line_color=Blues[256][64], legend_label='sum of the sinusoids')
    s2.xaxis.minor_tick_line_color = None
    s2.yaxis.minor_tick_line_color = None
    s2.title.text = "Resulting signal (sum of the sinusoids)"
    s2.title.align = "center"
    s2.title.text_color = '#2171b5'
    s2.title.text_font_size = "25px"
    s2.add_layout(Title(text="Time (s)", align="center"), "below")

    def update_random(nb_sin):
        source1.data = {'x_display': xs[:nb_sin],
                        'y_display': ys[:nb_sin],
                        'color': color_palette[:nb_sin],
                        'width': width_palette[:nb_sin]}

        source2.data = {'x': x,
                        'y_sum': sum(ys[:nb_sin]),
                        'signal': signal}
        push_notebook()

    layout = column(s1, s2)
    show(layout, notebook_handle=True)
    style = {'description_width': 'initial', 'handle_color': '#2171b5'}
    interact(update_random, nb_sin=ipywidgets.IntSlider(min=1, max=nb_points, step=1, value=nb_sin_init,
                                                        description='Number of sinusoids:', layout=Layout(width='95%'),
                                                        style=style))
