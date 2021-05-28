import numpy as np

from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, CustomJS, Slider, Title
from bokeh.plotting import Figure, output_file, show
from bokeh.io import output_notebook


def aliasing_widget():
    output_notebook()
    x = np.linspace(0, 1, 100)
    y = np.sin(10 * np.pi * x)
    Fs = 50
    x_undersampled = np.linspace(0, 1, Fs)
    y_undersampled = np.sin(10 * np.pi * x_undersampled)

    source1 = ColumnDataSource(data=dict(x=x, y=y))
    source2 = ColumnDataSource(data=dict(x_undersampled=x_undersampled, y_undersampled=y_undersampled))

    plot = Figure(plot_width=900, plot_height=300)
    plot.line('x', 'y', source=source1, line_width=5, line_color='#04aa6d', legend_label="original")
    plot.line('x_undersampled', 'y_undersampled', source=source2, line_width=5, line_color='#5a9bc7',
              legend_label="sampled")
    plot.title.text = "Aliasing of a 5Hz signal"
    plot.title.align = "center"
    plot.title.text_color = '#5a9bc7'
    plot.title.text_font_size = "25px"
    plot.add_layout(Title(text="Time (s)", align="center"), "below")
    plot.yaxis.visible = False

    callback = CustomJS(args=dict(source=source2), code="""
        var data = source.data;
        var fs = cb_obj.value
        var x = data['x_undersampled']
        var y = data['y_undersampled']

        for (var i = 0; i <  fs; i++) {
            x[i] = i*1/fs
            y[i] = Math.sin(10*Math.PI*x[i])
        }

        for (var i = fs; i <  x.length; i++) {
            x[i] = x[fs-1] 
            y[i] = y[fs-1]
        }
        source.change.emit();
    """)

    slider_fs = Slider(start=1, end=Fs, value=Fs, step=1, title="Sampling frequency (Hz)")
    slider_fs.js_on_change('value', callback)

    layout = column(plot, slider_fs)
    show(layout)
