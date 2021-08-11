import pandas as pd
from ipywidgets import interactive_output
import bqplot as bq
from bqplot import pyplot as plt
from bqplot import Axis

from .input import *
from .widgets import *
#from .simulation import *

#### scales
xs_lin = bq.LinearScale(min=0.25, max=6)
xs = bq.LogScale(min=0.25, max=6)
ys_lin = bq.LinearScale(min=0.05, max=1)
ys = bq.LogScale(min=0.05, max=1)
color_scale = pd.Series(plt.COLOR_CODES)
color_scale.index = range(color_scale.size)

# Figures
gran_ax_options={
        'x': dict(
            label='Size (mm)', 
            grid_lines='solid', 
            orientation='horizontal'), 
        'y': dict(
            label='Porcentagem Passante Acumulada', 
            grid_lines='solid', 
            orientation='vertical', 
            tick_format='0.2f')
        }
gran_fig = plt.figure(
        0, 
        title='Commulative Size Distribution', 
        title_style={'font-size': '20px'}, 
        animation_duration=1000, 
        axes_options=gran_ax_options,
        layout={'height':'100%', 'width':'100%'}, 
        legend_location='top-left',
        fig_margin={'top':0,'bottom':50, 'left':50, 'right':50},
        scale_x=xs, 
        scale_y=ys_lin
        )
for i in range(n_temp):
    plt.scatter(
            x=size_mm, 
            y=freq_a[i].cumsum()[::-1],
            scales={ 'x':xs, 'y':ys_lin },
            #stroke_width=2,
            colors=[color_scale.iloc[i]],
            figure=gran_fig
            )

    plt.plot(
            x=size_mm, 
            y=w0_exp[::-1].cumsum()[::-1],
            axes_options=gran_ax_options,
            scales={'x': xs, 'y': ys_lin},
            colors=['gray'],
            interpolation='linear',
            stroke_width=2,
            figure=gran_fig,
            #scales={'x': xs, 'y': ys_lin}
            ) 

# Breakage Function Figure
q_xax = bq.Axis(
        scale=xs, 
        label='Size (mm)', 
        grid_lines='solid'
        )
q_yax = bq.Axis(
        scale=ys, 
        orientation='vertical', 
        tick_format='0.2f', 
        label='Parâmetro de Quebra cumulativo, Bi,j', 
        grid_lines='solid'
        )
q_line = bq.Lines(
        x=size_mm, 
        y=bij[:,0][::-1].cumsum()[::-1],                  
        scales={'x': xs, 'y': ys}, 
        colors = ['magenta'], 
        stroke_width = 2, 
        interpolation = 'basis'
        )
q_fig= bq.Figure(
        title='Breakage', 
        title_style={'font-size': '20px'}, 
        legend_location='top-left',
        axes=[q_xax, q_yax],  
        marks=[q_line],  
        animation_duration=1000,
        axes_options=gran_ax_options,
        )
q_fig.layout.height= '80%'
q_fig.layout.width= '100%'

# Selection Function Figure
s_xax = bq.Axis(scale=xs, label='Size (mm)', grid_lines='solid')
s_yax = bq.Axis(
        scale=ys, 
        orientation='vertical', 
        tick_format='0.2f', 
        label='Taxa Específica de Quebra, min^-1', 
        grid_lines='solid'
        )
s_line = bq.Lines(
        x=size_mm, 
        y=Si, 
        scales={'x': xs, 'y': ys}, 
        colors = ['cyan'], 
        stroke_width = 2,                 
        interpolation = 'basis'
        )
si_exp_scatter = bq.Scatter(
        x=size_mm, 
        y=si_exp, 
        scales={'x': xs, 'y': ys}, 
        colors=['red']
        )
s_fig= bq.Figure(
        title='Selection', 
        title_style={'font-size': '20px'}, 
        legend_location='top-left',
        axes=[s_xax, s_yax], 
        marks=[s_line, si_exp_scatter], 
        animation_duration=1000,
        axes_options=gran_ax_options,
        )
s_fig.layout.height= '80%'
s_fig.layout.width= '100%'
