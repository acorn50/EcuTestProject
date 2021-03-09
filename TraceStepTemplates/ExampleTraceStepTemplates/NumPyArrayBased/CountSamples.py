import numpy

if any(name not in globals() for name
        in ('NumpyBasedTraceStep', 'SignalDefinition', 'ParameterDefinition')):
    from NumpyBasedTraceStep import NumpyBasedTraceStep, SignalDefinition, ParameterDefinition


class CountSamples(NumpyBasedTraceStep):
    """
    This is an implementation of NumpyBasedTraceStep.
    
    Use the interface as reference of available methods. Abstract methods have to be implemented.
    Other methods like GetDescription() are optionally overwritten. There are utility functions
    like CalculateRanges(), FitToAxis() that can be used in your code.
    """

    @staticmethod
    def GetInterfaceRevision():
        """
        Returns the interface revision of the trace step template.
        
        :note: This method is auto-generated for new implementations of NumpyBasedTraceStep. So do 
               not delete or modify this method!
        
        :rtype: int
        """
        return 1

    @classmethod
    def GetDescription(cls):
        """
        Returns the description of the trace step.
        
        :rtype: str
        """
        return 'Counts samples of the given signal and checks, whether the count lies between minSampleCount and maxSampleCount'

    @classmethod
    def GetSignals(cls):
        """
        Returns the incoming and outgoing signals of the trace step.
        
        :rtype: list[SignalDefinition]
        """
        return [SignalDefinition('Signal', 'IN', optional=False, description='')]

    @classmethod
    def GetParameters(cls):
        """
        Returns the input and return parameters.
        
        :rtype: list[ParameterDefinition]
        """
        return [ParameterDefinition('minSampleCount', 'IN', description=''),
                ParameterDefinition('maxSampleCount', 'IN', description=''),
                ParameterDefinition('totalSampleCount', 'OUT', description='')]

    def Check(self, parameters):
        """
        Is called initially before execution and should check the parameterization.
        If an error exists, a TypeError or ValueError should be raised.
        
        :param parameters: Dictionary with parameter values
        :type parameters: dict[str, object]
        :raise TypeError: Invalid type of a parameter.
        :raise ValueError: Invalid value of a parameter.
        """
        if not (isinstance(parameters['minSampleCount'], (int, type(None)))
                and isinstance(parameters['maxSampleCount'], (int, type(None)))):
            raise TypeError('Parameters minSampleCount and maxSampleCount must be an integer or None!')

    def Process(self, parameters, report, timeAxis, ranges, signals):
        """
        Method for performing the trace step template. Calculations can be performed based on
        the given signal values and their results can be stored in outgoing signals. Evaluation
        results and output parameters can be set.
        
        :note: It is recommended to evaluate over the given trigger ranges and set the result for
               each trigger range. The overall result will be automatically determined.
               
               It is possible to manually set the overall result using the :class:`Report` object;
               the automatic mechanism will be deactivated if used.
               
               Detailed spots are also reported on trigger ranges.
        :note: Access to values: All signal values within a trigger range can be accessed
               by its :class:`TriggerRange` object. Alternatively, all values of a signal can be
               accessed by the :class:`Signal` object.
        :note: To store calculated values in an outgoing signal the :class:`Signal` object is used:
               Signal.Emit(timestamps, values)
        :param parameters: Dictionary containing parameter values
        :type parameters: dict[str, object]
        :param report: The report object.
        :type report: :class:`.Report`
        :param timeAxis: The common time axis of the signals over the entire trace. A limitation
                         to the trigger ranges can be provided by a :class:`TriggerRange` object.
        :type timeAxis: numpy.ndarray
        :param ranges: List containing trigger ranges.
        :type ranges: list[TriggerRange]
        :param signals: Dictionary of signals.
        :type signals: dict[str, :class:`.Signal`]
        """

        # Copy parameters to local variables
        minSampleCount = parameters['minSampleCount']
        maxSampleCount = parameters['maxSampleCount']

        # Checking against minSampleCount / maxSampleCount only makes sense, if at least one of
        # these parameters have been provided.
        checkSampleCount = not (minSampleCount is None and maxSampleCount is None)

        # If checkSampleCount is set, we check against both, minSampleCount and maxSampleCount,
        # later on. Here we fix the case where only one of these two parameters is provided:
        if minSampleCount is None:
            minSampleCount = float('-inf')
        if maxSampleCount is None:
            maxSampleCount = float('inf')

        # Process() is called only once and receives a list of trigger ranges (or one range that
        # spans the entire time domain, when not using a trigger block). Here we iterate over each
        # of the ranges.
        for triggerRange in ranges:
            # triggerRange.GetValues() returns the values of the specified signal as a NumPy array,
            # which is cropped to the range, i.e. triggerRange.GetValues(u'Signal')[0] returns the first
            # value within the range, triggerRange.GetValues(u'Signal')[-1] returns the last. NumPy arrays have
            # a property shape that contains the number of elements per dimension (For one-dimensional
            # arrays, shape[0] equals size.). Hence, triggerRange.GetValues(u'Signal').shape[0] delivers the
            # number of samples within the range.
            count = triggerRange.GetValues('Signal').shape[0]

            # Check, whether the sample count lies between minSampleCount and maxSampleCount, and
            # update the result of the range accordingly
            if checkSampleCount:
                if minSampleCount <= count <= maxSampleCount:
                    triggerRange.SetResultSuccess()
                else:
                    triggerRange.SetResultFailed()

            # Set sample count as result text of the trigger range
            triggerRange.SetResultText('Sample count: %s' % count)

        # signals[u'Signal'].GetValues() and signals[u'Signal'].GetTimestamps() return the values and
        # timestamps of the specified signal, respectively. The returned NumPy arrays cover the
        # whole time domain of the signal, i.e. they are not cropped to a trigger range.
        # Hence, signals[u'Signal'].GetValues().shape[0] delivers the total number of samples.
        parameters['totalSampleCount'] = int(signals['Signal'].GetValues().shape[0])
