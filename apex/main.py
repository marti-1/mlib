import pickle
import numpy as np
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import time
import json
import requests

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

def import_file(filename):
    """Import dataset file in CSV format.
    
    Parameters
    ----------
    filename : string

    Returns
    -------
    data : list of dicts
    
    """
    return pd.read_csv(filename).to_dict('records')

def unix_time_to_dt(ts):
    """Converts UNIX timestamp to DateTime object.

    Parameters
    ----------
    ts : int

    Returns
    -------
    datetime : DateTime

    """
    try:
        return datetime.datetime.fromtimestamp(ts)
    except ValueError:
        return datetime.datetime.fromtimestamp(ts // 1000)

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

def plot(y):
    """Line plot of data."""
    plt.plot(y)
    plt.show()

def bar_chart(y, x = None, labels = None, label_every=None):
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
                if (i % opts['label_every'] != 0):
                    labels[i] = ''
        ax.set_xticklabels(labels, rotation = opts.get('rotation', 90))
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

def dataset(*args):
    """Load dataset.

    Available datasets:
    * `cryptocurrency`, `{slug}` -- where `slug` is an identifier of a cryptocurrency identical to one used in coinmarketcap.com to identify a cryptocurrency.

    Parameters
    ----------
    args : list
        Path to a dataset

    Returns
    -------
    dataset : list of dicts

    Examples
    --------

        Get bitcoin prices:

        >>> dataset('cryptocurrency', 'bitcoin')
        {'market_cap_by_available_supply': [[1367174841000, 1500517590], ...

    """
    if args[0] == 'cryptocurrency':
        slug = args[1]

        def historical_coin_url(slug, start, end):
            return 'https://graphs2.coinmarketcap.com/currencies/{slug}/{start}000/{end}000/'.format(
                        slug=slug, 
                        start=int(time.mktime(start.timetuple())), 
                        end=int(time.mktime(end.timetuple()))
                    )

        def get_coin_history(slug, start, end):
            url = historical_coin_url(slug, start, end)
            data = json.loads(requests.get(url).content)
            return data

        start = datetime.date(2013, 4, 28)
        end = datetime.date.today()
        return get_coin_history(slug, start, end)

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
