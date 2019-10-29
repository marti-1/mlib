import pickle
import numpy as np
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import time
import json
import requests

def serialize(obj, fname):
    with open(fname, 'wb') as handle:
        pickle.dump(obj, handle, protocol=pickle.HIGHEST_PROTOCOL)

def deserialize(fname):
    with open(fname, 'rb') as handle:
        b = pickle.load(handle)
    return b

def moving_avg(x, N):
     return np.convolve(x, np.ones((N,))/N, mode='valid')

def import_file(filename):
    return pd.read_csv(filename).to_dict('records')

def unix_time_to_dt(ts):
    try:
        return datetime.datetime.fromtimestamp(ts)
    except ValueError:
        return datetime.datetime.fromtimestamp(ts // 1000)

def date_trunc(dt, period = 'week'):
    if period == 'week':
        new_date = dt- datetime.timedelta(days=dt.weekday()+1)
        new_date = new_date.replace(hour=0,minute=0,second=0)
        return new_date

def plot(y):
    plt.plot(y)
    plt.show()

def bar_chart(y, x = None, opts = {}):
    ax = plt.gca()

    if (x is None):
        x = np.arange(len(y))

    plt.bar(x, y, align = 'center', alpha = .5)

    if 'labels' in opts:
        plt.xticks(x, opts['labels'])
        labels = ax.get_xticklabels()

        if 'label_every' in opts:

            for i, l in enumerate(labels):
                if (i % opts['label_every'] != 0):
                    labels[i] = ''
        ax.set_xticklabels(labels, rotation = opts.get('rotation', 90))
    plt.show()

def date_list_plot(dates, values, opts = {}):
    """
    DateListPlot(dates, [[v1], [v2], [v3]])
    DateListPlot(dates, [[v1], [v2]], opts = {'separate_axis': true})
    DateListPlot(dates, [v1])
    """
    # we need to plot multiple plots
    if isinstance(values[0], list):
        # we need things to be inverted
        if opts.get('separate_axis', False):
            assert(len(values) == 2)

            fig, ax1 = plt.subplots()

            color = 'C0'
            ax1.set_ylabel(opts['label'][0], color=color)
            ax1.plot(dates, values[0], color=color)
            ax1.tick_params(axis='y', labelcolor=color)

            ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

            color = 'C1'
            ax2.set_ylabel(opts['label'][1], color=color)  # we already handled the x-label with ax1
            ax2.plot(dates, values[1], color=color)
            ax2.tick_params(axis='y', labelcolor=color)

            fig.tight_layout()  # otherwise the right y-label is slightly clipped
        # TODO: cover multiple plots without inverted y-axis
    else:
        plt.plot(dates, values)
    plt.gcf().autofmt_xdate()
    plt.show()

def dataset(*args):
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
    out = {}
    for x in xs:
        key = fn(x)
        if key not in out:
            out[key] = []
        out[key].append(x)
    return out

def head(xs):
    return xs[:10]

def assoc(ds, k, v):
    return {**ds, k: v}
