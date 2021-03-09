import os

from tts.core.project.generator.ProjectGenerator import ProjectGenerator

__copyright__ = "Copyright © TraceTronic GmbH, Dresden"
__license__ = "This file is distributed as part of TraceTronic software products. You may use " \
              "this file only in accordance with the TraceTronic Software License Terms " \
              "(https://www.tracetronic.com/software-license-terms/"


class WsFilterGenExample(ProjectGenerator):
    """
    The Filter Generator creates a project according to the filter criteria, just as it is listed
    via the ECU-TEST
    """

    ID = 'curu15y2-s54r-s1cf-n630-vhxvyosvn70b'
    NAME = 'User-Workspacefilter-Generator'
    DESCRIPTION = 'The generator creates a project consisting of all packages and projects found ' \
                  'in the workspace according to the filter criteria.'
    SERIALIZE = {'searchCriteria':  ('search', 'unicode', ''),
                 'useExtendedMode': ('useExtendedMode', 'boolean', False)}

    def __init__(self):
        self.searchCriteria = ''
        self.useExtendedMode = False

    def GetDialog(self):
        from .WsFilterGenExampleDialog import WsFilterGenExampleDialog
        return WsFilterGenExampleDialog(self)

    def PreGeneration(self):
        # Check input variable
        if not isinstance(self.searchCriteria, str):
            raise AssertionError("Argument `searchCriteria` is no string, but {!r}.".format(
                    type(self.searchCriteria)))

        if not isinstance(self.useExtendedMode, bool):
            raise AssertionError("Argument `useExtendedMode` is no bool, but {!r}.".format(
                    type(self.useExtendedMode)))

        if self.searchCriteria is None or len(self.searchCriteria) == 0:
            raise AssertionError("No search string!")

    def GenerationIterator(self):
        cd = self.CreateCycleData(name='GeneratedExample')  # creates cycledata object
        project = cd.projectInstance  # The project instance to be completed and executed

        componentApi = self.api.ObjectApi.ProjectApi.ComponentApi
        workspaceApi = self.api.ObjectApi.WorkspaceApi

        matches_file_list = workspaceApi.SearchFiles(self.searchCriteria, self.useExtendedMode)
        matches_file_list.sort()

        for file_path in matches_file_list:
            if file_path == self.projectPath or file_path == self.sourceProjectPath:
                # no recursion
                continue

            filename = os.path.basename(file_path)

            if filename.endswith('.pkg'):
                packageCall = componentApi.CreatePackageCall(filename, file_path)
                project.AppendComponent(packageCall)

            elif filename.endswith('.prj'):
                projectCall = componentApi.CreateProjectCall(filename, file_path)
                project.AppendComponent(projectCall)

        yield cd

    def PostGeneration(self):
        print("Generation finished")

    def Check(self):
        errors = []
        try:
            self.PreGeneration()
        except AssertionError as e:
            errors.append(str(e))
        return errors
