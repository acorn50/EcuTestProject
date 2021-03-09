"""
This module contains an example of an user-defined Tooladapter. The source code of this example
can be found in the ECU-TEST installation directory under
``Templates/DefaultData/Utilities``.

A user-defined Tooladapter must be put in the Utilities directory of the current workspace. If a
Tooladapter is changed, it is necessary to stop the current test bench (if it uses the
Tooladapter) and select *Extras -> Update user libraries* in ECU-TEST.

A Tooladapter's module must contain the class implementing the Tooladapter's functionality. For
autodiscovery and autoimport of ECU-TEST the module must contain two special variables and two
special methods.
The required variables are:

 - TOOLNAME: The name used in the test bench configuration for this Tooladapter
 - TOOLCAPS: Must be set to Toolcaps.GetNull()

The required methods are:

 - :meth:`IsInstalled`: Check if the interfaced tool is installed on the computer
 - :meth:`CreateToolAdapter`: Method to create an instance of the Tooladapter

The Tooladapter's functionality can be implemented as ToolJobs and ToolProperties. Ports cannot
be implemented in user-defined Tooladapters.

:var TOOLNAME: The name used in the test bench configuration for this Tooladapter - REQUIRED
:vartype TOOLNAME: str
:var TOOLCAPS: Must be set to Toolcaps.GetNull() - REQUIRED
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

from random import random
import math

TOOLNAME = "BasicExampleAdapter"
TOOLCAPS = Toolcaps.GetNull()


def IsInstalled():
    """
    Checks whether the tool handled by this Tooladapter is installed on the
    computer running this ECU-TEST instance. If this Tooladapter does not use
    any external tool, it is save just to return True.

    :return: True if tool is installed
    :rtype: bool
    """
    return True


def CreateToolAdapter(host=None, port=None):
    '''
    Creates and returns an instance of the Tooladapter of this module.

    As these simple Tooladapters cannot be run remotely by the tool server,
    the host and port arguments must be ignored.

    :return: a ToolAdapterProxy of a ToolAdapter (e.g. :class:`ExampleAdapter`)
    :rtype: ToolAdapterProxy
    '''
    return ToolAdapterProxy(BasicExampleAdapter())


class BasicExampleAdapter(ToolAdapter):
    '''
    Sample implementation of a Tooladapter.

    The ToolDescriptor of the Tooladapter is created on initialization of the
    Tooladapter. It must match the Tooladapter:

     - Toolname argument must be set to TOOLNAME
     - For each JobDescriptor there must be a method with the name Job<jobname>() and a matching signature.

    :ivar _toolDesc: Descriptor of the Tooladapter
    :vartype _toolDesc: :class:`~tts.core.toolingFramework.interface.Descriptors.ToolDescriptor`

    '''
    def __init__(self):
        ToolAdapter.__init__(self)
        self._toolDesc = ToolDescriptor(
                            TOOLNAME,
                            [],  # must be an empty list
                            0,
                            # List of PropertyDescriptors:
                            [
                                PropertyDescriptor.CreateInstance(
                                    name="doRound",
                                    displayName="Do Round",
                                    description="round is applied on the result of each job",
                                    type=PropertyTypeId.bool,
                                    validReferences=None,
                                    default=False,
                                    readonly=False
                                ),
                                PropertyDescriptor.CreateInstance(
                                    name="roundingMethod",
                                    displayName="Rounding Method",
                                    description="Type of rounding",
                                    type=PropertyTypeId.string,
                                    validReferences=None,
                                    default='Nearest',
                                    domain=['Nearest', 'Floor', 'Ceiling'],
                                    readonly=False
                                ),
                            ],
                            # List of ToolJobs:
                            [
                             JobDescriptor("MultiplyAdd", [
                                    PropertyDescriptor.CreateInstance(
                                        name="a",
                                        displayName="a",
                                        description=None,
                                        type=PropertyTypeId.float
                                    ),
                                    PropertyDescriptor.CreateInstance(
                                        name="b",
                                        displayName="b",
                                        description=None,
                                        type=PropertyTypeId.float
                                    ),
                                    PropertyDescriptor.CreateInstance(
                                        name="c",
                                        displayName="c",
                                        description=None,
                                        type=PropertyTypeId.float
                                    )
                                ],
                                "Calculates a + (b * c)",
                                PropertyDescriptor.CreateInstance(
                                    name="result",
                                    description=None,
                                    type=PropertyTypeId.float),
                        ),
                            JobDescriptor("GenerateRandomNumber", [],
                                          "Random number between 0 and 100",
                                PropertyDescriptor.CreateInstance(
                                    name="result",
                                    description=None,
                                    type=PropertyTypeId.float),
                            ),
                        ]
                    )

    def JobMultiplyAdd(self, a, b, c):
        '''
        ToolJob implementation. Its name must be of the form Job<jobname>, where
        <jobname> is the jobname argument of the :class:`~tts.core.toolingFramework.interface.Descriptors.JobDescriptor`.
        Furthermore the signature of the method must match its ``paramDescriptionList``.

        .. note:: there is no type checking

        .. note:: access properties via self.GetProperty(<propertyName>) as str value or via
                  self.GetTypedProperty(<propertyName>) as correctly typed property according to
                  the type in the PropertyDescriptor.
        '''

        result = a + (b * c)
        if self.GetProperty("doRound").upper() == "TRUE":
            return self._RoundValue(result)
        return result

    def JobGenerateRandomNumber(self):
        '''

        .. seealso:: :meth:`JobMultiplyAdd`

        '''

        result = random() * 100
        if self.GetProperty("doRound").upper() == "TRUE":
            return self._RoundValue(result)
        return result

    def _RoundValue(self, value):
        '''
        This method demonstrates how properties with a "domain" may be evaluated.

        :return: Rounded value using the round method as specified by property "roundingMethod"
        '''

        # GetTypedProperty automatically returns the correct data type as opposed to GetProperty,
        # which always returns strings
        if self.GetTypedProperty('roundingMethod') == 'Nearest':
            return round(value)
        elif self.GetTypedProperty('roundingMethod') == 'Floor':
            return math.floor(value)
        elif self.GetTypedProperty('roundingMethod') == 'Ceiling':
            return math.ceil(value)
