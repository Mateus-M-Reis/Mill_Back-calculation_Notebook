from ipywidgets import VBox, HBox, Layout

from .widgets import *
from .figures import *

wids = HBox(
        [Run_sim, Retro_buttom, fit_buttom, opt_m ],
        layout=Layout(
            #border='1px solid red', 
            width = '100%',
            height = '5%', min_height = '5%',
            overflow='hidden hidden',
            align_items='center',
            )
        )

sim_ctrls = VBox([

            wids, 

            VBox(
                [ylog_ck, gran_fig], 
                layout=Layout(
                    width='100%',
                    height='50%', #min_height='50%',
                    overflow='hidden hidden',
                    ),
                style = { 'justify-content': 'space-around' }
                ),

            HBox([

                VBox(
                    [ s_fig, S_Panel ],
                    layout=Layout(
                        display='flex', 
                        #border='solid 0px', 
                        align_items='stretch', 
                        justify_content='space-between',
                        overflow='hidden hidden',
                        )), 

                VBox(
                    [ q_fig, Q_Panel ],
                    layout=Layout(
                        display='flex', 
                        #border='solid 0px', 
                        align_items='stretch', 
                        justify_content='space-between',
                        overflow='hidden hidden',)) 

                    ], 
                    layout=Layout(
                        display='flex', 
                        #border='1px solid white', 
                        align_items='stretch', 
                        justify_content='space-between', 
                        width = '100%',
                        height = '45%', min_height = '45%',
                        overflow='hidden hidden')
                    ), 

        ])

panel = HBox(
        [ sim_ctrls , output ], 
        layout=Layout(
            height= '95vh',
            width= '99%',
            overflow= 'hidden hidden'
            ),
        style = { 'justify_content': 'space-between' }
        )
