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

        self.professors = get_professors_df()
        self.five_stars = get_service_df()

    def get_programs_by_type(self, prog_type):
        pass