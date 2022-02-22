import pandas as pd
from ipywidgets import interactive_output
import bqplot as bq
from bqplot import pyplot as plt
from bqplot import Axis

from .input import *
from .widgets import *
#from .simulation import selecao, calc_Bij

#### scales
#xs_lin = bq.LinearScale(min=0.03, max=size_mm[0]+1)
xs = bq.LogScale(min=0.01, max=size_mm[0]+1)

ys_lin = bq.LinearScale(min=0.0, max=100)
ys_lin1 = bq.LinearScale(min=0.0, max=1)

ys = bq.LogScale(min=1, max=100)
ys1 = bq.LogScale(min=0.01, max=1)

color_scale = pd.Series(plt.COLOR_CODES)
color_scale.index = range(color_scale.size)

# Figures
gran_ax_options={
        'x': dict(
            label='Size (mm)', 
            grid_lines='solid', 
            orientation='horizontal',
            tick_format='0.2f',
            ), 
        'y': dict(
            label='Porcentagem Passante Acumulada', 
            grid_lines='solid', 
            orientation='vertical', 
            tick_format='0.1f'
            )
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

plt.plot(
        x=size_mm, 
        y=w0_exp[::-1].cumsum()[::-1]*100,
        axes_options=gran_ax_options,
        scales={'x': xs, 'y': ys_lin},
        colors=['gray'],
        interpolation='linear',
        stroke_width=2,
        figure=gran_fig,
        #scales={'x': xs, 'y': ys_lin}
        ) 

for i in range(n_temp):
    plt.scatter(
            x=size_mm, 
            y=freq_a[i][::-1],
            scales={ 'x':xs, 'y':ys_lin },
            #stroke_width=2,
            colors=[color_scale.iloc[i]],
            figure=gran_fig
            )

# Breakage Function Figure
q_xax = bq.Axis(
        scale=xs, 
        label='Size (mm)', 
        grid_lines='solid',
        tick_format='0.1f',
        tick_values=[0.1, 1],
        )
q_yax = bq.Axis(
        scale=ys1, 
        orientation='vertical', 
        label='Parâmetro de Quebra cumulativo, Bi,j', 
        grid_lines='solid',
        tick_format='0.1f', 
        tick_values=[0.1, 1],
        )
q_line = bq.Lines(
        x=size_mm, 
        y=Bij[:,0],#bij[:,0][::-1].cumsum()[::-1],                  
        scales={'x': xs, 'y': ys1}, 
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
        fig_margin={'top':0,'bottom':40, 'left':50, 'right':50},
        )
q_fig.layout.height= '100%'
q_fig.layout.width= '100%'

# Selection Function Figure
s_xax = bq.Axis(
        scale=xs, 
        label='Size (mm)', 
        grid_lines='solid',
        tick_format='0.1f',
        tick_values=[0.1, 1],
        )
s_yax = bq.Axis(
        scale=ys1, 
        orientation='vertical', 
        label='Taxa Específica de Quebra, min^-1', 
        grid_lines='solid',
        tick_format='0.1f', 
        tick_values=[0.1, 1],
        )
s_line = bq.Lines(
        x=size_mm, 
        y=Si, 
        scales={'x': xs, 'y': ys1}, 
        colors = ['cyan'], 
        stroke_width = 2,                 
        interpolation = 'basis'
        )
#si_exp_scatter = bq.Scatter(
#        x=size_mm, 
#        y=si_exp, 
#        scales={'x': xs, 'y': ys}, 
#        colors=['red']
#        )
s_fig= bq.Figure(
        title='Selection', 
        title_style={'font-size': '20px'}, 
        legend_location='top-left',
        axes=[s_xax, s_yax], 
        #marks=[s_line, si_exp_scatter], 
        marks=[s_line], 
        animation_duration=1000,
        axes_options=gran_ax_options,
        fig_margin={'top':0,'bottom':40, 'left':50, 'right':50},
        )
s_fig.layout.height= '100%'
s_fig.layout.width= '100%'
