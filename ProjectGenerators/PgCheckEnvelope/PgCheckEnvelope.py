import os

if __name__ != "__main__":
    # The parameter generator is running inside ECU-TEST.
    # Base class will be imported from ECU-TEST.
    from tts.core.project.generator.ParamGenerator import ParamGenerator
else:
    # The parameter generator is running at itself, for testing purposes.
    # Base class will be imported from current package.
    from ParamGenerator import ParamGenerator


class PgCheckEnvelope(ParamGenerator):
    """
    This is a small example on how a parameter generator should be implemented.
    """

    ID = '1c56f74f-e563-11e1-a7d1-001a6bfb0b78'
    NAME = 'CheckEnvelope'
    DESCRIPTION = 'Checks the envelope for all recordings in a specified directory'
    SERIALIZE = {'directory':     ('DIRECTORY', 'string', r''),
                 'formatDetails': ('FORMAT-DETAILS', 'string', ''),
                 'deltaT':        ('DELTA-T', 'float', 0.4),
                 'deltaY':        ('DELTA-Y', 'float', 25.0),
                 }
    """
    Here the instance variables are declared for serialization.
    """

    def __init__(self):
        """
        Method, to initalize the instance variables.
        """

        self.directory = r''
        """
        Initialize the name of the directory to check.
        """

        self.formatDetails = ''
        """
        Initialize the format details
        """

        self.deltaT = 0.4
        """
        Initialize the value for delta T in the envelope.
        """

        self.deltaY = 25.0
        """
        Initialize the value for delta Y in the envelope.
        """

        self.recordingList = []
        """
        Initialize the list of recordings
        """

    def GetDialog(self):
        """
        Returns the configuration dialog of the parameter generator.
        The dialog needs a reference to the parameter generator for getting and setting
        the parameter generator data.
        @rtype: L{DlgCheckEnvelope}
        @return: wxDialog
        """
        from .DlgCheckEnvelope import DlgCheckEnvelope
        return DlgCheckEnvelope(None, self)

    def PreGeneration(self):
        """
        The given directory will be scanned for recordings, for which the envelope
        will be checked.
        """

        self.recordingList = []
        if not os.path.isabs(self.directory):
            self.directory = os.path.join(os.path.dirname(__file__), self.directory)
        for name in os.listdir(self.directory):
            if os.path.splitext(name)[1] == '.csv':
                self.recordingList.append(os.path.join(self.directory, name))

    def GenerationIterator(self):
        for recording in self.recordingList:
            cycleData = self.CreateCycleData(name=os.path.basename(recording))
            cycleData.AddParameter('deltaT', self.deltaT)
            cycleData.AddParameter('deltaY', self.deltaY)

            recordingInfo = cycleData.AddRecordingInfo('actual recording group', recording)
            recordingInfo.FormatDetails = self.formatDetails

            yield cycleData

if __name__ == "__main__":
    # Running Testenvironment, for testing the parameter generator.
    from ParamGeneratorTestEnvironment import TestParamGenerator
    TestParamGenerator(PgCheckEnvelope)
