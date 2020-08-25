"""
Small scripts to keep the main file clean
"""

import pandas as pd
from src.constants import (
    CAPACITY_PV_KWP,
    CAPACITY_WIND_KW,
    CAPACITY_STORAGE_KWH,
    POWER_STORAGE_KW,
    CAPACITY_GENSET_KW,
    CAPACITY_PCOUPLING_KW,
    CAPACITY_RECTIFIER_AC_DC_KW,
    CAPACITY_INVERTER_DC_AC_KW,
    DEMAND_PROFILE,
)

from oemof.tools import logger
import logging

import matplotlib.pyplot as plt


def plot_results(pandas_dataframe, title, xaxis, yaxis):
    r"""
    Plots the results contained in pandas_dataframe

    Parameters
    ----------
    pandas_dataframe : Pandas DataFrame
                      Dataframe containing the results
    title : str
            title of the figure
    xaxis : str
            label for the x axis
    yaxis : str
            label for the y axis


    Returns
    -------
    Plots the correspoding DataFrame

    """
    """ general function for plots"""
    if plt is not None:
        # Plot demand
        ax = pandas_dataframe.plot()
        ax.set_title(title)
        ax.set_xlabel(xaxis)
        ax.set_ylabel(yaxis)
        plt.show()
    return


def define_base_capacities(oemof_results):
    """

    Parameters
    ----------
    oemof_results : Dictionary containing the oemof-results

    Returns
    -------
    capacities_base : Dictionary containing the selected

    """
    capacities_base = {
        CAPACITY_PV_KWP: oemof_results[CAPACITY_PV_KWP],
        CAPACITY_WIND_KW: oemof_results[CAPACITY_WIND_KW],
        CAPACITY_STORAGE_KWH: oemof_results[CAPACITY_STORAGE_KWH],
        POWER_STORAGE_KW: oemof_results[POWER_STORAGE_KW],
        CAPACITY_GENSET_KW: oemof_results[CAPACITY_GENSET_KW],
        CAPACITY_PCOUPLING_KW: oemof_results[CAPACITY_PCOUPLING_KW],
        CAPACITY_RECTIFIER_AC_DC_KW: oemof_results[CAPACITY_RECTIFIER_AC_DC_KW],
        CAPACITY_INVERTER_DC_AC_KW: oemof_results[CAPACITY_INVERTER_DC_AC_KW],
    }
    return capacities_base


def store_result_matrix(overall_results, experiment, oemof_results):
    """
    Storing results to vector and then result matrix for saving it in csv.
    """
    round_to_comma = 5
    result_series = pd.Series()

    for key in overall_results.columns.values:
        # Check if called value is in oemof results -> Remember: check if pandas index has certain index: pd.object.index.contains(key)
        if key in oemof_results:
            if isinstance(oemof_results[key], str):
                result_series = result_series.append(
                    pd.Series([oemof_results[key]], index=[key])
                )
            else:
                result_series = result_series.append(
                    pd.Series([round(oemof_results[key], round_to_comma)], index=[key])
                )
        # extend by item of demand profile
        elif key == DEMAND_PROFILE:
            result_series = result_series.append(
                pd.Series([experiment[key]], index=[key])
            )
        # Check if called value is a parameter of sensitivity_experiment_s
        elif key in experiment:
            if isinstance(experiment[key], str):
                result_series = result_series.append(
                    pd.Series([experiment[key]], index=[key])
                )
            else:
                result_series = result_series.append(
                    pd.Series([round(experiment[key], round_to_comma)], index=[key])
                )

    result_series = result_series.reindex(overall_results.columns, fill_value=None)

    overall_results = overall_results.append(
        pd.Series(result_series), ignore_index=True
    )

    return overall_results
