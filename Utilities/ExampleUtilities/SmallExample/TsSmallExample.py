import tts.Res

from tts.testExecution.api.UserUtility import TsUserUtility


class TsSmallExample(TsUserUtility):
    """
    This is a small example on how a utility should be implemented.
    """

    ID = '2dcc6e40-3859-11dd-82ff-000b5d5f5cc8'
    NAME = _('SmallExample')
    DESCRIPTION = _('This is a small example that copies the value of one variable to another.')
    SERIALIZE = {
                 'varFrom' : ('VARIABLENAME-FROM', 'string'),
                 'varTo': ('VARIABLENAME-TO', 'string')
                 }
    """
    Here the two instance variables are declared for serialization.
    """

    def UtilityInit(self):
        """
        Initialize the instance variables for the names of the two ECU-TEST variables
        used in this example.
        """
        self.varFrom = "var1"
        self.varTo = "var2"

    def UtilityReport(self, reportEngine, reportDataObject):
        """
        Specifies how the runtime data and other informations about this teststep are
        displayed in the test report.
        """
        reportItem = reportEngine.PReportItem
        reportItem.PInfo = "value copied"

        table = reportEngine.AddTableEntity()
        table.SetValue(0, 0, "Variable value")
        table.SetValue(1, 0, reportDataObject.GetDataValue("copiedValue"))
        reportEngine.Update(table)

        table = reportEngine.AddTableEntity()
        table.SetValue(0, 0, "Variable From")
        table.SetValue(0, 1, "Variable To")
        table.SetValue(1, 0, self.varFrom)
        table.SetValue(1, 1, self.varTo)
        reportEngine.Update(table)

        reportEngine.AddEvaluationEntity(reportDataObject.PResultObject)

    def GetDialog(self):
        """
        Returs the configuration dialog object of the Utility.
        The dialog needs a reference to the teststep for getting and setting
        the teststep data.

        :rtype: :class:`~ExampleUtilities.SmallExample.DlgSmallExample.DlgSmallExample`
        :return: Dialog object
        """
        from .DlgSmallExample import DlgSmallExample
        return DlgSmallExample(None, self)

    def GetUsedVariableNames(self):
        """
        Overwritten to specify the used variable names.

        :rtype: list
        :return: List of variable names used by this test step.
        """
        return [self.varFrom, self.varTo]

    def OnRun(self, reportDataObject):
        """
        Here the value from one to another variable is copied and
        the copied value is stored in
        :class:`~tts.testExecution.api.UserUtility.RdoUserUtility` to be available later on
        in the :meth:`UtilityReport` method.
        """
        theValue = self.GetVariableValue(self.varFrom)
        self.SetVariableValue(self.varTo, theValue)

        reportDataObject.SetDataValue("copiedValue", theValue)

