import numpy as np

from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, CustomJS, Slider, Title
from bokeh.plotting import Figure, output_file, show
from bokeh.io import output_notebook
from bokeh.palettes import Blues


def aliasing_widget():
    output_notebook()
    x = np.arange(0, 1.01, 0.01)
    y = np.sin(10 * np.pi * x)
    Fs = 50
    x_undersampled = np.arange(0, 1.01, 1 / Fs)
    y_undersampled = np.sin(10 * np.pi * x_undersampled)

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

    slider_fs = Slider(start=1, end=Fs, value=Fs, step=1, title="Sampling frequency (Hz)")
    slider_fs.js_on_change('value', callback)

    layout = column(plot, slider_fs)
    show(layout)


def square_signal_decomposition_widget():
    output_notebook()

    nb_points = 100
    x = np.linspace(0, 1, nb_points)
    y = [np.zeros((nb_points, len(x)))]
    xs = []
    ys = []

    for n in range(nb_points):
        xs.append(x)
        ys.append(4 / np.pi * np.sin(3 * np.pi * (2 * n + 1) * x) / (2 * n + 1))

    y_display = ys

    source = ColumnDataSource(data=dict(x=x, y_sum=sum(ys), xs=xs, ys=ys, y_display=ys, color=Blues[256][56:256:2],
                                        alpha=np.linspace(1, 0, 100)))

    s1 = Figure(plot_width=900, plot_height=300)
    s1.multi_line(xs='xs', ys='y_display', source=source, line_width=5, color='color', line_alpha='alpha')
    s1.title.text = "Fourier decomposition of a square signal"
    s1.title.align = "center"
    s1.title.text_color = '#5a9bc7'
    s1.title.text_font_size = "25px"
    s1.add_layout(Title(text="Time (s)", align="center"), "below")
    s1.xaxis.minor_tick_line_color = None
    s1.yaxis.minor_tick_line_color = None

    s2 = Figure(plot_width=900, plot_height=300)
    s2.line('x', 'y_sum', source=source, line_width=5, line_color='#5a9bc7')
    s2.xaxis.minor_tick_line_color = None
    s2.yaxis.minor_tick_line_color = None
    s2.add_layout(Title(text="Time (s)", align="center"), "below")

    callback = CustomJS(args=dict(source=source), code="""
        var data = source.data;
        var nb_sin = cb_obj.value
        var x = data['x']
        var ys = data['ys']
        var y_sum = data['y_sum']
        var y_display = data['y_display']

        for (var i = 0; i <  x.length; i++) { 
            y_sum[i] = 0
            for (var j = 0; j < nb_sin; j++) {
                y_sum[i] += ys[j][i]
            }
        }


        for (var i = 0; i < nb_sin; i++) {
            y_display[i] = ys[i]
        }
        for (var i = nb_sin; i < x.length; i++) {
            y_display[i] = []
        }

        source.change.emit();
    """)

    slider_nb_sin = Slider(start=1, end=100, value=100, step=1, title="Number of sinusoïds", bar_color='#5a9bc7')
    slider_nb_sin.js_on_change('value', callback)

    layout = column(s1, s2, slider_nb_sin)
    show(layout)
