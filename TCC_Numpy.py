#!/usr/bin/env python
# coding: utf-8

#### Importando bibliotecas
from __future__ import print_function
import numpy as np
import math
print(math.__doc__)

import pandas as pd
from pandas import ExcelFile

from lmfit import minimize, Parameters, report_fit, fit_report
import corner

from ipywidgets import interactive, interact, Output, Box, HBox, VBox,Layout, FloatText, Dropdown, Label,FloatSlider, interactive_output, Button, Checkbox, HTML, ToggleButton, HTMLMath, Accordion

from IPython.display import display, Image

import bqplot as bq
from bqplot import pyplot as plt

from matplotlib.pyplot import rcParams, style

rcParams['figure.figsize']=[11, 4]
style.use('dark_background')

pd.options.display.float_format = '{:,.4f}'.format
np.set_printoptions(linewidth=150, precision=4, suppress=True)

#get_ipython().run_cell_magic('javascript', '', "document.body.classList.add('theme-dark')")

#### Aquisição de Dados e Definições Iniciais

df = pd.read_excel('./dados/input.xlsx', sheet_name='input', header=None)

n_temp = np.int(df.iloc[0,1])
n_inter = np.int(df.iloc[0,2])

temp = df.iloc[2,0:int(n_temp)].values
si_exp = df.iloc[3,0:int(n_inter)].values

interval = np.arange(1, n_inter+2,1)

w0_exp = df.iloc[4,0:int(n_inter)].values
w0_exp = w0_exp

size = np.arange(n_inter+1)
for i in range(int(n_inter)):
    size[i] = 1000*(1/np.sqrt(2))**i

pe_exp = df.iloc[5:int(n_temp)+5, 0:int(n_inter)].values
############################################################
disc = np.zeros((n_temp, n_inter))
disc = pe_exp.copy()
for i in range(n_temp):
    disc[:,8][i] = 1 - disc[i,:8].sum()

freq_a=disc.copy()
freq_a = freq_a[:,::-1]
############################################################
# Definições Iniciais

n_temp = 6
n_inter = 9

upper_size_mm = 3.5
R=1/np.sqrt(2)

size_mm = np.zeros(n_inter)
for i in range(n_inter):
    size_mm[i]= upper_size_mm*R**(i-1)
size_rel = size_mm/size_mm[1]

Si= np.zeros(n_inter)

Bi1 = np.zeros((n_inter))
Bij = np.zeros((n_inter, n_inter))
bij = np.zeros((n_inter,n_inter))

############################################################
wi = np.ones(n_inter)
wi_mc = np.zeros((n_temp,n_inter))

#### Widgets

#S_title = Label(value='Função Seleção')
mu_s= FloatSlider(min=1.4,max=3.0,step=0.05,value=1.7,description='$\mu$')
lambda_s= FloatSlider(min=0.0,max=3.7,step=0.01,value=0.0, description='$\Lambda$')
A_s= FloatSlider(min=0.60,max=4,step=0.01,value=1.0, description='$A$')
alpha_s= FloatSlider(min=0.5,max=1.5,step=0.01,value=0.88, description='$\\alpha$')

Si_eq = Label(value='$$ S_i = A(x_i/x_1)^\\alpha Q_i$$', 
        layout=Layout(height='60px', 
            justfy_content = 'center')
        )

Qi_eq = Label(value='$$ Q_i = 1/(1+x_i/\mu)^\Lambda$$', 
        layout=Layout(height='60px', 
            justfy_content = 'center')
        )

S_Panel = VBox([VBox([HBox([A_s, alpha_s]), 
    Si_eq]), 
    VBox([HBox([mu_s, lambda_s]), 
        Qi_eq])])

    #Q_title =  Label(value='Função Quebra')
delta_s= FloatSlider(min=0,max=0.25,step=0.01,value=0,description='$\delta$')
phi_um_s= FloatSlider(min=0.25,max=0.75,step=0.01,value=0.60, description='$\Phi_1$')
gamma_s= FloatSlider(min=0.50,max=1.3,step=0.01,value=0.5, description='$\gamma$')
beta_s= FloatSlider(min=2.3,max=5.8,step=0.01,value=4.0, description='$\\beta$')

Bij_eq = Label(value="$$B_{i,j} = \Phi_j R^{(i-2)\gamma} + (1-\Phi_j) R^{(i-2)\\beta}$$",               layout=Layout(height='60px',
    justfy_content = 'center')
    )

Phi_j_eq = Label(value='$$ \Phi_j = \Phi_1 (x_j/x_1)^{-\delta}$$',                 layout=Layout(height='60px',
    justfy_content = 'center')
    )

flow_m= Dropdown(options=['batch-plug flow', 'fully mixed grinding', 'one large two small fully mixed reactors'],
        value='batch-plug flow', 
        description='Flow Model:', 
        disabled=False,
        layout=Layout(width='380px'), 
        style = {'description_width': '80px'})

Q_Panel = VBox([VBox([HBox([gamma_s, 
    beta_s]), 
    Bij_eq]
    ), 
    VBox([HBox([delta_s, 
        phi_um_s]), 
        Phi_j_eq])
    ])

####################################################################################################

simulation_Title = HTML(value="<h1>Simulação</h1>") 
Aquisicao_title = HTML(value="<h1>=Aquisição de Dados</h1>")

ej_eq = HTMLMath(
        value= "$ e_j = exp(-S_j \\tau) $", 
        layout={
            'border':'0px solid',
            'width':'405px', 
            'height':'80px',
            'align_items':'center',
            'justify_content':'center'
            })

Run_sim = Button(description='Rodar Simulação',
        tooltip='Rodar Simulação com os Parâmetros Atuais ')

Retro_buttom = Button(description='Retrocalc',
        tooltip=' Otimizar para Todas as Variaveis',
        button_style = 'success')

ylog_ck = Checkbox(value=False, description='Log Y', 
        style = {'description_width': '0px'},
        layout=Layout(width='150px', justify_content='flex-end')
        )
norm_ck = Checkbox(value=True, description='Normalizada?', 
        style = {'description_width': '0px'},
        layout=Layout(width='150px', justify_content='flex-end')
        )

retro_eq = HTMLMath(value="$$minimize\ SSQ = \sum_k \sum_{i=1}^{n} w_i(p_i\nobserved\ -p_i\ computed\ ) $$")
##################################################################################################
output = Output()
output.layout = Layout(width='450px', 
        height='1250px', 
        align_content='center', 
        border='1px solid')
##################################################################################################
opt_m = Dropdown(options=['leastsq', 
    'least_squares',
    'differential_evolution',
    'brute',
    'nelder', 
    'lbfgsb',
    'powell', 
    'cg',
    'dogleg',
    'slsqp',
    'shgo',
    'dual_annealing'],
    value='leastsq', 
    description='Optimization Method:', 
    disabled=False,
    layout=Layout(width='380px'), 
    style = {'description_width': '80px'})


# Cálculos Iniciais

#### Seleção
#$ Q_i=\frac{1}{1+\frac{x_{i}}{\mu}}^{\alpha} $
#
#$ S_{i}=A(\frac{x_{i}}{x_{j}})^{\alpha} Q_i$
#### Quebra
#$  \Phi_{j} = \phi_{1} (\frac{x_{j}}{x_{1}})^{-\delta} $
#$B_{i,1}= \phi_{1}R^{(i-2)\gamma} + (1-\phi_{1}) R^{(i-2)\beta}$

#### Vetores Seleção e Quebra

def selecao(mu, _lambda, A, alpha):
    return (A*(size_rel)**alpha)*(1/(1+(size_mm/mu)**_lambda))

Si= selecao(mu_s.value, lambda_s.value, A_s.value, alpha_s.value)
########################################################################################
def calc_Bij(delta, phi_um, gamma, beta):
    phi_j = (phi_um*(size_mm/size_mm[0])**(-delta))[::-1]
    for j in range(1, n_inter+1):
        for i in range(1, n_inter+1):
            if i < j:
                Bij[i-1,j-1] = 0.0
            elif i==j:
                Bij[i-1,j-1] = 1.0
            else:
                if j==1:
                    Bij[i-1,j-1] = phi_j[j-1]*R**((i-2)*gamma) + (1-phi_j[j-1])*R**((i-2)*beta)
                else:
                    Bij[i-1, j-1] = Bij[i-1-1, j-1-1]*phi_j[j-1] 
    return Bij
Bij=calc_Bij(delta_s.value, phi_um_s.value, gamma_s.value, beta_s.value)

print(Si,'\n\n', Bij)

def selecao(mu, _lambda, A, alpha):
    S = (A*(size_rel)**alpha)*(1/(1+(size_mm/mu)**_lambda))
    S[n_inter-1] = 0
    return S

Si= selecao(mu_s.value, lambda_s.value, A_s.value, alpha_s.value)
########################################################################################
def calc_Bij(delta, phi_um, gamma, beta):
    phi_j = (phi_um*(size_mm/size_mm[0])**(-delta))[::-1]
    for l in range(n_inter):
        if phi_j[l]>1.0:
            phi_j[l] = 1.0
    for j in range(1, n_inter+1):
        for i in range(1, n_inter+1):
            if i < j:
                Bij[i-1,j-1] = 0.0
            elif i==j:
                Bij[i-1,j-1] = 1.0
            else:
                if phi_j[j-1] > 1.0:
                    phi_j[j-1] = 1.0
                else:
                    Bij[i-1,j-1] = phi_j[j-1]*((size_mm[i-1]/size_mm[j-1+1])**gamma) +                 (1-phi_j[j-1])*((size_mm[i-1]/size_mm[j-1+1])**beta)
    return Bij
Bij=calc_Bij(delta_s.value, phi_um_s.value, gamma_s.value, beta_s.value)

print(Si,'\n\n', Bij)

#### Cálculo bij
def calc_bij(Bij_mat):
    for j in range(n_inter):
        for i in range(n_inter):
            if i<j:
                bij[i,j] = 0.0
            elif i==n_inter-1:
                bij[i,j] = Bij_mat[i,j]
            else:
                bij[i,j] = Bij_mat[i,j] - Bij_mat[i+1,j]
    return bij

bij = calc_bij(Bij)
bij[:n_inter, :n_inter]

#### Figuras

## # scales
xs_lin = bq.LinearScale(min=0.25, max=6)
xs = bq.LogScale(min=0.25, max=6)
ys_lin = bq.LinearScale(min=0.01, max=1)
ys = bq.LogScale(min=0.01, max=1)

gran_ax_options={'x': dict(label='Size (mm)', grid_lines='solid', orientation='horizontal'), 
        'y': dict(label='Porcentagem Passante Acumulada', grid_lines='solid', orientation='vertical', 
            tick_format='0.2f')
        }
color_scale = pd.Series(plt.COLOR_CODES)
color_scale.index = range(color_scale.size)
####################################################################################################
gran_fig = plt.figure(0, title='Freq acumulada', title_style={'font-size': '20px'}, 
        animation_duration=1000, axes_options=gran_ax_options,
        layout={'height':'400px', 'width':'580px'}, legend_location='top-left',
        fig_margin={'top':30,'bottom':30, 'left':30, 'right':30},
        scale_x=xs, scale_y=ys_lin
        )
for i in range(n_temp):
    plt.scatter(x=size_mm, 
            y=freq_a[i].cumsum()[::-1],
            scales={'x':xs,
                'y':ys_lin},
            #axes_options=gran_ax_options,
            #stroke_width=1,
            colors=[color_scale.iloc[i]],
            figure=gran_fig
            )

    plt.plot(x=size_mm, 
            y=w0_exp[::-1].cumsum()[::-1],
            axes_options=gran_ax_options,
            scales={'x': xs, 'y': ys_lin},
            colors=['gray'],
            interpolation='basis',
            stroke_width=2,
            figure=gran_fig,
            #scales={'x': xs, 'y': ys_lin}
            ) 
    ################################################################
# q_fig
q_xax = bq.Axis(scale=xs, label='Size (mm)', grid_lines='solid')
q_yax = bq.Axis(scale=ys, orientation='vertical', tick_format='0.2f', 
        label='Parâmetro de Quebra cumulativo, Bi,j', grid_lines='solid')
q_line = bq.Lines(x=size_mm, y=bij[:,0][::-1].cumsum()[::-1],                  scales={'x': xs, 'y': ys}, colors = ['magenta'], stroke_width = 2, interpolation = 'basis')
q_fig= bq.Figure(title='Função Quebra', title_style={'font-size': '20px'}, legend_location='top-left',
        axes=[q_xax, q_yax],  marks=[q_line],  animation_duration=1000)

q_fig.layout.height= '400px'
q_fig.layout.width= '580px'
####################################################################################################
# s_fig
s_xax = bq.Axis(scale=xs, label='Size (mm)', grid_lines='solid')
s_yax = bq.Axis(scale=ys, orientation='vertical', tick_format='0.2f', 
        label='Taxa Específica de Quebra, min^-1', grid_lines='solid')

s_line = bq.Lines(x=size_mm, y=Si, scales={'x': xs, 'y': ys}, colors = ['cyan'], stroke_width = 2,                 interpolation = 'basis')
si_exp_scatter = bq.Scatter(x=size_mm, y=si_exp, scales={'x': xs, 'y': ys}, colors = ['red'])

s_fig= bq.Figure(title='Função Seleção', title_style={'font-size': '20px'}, legend_location='top-left',
        axes=[s_xax, s_yax], marks=[s_line, si_exp_scatter], animation_duration=1000)

s_fig.layout.height= '400px'
s_fig.layout.width= '580px'

#### Atualizando Figuras

def update_sel_plot(mu, _lambda, A, alpha):
    s_line.y  =  selecao(mu, _lambda, A, alpha)
interactive_sel_plot = interactive_output(update_sel_plot, {'mu':mu_s, '_lambda':lambda_s, 'A':A_s, 'alpha':alpha_s})

def update_q_plot(delta, phi_um, gamma, beta):
    q_line.y =  np.array(calc_Bij(delta, phi_um, gamma, beta)[:,0])
interactive_q_plot = interactive_output(update_q_plot, {'delta':delta_s, 'phi_um':phi_um_s, 'gamma':gamma_s,'beta':beta_s})

# ### Painel1

informacoes_Panel = HBox([ VBox([ VBox([simulation_Title,
    flow_m]
    ),
    VBox([ej_eq, 
        opt_m])
    ],
    layout=Layout(display='flex', border='solid 0px', align_items='center', justify_content='flex-start', width = '410px')
    ),
    VBox([ VBox([ylog_ck,
        Run_sim]),
        Retro_buttom
        ],
        layout=Layout(display='flex', border='solid 0px', align_items='stretch', justify_content='flex-start', width = '160px'))
    ],
    layout=Layout(display='flex', border='solid 0px', align_items='stretch', justify_content='space-between', width = '595px'))

####################################################################################################

Painel_de_Teste = VBox([
    HBox([VBox([s_fig, S_Panel],
        layout=Layout(display='flex', border='solid 0px', align_items='stretch', justify_content='space-between')), 
        VBox([q_fig, Q_Panel],
            layout=Layout(display='flex', border='solid 0px', align_items='stretch', justify_content='space-between'))
        ],layout=Layout(display='flex', border='solid 0px', align_items='stretch', justify_content='space-between', width = '1170px')
        ),
    HBox([
        informacoes_Panel, gran_fig],
        layout=Layout(display='flex', border='solid 0px', align_items='stretch', justify_content='center', width = '1170px')
        )
    ])

####################################################################################################

output.layout = Layout(width='600px', height='1000px', max_height='1030px', min_width='675px', align_content='center', border='0px solid')
Painel_Final = HBox([ Painel_de_Teste , output])
Painel_Final

# # Program Luckie and Austin (1992) - Austin Cap 6
# 
# $ e_{j} = \int_0^\infty e^{s_{j}t} \phi(t) dt$
# 
# <ul>
#     <li>Batch/Plug Flow:  $ e_{j} = exp(-S_{i} t)\phi(t)dt $</li>
#     <li>Fully Mixed Grinding:  $e_{j} = \frac{1}{(1+S_{j}\tau)}$ </li>
#     <li>m equal reactors: $e_{j} = \frac{1}{(1+ \frac{S_{j}\tau}{m})^m} $ </li>
#     <ul><li>one large two small reactors: $e_{j} = \frac{1}{(1+
# S_{j}\tau_{1})(1+ S_{j}\tau_{2})^2}$</li>
# </ul></ul>

ej = np.zeros((np.int(n_inter)))

def calc_ej(tempo, Ss, flow_wid):
    if flow_wid.value == 'batch-plug flow':
        e = np.exp(-Ss*tempo)
    elif flow_wid.value == 'fully mixed grinding':
        e = 1/(1+Ss*tempo)
    else:
        e = 1/((1+Ss*tempo/0.5)*(1+Ss*tempo/0.25)**2)
    return e


print(size_mm, '\n\n', Si, '\n')
plt.figure(12, layout={'height':'300px', 'width':'580px'},
        fig_margin={'top':30,'bottom':30, 'left':30, 'right':30},
        title='ej')
plt.clear()
for i in range(n_temp):
    ej = calc_ej(temp[i], Si, flow_m)
    print(ej)
    plt.plot(size_mm, ej, colors=[color_scale.iloc[i-1]],
            interpolation='basis')
    plt.show()

# $ a_{ij}= \begin{cases}
# f_{i}-\sum_{k=1, i>1}^{i-1}a_{ik},  & i=j  \\
        # \frac{1}{S_{i}-S_{j}}\sum_{k=j}^{i-1}S_{k}b_{ik}a_{kj}, & i>j
# \end{cases} $
# aij = np.zeros((np.int(n_inter), np.int(n_inter)))
# #a_step = np.array()
# output.clear_output()
# i=1
# j=1
# def calc_aij_t(Ss, bs, fi):
#     for j in range(1, n_inter+1):
#         with output:
# print('\n################################################################################\n',
#                   'j =', j,
#                   '\n
# ################################################################################')
#         for i in range(1, n_inter+1):

#if i<j:
#    aij[i-1,j-1] = 0.0
#    with output:
#        print('\n', i,  j,'\t i < j \t\t\t aij(i,j) = ', 
#                aij[i-1, j-1], '\tOK\n ###############################################')   
#
#elif i==j:
#    if i==1:
#        aij[i-1, j-1] = fi[i-1]
#        with output:
#            print('\n', i,  j,'\t i = j \t  i=1 \t\t aij(i,j) = ', aij[i-1, j-1], '\n') 
#    elif i>1:
#        k=1
#        a_step = np.zeros(i-1-k+1)
#        for k in range(1, i-1+1):
#            a_step[k-1] = aij[i-1, k-1]
#        with output:
#            print('\n', a_step)
#
#        aij[i-1, j-1] = fi[i-1] - a_step.sum()
#        with output:
#            print('\n', i,  j,'\t i = j \t  i>1 \t\t aij(i,j) = ', aij[i-1, j-1], '\n')
#elif i>j:
#    with output:
#        print('###############################################\n', i,  j,'\t i > j \n')
#        k=j
#        a_step = np.zeros((i-1-k+1))
#        for k in range(j, i-1+1):
#            a_step[k-j] = Ss[k-1] * bs[i-1,k-1] * aij[k-1,j-1]
#        with output:
#            print('\n', a_step)
#        aij[i-1,j-1] = 1/(Ss[i-1]-Ss[j-1]) * a_step.sum()
#    with output:
#        print('\n', 1/(Ss[i-1]-Ss[j-1]), '\n\n\t\taij(i,j) =', aij[i-1, j-1], '\n')
#    return aij


# aij=calc_aij_t(Si, bij, w0_exp)
# print(aij, '\n\n', aij.sum(0))

aij = np.zeros((np.int(n_inter), np.int(n_inter)))
#a_step = np.array()
output.clear_output()

def calc_aij(Ss, bs, fi):
    for j in range(1, n_inter+1):
        for i in range(1,n_inter+1):
            if i<j:
                aij[i-1,j-1] = 0.0  

            elif i==j:
                if i==1:
                    aij[i-1, j-1] = fi[i-1]
                elif i>1:
                    k=1
                    a_step = np.zeros(i-1-k+1)
                    for k in range(1, i-1+1):
                        a_step[k-1] = aij[i-1, k-1]
                    aij[i-1, j-1] = fi[i-1] - a_step.sum()

            elif i>j:
                k=j
                a_step = np.zeros((i-1-k+1))
                for k in range(j, i-1+1):
                    a_step[k-1-j+1] = Ss[k-1] * bs[i-1,k-1] * aij[k-1,j-1]
                aij[i-1,j-1] = 1/(Ss[i-1]-Ss[j-1]) * a_step.sum()
    return aij

aij=calc_aij(Si, bij, w0_exp)
print(aij, '\n\n', aij.sum(0))


# $ p_{i} = \begin{cases} \sum_{j=1}^{i}a_{ij}e_{j}, &  n\geq i \geq 1
# \end{cases} $

ps = np.zeros(n_inter)

def calc_pi(a_s, es):
    for i in range(1, n_inter+1):
        j=1
        p_step = np.zeros(i-j+1)
        for j in range(1, i+1):
            p_step[j-1] = a_s[i-1,j-1] * es[j-1]
        ps[i-1] = p_step.sum()
    return ps

ps = calc_pi(aij, ej)
print('produto simulado = \n', ps, '\n\nsoma cumulativa =\n', ps[::-1].cumsum(0))


# ### Simulação do Produto

ps_mat = np.zeros((n_temp, n_inter))

def calc_mat_product(mu, _lambda, A, alpha, # seleção
        delta, phi_um, gamma, beta, #quebra
        w_init, tempo, flow_wid): # ej, pi

    Si = selecao(mu, _lambda, A, alpha)
    Bij = calc_Bij(delta, phi_um, gamma, beta)
    bij = calc_bij(Bij)

    for i in range(1, n_temp+1, 1):
        ej = calc_ej( temp[i-1], Si, flow_m)
        aij = calc_aij(Si, bij, w0_exp)

        ps = calc_pi(aij, ej)
        ps_mat[i-1] = ps
    return ps_mat

ps_mat = calc_mat_product(mu_s.value, lambda_s.value, A_s.value, alpha_s.value,  # seleção
        delta_s.value, phi_um_s.value, gamma_s.value, beta_s.value,  #quebra
        w0_exp, temp, flow_m)

print('ps_mat  = \n', ps_mat,'\n\nACUMULADA = \n', ps_mat[:,::-1].cumsum(1))

def break_sim(b):
    output.clear_output()
    ej_fig = plt.figure(4, layout={'height':'300px', 'width':'580px'},
            fig_margin={'top':30,'bottom':30, 'left':30, 'right':30},
            title='ej')
    plt.clear()
    #dij_fig = plt.figure(5, layout={'height':'350px', 'width':'580px'},
     #                   fig_margin={'top':15,'bottom':15, 'left':20, 'right':15})
    #plt.clear()

    Si = selecao(mu_s.value, lambda_s.value, A_s.value, alpha_s.value)
    Bij = calc_Bij(delta_s.value, phi_um_s.value, gamma_s.value, beta_s.value)
    bij = calc_bij(Bij)

    with output: 
        display(HTML(value='<h1>SIMULAÇÃO</h1>'),
                HTML(value='<h2>FUNÇÕES SELEÇÃO E QUEBRA</h2>'), 
                HTMLMath(Si_eq.value), Si, 
                HTMLMath(value=Bij_eq.value), Bij, 
                HTMLMath(value='$b_{i,j}=B_{i,j}-B_{i+1,j}$'), bij, 
                HTML(value='<h2>CÁLCULO DAS MATRIZES</h2>'),
                HTMLMath(value='$a_{i,j} = $'))   

        for i in range(1, n_temp+1):
            ej = calc_ej( temp[i-1], Si, flow_m)
        aij = calc_aij(Si, bij, w0_exp)

        ps = calc_pi(aij, ej)
        ps_mat[i-1] = ps

        plt.figure(4)
        plt.plot(x=size_mm,y=ej, interpolation='basis', colors=[color_scale.iloc[i-1]])

    gran_fig.marks=gran_fig.marks[0:n_temp+1]
    for i in range(1, n_temp+1):
        plt.figure(0)
        plt.plot(x=size_mm[::-1],
                y=ps_mat[:,::-1].cumsum(1)[i-1],
                interpolation='basis',
                #axes_options=gran_ax_options,
                stroke_width=2,
                colors=[color_scale.iloc[i-1]])

        with output:
            print(aij, '\n\n', aij.sum(0), '\n')

        display(HTMLMath(value=ej_eq.value))
        plt.show(4)

        print('\n', ps_mat)
        display(HTML(value='<h3> Frequência Acumulada </h3>'))
        print(ps_mat[:, ::-1].cumsum(1))


Run_sim.on_click(break_sim)


# # Minimizaçao

# ##### Parametros
params = Parameters()
# add with tuples: (NAME VALUE VARY MIN  MAX  EXPR  BRUTE_STEP)
params.add_many(('mu', mu_s.value, True, mu_s.min, mu_s.max, None, None),
        ('_lambda', lambda_s.value, False, lambda_s.min, lambda_s.max, None, None),
        ('A', A_s.value, True, A_s.min, A_s.max, None, None),
        ('alpha', alpha_s.value, True, alpha_s.min, alpha_s.max, None, None),

        ('delta', delta_s.value, False, delta_s.min, delta_s.max, None, None),
        ('phi_um', phi_um_s.value, True, phi_um_s.min, phi_um_s.max, None, None),
        ('gamma', gamma_s.value, False, gamma_s.min, gamma_s.max, None, None),
        ('beta', beta_s.value, False, beta_s.min, beta_s.max, None, None)
        )


# $ minimize SSQ = \sum_{i=1}^{n} w_i (p_i observed - p_i computed) $
def retro_calc(vals,
        w_init, tempo, flow_wid, pe_mat):

    parametros = vals.valuesdict()
    mu = parametros['mu'] 
    _lambda = parametros['_lambda']
    A = parametros['A']
    alpha = parametros['alpha']
    delta = parametros['delta']
    phi_um = parametros['phi_um']
    gamma = parametros['gamma']
    beta = parametros['beta']

    Si = selecao(mu, _lambda, A, alpha)
    Bij = calc_Bij(delta, phi_um, gamma, beta)
    bij = calc_bij(Bij)

    for i in range(1, n_temp+1, 1):
        ej = calc_ej( temp[i-1], Si, flow_wid)
        aij = calc_aij(Si, bij, w0_exp)

        ps = calc_pi(aij, ej)
        ps_mat[i-1] = ps

    wi_mc = np.ones((n_temp, n_inter)) - np.divide((np.subtract(disc[:,::-1].cumsum(1), 
        ps_mat[:,::-1].cumsum(1))**2), 
        ps_mat[:,::-1].cumsum(1))[::-1]

    return (wi_mc * (np.subtract(disc, ps_mat)**2)).sum(1)

retro_calc(params,
        w0_exp, temp, flow_m,
        disc)


# ### Minimização Moly-Cop
# def retro_start(b):
#     params = Parameters()
#     # add with tuples: (NAME VALUE VARY MIN  MAX  EXPR  BRUTE_STEP)
#     params.add_many(('mu', mu_s.value, True, mu_s.min, mu_s.max, None, None),
#                 ('_lambda', lambda_s.value, False, lambda_s.min, lambda_s.max,
# None, None),
#                 ('A', A_s.value, True, A_s.min, A_s.max, None, None),
#                 ('alpha', alpha_s.value, True, alpha_s.min, alpha_s.max, None,
# None),

#('delta', delta_s.value, False, delta_s.min, delta_s.max, None, None),
#('phi_um', phi_um_s.value, True, phi_um_s.min, phi_um_s.max, None, None),
#('gamma', gamma_s.value, False, gamma_s.min, gamma_s.max, None, None),
#('beta', beta_s.value, False, beta_s.min, beta_s.max, None, None)
#               )
#    output.clear_output()
#    with output:
#        display(HTML(value='<h1>RETROCALC</h1>'))
#        display(HTML(value='<h3>Iniciando Primeira Etapa</h3>'))
#        display(params)


# result1 = minimize(retro_calc, params,
#                        args=(w0_exp, temp, flow_m, disc),
#                        method=opt_m.value
#                  )
#     with output:
#         display(HTML(value='<h3>Primeira Etapa Concluída</h3>'))
#         display(report_fit(result1))
# print('###################################################################')

A_s.value = result1.params['A'].value
alpha_s.value = result1.params['alpha'].value
mu_s.value = result1.params['mu'].value
phi_um_s.value = result1.params['phi_um'].value

params['phi_um'].set(value=result1.params['phi_um'].value, vary=False)
##############################################################################
with output:
    display(HTML(value='<h3>Prosseguindo para Próxima Etapa</h3>'))
    display(params)

result2 = minimize(retro_calc, params, args=(w0_exp, temp, flow_m, disc))

with output:
    display(HTML(value='<h3>Segunda Etapa Concluída</h3>'))
    display(report_fit(result2))
    print('###################################################################')

A_s.value = result2.params['A'].value
alpha_s.value = result2.params['alpha'].value
mu_s.value = result2.params['mu'].value

params['mu'].set(value=result2.params['mu'].value, vary=False)

params['gamma'].set(vary=True)
##############################################################################
with output:
    display(HTML(value='<h3>Iniciando Terceira Etapa</h3>'))
    display(params)

result3 = minimize(retro_calc, params, args=(w0_exp, temp, flow_m, pe_exp))
with output:
    display(HTML(value='<h3>Terceira Etapa Concluída</h3>'))
    display(report_fit(result3))

##############################################################################"""
Retro_buttom.on_click(retro_start)
### Minimização Austin

def retro_start_A(b):

    params = Parameters()
    # add with tuples: (NAME VALUE VARY MIN  MAX  EXPR  BRUTE_STEP)
    params.add_many( ('mu', mu_s.value, False, mu_s.min, mu_s.max, None, None), ('_lambda', lambda_s.value, False, lambda_s.min, lambda_s.max, None, None), ('A', 0.0, True, A_s.min, A_s.max, None, None), ('alpha', alpha_s.value, True, alpha_s.min, alpha_s.max, None, None), ('delta', delta_s.value, False, delta_s.min, delta_s.max, None, None), ('phi_um', phi_um_s.value, True, phi_um_s.min, phi_um_s.max, None, None), ('gamma', gamma_s.value, False, gamma_s.min, gamma_s.max, None, None), ('beta', beta_s.value, False, beta_s.min, beta_s.max, None, None))
    output.clear_output()
    with output:
        display(HTML(value='<h1>RETROCALC</h1>'))
        display(HTML(value='<h3>Iniciando Primeira Etapa</h3>'))
        display(params)

    result1 = minimize( retro_calc, params, args=(w0_exp, temp, flow_m, disc), method=opt_m.value)

    with output:
        display(HTML(value='<h3>Primeira Etapa Concluída</h3>'))
        display(report_fit(result1))
        print('###################################################################')

    A_s.value = result1.params['A'].value
    alpha_s.value = result1.params['alpha'].value
    phi_um_s.value = result1.params['phi_um'].value

    params['A'].set(value=result1.params['A'].value, vary=False)
    params['alpha'].set(value=result1.params['alpha'].value, vary=False)
    params['phi_um'].set(value=result1.params['phi_um'].value, vary=False)
    ##############################################################################
    params['gamma'].set(vary=True)
    params['beta'].set(vary=True)

    with output:
        display(HTML(value='<h3>Prosseguindo para Próxima Etapa</h3>'))
        display(params)

    result2 = minimize(retro_calc, params, args=(w0_exp, temp, flow_m, disc))

    with output:
        display(HTML(value='<h3>Segunda Etapa Concluída</h3>'))
        display(report_fit(result2))
        print('###################################################################')

    gamma_s.value = result2.params['gamma'].value
    beta_s.value = result2.params['beta'].value

    params['gamma'].set(value=result1.params['gamma'].value, vary=False)
    params['beta'].set(value=result1.params['beta'].value, vary=False)
    ##############################################################################
    params['delta'].set(vary=True)

    with output:
        display(HTML(value='<h3>Iniciando Terceira Etapa</h3>'))
        display(params)

    result3 = minimize(retro_calc, params, args=(w0_exp, temp, flow_m, pe_exp))

    with output:
        display(HTML(value='<h3>Terceira Etapa Concluída</h3>'))
        display(report_fit(result3))

    delta_s.value = result2.params['delta'].value
    ##############################################################################

Retro_buttom.on_click(retro_start_A)


# ##### Atualizando Escala gran_plot

def update_gran_scale(ylog):
    if ylog == True:
        for i in range(len(gran_fig.marks)):
            gran_fig.marks[i].scales = {'x':xs, 'y':ys}
            gran_fig.axes[1].scale = ys
    else:    
        for i in range(len(gran_fig.marks)):
            gran_fig.marks[i].scales = {'x':xs, 'y':ys_lin}
            gran_fig.axes[1].scale = ys_lin

interactive_gran_plot = interactive_output(update_gran_scale, {'ylog':ylog_ck})

