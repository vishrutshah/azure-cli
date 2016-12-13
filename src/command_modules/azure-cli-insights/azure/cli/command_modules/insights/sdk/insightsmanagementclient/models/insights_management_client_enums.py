# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator 0.17.0.0
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from enum import Enum


class MetricStatisticType(Enum):

    average = "Average"
    min = "Min"
    max = "Max"
    sum = "Sum"


class TimeAggregationType(Enum):

    average = "Average"
    minimum = "Minimum"
    maximum = "Maximum"
    total = "Total"
    count = "Count"


class ComparisonOperationType(Enum):

    equals = "Equals"
    not_equals = "NotEquals"
    greater_than = "GreaterThan"
    greater_than_or_equal = "GreaterThanOrEqual"
    less_than = "LessThan"
    less_than_or_equal = "LessThanOrEqual"


class ScaleDirection(Enum):

    none = "None"
    increase = "Increase"
    decrease = "Decrease"


class ScaleType(Enum):

    change_count = "ChangeCount"
    percent_change_count = "PercentChangeCount"
    exact_count = "ExactCount"


class RecurrenceFrequency(Enum):

    none = "None"
    second = "Second"
    minute = "Minute"
    hour = "Hour"
    day = "Day"
    week = "Week"
    month = "Month"
    year = "Year"


class ConditionOperator(Enum):

    greater_than = "GreaterThan"
    greater_than_or_equal = "GreaterThanOrEqual"
    less_than = "LessThan"
    less_than_or_equal = "LessThanOrEqual"


class TimeAggregationOperator(Enum):

    average = "Average"
    minimum = "Minimum"
    maximum = "Maximum"
    total = "Total"
    last = "Last"
