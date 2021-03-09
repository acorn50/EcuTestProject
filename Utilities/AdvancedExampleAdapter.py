"""
This is an example of a user-defined ToolAdapter to showcase optional features and customization
possibilities for a ToolAdapter.
The source code of this example can be found in the ECU-TEST installation directory under
``Templates/DefaultData/Utilities``.

For a basic introduction to user-defined ToolAdapters please refer to the BasicExampleAdapter.

This user-defined ToolAdapter implements the following features:
    - hook methods to run commands on start and stop of a test bench configuration (
      :meth:`OnConfigure()`, :meth:`OnUnconfigure()`)
    - hook method to check the health of the connected tool (:meth:`IsBroken()`)
    - grouping of TBC options
    - check boxes or dropdown menus for TBC options
    - Tooljobs with complex return types
"""

###############################################################################
##
# Imports needed for every Tooladapter
from tts.core.toolingFramework.interface.Descriptors import ToolDescriptor, PropertyDescriptor, JobDescriptor
from tts.core.toolingFramework.interface.Properties import PropertyTypeId
from tts.core.toolingFramework.interface.Capabilities import Toolcaps
##
from tts.core.toolingFramework.interface.AbstractAdapter import ToolAdapter
from tts.core.toolingFramework.interface.Exceptions import ToollibError
from tts.core.toolingFramework.interface.Proxy import ToolAdapterProxy
##
###############################################################################

TOOLNAME = 'AdvancedExampleAdapter'
TOOLCAPS = Toolcaps.GetNull()


def IsInstalled():
    """
    .. seealso:: :meth:`BasicExampleAdapter.IsInstalled()`
    """
    return True


def CreateToolAdapter(host=None, port=None):  # pylint: disable=unused-argument
    """
    .. seealso:: :meth:`BasicExampleAdapter.IsInstalled()`
    """
    return ToolAdapterProxy(AdvancedExampleAdapter())


class AdvancedExampleAdapter(ToolAdapter):  # pylint: disable=no-toollib
    """
    Sample implementation of a ToolAdapter with additional feature.
    """

    def __init__(self):
        ToolAdapter.__init__(self)
        self._toolDesc = ToolDescriptor(
            TOOLNAME,
            [],  # must be an empty list
            0,
            # List of PropertyDescriptors:
            [
                # definition of first property group
                PropertyDescriptor.CreateInstance(
                    name='choiceExampleGroup',
                    displayName='First property group',
                    type=PropertyTypeId.group,
                ),
                # choice group inside the property group 'choiceExampleGroup'
                PropertyDescriptor.CreateInstance(
                    name='choiceParameter',
                    displayName='Choice group parameter',
                    description='An example parameter used to demonstrate choice '
                    'group behavior',
                    type=PropertyTypeId.choiceGroup,
                    validReferences=None,
                    default='Value A',
                    domain=['Value A', 'Value B'],
                    group='choiceExampleGroup'
                ),
                # property which is only displayed if 'Value A' is selected in
                # the previous choice group
                PropertyDescriptor.CreateInstance(
                    name='exampleCheckbox',
                    displayName='Check box for value A',
                    type=PropertyTypeId.bool,
                    default=True,
                    group='choiceParameter',
                    groupValue='Value A'
                ),
                # property which is only displayed if 'Value B' is selected in
                # the previous choice group
                PropertyDescriptor.CreateInstance(
                    name='exampleInteger',
                    displayName='Integer for Value B',
                    type=PropertyTypeId.int,
                    default=5,
                    group='choiceParameter',
                    groupValue='Value B'
                ),

                # definition of second property group
                PropertyDescriptor.CreateInstance(
                    name='secondPropertyGroup',
                    displayName='Second property group',
                    type=PropertyTypeId.group,
                ),
                PropertyDescriptor.CreateInstance(
                    name='stringValue',
                    displayName='String value',
                    description='Examplary property in the second property '
                    'group',
                    type=PropertyTypeId.string,
                    group='secondPropertyGroup'
                ),
            ],
            # List of ToolJobs:
            [
                # Tooljob with a complex return/result type
                JobDescriptor('GetCountryLanguageAndCurrency', [
                    PropertyDescriptor.CreateInstance(
                        name='country',
                        displayName='Country',
                        description=None,
                        type=PropertyTypeId.string,
                        domain=[
                            'Germany',
                            'Great Britain',
                            'France'
                        ],
                        default='France'
                    ),
                ],
                    'Demonstrates a grouped input parameter as well as complex return '
                    'types.',
                    # PropertyDescriptor for the return/result: For a complex return
                    # type the type of the result property should be a set to
                    # PropertyTypeId.object.
                    PropertyDescriptor.CreateInstance(
                    name='result',
                    description=None,
                    type=PropertyTypeId.object),
                ),
            ]
        )

    def OnConfigure(self):
        """
        This method is called on tool start (test bench start, manual start in
        configuration window). It can be used to start any external tool needed by this
        ToolAdapter. Raise a ToollibError to signal an error. If OnConfigure fails,
        OnUnconfigure will not be called. Use "pass" if no external tool is used.
        """

    def OnUnconfigure(self):
        """
        This method is called on tool shutdown, if the previous call to OnConfigure
        did not fail. It can be used to stop any tool needed by this ToolAdapter.
        Raise a ToollibError to signal an error. Use "pass" if no external tool is used.
        """

    def IsBroken(self):
        """
        This method is called before test execution and on configuration window update.
        Return True if any of the external tools used by this ToolAdapter cannot be used anymore
        (e.g connection lost, tool locked up). Otherwise or if no tool is used, return
        False.

        :return: True if tool is broken (not usable)
        :rtype: bool
        """
        return False

    def JobGetCountryLanguageAndCurrency(self, country):
        """
        Example Tooljob with a complex return type, in this example a tuple. For complex
        return values the type of the corresponding PropertyDescriptor for the return value needs
        to be set to PropertyTypeId.object.
        """
        if country == 'Germany':
            return ['German', 'Euro']
        if country == 'Great Britain':
            return ['English', 'Pound sterling']
        if country == 'France':
            return ['French', 'Euro']
        raise ValueError('Unknown country given')
