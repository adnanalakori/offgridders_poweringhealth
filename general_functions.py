'''
Small scripts to keep the main file clean
'''

import pandas

from oemof.tools import logger
import logging

class config_func():
    def cases():
        from config import simulated_cases
        listof_cases = []
        for keys in simulated_cases:
            if simulated_cases[keys] == True: listof_cases.append(keys)

        str_cases_simulated = ''
        for item in listof_cases:
            str_cases_simulated = str_cases_simulated + item + ', '

        logging.info('The cases simulated are: ' + str_cases_simulated[:-2])
        return listof_cases

'''
The handler for information on the specific case analysed in the case study ("experiment")
'''

class extract():
    def fuel(experiment):
        experiment_fuel = {}
        experiment_fuel.update({'price_fuel': experiment['price_fuel']})
        experiment_fuel.update({'combustion_value_fuel': experiment['combustion_value_fuel']})
        return experiment_fuel

    def shortage(experiment):
        experiment_shortage = {}
        experiment_shortage.update({'max_share_unsupplied_load': experiment['max_share_unsupplied_load']})
        experiment_shortage.update({'var_costs_unsupplied_load': experiment['var_costs_unsupplied_load']})
        return experiment_shortage

    def maingrid(experiment):
        experiment_maingrid = {}
        experiment_maingrid.update({'price_electricity_main_grid': experiment['price_electricity_main_grid']})
        return experiment_maingrid

    def storage(experiment):
        experiment_storage = {}
        experiment_storage.update({'cost_annuity_storage': experiment['cost_annuity_storage']})
        experiment_storage.update({'cost_var_storage': experiment['cost_var_storage']})
        experiment_storage.update({'storage_Crate': experiment['storage_Crate']})
        experiment_storage.update({'storage_loss_timestep': experiment['storage_loss_timestep']})
        experiment_storage.update({'storage_inflow_efficiency': experiment['storage_inflow_efficiency']})
        experiment_storage.update({'storage_outflow_efficiency': experiment['storage_outflow_efficiency']})
        return experiment_storage

    def pcoupling(experiment):
        experiment_pcoupling = {}
        experiment_pcoupling.update({'cost_annuity_pcoupling': experiment['cost_annuity_pcoupling']})
        experiment_pcoupling.update({'cost_var_pcoupling': experiment['cost_var_pcoupling']})
        experiment_pcoupling.update({'efficiency_pcoupling': experiment['efficiency_pcoupling']})
        return experiment_pcoupling

    def genset(experiment):
        experiment_generator = {}
        experiment_generator.update({'cost_annuity_genset': experiment['cost_annuity_genset']})
        experiment_generator.update({'cost_var_genset': experiment['cost_var_genset']})
        experiment_generator.update({'efficiency_generator': experiment['efficiency_generator']})
        return experiment_generator

    def pv(experiment):
        experiment_pv = {}
        experiment_pv.update({'cost_annuity_pv': experiment['cost_annuity_pv']})
        experiment_pv.update({'cost_var_pv': experiment['cost_var_pv']})
        return experiment_pv