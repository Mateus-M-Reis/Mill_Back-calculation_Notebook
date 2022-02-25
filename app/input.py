import pandas as pd
import numpy as np

df = pd.read_excel('./dados/input.xlsx', sheet_name='input', header=None, engine='openpyxl')

n_temp = np.int(df.iloc[0,1])
n_inter = np.int(df.iloc[0,2])

temp = df.iloc[1,0:int(n_temp)].values
si_exp = df.iloc[3,0:int(n_inter)].values*100

w0_exp = df.iloc[4,0:int(n_inter)].values

#######################################
disc = df.iloc[5:int(n_temp)+5, 0:int(n_inter)].values
freq_a = np.ones([n_temp, n_inter])*100 - disc.cumsum(1)[:,::-1]
#######################################

size_mm = df.iloc[2,0:int(n_inter)].values
size_mm_u = np.insert(size_mm, 0, 1.7, 0)[:-1]

Si= np.zeros(n_inter)

Bij = np.zeros((n_inter, n_inter))
bij = np.zeros((n_inter,n_inter))

##############################################################################

n_temp_cf = np.int(df.iloc[12, 1])
n_inter_cf = np.int(df.iloc[12, 2])

temp_cf = df.iloc[13, 0:n_temp_cf].values

size_mm_cf = df.iloc[14, 0:n_inter_cf].values/1000
w0_cf = df.iloc[15, 0:n_inter_cf].values

f_acum_cf = df.iloc[16:18, 0:n_inter_cf].values

Bi1 = np.zeros((n_inter_cf, n_inter_cf))
