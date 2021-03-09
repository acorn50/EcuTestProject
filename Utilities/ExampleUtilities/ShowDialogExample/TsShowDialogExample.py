import time
import tts.Res

from tts.lib.gui.dialogs.ThreadDialog import ThreadDialog

from tts.testExecution.api.UserUtility import TsUserUtility
from .RunDialogExample import RunDialogExample


class TsShowDialogExample(TsUserUtility):
    ID = '4c69cb5e-233a-11dd-b764-001c23232a0e'
    NAME = _('ShowDialogExample')
    DESCRIPTION = _('Demonstrates how to show and interact with a dialog during runtime.')

    def UtilityReport(self, reportEngine, reportDataObject):
        """
        The count value of the :class:`~ExampleUtilities.ShowDialogExample.RunDialogExample
        .RunDialogExample` that was shown during test execution is displayed in the test report.
        """
        reportItem = reportEngine.PReportItem
        reportItem.PInfo = reportDataObject.GetDataValue("count")

    def OnRun(self, reportDataObject):
        """
        Here is demonstrated how a dialog can be shown during test execution.
        Due to execution in a separate thread the
        :class:`~tts.lib.gui.dialogs.ThreadDialog.ThreadDialog` class has
        to be used.
        """
        dlgInteface = ThreadDialog(RunDialogExample, parent=None)
        dlgInteface.ShowModal()
        for i in range(200):
            if not dlgInteface.IsShown():
                break
            dlgInteface.SetValue("count", str(i))
            time.sleep(0.05)
        else:
            import wx
            dlgInteface.EndModal(wx.ID_ABORT)
        dlgInteface.WaitForDialog()
        count = dlgInteface.GetValue("count")
        dlgInteface.Destroy()
        reportDataObject.SetDataValue("count", count)



