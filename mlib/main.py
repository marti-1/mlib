import pickle
import numpy as np
import datetime
import time
import json
import requests
import arrow
import csv


#     ___ _ _
#    / __(_) | ___  ___
#   / _\ | | |/ _ \/ __|
#  / /   | | |  __/\__ \
#  \/    |_|_|\___||___/
#

def serialize(obj, fname):
    """Serialize object and store in a file."""
    with open(fname, 'wb') as handle:
        pickle.dump(obj, handle, protocol=pickle.HIGHEST_PROTOCOL)


def deserialize(fname):
    """Deserialize object stored in a file."""
    with open(fname, 'rb') as handle:
        b = pickle.load(handle)
    return b


def import_csv(filename, as_dicts=True):
    with open(filename, newline='') as csvfile:
        if as_dicts:
            reader = csv.DictReader(csvfile)
        else:
            reader = csv.reader(csvfile)
        return list(reader)

def import_json(filename, remote=False):
    if remote:
        return json.loads(requests.get(filename).content)
    else:
        with open(filename, 'r') as f:
            return json.load(f)


def export_csv(filename, data, as_dicts=True):
    with open(filename, 'w', newline='') as csvfile:
        if as_dicts:
            wr = csv.DictWriter(csvfile, fieldnames=data[0].keys())
            wr.writeheader()
            wr.writerows(data)
        else:
            wr = csv.writer(csvfile)
            wr.writerows(data)


def export_json(filename, data):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


#   _____ _
#  /__   (_)_ __ ___   ___
#    / /\/ | '_ ` _ \ / _ \
#   / /  | | | | | | |  __/
#   \/   |_|_| |_| |_|\___|
#

def unixtime_to_dt(ts):
    """Converts UNIX timestamp to DateTime object.

    Parameters
    ----------
    ts : int,string,double

    Returns
    -------
    datetime : DateTime

    """
    ts = int(ts)
    return arrow.get(ts).datetime


def dt_to_unixtime(dt):
    """Converts DateTime object into Unix time integer.

    Parameters
    ----------
    dt : DateTime

    Returns
    -------
    result : int

    """
    return int(time.mktime(dt.timetuple()))


def date_trunc(dt, period='week'):
    """Truncates DateTime object.

    Parameters
    ----------
    dt : DateTime
    period: {'week'}, optional

    """
    if period == 'week':
        new_date = dt - datetime.timedelta(days=dt.weekday() + 1)
        new_date = new_date.replace(hour=0, minute=0, second=0)
        return new_date


def str_to_dt(s):
    """Converts datetime string into a `datetime` object

    Parameters
    ----------
    s : string

    Returns
    -------
    dt : datetime

    """
    return arrow.get(s).datetime


#     ____      _ _           _   _
#    / ___|___ | | | ___  ___| |_(_) ___  _ __  ___
#   | |   / _ \| | |/ _ \/ __| __| |/ _ \| '_ \/ __|
#   | |__| (_) | | |  __/ (__| |_| | (_) | | | \__ \
#    \____\___/|_|_|\___|\___|\__|_|\___/|_| |_|___/
#

def group_by(xs, fn):
    """Group list by function.

    Parameters
    ----------
    xs : list
    fn : lambda function 
        Function used to create bucket key

    Returns
    -------
    out : dict


    """
    out = {}
    for x in xs:
        key = fn(x)
        if key not in out:
            out[key] = []
        out[key].append(x)
    return out


def head(xs):
    """Get first 10 elements from a list.

    Parameters
    ----------
    xs : list

    Returns
    -------
    top: list

    """
    return xs[:10]


def assoc(ds, k, v):
    """Immutable single attribute update of a dictionary.

    Parameters
    ----------
    ds : dict
    k : string 
        Key.
    v : string
        Value.

    Returns
    -------
    result : dict

    """
    return {**ds, k: v}


def unzip(xs):
    return zip(*xs)

def first(iterable, condition = lambda x: True):
    """
    Returns the first item in the `iterable` that
    satisfies the `condition`.

    If the condition is not given, returns the first item of
    the iterable.

    Raises `StopIteration` if no item satysfing the condition is found.

    >>> first( (1,2,3), condition=lambda x: x % 2 == 0)
    2
    >>> first(range(3, 100))
    3
    >>> first( () )
    Traceback (most recent call last):
    ...
    StopIteration
    """

    return next(x for x in iterable if condition(x))

def flatten(xs):
    return [item for sublist in xs for item in sublist]

def partition_by_mask(xs, mask):
    keys = np.unique(mask)
    out = []
    for key in keys:
        out.append(xs[np.where(mask == key)])
    return out

#                _ _   _                                   _
#    /\/\  _   _| | |_(_)_ __  _ __ ___   ___ ___  ___ ___(_)_ __   __ _
#   /    \| | | | | __| | '_ \| '__/ _ \ / __/ _ \/ __/ __| | '_ \ / _` |
#  / /\/\ \ |_| | | |_| | |_) | | | (_) | (_|  __/\__ \__ \ | | | | (_| |
#  \/    \/\__,_|_|\__|_| .__/|_|  \___/ \___\___||___/___/_|_| |_|\__, |
#                       |_|                                        |___/
import multiprocessing
from multiprocessing import Pool


def parallel(xs, fn, chunksize=1, n_workers=None):
    """Parallel execution of function over a list.

    Parameters
    ----------
    xs : list
    fn : function
    chunksize : int, optional
                Number of items to assign for each worker.
    n_workers : int, optional
                Number of parallel workers to run.
    
    Returns
    -------
    result : list

    Examples
    --------

        def f(x):
            time.sleep(.5)

        out = parallel(range(1000), f)

    """
    if n_workers is None:
        n_workers = multiprocessing.cpu_count()
    with Pool(n_workers) as p:
        return p.map(fn, xs, chunksize)
