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

    # get programs by their type
    def get_programs_by_type(self, program_type):
        return self.__get_programs_by_entity(program_type, 'Категорія')

    # get programs by their manager
    def get_programs_by_manager(self, manager):
        return self.__get_programs_by_entity(manager, '👩‍💼 Менеджер')

    # get programs by any feature it has
    def __get_programs_by_entity(self, obj, feature):
        programs_mask = np.zeros(self.programs_df.shape[0]) == 1

        for i in range(self.programs_df.shape[0]):
            if obj in self.programs_df[feature].iloc[i]:
                programs_mask[i] = True

        return self.programs_df.loc[programs_mask, 'Програма']