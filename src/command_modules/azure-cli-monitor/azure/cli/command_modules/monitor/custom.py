# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
from __future__ import print_function
import datetime
from azure.cli.core._util import CLIError


# 1 hour in milliseconds
DEFAULT_QUERY_TIME_RANGE = 3600000

# ISO format with explicit indication of timezone
DATE_TIME_FORMAT = '%Y-%m-%dT%H:%M:%SZ'


def list_metric_definitions(client, resource_uri, metric_names=None):
    '''Commands to manage metric definitions.
    :param str resource_uri: The identifier of the resource
    :param str metric_names: The list of metric names
    '''
    odata_filter = _metric_names_filter_builder(metric_names)
    metric_definitions = client.list(resource_uri, filter=odata_filter)
    return list(metric_definitions)


def _metric_names_filter_builder(metric_names=None):
    '''Build up OData filter string from metric_names
    '''
    filters = []
    if metric_names:
        for metric_name in metric_names:
            filters.append("name.value eq '{}'".format(metric_name))
    return ' or '.join(filters)


def list_metrics(client, resource_uri, time_grain,
                 start_time=None, end_time=None, metric_names=None):
    '''Lists the metric values for a resource.
    :param str resource_uri: The identifier of the resource
    :param str time_grain: The time grain. Granularity of the metric data returned in ISO 8601
                           duration format, eg "PT1M"
    :param str start_time: The start time of the query. In ISO format with explicit indication of
                           timezone: 1970-01-01T00:00:00Z, 1970-01-01T00:00:00-0500
    :param str end_time: The end time of the query. In ISO format with explicit indication of
                         timezone: 1970-01-01T00:00:00Z, 1970-01-01T00:00:00-0500
    :param str metric_names: The space separated list of metric names
    :param str metric_names: The list of metric names
    '''
    odata_filter = _metrics_odata_filter_builder(time_grain, start_time, end_time, metric_names)
    metrics = client.list(resource_uri, filter=odata_filter)
    return list(metrics)


def _metrics_odata_filter_builder(time_grain, start_time=None, end_time=None,
                                  metric_names=None):
    '''Build up OData filter string
    '''
    filters = []
    metrics_filter = _metric_names_filter_builder(metric_names)
    if metrics_filter:
        filters.append('({})'.format(metrics_filter))

    if time_grain:
        filters.append("timeGrain eq duration'{}'".format(time_grain))

    filters.append(_validate_time_range_and_add_defaults(start_time, end_time))
    return ' and '.join(filters)


def _validate_time_range_and_add_defaults(start_time, end_time,
                                          formatter='startTime eq {} and endTime eq {}'):
    end_time = _validate_end_time(end_time)
    start_time = _validate_start_time(start_time, end_time)
    time_range = formatter.format(start_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
                                  end_time.strftime('%Y-%m-%dT%H:%M:%SZ'))
    return time_range


def _validate_end_time(end_time):
    result_time = datetime.datetime.utcnow()
    if isinstance(end_time, str):
        result_time = datetime.datetime.strptime(end_time, DATE_TIME_FORMAT)
    return result_time


def _validate_start_time(start_time, end_time):
    if not isinstance(end_time, datetime.datetime):
        raise ValueError("Input '{}' is not valid datetime. Valid example: 2000-12-31T12:59:59Z"
                         .format(end_time))

    result_time = end_time - datetime.timedelta(seconds=DEFAULT_QUERY_TIME_RANGE)

    if isinstance(start_time, str):
        result_time = datetime.datetime.strptime(start_time, DATE_TIME_FORMAT)

    now = datetime.datetime.utcnow()
    if result_time > now:
        raise ValueError("start_time '{}' is later than Now {}.".format(start_time, now))

    return result_time


def list_activity_logs(client, correlation_id=None, resource_group=None, resource_uri=None,
                       resource_provider=None, start_time=None, end_time=None,
                       caller=None, status=None, max_events=50, select=None):
    '''Provides the list of activity logs.
    :param str correlation_id: The correlation id of the query
    :param str resource_group: The resource group
    :param str resource_uri: The identifier of the resource
    :param str resource_provider: The resource provider
    :param str start_time: The start time of the query. In ISO format with explicit indication of
                           timezone: 1970-01-01T00:00:00Z, 1970-01-01T00:00:00-0500
    :param str end_time: The end time of the query. In ISO format with explicit indication of
                         timezone: 1970-01-01T00:00:00Z, 1970-01-01T00:00:00-0500
    :param str caller: The caller to look for when querying
    :param str status: The status value to query (ex: Failed)
    :param str max_events: The maximum number of records to be returned by the command
    :param str select: The list of event names
    '''
    present_switch = 0
    for param in [correlation_id, resource_group, resource_uri, resource_provider]:
        present_switch = present_switch + (1 if param else 0)

    if present_switch > 1:
        raise CLIError("'--correlation-id', '--resource-group', '--resource-uri'"
                       " and '--resource-provider' are optional and mutually exclusive.")

    formatter = "eventTimestamp ge {} and eventTimestamp le {}"
    odata_filters = _validate_time_range_and_add_defaults(start_time, end_time,
                                                          formatter=formatter)

    if correlation_id:
        odata_filters = _process_prameter(odata_filters, 'correlation_id',
                                          correlation_id, 'correlationId')
    elif resource_group:
        odata_filters = _process_prameter(odata_filters, 'resource_group',
                                          resource_group, 'resourceGroupName')
    elif resource_uri:
        odata_filters = _process_prameter(odata_filters, 'resource_uri',
                                          resource_uri, 'resourceId')
    elif resource_provider:
        odata_filters = _process_prameter(odata_filters, 'resource_provider',
                                          resource_provider, 'resourceProvider')
    if caller:
        odata_filters = _process_prameter(odata_filters, 'caller',
                                          caller, 'caller')
    if status:
        odata_filters = _process_prameter(odata_filters, 'status',
                                          status, 'status')
    if max_events:
        max_events = int(max_events)

    select_filter = _activity_logs_select_filter_builder(select)
    print(odata_filters)
    activity_logs = client.list(filter=odata_filters, select=select_filter)
    return _limit_results(activity_logs, max_events)


def _activity_logs_select_filter_builder(events=None):
    '''Build up select filter string from events
    '''
    if events:
        return ' , '.join(events)
    return None


def _process_prameter(default_filter, field_name, field_value, field_label):
    if not field_value:
        raise CLIError('Value for {} can not be empty.'.format(field_name))

    return _add_condition_if_present(default_filter, field_label, field_value)


def _add_condition_if_present(default_filter, field_label, field_value):
    if not field_value:
        return default_filter

    return "{} and {} eq '{}'".format(default_filter, field_label, field_value)


def _limit_results(paged, limit):
    results = []
    for index, item in enumerate(paged):
        if index < limit:
            results.append(item)
        else:
            break
    return list(results)
