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
        ps_mat[i-1] = ps*100
        
    #wi_mc = np.ones((n_temp, n_inter)) - \
    #        np.divide(
    #                (np.subtract(freq_a, ps_mat[:,::-1].cumsum(1))**2), 
    #                ps_mat[:,::-1].cumsum(1)
    #                )[::-1]
    
    return (np.subtract(freq_a, ps_mat[:,::-1].cumsum(1))**2).sum(1)

    #wi_mc = np.ones((n_temp, n_inter)) - \
    #        np.divide(
    #                (np.subtract(disc[:,::-1].cumsum(1), ps_mat[:,::-1].cumsum(1))**2), 
    #                ps_mat[:,::-1].cumsum(1)
    #                )[::-1]
    #
    #return (wi_mc * (np.subtract(disc, ps_mat)**2)).sum(1)


def update_gran_plot():
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

def retro_calc_Austin(b):

    params = Parameters()

    # add with tuples: (NAME VALUE VARY MIN  MAX  EXPR  BRUTE_STEP)
    params.add_many( 
            ('mu', mu_s.value, False, mu_s.min, mu_s.max, None, 0.01), 
            ('_lambda', lambda_s.value, False, lambda_s.min, lambda_s.max, None, 0.01), 
            ('A', 0.0, True, A_s.min, A_s.max, None, 0.01), 
            ('alpha', alpha_s.value, True, alpha_s.min, alpha_s.max, None, 0.01), 
            ('delta', delta_s.value, False, delta_s.min, delta_s.max, None, 0.01), 
            ('phi_um', phi_um_s.value, True, phi_um_s.min, phi_um_s.max, None, 0.01), 
            ('gamma', gamma_s.value, True, gamma_s.min, gamma_s.max, None, 0.01), 
            ('beta', beta_s.value, True, beta_s.min, beta_s.max, None, 0.01)
            )

    output.clear_output()
    with output:
        display(
                HTML(value='<h1>RETROCALC</h1>'),
                HTML(value='<h3>Iniciando Primeira Etapa</h3>'),
                Label(
                    value='Varing the foloowing variables:\n $A$, $\\alpha$, $\gamma$, $\\beta$, $\Phi_1$'
                    ),
                params
                )

    first_result = minimize(
            retro_calc, 
            params, 
            args=(w0_exp, temp, flow_m, disc), 
            method=opt_m.value,
            )

    with output:
        display(HTML(value='<h4>Primeira Etapa Concluída</h4>'))
        print('###################################################################')
        display( report_fit(first_result) )
        print('###################################################################')

    A_s.value = first_result.params['A'].value
    alpha_s.value = first_result.params['alpha'].value
    phi_um_s.value = first_result.params['phi_um'].value
    gamma_s.value = first_result.params['gamma'].value
    beta_s.value = first_result.params['beta'].value
    update_gran_plot()

    ##############################################################################

    params['A'].set(value=first_result.params['A'].value, vary=False)
    params['alpha'].set(value=first_result.params['alpha'].value, vary=False)
    params['phi_um'].set(value=first_result.params['phi_um'].value, vary=False)
    params['gamma'].set(value=first_result.params['gamma'].value, vary=False)
    params['beta'].set(value=first_result.params['beta'].value, vary=False)
    params['delta'].set(vary=True)

    with output:
        display(
                HTML(value='<h3>Iniciando Segunda Etapa</h3>'),
                Label(
                    value='Varing the foloowing variables:\n \
                            $A$, $\\alpha$, $\gamma$, $\\beta$, $\Phi_1$, $\delta$'
                    ),
                params
                )

    second_result = minimize(
            retro_calc,
            params, 
            args=(w0_exp, temp, flow_m, disc),
            method=opt_m.value,
            )

    with output:
        display(HTML(value='<h4>Segunda Etapa Concluída</h4>'))
        print('###################################################################')
        display( report_fit(second_result) )
        print('###################################################################')

    #A_s.value = second_result.params['A'].value
    #alpha_s.value = second_result.params['alpha'].value
    #phi_um_s.value = second_result.params['phi_um'].value
    #gamma_s.value = second_result.params['gamma'].value
    #beta_s.value = second_result.params['beta'].value
    delta_s.value = second_result.params['delta'].value
    update_gran_plot()

    ###############################################################################

    params['mu'].set(vary=True)
    params['_lambda'].set(vary=True)
    #params['A'].set(value=second_result.params['A'].value, vary=False)
    #params['alpha'].set(value=second_result.params['alpha'].value, vary=False)
    #params['phi_um'].set(value=second_result.params['phi_um'].value, vary=False)
    #params['gamma'].set(value=second_result.params['gamma'].value, vary=False)
    #params['beta'].set(value=second_result.params['beta'].value, vary=False)
    params['delta'].set(value=second_result.params['delta'].value, vary=False)

    with output:
        display(
                HTML(value='<h3>Iniciando Terceira Etapa</h3>'),
                Label( value='Varing the foloowing variables:\n $\mu$, $\Lambda$' ),
                params
                )

    third_result = minimize(
            retro_calc, 
            params, 
            args=(w0_exp, temp, flow_m, disc),
            method=opt_m.value,
            )

    with output:
        display(HTML(value='<h4>Terceira Etapa Concluída</h4>'))
        print('###################################################################')
        display(report_fit(third_result))
        print('###################################################################')

    mu_s.value = third_result.params['mu'].value
    lambda_s.value = third_result.params['_lambda'].value
    update_gran_plot()
