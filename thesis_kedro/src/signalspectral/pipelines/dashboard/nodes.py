"""
This is a boilerplate pipeline 'dashboard'
generated using Kedro 0.18.0
"""

import matplotlib.pyplot as plt
import datetime
import numpy as np
from matplotlib import cm
from kedro.extras.datasets.matplotlib import MatplotlibWriter

def create_dashboard(df, dfmm, dfc, dfcf,
                     df_f, df_t, df_Sxx,
                     df_lines, df_KL, df_components,
                     dfT, dfMMS, dfAVG, dfO, dfIG, dfPC,
                     name):
    """"use matplotlib to create dashboard including all performance indicators from preprocessing and spectral analysis
    as well as the warnings from evaluation"""

    fig, axs = plt.subplots(15, figsize=(10, 20), constrained_layout=True)
    fig.suptitle('Analysis Dataset {}'.format(name), y=1.01)

    # plot original temperature data
    axs[0].plot(df['EventDt'], df['Temp'], label='Temperature')
    axs[0].set_title("Temperature")
    axs[0].set_xlabel("Date")
    axs[0].set_ylabel("Temperature [°C]")
    axs[0].legend(['Temperature'], loc='center left', bbox_to_anchor=(1, 0.5),
                  fancybox=True, shadow=True)

    # plot daily minimum and maximum temperature
    axs[2].plot(dfmm['EventDt'], dfmm['max Temp'], label='max Temperature', color='red')
    axs[2].plot(dfmm['EventDt'], dfmm['min Temp'], label='min Temperature', color='royalblue')
    axs[2].set_title("Daily minimum and maximum temperature")
    axs[2].set_xlabel("Date")
    axs[2].set_ylabel("Temperature [°C]")
    axs[2].legend(['Maximum temperature', 'Minimum temperature'], loc='center left', bbox_to_anchor=(1, 0.5),
                  fancybox=True, shadow=True)

    # plot one day Tukey window convoluted temperature as average temperature
    axs[4].plot(dfc['EventDt'], dfc['gauss_1day'], label='avg Temperature')
    axs[4].set_title("Temperature average (1-day Tukey convolution)")
    axs[4].set_xlabel("Date")
    axs[4].set_ylabel("Temperature [°C]")
    axs[4].legend(['Average temperature'], loc='center left', bbox_to_anchor=(1, 0.5),
                  fancybox=True, shadow=True)

    # plot daily standard deviation of the temperature
    axs[6].plot(dfmm['EventDt'], dfmm['std Temp'], label='SD')
    axs[6].set_title("Daily temperature standard deviation")
    axs[6].set_xlabel("Date")
    axs[6].set_ylabel("Temperature [°C]")
    axs[6].legend(['Temperature SD'], loc='center left', bbox_to_anchor=(1, 0.5),
                  fancybox=True, shadow=True)
    #####
    ###
    #

    f = df_f.T.to_numpy()[0]
    t = df_t.T.to_numpy()[0]
    Sxx = df_Sxx.to_numpy()

    # create corresponding date xaxis for the spectral performance indicators
    end_date = dfcf['EventDt'].iloc[-1]
    start_date = dfcf['EventDt'].iloc[0]
    timestep = (end_date - (start_date + datetime.timedelta(seconds=t[0]))) / len(t)
    xmin, xmax = axs[0].get_xlim()
    t_dates = [start_date + timestep * i for i in range(1, len(t) + 1)]

    #
    ###
    #####
    # PLOT SPECTRAL PERFORMANCE INDICATORS
    # plot the spectrogram
    axs[8].pcolormesh(t_dates, f, np.log10(Sxx), shading='gouraud')
    axs[8].set_xlim((xmin, xmax))
    axs[8].set_yscale('symlog')
    axs[8].set_title("Spectrogram")
    axs[8].set_xlabel("Date")
    axs[8].set_ylabel("Frequency [Hz]")
    sm = plt.cm.ScalarMappable(cmap=cm.viridis, norm=plt.Normalize(vmin=0, vmax=1))
    cbar = fig.colorbar(sm, ax=axs[8], location='right', ticks=[0, 1], aspect=10)
    cbar.ax.set_yticklabels(['Low', 'High'])

    df_lines.columns = df_lines.columns.astype(int)
    lines = df_lines.to_dict(orient='list')
    # plot the absolute octave intensities as a heatmap line per octave
    for i in range(1, len(lines) + 1):
        y = [i for j in range(len(lines[i]))]
        axs[9].scatter(x=t_dates, y=y, c=cm.viridis_r(np.abs([k / max(lines[i]) if k != 0 else 0 for k in lines[i]])),
                       edgecolor='none')
    axs[9].set_yticks([1, 2, 3, 4, 5])
    axs[9].set_title("Sum of intensities per octave")
    axs[9].set_xlabel("Date")
    axs[9].set_ylabel("Octave")
    sm = plt.cm.ScalarMappable(cmap=cm.viridis_r, norm=plt.Normalize(vmin=0, vmax=1))
    cbar = fig.colorbar(sm, ax=axs[9], location='right', ticks=[0, 1], aspect=10)
    cbar.ax.set_yticklabels(['Low', 'High'])

    df_KL.columns = df_KL.columns.astype(int)
    # plot entropy = information gain of the spectrum
    axs[11].plot(t_dates, df_KL[1], label='KL divergence', color='g')
    axs[11].set_title("Information gain")
    axs[11].set_xlabel("Date")
    axs[11].set_ylabel("Kullback-Leibner divergence")
    axs[11].legend(['Kullback-Leibner divergence'], loc='center left', bbox_to_anchor=(1, 0.5),
                   fancybox=True, shadow=True)

    df_components.columns = df_components.columns.astype(int)
    components = df_components.to_numpy()
    # plot first two principal components of the ocatve intensities
    axs[13].set_prop_cycle('color', ['limegreen', 'gold'])
    axs[13].plot(t_dates, components)
    axs[13].set_title("Principal components of octave intensities")
    axs[13].set_xlabel("Date")
    axs[13].set_ylabel("Principal component")
    axs[13].legend(['PC 1', 'PC 2'], loc='center left', bbox_to_anchor=(1, 0.5),
                   fancybox=True, shadow=True)
    #####
    ###
    #

    #
    ###
    #####
    # PLOT WARNINGS (EVALUATION)
    # plot temperature warnings
    axs[1].plot(dfT['EventDt'], dfT['warnings_temp'])
    axs[1].set_title("Temperature evaluation")
    axs[1].set_ylim([-1, 1])
    axs[1].axes.get_xaxis().set_visible(False)
    axs[1].legend(['Temperature warnings'], loc='center left', bbox_to_anchor=(1, 0.5),
                  fancybox=True, shadow=True)
    axs[0].get_shared_x_axes().join(axs[0], axs[1])

    # plot minimum and maximum warnings
    axs[3].set_prop_cycle('color', ['royalblue', 'red'])
    axs[3].plot(dfMMS['EventDt'], dfMMS[['warnings_min', 'warnings_max']])
    axs[3].set_title("Temperature minimum and maximum evaluation")
    axs[3].set_ylim([-1, 1])
    axs[3].axes.get_xaxis().set_visible(False)
    axs[3].legend(['Minimum temperature warnings', 'Maximum temperature warnings'], loc='center left',
                  bbox_to_anchor=(1, 0.5),
                  fancybox=True, shadow=True)
    axs[2].get_shared_x_axes().join(axs[2], axs[3])

    # plot average temperature warnings
    axs[5].plot(dfAVG['EventDt'], dfAVG['warnings_avg'])
    axs[5].set_title("Temperature average evaluation")
    axs[5].set_ylim([-1, 1])
    axs[5].axes.get_xaxis().set_visible(False)
    axs[5].legend(['Average temperature warnings'], loc='center left', bbox_to_anchor=(1, 0.5),
                  fancybox=True, shadow=True)
    axs[4].get_shared_x_axes().join(axs[4], axs[5])

    # plot temperature standard deviation warnings
    axs[7].plot(dfMMS['EventDt'], dfMMS['warnings_std'])
    axs[7].set_title("Temperature standard deviation evaluation")
    axs[7].set_ylim([-1, 1])
    axs[7].axes.get_xaxis().set_visible(False)
    axs[7].legend(['Temperature SD warnings'], loc='center left', bbox_to_anchor=(1, 0.5),
                  fancybox=True, shadow=True)
    axs[6].get_shared_x_axes().join(axs[6], axs[7])

    # plot octave intensities warnings
    axs[10].plot(t_dates, dfO[['warnings_oct1', 'warnings_oct2', 'warnings_oct3', 'warnings_oct4', 'warnings_oct5']])
    axs[10].set_title("Octave intensities evaluation")
    axs[10].set_ylim([-1, 1])
    axs[10].axes.get_xaxis().set_visible(False)
    axs[10].legend(['warnings oct1', 'warnings oct2', 'warnings oct3', 'warnings oct4', 'warnings oct5'], loc='center left',
                   bbox_to_anchor=(1, 0.5),
                   fancybox=True, shadow=True)
    axs[9].get_shared_x_axes().join(axs[9], axs[10])

    # plot information gain warnings
    axs[12].plot(t_dates, dfIG['warnings_IG'], color='g')
    axs[12].set_title("Information gain evaluation")
    axs[12].set_ylim([-1, 1])
    axs[12].axes.get_xaxis().set_visible(False)
    axs[12].legend(['Information gain warnings'], loc='center left', bbox_to_anchor=(1, 0.5),
                   fancybox=True, shadow=True)
    axs[11].get_shared_x_axes().join(axs[11], axs[12])

    # plot principal components warnings
    axs[14].set_prop_cycle('color', ['limegreen', 'gold'])
    axs[14].plot(t_dates, dfPC[['warnings_PC0', 'warnings_PC1']])
    axs[14].set_title("Principal components of octave intensities evaluation")
    axs[14].set_ylim([-1, 1])
    axs[14].axes.get_xaxis().set_visible(False)
    axs[14].legend(['warnings PC1', 'warnings PC2'], loc='center left', bbox_to_anchor=(1, 0.5),
                   fancybox=True, shadow=True)
    axs[13].get_shared_x_axes().join(axs[13], axs[14])

    # save figure to specified path
    single_plot_writer = MatplotlibWriter(filepath="data/03_primary/dashboard_{}.png".format(name))
    single_plot_writer.save(fig)
    #####
    ###
    #