import numpy

if any(name not in globals() for name 
        in ('NumpyBasedTraceStep', 'SignalDefinition', 'ParameterDefinition')):
    from NumpyBasedTraceStep import NumpyBasedTraceStep, SignalDefinition, ParameterDefinition


class CheckThreshold(NumpyBasedTraceStep):
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
        return 'Checks whether the given signal exceeds the given threshold'

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
        return [ParameterDefinition('threshold', 'IN', description=''),
                ParameterDefinition('maxValue', 'OUT', description='')]

    @classmethod
    def GetTimeAxisDefinition(cls):
        """
        Returns how the common time axis is determined. Only the logical operators **and** and 
        **or** as well as references to the time axes of the signals by using the signal name are
        permitted. The use of brackets is allowed.
        
        :note: If a signal is not defined on the common time axis, its value is determined
               according to its interpolation rule.
        
        :return: Convention for building the common time axis (e.g. **'Sig1 or Sig2'**). If None,
                 all time axes are merged to a common time axis. This corresponds to an
                 OR concatenation of the individual time axes.
        :rtype: str
        """
        # e.g. 'Sig1 or Sig2' - timestamps either from Sig1 or Sig2 (default behavior)
        # e.g. 'Sig1 and Sig2' - only timestamps common to both Sig1 and Sig2
        return ''

    def Check(self, parameters):
        """
        Is called initially before execution and should check the parameterization.
        If an error exists, a TypeError or ValueError should be raised.
        
        :param parameters: Dictionary with parameter values
        :type parameters: dict[str, object]
        :raise TypeError: Invalid type of a parameter.
        :raise ValueError: Invalid value of a parameter.
        """
        if not isinstance(parameters['threshold'], (int, float)):
            raise TypeError('Parameter threshold must be a number!')

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
        threshold =  parameters['threshold']

        # Maximum value, we have found so far. Initially this is NaN (not a number).
        maxValue = float('NaN')

        # Process() is called only once and receives a list of trigger ranges (or one range that
        # spans the entire time domain, when not using a trigger block). Here we iterate over each
        # of the ranges. 
        for triggerRange in ranges:
            # triggerRange.GetValues() returns the values of the specified signal as a NumPy array,
            # which is cropped to the range, i.e. triggerRange.GetValues(u'Signal')[0] returns the first
            # value within the range, triggerRange.GetValues(u'Signal')[-1] returns the last. 
            values = triggerRange.GetValues('Signal')
            # Analogously, triggerRange.GetTimestamps() returns the timestamps, cropped to the current 
            # range. No signal name needs to be specified, as all signals are mapped to a common time axis. 
            timestamps = triggerRange.GetTimestamps()

            # Check, whether triggerRange contains any values
            if values.size > 0:
                # values.max() returns the maximum value within the current range. The global
                # maxValue is updated accordingly.
                maxInRange = values.max()
                maxValue = max(maxInRange, maxValue)
                # thresholdExceededMask is an new Boolean array that contains True wherever the
                # corresponding element in values exceeds the given threshold.
                thresholdExceededMask = values > threshold
                # Report FAILED, when threshold is exceeded at least once
                if thresholdExceededMask.any():
                    triggerRange.SetResultFailed()
                    triggerRange.SetResultText('Threshold exceeded. Maximum in range: {}.'.format(maxInRange))
                else:
                    triggerRange.SetResultSuccess()
            else:
                triggerRange.SetResultText('No values in the given trigger range.')

            # The report shall contain contiguous sub-ranges, where the threshold is either
            # satisfied or exceeded. The method CalculateRanges() can be used to create such
            # sub-ranges from a Boolean mask.
            resultIds = [report.RESULT_ID_SUCCESS, report.RESULT_ID_FAILED]
            resultMessages = ['Check OK', 'Check FAILED']
            for subRange in self.CalculateRanges(thresholdExceededMask):
                triggerRange.Range(
                    timestamps[subRange[0]], timestamps[subRange[1]-1], 
                    resultMessages[subRange[2]], resultIds[subRange[2]])

        # Write back the determined maximum value
        parameters['maxValue'] = maxValue
