from urllib import parse
import pickle
import numpy as np
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import time
import json
import requests
import collections
import os
import arrow
import csv

import pkg_resources


def serialize(obj, fname):
    """Serialize object and store in a file."""
    with open(fname, 'wb') as handle:
        pickle.dump(obj, handle, protocol=pickle.HIGHEST_PROTOCOL)

def deserialize(fname):
    """Deserialize object stored in a file."""
    with open(fname, 'rb') as handle:
        b = pickle.load(handle)
    return b

def moving_avg(x, N):
    """Compute moving average.

    Parameters
    ----------
    x : list or ndarray
    N : int
        Window size.

    Returns
    -------
    result : ndarray
    
    """
    return np.convolve(x, np.ones((N,))/N, mode='valid')

def import_file(filename, fmt=None, as_dicts = True):
    """Import dataset file in CSV/JSON format.
    
    Parameters
    ----------
    filename : string
    fmt : {"csv", "json"}, optional
        format of the imported file
    as_dicts : bool, optional
        should CSV file representing rows be dicts

    Returns
    -------
    data : list of dicts/lists

    Examples
    --------

        Import CSV file

        >>> import_file('filename.csv', as_dicts = False)

        Import remote JSON

        >>> import_file('https://remote.path/of/file', fmt = 'json')
    """

    def is_http_uri(x):
        if len(x) > 4 and x[:4] == 'http':
            return True
        else:
            return False

    _, file_extension = os.path.splitext(filename)
    if fmt is None:
        fmt = file_extension[1:]

    if is_http_uri(filename) and fmt == 'json':
        return json.loads(requests.get(filename).content)
    elif not is_http_uri(filename):
        if fmt == 'csv':
            if as_dicts:
                df = pd.read_csv(filename)
                return df.to_dict('records')
            else:
                with open(filename, newline='') as csvfile:
                    return list(csv.reader(csvfile))
        elif fmt == 'json':
            with open(filename, 'r') as f:
                return json.load(f)
        else:
            raise Exception('File type "{0}" is not supported'.format(fmt))

def export(xs, filename, fmt = 'csv'):
    """Exports list to a file.

    Parameters
    ----------
    xs : list
    filename: string
    fmt : {"csv"}, optional
        format of the exported file

    """
    assert(fmt in set(['csv', 'json']))
    with open(filename, 'w', newline='') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        for x in xs:
            wr.writerow(x)


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
    try:
        return datetime.datetime.fromtimestamp(ts)
    except ValueError:
        return datetime.datetime.fromtimestamp(ts // 1000)

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

def date_trunc(dt, period = 'week'):
    """Truncates DateTime object.

    Parameters
    ----------
    dt : DateTime
    period: {'week'}, optional

    """
    if period == 'week':
        new_date = dt- datetime.timedelta(days=dt.weekday()+1)
        new_date = new_date.replace(hour=0,minute=0,second=0)
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

def plot(ys, xs = None, opts = None):
    """Line plot of data.

    Parameters
    ----------
    ys : list or list of lists
    xs : list or list of lists, optional

    Examples
    --------

        >>> plot([a, b] opts = [
                {'linewidth' : 1, 'linestyle':'dashed'},
                {'linewidth' : 1},
            ])

    """

    if isinstance(ys[0], (collections.Sequence, np.ndarray)):

        if opts is None:
            opts = [{}] * len(ys)

        for idx, y in enumerate(ys):
            if xs is not None:
                plt.plot(y, xs[idx], **opts[idx])
            else:
                plt.plot(y, **opts[idx])
    else:
        if opts is None:
            opts = {}
        if xs is not None:
            plt.plot(ys, xs, opts)
        else:
            plt.plot(ys, opts)
    plt.show()

def bar_chart(y, x = None, labels = None, label_every=None, xlabel_rotation = 90):
    """Bar chart of data.

    Parameters
    ----------
    y : list or ndarray
    x : list or ndarray, optional
    labels: list, optional
        List of labels of xticks.
    label_every: int, optional
        Only label every xtick_idx % label_every == 0

    """
    ax = plt.gca()

    if (x is None):
        x = np.arange(len(y))

    plt.bar(x, y, align = 'center', alpha = .5)

    if labels is not None:
        plt.xticks(x, labels)
        labels = ax.get_xticklabels()

        if label_every is not None:
            for i, l in enumerate(labels):
                if (i % label_every != 0):
                    labels[i] = ''
        ax.set_xticklabels(labels, rotation = xlabel_rotation)
    plt.show()

def date_list_plot(dates, values, separate_axis = False, ylabel = '', ylabel2 = ''):
    """Plot points at a sequence of dates.

    Parameters
    ----------
    dates : list of strings
    values : list or list of two lists
    separate_axis : bool, optional
        Should separate axis be created for every list of values.
    ylabel : string, optional
        Label of first y-axis
    ylabel2 : string, optional
        Label of second y-axis

    Examples
    --------

        Plot single list of values by date:

        >>> date_list_plot(['2019-01-01', '2019-02-01'], [1,2])

        Plot two lists of values by date:

        >>> date_list_plot(['2019-01-01', '2019-02-01'], [[1,2],[2,3]], separate_axis = True, ylabel = "Price (USD)", ylabel2 = "Price (BTC)")

    """
    # we need to plot multiple plots
    if isinstance(values[0], list):
        # we need things to be inverted
        if separate_axis:
            assert(len(values) == 2)

            fig, ax1 = plt.subplots()

            color = 'C0'
            ax1.set_ylabel(ylabel, color=color)
            ax1.plot(dates, values[0], color=color)
            ax1.tick_params(axis='y', labelcolor=color)

            ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

            color = 'C1'
            ax2.set_ylabel(ylabel2, color=color)  # we already handled the x-label with ax1
            ax2.plot(dates, values[1], color=color)
            ax2.tick_params(axis='y', labelcolor=color)

            fig.tight_layout()  # otherwise the right y-label is slightly clipped
        # TODO: cover multiple plots without inverted y-axis
    else:
        plt.plot(dates, values)
    plt.gcf().autofmt_xdate()
    plt.show()

def dataset(*args, **kwargs):
    """Load dataset.

    Available datasets:
    * `cryptocurrency`, `{slug}` -- where `slug` is an identifier of a cryptocurrency identical to one used in coinmarketcap.com to identify a cryptocurrency.

    Parameters
    ----------
    args : list
        Path to a dataset
    kwargs : additional parameters

    Returns
    -------
    dataset : list of dicts

    Examples
    --------

        Get bitcoin prices:

        >>> dataset('cryptocurrency', 'bitcoin')
        [(1367272801, 143.99990845), (1367359201, 139.00004578),...

    """

    def historical_price(slug_id, start = None, end = None, interval = '1d'):
        if start is None:
            start = unixtime_to_dt(1367193601)

        if end is None:
            end = unixtime_to_dt(int(time.time()))

        url = 'https://web-api.coinmarketcap.com/v1/cryptocurrency/quotes/historical?convert=USD&format=chart_crypto_details&id={0}&interval={3}&time_end={2}&time_start={1}'.format(slug_id, dt_to_unixtime(start), dt_to_unixtime(end), interval)

        data = import_file(url, fmt='json')
        if data['status']['error_message'] is not None:
            raise Exception(data['status']['error_message'])
        data = data['data']
        prices = {(dt_to_unixtime(str_to_dt(ts)), row['USD'][0]) for ts, row in data.items()}
        return sorted(prices, key=lambda x: x[0])


    if args[0] == 'cryptocurrency':
        slug = args[1]
        id_slug = import_file(pkg_resources.resource_filename(__name__, 'data/cryptocurrency/cryptocurrency_id_slug.csv'), as_dicts = False)
        id_by_slug = {x[1]: int(x[0]) for x in id_slug}
        return historical_price(
            id_by_slug[slug],
            start = kwargs.get('start', None),
            end = kwargs.get('end', None),
            interval = kwargs.get('interval', '1d')
        )

    raise Exception('{0} is unknown dataset'.format(','.join(args)))


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

def join(x, y):
    """Join two arrays of tuples on the first element.

    Parameters
    ----------
    x : list
    y : list

    Returns
    -------
    result : list

    """
    out = []
    x_sorted = sorted(x, key=lambda k: k[0])
    y_sorted = sorted(y, key=lambda k: k[0])
    i = 0
    j = 0
    while i < len(x_sorted) and j < len(y_sorted):
        if x_sorted[i][0] < y_sorted[j][0]:
            i+=1
            continue
        if x_sorted[i][0] > y_sorted[j][0]:
            j+=1
            continue
        if x_sorted[i][0] == y_sorted[j][0]:
            r = [x_sorted[i][0]]
            r += x_sorted[i][1:] + y_sorted[j][1:]
            out.append(r)
            i += 1
            j += 1
    return out

import multiprocessing
from multiprocessing import Pool

def parallel(xs, fn, chunksize = 1, n_workers = None):
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
