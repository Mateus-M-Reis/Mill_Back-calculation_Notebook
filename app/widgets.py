from ipywidgets import (
        FloatSlider, Dropdown, Label, Checkbox, Button,
        HBox, VBox, Layout, HTML, HTMLMath, Output
        )

#S_title = Label(value='Função Seleção')
mu_s= FloatSlider(
        min=1.4,max=3.0,step=0.05,value=1.7,
        description='$\mu$',
        style={'description_width': '10%'},
        )
vary_mu_s = Checkbox(
        value=False, indent=False, layout={'width':'auto'})
lambda_s= FloatSlider(min=0.0,max=3.7,step=0.01,
        value=0.0, description='$\Lambda$',
        style={'description_width': '10%'},
        )
vary_lambda_s = Checkbox(
        value=False, indent=False, layout={'width':'auto'})
A_s= FloatSlider(
        min=0.01,max=4,step=0.01,value=0.1, 
        description='$A$',
        style={'description_width': '10%'},
        )
vary_A_s = Checkbox(
        value=True, indent=False, layout={'width':'auto'})
alpha_s= FloatSlider(
        min=0.5,max=1.5,step=0.01,value=0.88, 
        description='$\\alpha$',
        style={'description_width': '10%'},
        )
vary_alpha_s = Checkbox(
        value=True, indent=False, layout={'width':'auto'})

Si_eq = Label(
        value='$$ S_i = A(x_i/x_1)^\\alpha Q_i $$', 
        layout=Layout(
            height='60px', justfy_content = 'center'))
Qi_eq = Label(
        value='$$ Q_i = 1/(1+x_i/\mu)^\Lambda $$', 
        layout=Layout(
            height='60px', justfy_content = 'center'))

S_Panel = VBox([
    VBox([
        HBox([
            HBox([vary_A_s, A_s]), HBox([vary_alpha_s, alpha_s])],
            layout=Layout(overflow='hidden hidden')), 
        Si_eq]), 
    VBox([
        HBox([
            HBox([vary_mu_s, mu_s]), HBox([vary_lambda_s, lambda_s])],
            layout=Layout(overflow='hidden hidden')), 
        Qi_eq]) ])

delta_s= FloatSlider(
        min=0,max=0.25,step=0.01,value=0,
        description='$\delta$',
        style={'description_width': '10%'},)
vary_delta_s = Checkbox(
        value=False, indent=False, layout={'width':'auto'})
phi_um_s= FloatSlider(
        min=0.25,max=0.75,step=0.01,value=0.60, 
        description='$\Phi_1$',
        style={'description_width': '10%'},)
vary_phi_um_s = Checkbox(
        value=True, indent=False, layout={'width':'auto'})
gamma_s= FloatSlider(
        min=0.50,max=1.3,step=0.01,value=0.5, 
        description='$\gamma$',
        style={'description_width': '10%'})
vary_gamma_s = Checkbox(
        value=True, indent=False, layout={'width':'auto'})
beta_s= FloatSlider(
        min=2.3,max=5.8,step=0.01,value=4.0, 
        description='$\\beta$',
        style={'description_width': '10%'})
vary_beta_s = Checkbox(
        value=True, indent=False, layout={'width':'auto'})

Bij_eq = Label(
        value="$$ B_{i,j} = \Phi_j R^{(i-2)\gamma} + (1-\Phi_j) R^{(i-2)\\beta} $$",
        layout=Layout(
            height='60px',
            justfy_content = 'center'))
Phi_j_eq = Label(
        value='$$ \Phi_j = \Phi_1 (x_j/x_1)^{-\delta}$$',
        layout=Layout(
            height='60px',
            justfy_content = 'center'))

Q_Panel = VBox([
    VBox([
        HBox([ 
            HBox([vary_gamma_s, gamma_s]), 
            HBox([vary_beta_s, beta_s]) ],
            layout=Layout(overflow='hidden hidden')), 
        Bij_eq]), 
    VBox([
        HBox([ 
            HBox([vary_delta_s, delta_s]),
            HBox([vary_phi_um_s, phi_um_s]) ],
            layout=Layout(overflow='hidden hidden')), 
        Phi_j_eq]) ])

flow_m= Dropdown(
        options=[
            'batch-plug flow', 
            'fully mixed grinding', 
            'one large two small fully mixed reactors'
            ],
        value='batch-plug flow', 
        description='Flow Model:', 
        disabled=True,
        layout=Layout(width='100%'),
        style={'description_width': '27%'})

ej_eq = HTMLMath(
        value= "$ e_j = exp(-S_j \\tau) $", 
        layout={
            'border':'0px solid',
            'width':'405px', 
            'height':'80px',
            'align_items':'center',
            'justify_content':'center' })

Run_sim = Button(
        description='Simulate',
        tooltip='Rodar Simulação com os Parâmetros Atuais ',
        style={'width': '25%', 'min-width': '25%'})

Retro_buttom = Button(
        description='Retrocalc',
        tooltip=' Otimizar para Todas as Variaveis',
        button_style = 'success',
        style={'width': '25%'})

fit_buttom = Button(
        description='Cinetic Fit',
        tooltip='Cinetic Fit Breakage than Selection',
        button_style = 'primary',
        style={'width': '25%'})

ylog_ck = Checkbox(
        value=False, 
        description='Log Y', 
        layout = Layout( width='20%' ),
        style = { 'description_width': '0px' })
norm_ck = Checkbox(value=True, description='Normalizada?', 
        style = {'description_width': '0px'},
        layout=Layout(width='150px', justify_content='flex-end'))

retro_eq = HTMLMath(
        value="$$ minimize\ SSQ = \sum_k \sum_{i=1}^{n} w_i(p_i\nobserved\ -p_i\ computed\ ) $$")

output = Output()
output.layout = Layout(
        width='65%', 
        height='99%', 
        #border='1px solid gray',
        overflow='hidden visible'
        )

opt_m = Dropdown(
        options=[
            'leastsq', 
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
            'dual_annealing' ],
        value='leastsq', 
        description='Optimization Method:', 
        disabled=False,
        style = { 
            'description_width': '65%',
            'width': '25%', 'min-width': '25%' })
