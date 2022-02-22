from ipywidgets import HTML, HTMLMath
from IPython.display import display
import bqplot.pyplot as plt

from .input import *
from .widgets import *
from .figures import gran_fig, color_scale, gran_ax_options
from .layout import panel

R=1/np.sqrt(2)

def selecao(mu, _lambda, A, alpha):
    S = (A*(size_mm/size_mm[0])**alpha)*(1/(1+(size_mm/mu))**_lambda)
    S[n_inter-1] = 0
    return S

def calc_Bij(delta, phi_um, gamma, beta):
    phi_j = (phi_um*(size_mm/size_mm[0])**(-delta))#[::-1]
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
                #Bij[i-1,j-1] = phi_j[j-1]*((size_mm[i-1-1]/size_mm[j-1])**gamma) + \
                #        (1-phi_j[j-1])*((size_mm[i-1-1]/size_mm[j-1])**beta)
                #Bij[i-1,j-1] = phi_j[0]*((size_mm[i-1-1]/size_mm[0])**gamma) + \
                #        (1-phi_j[0])*((size_mm[i-1-1]/size_mm[0])**beta)
                #Bij[i-1,j-1] = phi_j[j-1]*R**((i-j-1)*gamma) + \
                #        (1-phi_j[j-1])*R**((i-j-1)*beta)
                Bij[i-1,j-1] = phi_j[0]*R**((i-2)*gamma) + \
                        (1-phi_j[0])*R**((i-2)*beta)
    return Bij

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

def calc_ej(tempo, Ss, flow_wid): 
    if flow_wid.value == 'batch-plug flow':
        e = np.exp(-Ss*tempo)
    elif flow_wid.value == 'fully mixed grinding':
        e = 1/(1+Ss*tempo)
    else:
        e = 1/((1+Ss*tempo/0.5)*(1+Ss*tempo/0.25)**2)
    return e

def calc_aij(Ss, bs, fi):

    n_inter = Ss.shape[0]
    aij = np.zeros((np.int(n_inter), np.int(n_inter)))

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

def calc_pi(a_s, es):

    ps = np.zeros(n_inter)

    for i in range(1, n_inter+1):
        j=1
        p_step = np.zeros(i-j+1)
        for j in range(1, i+1):
            p_step[j-1] = a_s[i-1,j-1] * es[j-1]
        ps[i-1] = p_step.sum()
    return ps

def calc_mat_product(
        mu, _lambda, A, alpha, # seleção
        delta, phi_um, gamma, beta, #quebra
        w_init, tempo, flow_wid): # ej, pi

    ps_mat = np.zeros((n_temp, n_inter))

    Si = selecao(mu, _lambda, A, alpha)
    Bij = calc_Bij(delta, phi_um, gamma, beta)
    bij = calc_bij(Bij)

    for i in range(1, n_temp+1, 1):
        ej = calc_ej( temp[i-1], Si, flow_m)
        aij = calc_aij(Si, bij, w0_exp)

        ps = calc_pi(aij, ej)
        ps_mat[i-1] = ps
    return ps_mat

def break_sim(b):
    output.clear_output()
    with output:
        display( 
                HTML('<h1>Starting Simulation</h1>'),
                HTML(value='<h2>Breakage and Selection Functions</h2>'))

    ps_mat = np.zeros((n_temp, n_inter))

    Si = selecao(mu_s.value, lambda_s.value, A_s.value, alpha_s.value)
    with output:
        display(HTMLMath('$ S_i= $'), Si, HTML('<br />') )

    Bij = calc_Bij(delta_s.value, phi_um_s.value, gamma_s.value, beta_s.value)
    with output:
        display( HTMLMath('$ B_{i,j}= $'), Bij, HTML('<br />') )

    bij = calc_bij(Bij)
    with output:
        display( HTMLMath(value='$b_{i,j} = $'), bij, HTML('<br />') )

    with output:
        display(HTML('<h2>Matrix Calculation</h2>'))

    for i in range(1, n_temp+1):

        ej = calc_ej( temp[i-1], Si, flow_m)

        aij = calc_aij(Si, bij, w0_exp)

        ps = calc_pi(aij, ej)
        ps_mat[i-1] = ps


    if len(gran_fig.marks)>(n_temp+1):
        for i in range(1, n_temp+1):
            gran_fig.marks[i+n_temp].y = ps_mat[:,::-1].cumsum(1)[i-1]*100

    else:
        for i in range(1, n_temp+1):
            plt.figure(0)
            plt.plot(
                    x=size_mm[::-1],
                    y=ps_mat[:,::-1].cumsum(1)[i-1]*100,
                    interpolation='basis',
                    stroke_width=2,
                    colors=[color_scale.iloc[i-1]])

    with output:
        display( HTMLMath('$a_{i,j}$'), aij, aij.sum(0), HTML('<br />'),)

        display(HTML(value='<h3> Matrix dos Produtos </h3>'))
        print('\n', ps_mat)

        display(HTML(value='<h3> Frequência Acumulada </h3>'))
        print(ps_mat[:, ::-1].cumsum(1)*100)
