from .pso import pso

from tts.core.project.generator.OptimizerBase import OptimizerBase


class ParticleSwarmOptimizer(OptimizerBase):
    """
    This is a metaheuristic optimization generator based on a particle swarm algorithm. The used
    implementation is called pyswarm and is available here: https://pythonhosted.org/pyswarm/

    The operating principle of an ECU-TEST optimizer is to generate input parameters for new test
    runs based on the results of previous test runs. The main method of an optimizer is
    Generate(), which is called once the parameter generation is started.

    A GUI dialog is automatically generated, which contains:
        - inputs for the search boundaries of each input variable (can be used or ignored by the
        algorithm)
        - controls to configure a preceding, "classic" parameter variation (optional,
        only displayed if flag ENABLE_PARAMETER_VARIATION is set to True)
        - inputs for each entry in the SERIALIZE dict, which can be used to parametrize the
        optimizer
    """

    # Mandatory unique identifier. For convenience use an online UUID generator tool.
    ID = '603089f2-4f80-4dbc-9157-64fec37c913c'

    # Mandatory. The screen name of the optimizer.
    NAME = 'Particle swarm optimizer'

    # Optional. A description that is displayed in ECU-TEST on hover.
    DESCRIPTION = 'A metaheuristic which optimizes a given output metric of a package over ' \
                  'multiple test runs by varying its input parameters.'

    # If true, the GUI displays controls for a preceding parameter variation.
    ENABLE_PARAMETER_VARIATION = False

    """
    Here you can add all parameters you want to save for this optimizer. Parameters named here
    are also automatically displayed in the GUI. The format of an entry is:
    
    u'attributeName': (u'SERIALIZATION_NAME', u'datatype')
    
    where attributeName is the name of the class attribute in which the saved/given value is
    injected. SERIALIZATION_NAME is the tag under which the data is saved in the xml and
    should be all caps and not contain any spaces. It is also used as the displayed name
    for the parameter in the GUI. Last, the datatype is responsible to display the correct input 
    field in the GUI.
    """
    SERIALIZE = {
        '_optimizeMode': ('OPTIMIZATION-MODE', 'string'),
        '_outputToOptimize': ('OUTPUT-TO-OPTIMIZE', 'string'),
        '_swarmSize': ('SWARM-SIZE', 'integer'),
        '_omega': ('OMEGA', 'float'),
        '_phip': ('PARTICLE-SEARCH-SPREAD', 'float'),
        '_phig': ('SWARM-SEARCH-SPREAD', 'float'),
        '_maxIterations': ('MAX-ITERATIONS', 'integer'),
        '_minStep': ('MIN-STEP-SIZE', 'float'),
        '_minFunc': ('MIN-FUNCTION-CHANGE', 'float')
    }

    def __init__(self):
        # Call super constructor
        OptimizerBase.__init__(self)

        # The values defined here are used as default values in the GUI

        # General optimization parameters
        self._outputToOptimize = ''
        self._optimizeMode = 'min'

        # Particle swarm parameters
        self._swarmSize = 10
        self._omega = 0.5
        self._phip = 0.5
        self._phig = 0.5
        self._maxIterations = 20
        self._minStep = 1e-8
        self._minFunc = 1e-8

    def Generate(self, testRunFunction):
        """
        This method is called once and generates new test runs - therefore the main optimization
        routine should be located here. To start a new test run the optimization algorithm can
        call the testRunFunction with one or multiple new input parameter sets. For each set a
        test run is done by ECU-TEST, after the given sets are done the testRunFunction returns
        the corresponding test run results.
        When this method finishes, the optimizer has also completed work.
        If a normal parameter variation is configured (flag ENABLE_PARAMETER_VARIATION),
        it is executed before this method is called. The input parameters and results can then be
        obtained by calling self.GetLastReturnSets()

        :param testRunFunction: If this function is called, an ECU-TEST test run is started.
                                The function expects either a single parameter set or a list of
                                parameter sets. A parameter set must be an instance of
                                class CycleData and can be created with the method
                                self.CreateCycleData(). It returns a list of dicts (one for each
                                given parameter set) which each contain all output results of a
                                test run.
        """

        inputParameters, lowerBounds, upperBounds = self.__TransformBounds(self.GetMinMaxValues())

        def FunctionToOptimize(inputs):
            """
            We have to wrap the testRunFunction, since its inputs and outputs are incompatible
            with the particle swarm optimizer, which awaits a function of the form
                singleOutput = f([param1, param2, ..., paramN])

            :param inputs: list(input1, input2, ...)
            :return: single float result of a test run with the given inputs
            """
            inputDict = dict(zip(inputParameters, inputs))
            cycleData = self.CreateCycleData(inputDict)
            result = testRunFunction(cycleData)[0][self._outputToOptimize]

            # We transform the result since pyswarm can only minimize a given function,
            # but we also want to be able to maximize it or optimize it to a given value.
            loss = self.__CalculateLoss(result)
            return loss

        # This is where all of the optimization happens. Pyswarm internally calls our
        # FunctionToOptimize a number of times which results in an equal number of test runs.
        minParameters, minResult = pso(FunctionToOptimize, lowerBounds, upperBounds,
                                       swarmsize=self._swarmSize,
                                       omega=self._omega,
                                       phip=self._phip,
                                       phig=self._phig,
                                       maxiter=self._maxIterations,
                                       minstep=self._minStep,
                                       minfunc=self._minFunc)

        print(('Minimal result achieved: {0:0.3f} '
              'at parameters {1}'.format(minResult, list(zip(inputParameters, minParameters)))))

    def __TransformBounds(self, parameterBounds):
        """
        Transform the min/max boundary values from the structure given by ECU-TEST to the
        structure needed by pyswarm.
        :param parameterBounds: {parameter name: (minValue, maxValue)}
        :return: list(parameter names), list(minValues), list(maxValues)
        """
        paramNames = []
        lowerBounds = []
        upperBounds = []
        for paramName, bounds in parameterBounds.items():
            paramNames.append(paramName)
            lowerBounds.append(bounds[0])
            upperBounds.append(bounds[1])
        return paramNames, lowerBounds, upperBounds

    def __CalculateLoss(self, result):
        if self._optimizeMode.lower() == 'min':
            return result
        if self._optimizeMode.lower() == 'max':
            return -result

        # Calculate squared error if a number is given
        try:
            target = float(self._optimizeMode)
        except ValueError:
            raise ValueError('The optimization mode must be either "min", "max" or a scalar.')
        return (target - result) ** 2
