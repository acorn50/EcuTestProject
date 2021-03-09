from tts.testExecution.api.UserUtility import TsAXSUtility
from tts.core.axs.interface.Interface import Interface
from tts.core.axs.interface.constraint.NumericType import NumericType
from tts.core.axs.interface.constraint.TextType import TextType


class TsSimpleCalculationExample(TsAXSUtility):
    """
    This is a small example on how a AXSUtility should be implemented.
    """

    ID = '5c256353-1dc4-4651-8faf-af0e58dfe636'
    NAME = _('SimpleCalculationExample')
    DESCRIPTION = _('Das ist ein kleines Beispiel, wie ein AXSUtility implementiert werden sollte (einfache Berechnung).')

    def __init__(self):
        self.SUPPORTED_OPERATIONS = {"Addition" : self.Addition, \
                            "Subtraction" : self.Subtraction, \
                            "Multiplication" : self.Multiplication, \
                            "Division" : self.Division}
        TsAXSUtility.__init__(self)

    def Addition(self, a, b):
        """
        Addition of 2 values.
        """
        return a + b

    def Subtraction(self, a, b):
        """
        Subtraction of 2 values.
        """
        return a - b

    def Multiplication(self, a, b):
        """
        Multiplication of 2 values.
        """
        return a * b

    def Division(self, a, b):
        """
        Division of 2 values.
        """
        return float(a) / b

    @staticmethod
    def GetBitmap():
        """
        Return the utility-icon.

        :rtype: wx.Bitmap
        """
        import tts.Res
        return tts.Res.GetBitmap("calculationexample", "utilities")

    @classmethod
    def GetInterface(cls):
        """
        Return an interface which specifies our arguments.
        """
        interface = Interface()

        #operation
        constraint = TextType("operation")
        constraint.AddTextEntry("Addition")
        constraint.AddTextEntry("Subtraction")
        constraint.AddTextEntry("Multiplication")
        constraint.AddTextEntry("Division")
        constraint.SetDefaultValue("Multiplication")
        interface.AddArgument(constraint)

        #a
        constraint = NumericType("a")
        constraint.SetDefaultValue(2)
        interface.AddArgument(constraint)

        #b
        constraint = NumericType("b")
        constraint.SetDefaultValue(12)
        interface.AddArgument(constraint)

        #result
        constraint = NumericType("result")
        constraint.SetDefaultValue(24)
        interface.AddReturn(constraint)

        return interface

    def OnRun(self, userExcInst, testEngine):
        """
        Implementation of the simple calculation.
        """
        #get values a, b
        a = userExcInst.GetRawArgumentValue("a")
        b = userExcInst.GetRawArgumentValue("b")

        #get the choosen calc operations
        operation = userExcInst.GetRawArgumentValue("operation")

        #validations
        if operation not in self.SUPPORTED_OPERATIONS:
            raise ValueError("Choosen operation is not supported.")
        if None in (a, b):
            raise ValueError("Operands are not present.")

        #execute operation and set return result
        result = self.SUPPORTED_OPERATIONS[operation](a, b)
        userExcInst.SetRawReturnValue("result", result)

    def GetReportInfos(self):
        """
        Overwrite to add custom information in the test report.

        :return: Dictionary containing key value pairs to be shown in the report
        :rtype: dict{str:str}
        """
        return {}


