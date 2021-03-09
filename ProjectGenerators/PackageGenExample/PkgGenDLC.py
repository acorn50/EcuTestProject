import os

from tts.core.project.generator.PackageGenerator import PackageGenerator


class PkgGenDLC(PackageGenerator):

    ID = 'ef3e2740-6e91-11e6-a3ae-fcf8aeb9b2bf'
    NAME = 'DLC check Generator'
    DESCRIPTION = 'Generates DLC checks for all frames on selected bus'
    SERIALIZE = {'busName': ('BUS-NAME', 'string', r'')}

    def __init__(self):
        self.busName = "A-CAN"
        self.templatePackage = "ExamplePackages\\PackageGenExample\\DLC-TEST_Template.pkg"
        packagePath = self.api.GetSetting('packagePath')
        self.templatePath = os.path.join(packagePath, self.templatePackage)
        self.framesList = []

    def GetBusName(self):
        return self.busName

    def SetBusName(self, busName):
        self.busName = busName

    def GetDialog(self):
        from .DlgBusSelect import DlgBusSelect
        return DlgBusSelect(None, self)

    def PreGeneration(self):
        # Collect all frames from Bus database
        self.framesList = self.api.DataBrowser.BrowseBus(self.busName).ListFrames()

    def GenerationIterator(self):
        cycleData = self.CreateCycleData("DLC-Check", self.templatePath)

        pkg = cycleData.packageInstance
        objectApi = cycleData.objectApi

        signalGroup = pkg.GetSignalGroups()[0]
        traceAnalysis = pkg.GetTraceAnalyses()[0]

        # Iterate over all Frames
        for frame in self.framesList:
            frameName = frame.GetName()

            firstSignal = self.api.DataBrowser.BrowseBus(self.busName).ListSignals(frameName)[0]
            mappingApi = objectApi.PackageApi.MappingApi
            mappingItem = mappingApi.CreateBusSignalWithPduMappingItem(self.busName,
                                                                       firstSignal.GetName(),
                                                                       frame.GetTxEcuNames()[0],
                                                                       frameName)
            signalGroup.AppendMappingItem(mappingItem)

            if frame.GetId() is not None:
                msgId = '0x%x' % frame.GetId()
            else:
                msgId = None

            traceStep = objectApi.PackageApi.TraceAnalysisApi.CreateTemplateBasedTraceStep(
                frameName)
            episode = traceAnalysis.GetTraceSteps()[0]
            episode.AppendTraceStep(traceStep)
            traceStep.SetTemplateById("BusCheck\CheckBusFrameDlc")
            traceStep.AssignGenericSignal("FrameID", traceAnalysis.GetGenericSignal("FrameID"))
            traceStep.AssignGenericSignal(
                "FrameLength", traceAnalysis.GetGenericSignal("FrameLength"))
            traceStep.SetParameter("id", msgId)
            traceStep.SetParameter("dlc", frame.GetFrameLength())

        yield cycleData

    def PostGeneration(self):
        pass
