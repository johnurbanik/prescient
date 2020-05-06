import numpy as np
import pandas as pd

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


def seed_paginated_access(base_time, user_count=1000, req_per_user=100):
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

    df.loc[df.action == 0, 'key'] = np.random.randint(0, 1e6, 1000)
    df['key'] = fill_series(df['key'], lambda x: (x + 10) % int(1e6))  # paginate by 10
    df = df.assign(value=data.loc[df['key'].values].values)
    df = df.reset_index().rename({'index': 'time'}).drop('action', axis=1)

    df.to_sql('AccessLog', con=db.engine, index=False, if_exists='append', chunksize=1000)


if __name__ == '__main__':
    seed_paginated_access(pd.Timestamp.now())
