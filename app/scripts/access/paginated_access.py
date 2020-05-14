import numpy as np
import pandas as pd

from app import app
from app.models import db, AccessLog


def fill_series(series, strat):
    new_vals = np.empty(len(series))
    for i in range(len(series)):
        curr_val = series.iloc[i]
        if np.isnan(curr_val):
            new_vals[i] = strat(new_vals[i - 1])
        else:
            new_vals[i] = curr_val
    return pd.Series(new_vals, index=series.index).astype(int)


def func(x):
    if (x % 2 == 0):
        return int(x * 1.2) % int(1e6)

    elif (x % 3 == 0):
        return int(x / 3) % int(1e6)
    else:
        return (x + 30) % int(1e6)


def seed_paginated_access(base_time, user_count=100000, req_per_user=10):
    try:
        db.session.query(AccessLog).delete()
        db.session.commit()
    except Exception:
        db.session.rollback()
    data = pd.read_sql('KV', db.engine, index_col='key')

    start_times = base_time + np.array([pd.Timedelta(seconds=x) for x in np.random.randint(0, 1e4, user_count)])

    df = pd.concat([
        pd.DataFrame(
            np.array([np.ones(req_per_user) * idx, range(req_per_user)]).T,
            index=pd.date_range(start, periods=req_per_user, freq='1min'),
            columns=['user_id', 'action']
        ) for idx, start in enumerate(start_times)
    ]).astype(int)

    df.loc[df.action == 0, 'key'] = np.random.randint(0, 1e6, user_count)
    df['key'] = fill_series(df['key'], func)  # paginate by 10
    df = df.assign(value=data.loc[df['key'].values].values)
    df = df.reset_index().rename({'index': 'time'}, axis=1).drop('action', axis=1).sort_values('time')
    df.to_sql('access_log', con=db.engine, index=False, if_exists='append', chunksize=1000)


if __name__ == '__main__':
    seed_paginated_access(pd.Timestamp.now())
