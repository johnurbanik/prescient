import numpy as np
import pandas as pd

from app import app
from app.models import db


def populate_db():
    # TODO: Don't wipe all data
    db.drop_all()
    db.create_all()
    keys = pd.Series(np.arange(0, int(1e6)))
    values = pd.Series(np.random.randint(0, 1e6, int(1e6)))
    df = pd.concat([keys, values], axis=1)
    df.columns = ['key', 'value']
    df.to_sql('KV', con=db.engine, index=False, if_exists='append', chunksize=1000)


if __name__ == '__main__':
    populate_db()
