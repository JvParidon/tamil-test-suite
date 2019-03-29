import csv
import os
import numpy as np
import pandas as pd
import pymc3 as pm
from bambi import Model
import matplotlib.pyplot as plt
import seaborn as sns

def tsv_to_df(experiment):
    dfs = []
    path = os.path.join('data/', experiment)
    for subject in sorted(os.listdir(path)):
        if os.path.isdir(os.path.join(path, subject)):
            for filename in sorted(os.listdir(os.path.join(path, subject))):
                if filename.endswith('.tsv'):
                    # print(subject + ' ' + filename)
                    df = pd.read_csv(os.path.join(path, subject, filename), sep='\t')
                    if experiment == 'Cambridge':
                        if 'cars' in filename:
                            df = df[['condition1', 'RT', 'ACC', 'literate', 'number']]
                            df = df.rename(columns={'condition1': 'trialNo'})
                            df['trialNo'] = df['trialNo'].apply(lambda x: pd.to_numeric(x, errors='coerce'))
                            df = df.dropna()
                            df = df[df['trialNo'] > 18]
                            df['category'] = 'cars'
                        elif 'bikes' in filename:
                            df = df[['stim1', 'RT', 'ACC', 'literate', 'number']]
                            df = df.rename(columns={'stim1': 'trialNo'})
                            df['trialNo'] = df['trialNo'].apply(lambda x: pd.to_numeric(x, errors='coerce'))
                            df = df.dropna()
                            df = df[df['trialNo'].astype(int) > 21]
                            df['category'] = 'bikes'
                        elif 'faces' in filename:
                            df = df[['trialNo', 'RT', 'ACC', 'literate', 'number']]
                            df['trialNo'] = df['trialNo'].apply(lambda x: pd.to_numeric(x, errors='coerce'))
                            df = df.dropna()
                            df = df[df['trialNo'] > 18]
                            df['category'] = 'faces'
                    elif experiment == 'Ravens':
                        df = df[['picture', 'RT', 'ACC', 'literate', 'number']]
                        df = df.rename(columns={'picture': 'item'})
                        df = df[df['ACC'].notnull()]
                        df['list'] = filename[0]
                        df['list_binary'] = 0 if (filename[0] == 'a') else 1
                    elif experiment == 'Illusions':
                        df = df[['Trialnumber', 'IllusionType', 'Condition', 'RT', 'ACC', 'literate', 'number']]
                        df = df[df['ACC'].notnull()]
                    df['pp'] = df['literate'] + '_' + df['number'].astype(str)
                    df['subject'] = subject
                    dfs += [df]
    df = pd.concat(dfs, sort=False)
    df['literate_binary'] = pd.get_dummies(df['literate'])['y']
    return df

if __name__ == '__main__':
    selected_experiment = 'Illusions'

    if selected_experiment == 'Illusions':
        df = tsv_to_df('Illusions')
        df.to_csv('illusions.tsv', sep='\t')

        g = sns.catplot(hue='literate', y='ACC', x='Condition', kind='violin', data=df.groupby(['pp', 'literate', 'Condition'], as_index=False).mean())
        plt.show()

        df = df[df['literate'] != 'low']
        df = df[df['IllusionType'] != 'ambiguous']
        df['control'] = pd.get_dummies(df['Condition'])['control']
        df['colour'] = pd.get_dummies(df['IllusionType'])['colour']

        model = Model(df)
        results = model.fit('ACC ~ literate_binary + control + colour + literate_binary:control + literate_binary:colour + control:colour', random=['1|Trialnumber', '1|pp'], samples=5000, tune=1000, chains=3, cores=3, family='bernoulli')
        pm_model = model.backend.model
        pm.model_to_graphviz(pm_model).view()
        trace = model.backend.trace
        print(trace.varnames)
        print(pm.summary(trace, varnames=['Intercept', 'literate_binary', 'control', 'colour', 'literate_binary:control', 'literate_binary:colour', 'control:colour'], transform=np.exp))
        pm.traceplot(trace, transform=np.exp)
        plt.show()
        pm.plot_posterior(trace, kde_plot=True, varnames=['Intercept', 'literate_binary', 'control', 'colour', 'literate_binary:control', 'literate_binary:colour', 'control:colour'], transform=np.exp)
        plt.show()

    elif selected_experiment == 'Ravens':
        df = tsv_to_df('Ravens')
        df.to_csv('ravens.tsv', sep='\t')

        g = sns.FacetGrid(df, row='ACC', col='literate', margin_titles=True)
        g.map(sns.distplot, 'RT', bins=np.arange(0, 40, 5), kde=False)  #norm_hist=False)
        g.set(xlim=(0, 50))
        plt.show()

        print(df['literate'].value_counts())
        print(df.groupby('literate').mean())
        df = df[df['literate'] != 'low']
        print(df.groupby(['literate_binary', 'list_binary']).mean())

        model = Model(df)
        results = model.fit('ACC ~ literate_binary * list_binary', random=['1|item', '1|pp'], samples=5000, tune=1000, chains=3, cores=3, family='bernoulli')
        pm_model = model.backend.model
        pm.model_to_graphviz(pm_model).view()
        trace = model.backend.trace
        print(trace.varnames)
        print(pm.summary(trace, varnames=['Intercept', 'literate_binary', 'list_binary', 'literate_binary:list_binary'], transform=np.exp))
        pm.traceplot(trace, transform=np.exp)
        plt.show()
        pm.plot_posterior(trace, kde_plot=True, varnames=['Intercept', 'literate_binary', 'list_binary', 'literate_binary:list_binary'], transform=np.exp)
        plt.show()

    elif selected_experiment == 'Cambridge':
        df = tsv_to_df('Cambridge')
        df.to_csv('cambridge.tsv', sep='\t')

        print(df['literate'].value_counts())
        print(df.groupby('literate').mean())
        print(df.groupby(['literate_binary', 'category']).mean())

        df = df[df['literate'] != 'low']

        df['cars'] = pd.get_dummies(df['category'])['cars']
        df['faces'] = pd.get_dummies(df['category'])['faces']

        model = Model(df)
        results = model.fit('ACC ~ literate_binary + cars + faces + literate_binary:cars + literate_binary:faces', random=['1|trialNo', '1|pp'], samples=5000, tune=1000, chains=3, cores=3, family='bernoulli')
        pm_model = model.backend.model
        pm.model_to_graphviz(pm_model).view()
        trace = model.backend.trace
        print(trace.varnames)
        print(pm.summary(trace, varnames=['Intercept', 'literate_binary', 'cars', 'faces', 'literate_binary:cars', 'literate_binary:faces'], transform=np.exp))
        pm.traceplot(trace, transform=np.exp)
        plt.show()
        pm.plot_posterior(trace, kde_plot=True, varnames=['Intercept', 'literate_binary', 'cars', 'faces', 'literate_binary:cars', 'literate_binary:faces'], transform=np.exp)
        plt.show()
