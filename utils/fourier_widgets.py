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
    output_notebook()  # Create the widget directly in the Jupyter Notebook
    x = np.arange(0, 1.01, 0.01)  # Time vector for the original signal
    y = np.sin(10 * np.pi * x)  # Creation of the original signal
    Fs = 50
    x_undersampled = np.arange(0, 1.01, 1 / Fs)  # Time vectors for every undersampled signals
    y_undersampled = np.sin(10 * np.pi * x_undersampled)  # Every undersampled signals
    source1 = ColumnDataSource(data=dict(x=x, y=y))
    source2 = ColumnDataSource(data=dict(x_undersampled=x_undersampled, y_undersampled=y_undersampled))
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
    callback = CustomJS(args=dict(source=source2), code="""
        var data = source.data;
        var fs = cb_obj.value
        var x = data['x_undersampled']
        var y = data['y_undersampled']
        for (var i = 0; i <  fs+1; i++) {
            x[i] = i*1/fs
            y[i] = Math.sin(10*Math.PI*x[i])
        }
        for (var i = fs+1; i <  x.length; i++) {
            x[i] = x[fs] 
            y[i] = y[fs]
        }
        source.change.emit();
    """)
    slider_fs = Slider(start=1, end=Fs, value=Fs, step=1, title="Sampling frequency (Hz)", bar_color=Blues[256][64])
    slider_fs.js_on_change('value', callback)
    layout = column(plot, slider_fs)
    show(layout)


def square_signal_decomposition_widget():
    output_notebook()

    nb_points = 100  # Number of time points in the signal
    x = np.linspace(0, 1, nb_points)
    xs = []
    ys = []

    nb_sin_max = 33

    for n in range(nb_sin_max):  # We will limit the max number of sinusoids to 33 (for clarity + speed)
        xs.append(x)
        ys.append(4 / np.pi * np.sin(3 * np.pi * (2 * n + 1) * x) / (
                    2 * n + 1))  # Approximation of square signal with sinusoids

    color_palette = list(Blues[256][0:256:256 // nb_sin_max][:nb_sin_max])
    width_palette = np.linspace(5, 1, nb_sin_max).tolist()

    nb_sin_init = 10  # Initial number of sinusoids to display
    source1 = ColumnDataSource(data=dict(x_display=xs[:nb_sin_init],
                                         y_display=ys[:nb_sin_init],
                                         color=color_palette[:nb_sin_init],
                                         width=width_palette[:nb_sin_init]))
    source2 = ColumnDataSource(data=dict(x=x,
                                         y_sum=sum(ys[:nb_sin_init])))

    s1 = Figure(plot_width=950, plot_height=300)
    s1.multi_line(xs='x_display', ys='y_display', color='color', line_width='width', source=source1)
    s1.title.text = "Fourier decomposition of a square signal"
    s1.title.align = "center"
    s1.title.text_color = '#2171b5'
    s1.title.text_font_size = "25px"
    s1.add_layout(Title(text="Time (s)", align="center"), "below")
    s1.xaxis.minor_tick_line_color = None
    s1.yaxis.minor_tick_line_color = None

    s2 = Figure(plot_width=950, plot_height=300)
    s2.line('x', 'y_sum', line_width=5, line_color='#2171b5', source=source2)
    s2.xaxis.minor_tick_line_color = None
    s2.yaxis.minor_tick_line_color = None
    s2.title.text = "Resulting signal (sum of the sinusoids)"
    s2.title.align = "center"
    s2.title.text_color = '#2171b5'
    s2.title.text_font_size = "25px"
    s2.add_layout(Title(text="Time (s)", align="center"), "below")

    callback = CustomJS(args=dict(source1=source1,
                                  source2=source2,
                                  color_palette=color_palette,
                                  width_palette=width_palette,
                                  xs=xs,
                                  ys=ys),
                        code="""
        var nb_sin = cb_obj.value
        var data1 = source1.data;
        var x_display = data1['x_display'];
        var y_display = data1['y_display'];
        var color = data1['color'];
        var width = data1['width'];
    
        var data2 = source2.data;
        var x = data2['x'];
        var y_sum = data2['y_sum'];
    
        for (var i = 0; i <  x.length; i++) { 
            y_sum[i] = 0;
            for (var j = 0; j < nb_sin; j++) {
                y_sum[i] += ys[j][i];
            };
        };
        
        for (var i = 0; i < nb_sin; i++) {
            x_display[i] = xs[i];
            y_display[i] = ys[i];
            color[i] = color_palette[i];
            width[i] = width_palette[i];
        };
        for (var i = nb_sin; i < x.length; i++) {
            x_display[i] = [];
            y_display[i] = [];
            color[i] = [];
            width[i] = [];
        };
        source1.change.emit();
        source2.change.emit();
    """)

    slider_nb_sin = Slider(start=1, end=nb_sin_max, value=nb_sin_init, step=1, title="Number of sinusoïds",
                           bar_color=Blues[256][64])
    slider_nb_sin.js_on_change('value', callback)

    layout = column(s1, s2, slider_nb_sin)
    show(layout)


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

    nb_sin_max = 33
    nb_sin_init = 10

    color_palette = list(Blues[256][0:256:256 // nb_sin_max][:nb_sin_max])
    width_palette = np.linspace(5, 1, nb_sin_max).tolist()

    source1 = ColumnDataSource(data=dict(x_display=xs[:nb_sin_init],
                                         y_display=ys[:nb_sin_init],
                                         color=color_palette[:nb_sin_init],
                                         width=width_palette[:nb_sin_init]))

    source2 = ColumnDataSource(data=dict(x=x,
                                         y_sum=sum(ys[:nb_sin_init]),
                                         signal=signal))

    s1 = Figure(plot_width=900, plot_height=300)
    s1.multi_line(xs='x_display', ys='y_display', color='color', line_width='width', source=source1)
    s1.title.text = "Fourier decomposition of a random signal"
    s1.title.align = "center"
    s1.title.text_color = '#2171b5'
    s1.title.text_font_size = "25px"
    s1.add_layout(Title(text="Time (s)", align="center"), "below")
    s1.xaxis.minor_tick_line_color = None
    s1.yaxis.minor_tick_line_color = None

    s2 = Figure(plot_width=900, plot_height=300)
    s2.line('x', 'signal', line_width=5, line_color='#aaaaaa', legend_label='original signal', source=source2)
    s2.line('x', 'y_sum', line_width=5, line_color=Blues[256][64], legend_label='sum of the sinusoids', source=source2)
    s2.xaxis.minor_tick_line_color = None
    s2.yaxis.minor_tick_line_color = None
    s2.title.text = "Resulting signal (sum of the sinusoids)"
    s2.title.align = "center"
    s2.title.text_color = '#2171b5'
    s2.title.text_font_size = "25px"
    s2.add_layout(Title(text="Time (s)", align="center"), "below")

    callback = CustomJS(args=dict(source1=source1,
                                  source2=source2,
                                  color_palette=color_palette,
                                  width_palette=width_palette,
                                  xs=xs,
                                  ys=ys),
                        code="""
        var nb_sin = cb_obj.value
        var data1 = source1.data;
        var x_display = data1['x_display'];
        var y_display = data1['y_display'];
        var color = data1['color'];
        var width = data1['width'];

        var data2 = source2.data;
        var x = data2['x'];
        var y_sum = data2['y_sum'];

        for (var i = 0; i <  x.length; i++) { 
            y_sum[i] = 0;
            for (var j = 0; j < nb_sin; j++) {
                y_sum[i] += ys[j][i];
            };
        };

        for (var i = 0; i < nb_sin; i++) {
            x_display[i] = xs[i];
            y_display[i] = ys[i];
            color[i] = color_palette[i];
            width[i] = width_palette[i];
        };

        for (var i = nb_sin; i < x.length; i++) {
            x_display[i] = [];
            y_display[i] = [];
            color[i] = [];
            width[i] = [];
        };
        source1.change.emit();
        source2.change.emit();
    """)

    slider_nb_sin = Slider(start=1, end=nb_points, value=nb_sin_init, step=1, title="Number of sinusoïds",
                           bar_color=Blues[256][64])
    slider_nb_sin.js_on_change('value', callback)

    layout = column(s1, s2, slider_nb_sin)
    show(layout)
