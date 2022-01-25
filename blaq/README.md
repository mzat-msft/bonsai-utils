# Blaq (Bonsai LogAnalytics Queries)

A collection of useful queries for LogAnalytics workspaces connected to
Bonsai.

## Install

The package can be used as a library. At the moment the only way it can be
installed is by

1. Cloning the [bonsai-utils](https://github.com/mzat-msft/bonsai-utils) repo
2. In `bonsai-utils/blaq` folder, type

```bash
pip install .
```

After that you can simply import the functions defined in the package.
For a selected list of available functions please keep reading.

## Queries

All queries assumes that the user provides the LogAnalytics workspace ID as
env variable named `LOG_WORKSPACE_ID`. This information can be obtained from
the azure portal page related to the workspace in Bonsai's Resource Group.

Queries results are returned to the user as Pandas' dataframes.

### Get all data from a custom assessment

A helper function to get all entries related to a custom assessment.

Example usage:

```python
from blaq import get_assessment_data

data = get_assessment_data('custom_assessment_1', brain_name='brain', brain_version='21')
data = get_assessment_data('custom_assessment_1', brain_name='brain')
data = get_assessment_data('custom_assessment_1')
```
