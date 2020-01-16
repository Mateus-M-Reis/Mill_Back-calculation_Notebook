# Mill_Back-calculation_Notebook
Notebook for interactive simulation and determination of ball milling breakage parameters, built on top of [numpy](https://github.com/numpy/numpy), [lmfit](https://github.com/lmfit/lmfit-py), [ipywidgets](https://github.com/jupyter-widgets/ipywidgets) and [bqplot](https://github.com/bloomberg/bqplot).

![](https://github.com/Mateus-M-Reis/Mill_Back-calculation_Notebook/blob/master/gifs/retro_gif%20(cópia).gif)

# Installation

Create new conda environment:

`conda create -n millSim_env python=3`

activate env

`source activate millSim_env`

install packages:

`conda install -c conda-forge notebook jupyterlab ipywidgets bqplot voila`

`pip install lmfit`

enable JupyterLab extensions

`jupyter labextension install @jupyter-widgets/jupyterlab-manager bqplot`
