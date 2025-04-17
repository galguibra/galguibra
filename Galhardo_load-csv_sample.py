"""Processes CSV imports into pandas DataFrames.

Summary
-------
    load_csv is based on the existing pandas.read_csv, but allows batch
    importing while leveraging a pre-defined nested dictionary and a CSV object
    class to manage relative paths to the appropriate directory within the
    resource namespace package.
    
@author: Guilherme Galhardo
"""

import pandas as pd
import numpy as np
import collections
import typing
import importlib.resources


class FileOrganizer(collections.OrderedDict):
    """Nested dictionary for storing file names and righthand column bounds.
    
    Allows direct access to values on nested inner layers using the typical
    dict access syntax, e.g. dict[key_0]...[key_n], and retains the order of
    entries.
    
    Public Methods
    --------------
    get_file_info
        Recursive retrieval function that optionally outputs file names, file
        bounds, or both. Calls _yield_inner as a subroutine.
    
    Private Methods
    ---------------
    __missing__
    
    _yield_all
        
    """
    def __missing__(self, key: str):
        # Enable simplified layered lookup through dictionary layers.
        value = self[key] = FileOrganizer()
        return value
        
    def _yield_inner(self):
        # Iterate recursively through dictionary and yield all innermost items.
        for key, value in self.items():
            if isinstance(value, FileOrganizer):
                yield from value._yield_inner()
            else:
                yield key, value
                
    def get_file_info(self, mode: str) -> list[str | int | tuple[str, int]]:
        """Output list containing choice of file names, file bounds, or both.
        
        Calls recursive _yield_inner method to gather items.
        
        Parameters
        ----------
        mode : str
            Determines if info will return a list of file names, file bounds,
            or both. If passed as 'both', list items will be tuples of the form
            (name, bound).
            
        Returns
        -------
        info : list[str | int | tuple[str, int]]
            A list of file names, file bounds, or both, depending on the value
            of mode. If mode is passed as 'both', the list will contain tuples
            with both names and bounds.
          
        """
        contents = dict(self._yield_inner())

        if mode == "names":
            info = list(contents.keys())
        elif mode == "bounds":
            info = list(contents.values())
        elif mode == "both":
            info = list(contents.items())
        else:
            raise ValueError("Mode must be one of 'name' 'bounds' or 'both'.")
            
        return info
        

# Loadable datasets with righthand column bounds, organized by category.
FILE_DICT = FileOrganizer(
    [
        (
            "non-data",
            FileOrganizer(
                [("attendance", 1), ("demographics", 8), ("strata", 1)]
            ),
        ),
        (
            "behavior",
            FileOrganizer(
                [
                    ("coparenting", 14),
                    ("involvement", 42),
                    ("self-efficacy", 20),
                    ("stress", 37),
                ]
            ),
        ),
        (
            "self-appraisal",
            FileOrganizer(
                [("follow-up", 26), ("primiparous", 26), ("multiparous", 26)]
            ),
        ),
    ]
)


class CSV:
    """Represents a CSV file to be loaded for import using load_csv.

    Attributes
    ----------
    name : str
        Name of file without path or file extension.
        
    header : int
        Indicates which row should be read as the header row if the data
        has labelled headers. Default is None.

    Returns
    -------
        df : pd.DataFrame
            Pandas DataFrame containing the data from the file.
    """
    def __init__(self, name: str, header: int | None = None) -> None:
        self.name = name
        self.header = header
        
        if self.name not in FILE_DICT.get_file_info("names"):
            raise ValueError(
            "File not found. Please input a file from FILE_DICT."
            )

        # sets initial namespace directory to generate file path.
        self.path = "resources.raw"

        """adjusts working directory as needed to further specify file path.

        also sets bounds for file import by checking the file name against
        the index of its rightmost column.
        """
        if self.name in FILE_DICT["non-data"].keys():
            self.bound = FILE_DICT["non-data"][self.name]
        else:
            prefix = "data"
            group = (
                "behavior"
                if name in FILE_DICT["behavior"].keys()
                else "self_appraisal"
            )

            self.bound = FILE_DICT[f"{group}"][self.name]

            self.path += f".{prefix}.{group}"

            if group == "behavior":
                pass
            elif self.name == "follow_up":
                self.path += ".baseline"
            else:
                pass

        csv = importlib.resources.files(self.path)

        # reads file into a pandas dataframe.
        with importlib.resources.as_file(csv / f"{name}.csv") as file:

            self.df = pd.read_csv(
                file,
                sep=",",
                usecols=np.arange(self.bound),
                header=self.header,
            )

    def __call__(self) -> pd.DataFrame:
        """Make self.df assignable by calling the CSV.

        Returns
        -------
        df : pd.DataFrame
            dataframe containing the data from the file.
        """
        return self.df


def load_csv(
    names: list[str], 
    headers: list[int | None ] | None = None,
) -> pd.DataFrame | list[pd.DataFrame]:
    """Batch-convert input .csv files to pandas dataframes.

    Parameters
    ----------
    names : list[str]
        List of each input file's name, without filepath or .csv extension.
    
    Optional Parameters
    -------------------
    headers : list[int | None] | None 
        List of rows that should be read as the column labels for each
        respective file, if labels are provided. default is None for any
        file without labels.

    Returns
    -------
    frames : pd.DataFrame | list[pd.DataFrame]
        list of pandas dataframes corresponding to each file input.

    """
    names = names
    headers = headers

    if headers is not None:
        # collates each file's set of parameters into a tuple.
        param_cross = [
            (name, header) for (name, header) in list(zip(names, headers))
        ]

        # constructs/calls each file's CSV class instance to obtain dataframe.
        frames = [
            csv()
            for csv in [
                CSV(
                    *params,
                )
                for params in param_cross
            ]
        ]
    else:
        frames = [csv() for csv in [CSV(name) for name in names]]

    # checks for a singleton frame to avoid an unnecessary list.
    if len(frames) > 1:
        pass
    else:
        frames = frames[0]

    return frames
