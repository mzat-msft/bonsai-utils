"""
Main connector to Log Analytics.

Please check:
https://docs.microsoft.com/en-us/python/api/overview/azure/monitor-query-readme?view=azure-python
"""
from copy import deepcopy
import json
import os
from typing import Union

import pandas as pd
from azure.identity import DefaultAzureCredential
from azure.monitor.query import LogsQueryClient, LogsQueryStatus

__all__ = [
    'LogsQueryConnector',
    'get_assessment_data',
]


class LogsQueryConnector:
    def __init__(self):
        self.client = LogsQueryClient(DefaultAzureCredential())

    def query(
            self,
            query: str,
            timespan=None,
            workspace_id: str = None
    ) -> pd.DataFrame:
        workspace_id = (
            workspace_id
            if workspace_id is not None
            else os.getenv('LOG_WORKSPACE_ID')
        )
        response = self.client.query_workspace(
            workspace_id=workspace_id,
            query=query,
            timespan=timespan,
        )
        if response.status == LogsQueryStatus.PARTIAL:
            error = response.partial_error
            data = response.partial_data
            print(error.message)
        elif response.status == LogsQueryStatus.SUCCESS:
            data = response.tables
        df = pd.DataFrame(data=data[0].rows, columns=data[0].columns)
        df = df.drop_duplicates()
        df = df.reset_index(drop=True)
        return df


def is_json_dict(elem):
    """Return True when elem is properly formed JSON dictionary."""
    try:
        parsed = json.loads(elem)
    except (json.decoder.JSONDecodeError, TypeError):
        return False

    try:
        parsed.keys()
        return True
    except AttributeError:
        return False


def columnify_json(df_orig: pd.DataFrame, keep_orig=False) -> pd.DataFrame:
    """Search for JSON in columns and normalize into multiple columns."""
    df = deepcopy(df_orig)

    if len(df) <= 0:
        return df
    elif len(df) != max(df.index) + 1:
        raise ValueError("df.index must be in range(0, len(df) - 1)")

    for col in df.columns:
        if df[col].apply(is_json_dict).sum() == 0:
            continue
        col_json = df[col].fillna('{}').apply(lambda x: json.loads(x))
        # TODO: Understand why pd.json_normalize casts some int to float
        df_col = pd.json_normalize(col_json)
        if len(df_col) and not df_col.empty:
            # Join on index, hence the requirement of indices in correct range
            df = df.join(df_col)
        if not keep_orig:
            df = df.drop(columns=col)
    return df


def get_assessment_data(
        assessment_name: str,
        *,
        brain_name: str = None,
        brain_version: Union[str, int] = None,
) -> pd.DataFrame:
    """Get custom assessment data."""
    where_clause = f"where AssessmentName_s == '{assessment_name}'\n"
    if brain_name is not None:
        where_clause = where_clause.rstrip() + f" and BrainName_s == '{brain_name}'\n"

    if brain_version is not None:
        where_clause = (
            where_clause.rstrip() + f" and BrainVersion_d == '{brain_version}'\n"
        )

    query = f"""
        EpisodeLog_CL
          | {where_clause}
          | join kind=inner (
              IterationLog_CL
              | sort by Timestamp_t desc
          ) on EpisodeId_g
          | project
              Brain=BrainName_s,
              BrainVersion=BrainVersion_d,
              AssessmentName = AssessmentName_s,
              EpisodeId = EpisodeId_g,
              IterationIndex = IterationIndex_d,
              Timestamp = Timestamp_t,
              SimConfig = parse_json(SimConfig_s),
              SimState = parse_json(SimState_s),
              SimAction = parse_json(SimAction_s),
              Reward = Reward_d,
              CumulativeReward = CumulativeReward_d,
              GoalMetrics = parse_json(GoalMetrics_s),
              Terminal = Terminal_b,
              FinishReason = FinishReason_s,
              LessonIndex = LessonIndex_d,
              EpisodeType = EpisodeType_s
          | order by EpisodeId asc, IterationIndex asc
    """
    log_query = LogsQueryConnector()
    data = log_query.query(query)
    data = columnify_json(data)
    return data
