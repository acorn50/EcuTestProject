from tts.testExecution.api.UserUtility import TsAXSUtility
from tts.core.axs.interface.Interface import Interface
from tts.core.axs.interface.constraint.NumericType import NumericType
from tts.core.axs.interface.constraint.TextType import TextType


class TsLinspaceExample(TsAXSUtility):
    """
    This is a small example on how a AXSUtility can be implemented.
    """

    ID = 'dd7b2b14-7b18-4234-9758-9eacdebc6f40'
    NAME = _('TsLinspaceExample')
    DESCRIPTION = _('Das ist ein kleines Beispiel, wie ein AXSUtility implementiert werden kann (aequidistante Liste).')

    def __init__(self):
        TsAXSUtility.__init__(self)

    @classmethod
    def GetInterface(cls):
        """
        Return an interface which specifies our arguments.
        """
        interface = Interface()

        # startpoint
        constraint = NumericType("startpoint")
        constraint.SetDefaultValue(0)
        interface.AddArgument(constraint)

        # endpoint
        constraint = NumericType("endpoint")
        constraint.SetDefaultValue(100)
        interface.AddArgument(constraint)

        # length
        constraint = NumericType("length")
        constraint.SetDefaultValue(3)
        interface.AddArgument(constraint)

        # includeEndpoint
        constraint = TextType("includeEndpoint")
        constraint.AddTextEntry("yes")
        constraint.AddTextEntry("no")
        constraint.SetDefaultValue("yes")
        interface.AddArgument(constraint)

        # result
        constraint = TextType("result")
        constraint.SetDefaultValue(str([0.0, 50.0, 100.0]))
        interface.AddReturn(constraint)

        return interface

    def OnPreProcess(self, testEngine):
        """
        Overwrite to implement pre execution behavior.
        This methode is called before running the testcase.
        """
        # use a list to store the reportInfos for a repeatedly used utility
        self.reportInfos = []

    def OnRun(self, userExcInst, testEngine):
        """
        Implementation of the simple calculation.
        """
        import numpy as np
        import tts.core.common.Constants
        additionalReportInfos = {}

        # get values startpoint, endpoint, length
        startpoint = userExcInst.GetRawArgumentValue("startpoint")
        endpoint = userExcInst.GetRawArgumentValue("endpoint")
        num = userExcInst.GetRawArgumentValue("length")

        # get includeEndpoint
        includeEndpoint = userExcInst.GetRawArgumentValue("includeEndpoint")
        includeEndpoint = includeEndpoint == "yes"

        # validations
        if None in (startpoint, endpoint, num):
            raise ValueError("Operands are not present.")

        # calculate linspace and set return result
        result = list(np.linspace(startpoint, endpoint, num, includeEndpoint))
        stepsize = result[1] - result[0]
        additionalReportInfos["Stepsize"] = stepsize
        userExcInst.SetRawReturnValue("result", str(result))

        # fill reportInfos
        self.reportInfos.append(additionalReportInfos)

        return tts.core.common.Constants.RESULT_ID_NONE

    def GetReportInfos(self):
        """
        Overwrite to add custom information in the test report.

        :return: Dictionary containing key value pairs to be shown in the report
        :rtype: dict{str:str}
        """
        return self.reportInfos.pop(0)


