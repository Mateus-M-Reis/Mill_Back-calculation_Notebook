import pandas as pd
import numpy as np

df = pd.read_excel('./dados/input.xlsx', sheet_name='input', header=None, engine='openpyxl')

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
#######################################
disc = np.zeros((n_temp, n_inter))
disc = pe_exp.copy()
for i in range(n_temp):
    disc[:,8][i] = 1 - disc[i,:8].sum()

freq_a=disc.copy()
freq_a = freq_a[:,::-1]
######################################
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

wi = np.ones(n_inter)
wi_mc = np.zeros((n_temp,n_inter))
