#### Importando bibliotecas
from __future__ import print_function
import numpy as np
import math
import pandas as pd
from lmfit import minimize, Parameters, report_fit, fit_report
import corner
import bqplot as bq
from ipywidgets import interactive_output
from bqplot import pyplot as plt

pd.options.display.float_format = '{:,.4f}'.format
np.set_printoptions(linewidth=150, precision=4, suppress=True)

from .widgets import *
from .figures import gran_fig, q_fig, s_fig, s_line, q_line, xs, ys, ys_lin
from .layout import panel

from .simulation import selecao, calc_Bij, break_sim
from .retrocalc import retro_calc_Austin
from .cinetic_fit import c_fit

class App():
    """
    Base App class
    """
    def __init__(self):

        self.layout = panel

        Run_sim.on_click(break_sim)

        Retro_buttom.on_click(retro_calc_Austin)

        fit_buttom.on_click(c_fit)

# Atualizando Escala gran_plot
def update_gran_scale(ylog):
    if ylog == True:
        for i in range(len(gran_fig.marks)):
            gran_fig.marks[i].scales = {'x':xs, 'y':ys}
            gran_fig.axes[1].scale = ys
    else:    
        for i in range(len(gran_fig.marks)):
            gran_fig.marks[i].scales = {'x':xs, 'y':ys_lin}
            gran_fig.axes[1].scale = ys_lin

interactive_gran_plot = interactive_output(
        update_gran_scale, 
        { 'ylog': ylog_ck } )

def update_sel_plot(mu, _lambda, A, alpha):
    s_line.y = selecao(
            mu, _lambda, A, alpha)

def update_q_plot(delta, phi_um, gamma, beta):
    q_line.y = np.array(
            calc_Bij(delta, phi_um, gamma, beta)[:,0])

# Atualizando Figura Função Seleção
interactive_sel_plot = interactive_output(
        update_sel_plot, 
        {
            'mu':mu_s, 
            '_lambda':lambda_s, 
            'A':A_s, 
            'alpha':alpha_s
            }
        )

# Atualizando Figura Função Quebra
interactive_q_plot = interactive_output(
        update_q_plot, 
        {
            'delta':delta_s, 
            'phi_um':phi_um_s, 
            'gamma':gamma_s,
            'beta':beta_s
            }
        )

