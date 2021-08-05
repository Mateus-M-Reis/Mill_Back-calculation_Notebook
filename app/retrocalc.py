import numpy as np
from lmfit import minimize, Parameters, report_fit, fit_report
from IPython.display import display

from .input import *
from .simulation import *
from .widgets import *

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
    
    ps_mat = np.zeros((n_temp, n_inter))
    for i in range(1, n_temp+1, 1):
        ej = calc_ej( temp[i-1], Si, flow_wid)
        aij = calc_aij(Si, bij, w0_exp)
        
        ps = calc_pi(aij, ej)
        ps_mat[i-1] = ps
        
    wi_mc = np.ones((n_temp, n_inter)) - np.divide((np.subtract(disc[:,::-1].cumsum(1), 
                                                                ps_mat[:,::-1].cumsum(1))**2), 
                                                   ps_mat[:,::-1].cumsum(1))[::-1]
    
    return (wi_mc * (np.subtract(disc, ps_mat)**2)).sum(1)

def retro_calc_Austin(b):

    params = Parameters()

    # add with tuples: (NAME VALUE VARY MIN  MAX  EXPR  BRUTE_STEP)
    params.add_many( 
            ('mu', mu_s.value, False, mu_s.min, mu_s.max, None, None), 
            ('_lambda', lambda_s.value, False, lambda_s.min, lambda_s.max, None, None), 
            ('A', 0.0, True, A_s.min, A_s.max, None, None), 
            ('alpha', alpha_s.value, True, alpha_s.min, alpha_s.max, None, None), 
            ('delta', delta_s.value, False, delta_s.min, delta_s.max, None, None), 
            ('phi_um', phi_um_s.value, True, phi_um_s.min, phi_um_s.max, None, None), 
            ('gamma', gamma_s.value, False, gamma_s.min, gamma_s.max, None, None), 
            ('beta', beta_s.value, False, beta_s.min, beta_s.max, None, None))

    output.clear_output()
    with output:
        display(
                HTML(value='<h1>RETROCALC</h1>'),
                display(HTML(value='<h3>Iniciando Primeira Etapa</h3>')),
                params
                )

    first_result = minimize(
            retro_calc, 
            params, 
            args=(w0_exp, temp, flow_m, disc), 
            method=opt_m.value)

    with output:
        display(HTML(value='<h3>Primeira Etapa Concluída</h3>'))
        display(
                report_fit(first_result)
                )
        print('###################################################################')

    A_s.value = first_result.params['A'].value
    alpha_s.value = first_result.params['alpha'].value
    phi_um_s.value = first_result.params['phi_um'].value

    params['A'].set(value=first_result.params['A'].value, vary=False)
    params['alpha'].set(value=first_result.params['alpha'].value, vary=False)
    params['phi_um'].set(value=first_result.params['phi_um'].value, vary=False)
    ##############################################################################
    params['gamma'].set(vary=True)
    params['beta'].set(vary=True)

    with output:
        display(HTML(value='<h3>Prosseguindo para Próxima Etapa</h3>'))
        display(params)

    second_result = minimize(
            retro_calc,
            params, 
            args=(w0_exp, temp, flow_m, disc))

    with output:
        display(HTML(value='<h3>Segunda Etapa Concluída</h3>'))
        display(report_fit(second_result))
        print('###################################################################')

    gamma_s.value = second_result.params['gamma'].value
    beta_s.value = second_result.params['beta'].value

    params['gamma'].set(value=first_result.params['gamma'].value, vary=False)
    params['beta'].set(value=first_result.params['beta'].value, vary=False)
    ##############################################################################
    params['delta'].set(vary=True)

    with output:
        display(HTML(value='<h3>Iniciando Terceira Etapa</h3>'))
        display(params)

    third_result = minimize(retro_calc, params, args=(w0_exp, temp, flow_m, pe_exp))

    with output:
        display(HTML(value='<h3>Terceira Etapa Concluída</h3>'))
        display(report_fit(third_result))

    delta_s.value = second_result.params['delta'].value
    ##############################################################################
