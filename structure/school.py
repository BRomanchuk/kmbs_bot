import numpy as np

from data_loader import get_programs_df, get_service_df, get_managers_df, get_professors_df


class School:
    def __init__(self):
        self.program_types = {
            'mba': ['pmba', 'emba', 'mbaf'],
            'edp': ["strategy", "management", "marketing", "people", "finance",
                    "projects", "pr", "service", "sales", "toc", "mediation"],
            'sdp': ['slp', 'ssa']
        }

        self.programs_df = get_programs_df()
        self.managers_df = get_managers_df()

        self.professors_df = get_professors_df()
        self.five_stars_df = get_service_df()

    def get_programs(self):
        """
        get array of programs names
        :return: np.array
        """
        return self.programs_df['Програма'].to_numpy()

    def get_professors(self):
        """
        get array of professors names
        :return: np.array
        """
        return self.professors_df['Викладач'].to_numpy()

    def get_managers(self):
        """
        get array of managers names
        :return: np.array
        """
        return self.managers_df['Менеджер'].to_numpy()

    def get_five_stars(self):
        """
        get array of five_stars names
        :return: np.array
        """
        return self.five_stars_df['5stars'].to_numpy()

    def get_program(self, name):
        """
        get program by its name
        :param name: str
        :return: pd.DataFrame
        """
        program_mask = (self.programs_df['Програма'] == name)
        return self.programs_df.loc[program_mask]

    def get_programs_by_type(self, program_type):
        """
        get programs by their type
        :param program_type: str
        :return: np.array
        """
        return self.__get_programs_by_entity(program_type, 'Категорія')

    def get_programs_by_manager(self, manager):
        """
        get programs by their type
        :param manager: str
        :return: np.array
        """
        return self.__get_programs_by_entity(manager, '👩‍💼 Менеджер')

    # get programs by any feature it has
    def __get_programs_by_entity(self, obj, feature):
        programs_mask = np.zeros(self.programs_df.shape[0]) == 1

        for i in range(self.programs_df.shape[0]):
            if obj in self.programs_df[feature].iloc[i]:
                programs_mask[i] = True

        return self.programs_df.loc[programs_mask, 'Програма'].to_numpy()
