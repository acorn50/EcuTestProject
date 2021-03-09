import os

from datetime import date

from tts.core.project.generator.ProjectGenerator import ProjectGenerator


class ProjectGeneratorExample(ProjectGenerator):

    ID = '64ada5a1-d42f-11e3-9cdf-080027005456'
    NAME = 'ProjectGenerator-Example'
    DESCRIPTION = 'Create a project with all packages from the "everyday" directory and on ' \
                  'weekeends additional with all packages from the weekend sub directory.'
    SERIALIZE = {}

    def __init__(self):
        pass

    def GetDialog(self):
        return None

    def PreGeneration(self):
        print("Start generation")

    def GenerationIterator(self):
        print("Run generation")

        cd = self.CreateCycleData()  # creates cycledata object
        cd.SetName("GeneratedExample")
        project = cd.projectInstance  # The project instance to be completed and executed
        objectApi = cd.objectApi  # The Object API which is used to create test steps
        componentApi = objectApi.ProjectApi.ComponentApi

        pkgBasePath = os.path.join(self.api.GetSetting('packagePath'), "ExamplePackages",
                                   "ProjectGenExample")
        everydayPath = os.path.join(pkgBasePath, "everyday")
        for root, dirnames, filenames in os.walk(everydayPath):
            for filename in filenames:
                packageCall = componentApi.CreatePackageCall(filename,
                                                             os.path.join(root, filename))
                project.AppendComponent(packageCall)

        if date.today().weekday() in (5, 6):  # 5 == Saturday, 6 == Sunday
            weekendPath = os.path.join(pkgBasePath, "weekend")
            for root, dirnames, filenames in os.walk(weekendPath):
                for filename in filenames:
                    packageCall = componentApi.CreatePackageCall(filename,
                                                                 os.path.join(root, filename))
                    project.AppendComponent(packageCall)
        yield cd

    def PostGeneration(self):
        print("Generation finished")

    def Check(self):
        return []  # [u'An example error message!']
