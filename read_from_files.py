import pandas as pd

# requires xlrd

class csv_input():
    def project_site_timeseries(experiments, project_sites):

        for project_site in project_sites:
            demand, pv_generation_per_kWp, wind_generation_per_kW = csv_input.from_file(project_site)

        for experiment in experiments:
            for project_site in project_sites:
                if experiment['project_site_name']==project_site['project_site_name']:
                    experiment.update({'demand': demand,
                                       'pv_generation_per_kWp': pv_generation_per_kWp,
                                       'wind_generation_per_kW': wind_generation_per_kW})

        return

    def from_file(project_site):
        data_set = pd.read_csv(project_site['timeseries_file'])

        # Anpassen des timestamps auf die analysierte Periode
        index = pd.DatetimeIndex(data_set[project_site['title_demand']].values)
        index = [item + pd.DateOffset(year=date_time_index[0].year) for item in index]

        # reading pv_generation values - adjust to panel area or kWp and if in Wh!
        pv_generation_per_kWp = pd.Series(data_set[project_site['title_pv']].values, index=index)
        wind_generation_per_kW = pd.Series(data_set[project_site['title_wind']].values, index=index)

        logging.info(
            'Total annual pv generation at project site (kWh/a/kWp): ' + str(round(pv_generation_per_kWp.sum())))

        if display_graphs_solar == True:
            helpers.plot_results(pv_generation_per_kWp[date_time_index], "PV generation at project site",
                                 "Date",
                                 "Power kW")

        return demand[date_time_index], pv_generation_per_kWp[date_time_index], wind_generation_per_kW[date_time_index]

class excel_template():

    def settings():
        file = './inputs/input_template_excel.xlsx'
        sheet_settings = 'settings'
        sheet_input_constant = 'input_constant'
        sheet_input_sensitivity = 'input_sensitivity'
        sheet_project_sites = 'project_sites'
        sheet_case_definitions = 'case_definitions'

        settings = excel_template.get_settings(file, sheet_settings)
        parameters_constant_units, parameters_constant_values = excel_template.get_parameters_constant(file, sheet_input_constant)
        parameters_sensitivity = excel_template.get_parameters_sensitivity(file, sheet_input_sensitivity)
        project_sites = excel_template.get_project_sites(file, sheet_project_sites)
        case_definitions = excel_template.get_case_definitions(file, sheet_case_definitions)
        return settings, parameters_constant_values, parameters_sensitivity, project_sites, case_definitions

    def get_data(file, sheet, header_row, index_column, last_column):
        data = pd.read_excel(file,
                             sheet_name=sheet,
                             header=header_row-1,
                             index_col=0,
                             usecols=index_column+":"+last_column)
        data = data.dropna()
        return data

    def identify_true_false(entry):
        if entry == 'True':
            entry = True
        elif entry == 'False':
            entry = False
        else:
            pass

        return entry

    def get_settings(file, sheet_settings):
        settings = excel_template.get_data(file, sheet_settings, 11, "B", "C")
        settings = settings.to_dict(orient='dict')
        settings = settings['setting_value']
        # Translate strings 'True' and 'False' from excel sheet to True and False
        for key in settings:
            settings[key] = excel_template.identify_true_false(settings[key])
        return settings

    def get_parameters_constant(file, sheet_input_constant):
        parameters_constant = excel_template.get_data(file, sheet_input_constant, 1, "A", "C")
        parameters_constant = parameters_constant.to_dict(orient='dict')
        parameters_constant_units = parameters_constant['Unit']
        parameters_constant_values = parameters_constant['Value']
        return parameters_constant_units, parameters_constant_values

    def get_parameters_sensitivity(file, sheet_input_sensitivity):
        parameters_sensitivity = excel_template.get_data(file, sheet_input_sensitivity, 1, "A", "D")
        parameters_sensitivity = parameters_sensitivity.to_dict(orient='index')
        return parameters_sensitivity

    def get_project_sites(file, sheet_project_sites):
        project_sites = excel_template.get_data(file, sheet_project_sites, 2, "A", "D")
        evaluated_locations = len(project_sites.columns)
        # todo logging of evaluated project sites
        project_site_name_list = [project_sites.columns[i] for i in range(0, len(project_sites.columns))]
        project_sites = project_sites.to_dict(orient='index')
        # Translate strings 'True' and 'False' from excel sheet to True and False
        for site in project_sites:
            for key in project_sites[site]:
                project_sites[site][key] = excel_template.identify_true_false(project_sites[site][key])
        return project_sites

    def get_case_definitions(file, sheet_project_sites):
        case_definitions = excel_template.get_data(file, sheet_project_sites, 16, "A", "H")
        # todo logging message for evaluated cases - also consider setting "perform_simulation"
        case_list = [case_definitions.columns[i] for i in range(0, len(case_definitions.columns))]
        # here: if case_list perform_simulation==False: remove column
        case_definitions = case_definitions.to_dict(orient='dict')
        # Translate strings 'True' and 'False' from excel sheet to True and False
        for case in case_definitions:
            for key in case_definitions[case]:
                case_definitions[case][key] = excel_template.identify_true_false(case_definitions[case][key])
        return case_definitions