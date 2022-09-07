import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.formula.api as smf
from stargazer.stargazer import Stargazer, LineLocation
from IPython.core.display import HTML
import math

#Set necessary variable in the global space
path = r'C:\Users\Kemin\Desktop\Noto task to send'
fname= 'Noto_data_task.csv'
trend_break = 1992

#Load the data
df = pd.read_csv(os.path.join(path, fname))

#Creat the time trend variable
df.loc[:, 't'] = df.loc[:, 'year']-1963

#Funcitions that help create trend break variable
def years_after_trend_break(df):    
   return df['year']-trend_break if df['year'] > trend_break else 0


def post_year_indicator(df):    
   return 1 if df['year'] > trend_break else 0

#Q1

#Model for Detrended Wage Differential 
detrended_model_1 = smf.ols('clphsg_all ~ t', data=df)

detrended_result_1 = detrended_model_1.fit()

df['residual_1'] = df['clphsg_all'] - detrended_result_1.predict()

#Model for Detrended Relative Supply
detrended_model_2 = smf.ols('eu_lnclg ~ t', data=df)

detrended_result_2 = detrended_model_2.fit()

df['residual_2'] = df['eu_lnclg'] - detrended_result_2.predict()

#Katz-Murphy Model
katz_period = range(1963, 1988)

df_katz = df[df['year'].isin(katz_period)]

katz_model = smf.ols('clphsg_all ~ t + eu_lnclg', data=df_katz)

katz_result = katz_model.fit()

#Get fitted value of this model through year 2008
df['katz_predict'] = katz_result.params[0] + katz_result.params[1]*df['t'] + katz_result.params[2]*df['eu_lnclg']


#Reproduce Figure 4

fig, axs = plt.subplots(2,1, figsize=(16,16), gridspec_kw={'height_ratios': [1, 1]})

#Graph A
axs[0].plot(df['year'], df['residual_1'], linestyle='solid', marker='o',
        markersize=4, label ='Detrended Wage Differential')

axs[0].plot(df['year'], df['residual_2'], linestyle='dashed', marker='o',
        markersize=4, label='Detrended Relative Supply')

axs[0].axhline(0, color='black', linewidth=1)

axs[0].xaxis.set_ticks(np.arange(min(df['year']), max(df['year']), 6))

axs[0].yaxis.set_ticks(np.arange(-0.15, 0.20, 0.05))

axs[0].legend(loc='upper center', bbox_to_anchor=(0.5, -0.03),
          fancybox=True, shadow=True, ncol=2)

axs[0].set_title('A. Detrended College/High School Wage Differential and Relative Supply, 1963-2008')

axs[0].set_ylabel('Log Points')

#Graph B
axs[1].plot(df['year'], df['clphsg_all'], linestyle='solid', marker='o',
        markersize=4, label ='Observed CLG/HS Gap')

axs[1].plot(df['year'], df['katz_predict'], linestyle='dashed', marker='o',
        markersize=4, label ='Katz-Murphy Predicted Wage Gap: 1963-1987 Trend')

axs[1].axvline(1987, color='black', linewidth=1)

axs[1].axvline(1992, color='black', linewidth=1)

axs[1].xaxis.set_ticks(np.arange(min(df['year']), max(df['year']), 6))

axs[1].yaxis.set_ticks(np.arange(0.35, 0.80, 0.10))

axs[1].legend(loc='upper center', bbox_to_anchor=(0.5, -0.03),
          fancybox=True, shadow=True, ncol=2)

axs[1].set_title('B. Katz-Murphy Prediction Model for the College/High School Wage Gap')

axs[1].set_ylabel('Log Wages Gap')


plt.tight_layout()

plt.show()

fig.savefig('Figure 4.png')

#Q2


#Reproduce table 2

# Table 2 Column 1

col1_result = katz_result

#Table 2 Column 2 

col2_model = smf.ols('clphsg_all ~ t + eu_lnclg', data=df)

col2_result = col2_model.fit()

#Table 2 Column 3

#Assume trend_break is in 1992

df['t_after_trend_break'] = df.apply(years_after_trend_break, axis=1)
df['post_trend_break'] = df.apply(post_year_indicator, axis=1)
df['t_x_post_trend_break'] = df['t_after_trend_break']*df['post_trend_break']

col3_model = smf.ols('clphsg_all ~ t + eu_lnclg + t_x_post_trend_break', data=df)

col3_result = col3_model.fit()

#Table 2 Column 4

df['t_quadratic'] = (df['t']**2)/100

col4_model = smf.ols('clphsg_all ~ t + t_quadratic + eu_lnclg', data=df)

col4_result = col4_model.fit()

#Table 2 Column 5

df['t_cubic'] = (df['t']**3)/1000

col5_model = smf.ols('clphsg_all ~ t + t_quadratic + t_cubic + eu_lnclg', data=df)

col5_result = col5_model.fit()

#Create regression table using Stargazer
stargazer = Stargazer([col1_result,col2_result,col3_result,col4_result,col5_result])

stargazer.dependent_variable_name('')

stargazer.title('REGRESSION MODELS FOR THE COLLEGE/HIGH SCHOOL LOG WAGE GAP, 1963-2008')

stargazer.covariate_order(['eu_lnclg', 't', 't_quadratic', 't_cubic', 't_x_post_trend_break', 'Intercept'])

stargazer.rename_covariates({'eu_lnclg': 'CLG/HS relative supply', 't': 'Time', 't_quadratic': 'Time^2/100',
                             't_cubic': 'Time^3/1000','t_x_post_trend_break': 'Time*post-1992',
                             'Intercept': 'Constant'})

stargazer.add_line('Elasticity of substitution', [round((1/-0.612),3), round((1/-0.339),3), 
                                                  round((1/-0.644),3), round((1/-0.562),3), 
                                                  round((1/-0.556),3)])

stargazer.add_line('', [f'({round(math.sqrt((1/-0.612)**4*(0.128)**2),3)})', 
                        f'({round(math.sqrt((1/-0.339)**4*(0.043)**2),3)})',
                        f'({round(math.sqrt((1/-0.644)**4*(0.066)**2),3)})',
                        f'({round(math.sqrt((1/-0.562)**4*(0.112)**2),3)})',
                        f'({round(math.sqrt((1/-0.556)**4*(0.094)**2),3)})'])
                        

stargazer.add_line('p-value for Elasticity of substitution', [0.000, 0.000, 0.000, 0.000, 0.000])

#Save it as html                   
result_table = stargazer.render_html()

with open("Table 2.html", "w") as file:
    file.write(result_table)

#Q3


#Loop to obtain all Rsquare from models with diffrent trend break assumptions

trend_break_Rsquare_list = []

for trend_break in range(1964, 2008):
    trend_break = trend_break
    df['t_after_trend_break'] = df.apply(years_after_trend_break, axis=1)
    df['post_trend_break'] = df.apply(post_year_indicator, axis=1)
    df['t_x_post_trend_break'] = df['t_after_trend_break']*df['post_trend_break']
    max_Rsquare_model = smf.ols('clphsg_all ~ t + eu_lnclg + t_x_post_trend_break', data=df)
    max_Rsquare_result =  max_Rsquare_model.fit()
    max_Rsquare = max_Rsquare_result.rsquared
    trend_break_Rsquare_list.append(max_Rsquare)

#Print out the trend break year that makes the largest Rsquare and the Rsquare
for trend_break, max_Rsquare in zip(range(1964, 2008),trend_break_Rsquare_list):
    if max_Rsquare == max(trend_break_Rsquare_list):
        print(f'The trend break year that can maximize Rsquare is {trend_break}, and the Rsquare is {round(max_Rsquare, 3)}')
        
    
