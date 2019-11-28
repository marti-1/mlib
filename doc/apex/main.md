# Table of Contents

  * [main](#main)
    * [serialize](#main.serialize)
    * [deserialize](#main.deserialize)
    * [moving\_avg](#main.moving_avg)
    * [import\_file](#main.import_file)
    * [export](#main.export)
    * [unixtime\_to\_dt](#main.unixtime_to_dt)
    * [dt\_to\_unixtime](#main.dt_to_unixtime)
    * [date\_trunc](#main.date_trunc)
    * [str\_to\_dt](#main.str_to_dt)
    * [plot](#main.plot)
    * [bar\_chart](#main.bar_chart)
    * [date\_list\_plot](#main.date_list_plot)
    * [dataset](#main.dataset)
    * [group\_by](#main.group_by)
    * [head](#main.head)
    * [assoc](#main.assoc)
    * [join](#main.join)
    * [parallel](#main.parallel)

# `main`


## `serialize()`

```python
def serialize(obj, fname)
```

Serialize object and store in a file.

## `deserialize()`

```python
def deserialize(fname)
```

Deserialize object stored in a file.

## `moving_avg()`

```python
def moving_avg(x, N)
```

Compute moving average.

Parameters
----------
x : list or ndarray
N : int
    Window size.

Returns
-------
result : ndarray

## `import_file()`

```python
def import_file(filename, fmt=None, as_dicts=True)
```

Import dataset file in CSV/JSON format.

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

## `export()`

```python
def export(xs, filename, fmt='csv')
```

Exports list to a file.

Parameters
----------
xs : list
filename: string
fmt : {"csv"}, optional
    format of the exported file

## `unixtime_to_dt()`

```python
def unixtime_to_dt(ts)
```

Converts UNIX timestamp to DateTime object.

Parameters
----------
ts : int,string,double

Returns
-------
datetime : DateTime

## `dt_to_unixtime()`

```python
def dt_to_unixtime(dt)
```

Converts DateTime object into Unix time integer.

Parameters
----------
dt : DateTime

Returns
-------
result : int

## `date_trunc()`

```python
def date_trunc(dt, period='week')
```

Truncates DateTime object.

Parameters
----------
dt : DateTime
period: {'week'}, optional

## `str_to_dt()`

```python
def str_to_dt(s)
```

Converts datetime string into a `datetime` object

Parameters
----------
s : string

Returns
-------
dt : datetime

## `plot()`

```python
def plot(ys, xs=None, opts=None)
```

Line plot of data.

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

## `bar_chart()`

```python
def bar_chart(y, x=None, labels=None, label_every=None, xlabel_rotation=90)
```

Bar chart of data.

Parameters
----------
y : list or ndarray
x : list or ndarray, optional
labels: list, optional
    List of labels of xticks.
label_every: int, optional
    Only label every xtick_idx % label_every == 0

## `date_list_plot()`

```python
def date_list_plot(dates, values, separate_axis=False, ylabel='', ylabel2='')
```

Plot points at a sequence of dates.

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

## `dataset()`

```python
def dataset(args, *,, ,, kwargs)
```

Load dataset.

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

## `group_by()`

```python
def group_by(xs, fn)
```

Group list by function.

Parameters
----------
xs : list
fn : lambda function 
    Function used to create bucket key

Returns
-------
out : dict

## `head()`

```python
def head(xs)
```

Get first 10 elements from a list.

Parameters
----------
xs : list

Returns
-------
top: list

## `assoc()`

```python
def assoc(ds, k, v)
```

Immutable single attribute update of a dictionary.

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

## `join()`

```python
def join(x, y)
```

Join two arrays of tuples on the first element.

Parameters
----------
x : list
y : list

Returns
-------
result : list

## `parallel()`

```python
def parallel(xs, fn, chunksize=1, n_workers=None)
```

Parallel execution of function over a list.

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

