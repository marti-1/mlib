Module apex.main
================

Functions
---------

    
`assoc(ds, k, v)`
:   Immutable single attribute update of a dictionary.
    
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

    
`bar_chart(y, x=None, labels=None, label_every=None)`
:   Bar chart of data.
    
    Parameters
    ----------
    y : list or ndarray
    x : list or ndarray, optional
    labels: list, optional
        List of labels of xticks.
    label_every: int, optional
        Only label every xtick_idx % label_every == 0

    
`dataset(*args)`
:   Load dataset.
    
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

    
`date_list_plot(dates, values, separate_axis=False, ylabel='', ylabel2='')`
:   Plot points at a sequence of dates.
    
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

    
`date_trunc(dt, period='week')`
:   Truncates DateTime object.
    
    Parameters
    ----------
    dt : DateTime
    period: {'week'}, optional

    
`deserialize(fname)`
:   Deserialize object stored in a file.

    
`group_by(xs, fn)`
:   Group list by function.
    
    Parameters
    ----------
    xs : list
    fn : lambda function 
        Function used to create bucket key
    
    Returns
    -------
    out : dict

    
`head(xs)`
:   Get first 10 elements from a list.
    
    Parameters
    ----------
    xs : list
    
    Returns
    -------
    top: list

    
`import_file(filename)`
:   Import dataset file in CSV format.
    
    Parameters
    ----------
    filename : string
    
    Returns
    -------
    data : list of dicts

    
`moving_avg(x, N)`
:   Compute moving average.
    
    Parameters
    ----------
    x : list or ndarray
    N : int
        Window size.
    
    Returns
    -------
    result : ndarray

    
`plot(y)`
:   Line plot of data.

    
`serialize(obj, fname)`
:   Serialize object and store in a file.

    
`unix_time_to_dt(ts)`
:   Converts UNIX timestamp to DateTime object.
    
    Parameters
    ----------
    ts : int
    
    Returns
    -------
    datetime : DateTime