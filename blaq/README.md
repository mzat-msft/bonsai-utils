# Blaq (Bonsai LogAnalytics Queries)

A collection of useful queries for LogAnalytics workspaces connected to
Bonsai.

## Install

The package can be used as a library.  Currently, the package is not available
on PyPI, therefore it can be installed in two alternative ways.
After successful installation you can simply import the functions defined in
the package.  For a selected list of available functions please read below.

#### Install by cloning the repo

First clone the [bonsai-utils](https://github.com/mzat-msft/bonsai-utils) repo.
Then, `cd` into `bonsai-utils/blaq` and type

```bash
pip install .
```

#### Install from Github link

Type in a shell

```bash
pip install -e 'git+https://github.com/mzat-msft/bonsai-utils/#egg=pkg&subdirectory=blaq'
```

## Queries

All queries assumes that the user provides the LogAnalytics workspace ID as
env variable named `LOG_WORKSPACE_ID`.  This information can be obtained from
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

### Run a custom query

If none of the implemented queries is useful for your use case, you can
always run a custom query by using the function

```python
get_query(query, flatten_json=True)
```

`flatten_json` is used for flattening json columns, that is create a column
for each key in a json dictionary.
