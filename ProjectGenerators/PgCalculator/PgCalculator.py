import os
import csv

from tts.core.project.generator.ParamGenerator import ParamGenerator


class PgCalculator(ParamGenerator):
    """
    This is a small example on how a parameter generator should be implemented.
    """

    ID = '56fe8f8f-e11d-11df-a48c-12386bddbbec'
    NAME = 'Calculator'
    DESCRIPTION = 'Arithmetic operations with two numbers.'
    SERIALIZE = {'filename' : ('FILENAME', 'string', r'')}
    """
    Here the instance variables are declared for serialization.
    """

    ARITHMETIC = {'+': 'Addition',
                  '-': 'Substraction',
                  '*': 'Multiplication',
                  '/': 'Division'}
    """
    Dictionary, to map an arithmetic operation to a package or cycle name
    """

    def __init__(self):
        """
        Method, to initalize the instance variables.
        """
        self.filename = r''
        """
        Initialize the name of the csv file.
        """
        self.fileDescriptor = None
        """
        Initialize the file descriptor, to parse the csv file.
        """

    def GetFilename(self):
        """
        Returns name of csv file.
        For use in the configuration dialog.
        @return: Name of csv file.
        @rtype: str
        """
        return self.filename

    def SetFilename(self, filename):
        """
        Sets name of csv file.
        For use in the configuration dialog.
        @param filename: Name of csv file.
        @type filename: str
        """
        self.filename = filename

    def GetDialog(self):
        """
        Returns the configuration dialog of the parameter generator.
        The dialog needs a reference to the parameter generator for getting and setting
        the parameter generator data.
        @rtype: L{DlgCalculator}
        @return: wxDialog
        """
        from .DlgCalculator import DlgCalculator
        return DlgCalculator(None, self)

    def PreGeneration(self):
        """
        A file descriptor to the csv file will be opend.
        """
        self.fileDescriptor = open(self.filename, 'r', encoding="utf-8")

    def GenerationIterator(self):
        """
        Method, to implement the iteration over the lines in the csv file.
        One line in the csv file contains the first operator, an arithmetic operation
        and a second operator. This data will be stored in the parameter and constants
        dictionaries. With all this data, a L{CyleData} object will be created and
        yield to the caller of this method.
        """
        for row in csv.reader(self.fileDescriptor, delimiter=";"):
            firstNumber = row[0].strip()
            arithmetic = row[1].strip()
            secondNumber = row[2].strip()

            cycleData = self.CreateCycleData(name=self.ARITHMETIC[arithmetic])

            cycleData.AddParameter('firstNumber', int(firstNumber))
            cycleData.AddParameter('secondNumber', int(secondNumber))

            cycleData.AddAttribute('Description', 'Test calculation of {} {} {}'.format(firstNumber, arithmetic, secondNumber))

            cycleData.AddConst('ARITHMETIC', '%s.pkg' % self.ARITHMETIC[arithmetic])

            yield cycleData

    def PostGeneration(self):
        """
        The file descriptor to the csv file will be closed.
        """
        self.fileDescriptor.close()

    def Check(self):
        '''
        Is executed when the containing project is checked.
        Verify the existence of the file.
        '''
        errors = []
        if not os.path.exists(self.GetFilename()):
            errors.append('Path "{0}" doesn''t exist!'.format(self.GetFilename()))

        return errors
