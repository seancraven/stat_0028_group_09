from __future__ import annotations
import numpy as np
import pandas as pd
from typing import Union, Any, Dict


class BikeData:
    """
    BikeData provides a set of methods which can be used to extract and plot
    subsets from the bike rental dataset.
    """

    def __init__(self, data: Union[str, pd.DataFrame]):
        """
        Bike data can be initialized with a csv or a dataframe.
        Args:
            data: string path to csv, or a dataframe with the same
                features.
        """
        self.types = [
            "hourly",
            "daily",
        ]
        self.data = self._data_df(data)
        self.type = self._find_type()
        # instant column are just index
        self._drop_instant()
        self.features = self.data.columns.to_list()

    def _drop_instant(self):
        try:
            self.data["instant"]
            self.data.drop("instant")
        except KeyError:
            pass

    def _data_df(self, data):
        if not isinstance(data, pd.DataFrame):
            return pd.read_csv(data)
        else:
            return data

    def subset(self, **subset_dicts) -> BikeData:
        """
        Produces a new instance of the BikeData Class, where all of the
        entries obey the conditions passed.

        Each kwarg takes a dictionary of the form kwarg={column: vale}.
        The kwarg itself determines what operator is used.
        column must be a string in self.features. The value is that which
        The equality is applied to.

        Examples:
            BikeData(..).subset(eq={"hr":10})
            This returns a new bikedata instance, where the data is only
            that where hr == 10.

        Keyword Args:
             eq: ==
             l: <
             leq: <=
             g: >
             geq: >=


        Returns:
            subset: BikeData instance where the data is a subset that obeys
                all of the constraints passed.

        """
        _op = {
            "eq": np.equal,
            "l": np.less,
            "leq": np.less_equal,
            "g": np.greater,
            "geq": np.greater_equal,
        }
        mask = []
        for comparison_op, dict in subset_dicts.items():
            assert comparison_op in _op.keys()
            for key, value in dict.items():
                assert key in self.features
                mask.append(_op[comparison_op](self.data[key], value))
        mask = np.bitwise_and.reduce(mask)
        subset = self.data.loc[mask]
        return BikeData(subset)

    def column_reduce(
        self, reduction_key: str, reduction_column: str, reduction_operator=np.sum
    ) -> Dict:
        """
        Performs a functional reduction of the reduction column, which have
        the same values in the reduction key values in the bike data object.

        Args:
            reduction_column: Column of values which the values are reduced over.
            reduction_key: Column of values which defines set of values
                which the reduction is performed over. The sets are formed
                of values which have the same key.
            reduction_operator: Operator that maps set to single value

        Returns:
            reduction : dataframe of size (unique keys, 2)
            Column[0] keys
            Column[1] reduce(set of values with same keys)
        """
        unique_keys = np.unique(self.data[reduction_key])
        reduction = {}
        for key in unique_keys:
            mask = self.data[reduction_key] == key
            reduction[key] = reduction_operator((self.data[reduction_column])[mask])
        return reduction

    def union(self, bikedata):
        """
        Adds the data from two instances of BikeData.
        This is designed for joining mutually exclusive subsets.
        """
        union_data = pd.concat((self.data, bikedata.data), ignore_index=True)
        union_data.sort_values(by="hr")
        return BikeData(union_data)

    def _find_type(self) -> str:
        hourly_features = [
            "instant",
            "dteday",
            "season",
            "yr",
            "mnth",
            "hr",
            "holiday",
            "weekday",
            "workingday",
            "weathersit",
            "temp",
            "atemp",
            "hum",
            "windspeed",
            "casual",
            "registered",
            "cnt",
        ]
        daily_features = [
            "instant",
            "dteday",
            "season",
            "yr",
            "mnth",
            "holiday",
            "weekday",
            "workingday",
            "weathersit",
            "temp",
            "atemp",
            "hum",
            "windspeed",
            "casual",
            "registered",
            "cnt",
        ]
        if set(self.data.columns.to_list()).issuperset(hourly_features):
            return "hourly"
        elif set(self.data.columns.to_list()).issuperset(daily_features):
            return "daily"
        else:
            print("Not a valid Dataset, lacks the correct features.")
            print("Missing features:")
            for i in self.data.columns.to_list():
                if i not in (hourly_features or daily_features):
                    print(i)
            raise KeyError


if __name__ == "__main__":
    daily = BikeData("day.csv")
    hourly = BikeData("hour.csv")
    spring_summer = daily.subset(leq={"season": 2}, eq={"holiday": 0, "workingday": 1})
    assert spring_summer.data["season"].all() < 2
    assert spring_summer.data["workingday"].all() == 1
    assert spring_summer.data["holiday"].all() == 0
