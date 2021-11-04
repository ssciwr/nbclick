# nbclick - Turn Jupyter notebooks into command line applications

`nbclick` allows you to modify and run Jupyter notebooks from the commandline.
It builds on top of [nbparameterise](https://github.com/takluyver/nbparameterise) which allows
programmatic extraction and modification of parameters of Jupyter notebooks.

## Installation

`nbclick` can be installed using `pip`:

```
python -m pip install git+https://github.com/ssciwr/nbclick.git
```

## Running nbclick

After installation, you can run `nbclick` using the commandline:

```
nbclick --help
```

The most important argument is the `NOTEBOOK` parameter. For a given notebook,
you can again use `--help` to display the configuration options:

```
nbclick mynotebook.ipynb --help
```

Running without `--help` will programmatically execute the notebook with
the parameters specified on the command line.

## Preparing a notebook for execution with nbclick

`nbclick` relies on `nbparameterise` to extract command line options from your
Jupyter notebook. The best way to specify customizable parameters is to place
them into the first code cell of the notebook as simple assignments:

```python
num_samples = 1000      # The number of samples to draw
outfile = "output.csv"  # The filename to store the results
```

For above case, the output of `nbclick notebook.ipynb --help` will be:

```
Usage: nbclick notebook.ipynb [OPTIONS]

Options:
  --num_samples INTEGER  The number of samples to draw  [default: 1000]
  --outfile TEXT         The filename to store the results  [default:
                         output.csv]
  --help                 Show this message and exit.
```