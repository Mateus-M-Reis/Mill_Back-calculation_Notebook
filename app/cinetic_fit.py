import numpy as np
from lmfit import minimize, Parameters, report_fit, fit_report
from IPython.display import display

from .input import *
from .simulation import *
from .widgets import *
from .figures import gran_fig, color_scale, gran_ax_options
from .retrocalc import update_gran_plot

def calc_Bij_cf(gamma, beta, phi_um):
    for j in range(1, n_inter+1):
        for i in range(1, n_inter+1):
            if i < j:
                Bij[i-1,j-1] = 0.0
            elif i==j:
                Bij[i-1,j-1] = 1.0
            else:
                Bij[i-1,j-1] = phi_um*R**((i-j-1)*gamma) + \
                        (1-phi_um)*R**((i-j-1)*beta)
    return Bij

def calc_Bij_cf_1(gamma, beta, phi_um):
    for j in range(1, n_inter_cf+1):
        for i in range(1, n_inter_cf+1):
            if i < j:
                Bi1[i-1,j-1] = 0.0
            elif i==j:
                Bi1[i-1,j-1] = 1.0
            else:
                Bi1[i-1,j-1] = phi_j[j-1]*R**((i-j-1)*gamma) + \
                        (1-phi_j[j-1])*R**((i-j-1)*beta)
    return Bi1

def update_gran_plot_cf():
    ps_mat = np.zeros((n_temp, n_inter))
    Si = selecao(mu_s.value, lambda_s.value, A_s.value, alpha_s.value)
    Bij = calc_Bij(delta_s.value, phi_um_s.value, gamma_s.value, beta_s.value)
    bij = calc_bij(Bij)

    for i in range(1, n_temp+1):
        ej = calc_ej( temp[i-1], Si, flow_m)
        aij = calc_aij(Si, bij, w0_exp)
        ps = calc_pi(aij, ej)
        ps_mat[i-1] = ps*100

        if len(gran_fig.marks)>(n_temp+1):
            for i in range(1, n_temp+1):
                gran_fig.marks[i+n_temp].y = ps_mat[:,::-1].cumsum(1)[i-1][1:]
        else:
            for i in range(1, n_temp+1):
                plt.figure(0)
                plt.plot(
                        x=size_mm[:-1][::-1],
                        y=ps_mat[:,::-1].cumsum(1)[i-1][1:],
                        interpolation='basis',
                        stroke_width=2,
                        colors=[color_scale.iloc[i-1]])

def opt_cf_1(vals,
        w_init, tempo, flow_wid):
    
    parametros = vals.valuesdict()

    A = parametros['A']
    alpha = parametros['alpha']
    mu = parametros['mu'] 
    _lambda = parametros['_lambda']

    gamma = parametros['gamma']
    beta = parametros['beta']
    phi_um = parametros['phi_um']

    Si = selecao(mu, _lambda, A, alpha)
    Bij = calc_Bij_cf(gamma, beta, phi_um)
    bij = calc_bij(Bij)
    
    ps_mat = np.zeros(n_inter)
    ej = calc_ej( tempo[n_temp-1], Si, flow_wid)
    aij = calc_aij(Si, bij, w_init)
    
    ps = calc_pi(aij, ej)
    ps_mat = ps*100

    with output: display(freq_a[n_temp-1])
    with output: display(ps_mat[::-1].cumsum())
    with output: display(np.subtract(freq_a[n_temp-1], ps_mat[::-1].cumsum())**2)
    with output: display(HTML('<br >'))
        
    return np.subtract(freq_a[n_temp-1], ps_mat.cumsum())**2

def c_fit(b):

    params = Parameters()

    # add with tuples: (NAME VALUE VARY MIN  MAX  EXPR  BRUTE_STEP)
    params.add_many( 
            ('A', 0.0, False, A_s.min, A_s.max, None, 0.01), 
            ('alpha', alpha_s.value, False, alpha_s.min, alpha_s.max, None, 0.01), 
            ('mu', mu_s.value, False, mu_s.min, mu_s.max, None, 0.01), 
            ('_lambda', lambda_s.value, False, lambda_s.min, lambda_s.max, None, 0.01), 

            ('gamma', gamma_s.value, True, gamma_s.min, gamma_s.max, None, 0.01), 
            ('beta', beta_s.value, True, beta_s.min, beta_s.max, None, 0.01),
            ('phi_um', phi_um_s.value, True, phi_um_s.min, phi_um_s.max, None, 0.01), 
            )

    output.clear_output()
    with output:
        display(
                HTML(value='<h1>Cinetic Fit</h1>'),
                HTML(value='<h3>Iniciando Primeira Etapa</h3>'),
                Label(
                    value='Varing the foloowing variables:\n \
                            $\gamma$, $\\beta$, $\Phi_1$'),
                params
                )

    first_result = minimize(
            opt_cf_1, 
            params, 
            args=(w0_exp, temp, flow_m), 
            method=opt_m.value,
            )

    with output:
        display(HTML(value='<h4>Primeira Etapa Concluída</h4>'))
        print('###################################################################')
        display( report_fit(first_result) )
        print('###################################################################')

    phi_um_s.value = first_result.params['phi_um'].value
    gamma_s.value = first_result.params['gamma'].value
    beta_s.value = first_result.params['beta'].value
    update_gran_plot()

    ##############################################################################

    params['A'].set(vary=False)
    params['alpha'].set(vary=False)
    params['mu'].set(vary=True)
    params['_lambda'].set(vary=True)

    params['gamma'].set(value=first_result.params['gamma'].value, vary=False)
    params['beta'].set(value=first_result.params['beta'].value, vary=False)
    params['phi_um'].set(value=first_result.params['phi_um'].value, vary=False)

    with output:
        display(
                HTML(value='<h3>Iniciando Segunda Etapa</h3>'),
                Label(
                    value='Varing the foloowing variables:\n \
                            $A$, $\\alpha$, $\mu$, $\Lambda$'),
                params
                )

    second_result = minimize(
            opt_cf,
            params, 
            args=(w0_exp, temp, flow_m),
            method=opt_m.value,
            )

    with output:
        display(HTML(value='<h4>Segunda Etapa Concluída</h4>'))
        print('###################################################################')
        display( report_fit(second_result) )
        print('###################################################################')

    A_s.value = second_result.params['A'].value
    alpha_s.value = second_result.params['alpha'].value
    mu_s.value = second_result.params['mu'].value
    lambda_s.value = second_result.params['_lambda'].value

    update_gran_plot()
