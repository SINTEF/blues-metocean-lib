import json
from math import floor
from typing import Callable, Dict, Sequence, Tuple

import numpy as np
from numpy import arange, ndarray, number


class Scatter:
    """A class for storing and combining scatter data
    """

    class Bins(dict):
        """Based on collections.Counter but with support for adding lists"""

        def __add__(self, other):
            if not isinstance(other, Scatter.Bins):
                return NotImplemented
            result = Scatter.Bins()
            for elem, count in self.items():
                ov = other[elem]
                newcount = count + ov
                result[elem] = newcount
            for elem, count in other.items():
                if elem not in self:
                    result[elem] = count
            return result

    def __init__(self, bin_size=1.0) -> None:
        """
        Parameters
        ----------
        bin_size : float
            The bin size to use default is 1.0
        """
        self.bin_size = bin_size
        self.bins = Scatter.Bins()

    def add(self, x: number, y: number, **kwargs) -> Dict:
        """Add a point to the scatter. Optionally add additional data stored in the bin"""
        xbin = floor(x / self.bin_size)
        ybin = floor(y / self.bin_size)
        ybins = self.bins.get(xbin, Scatter.Bins())
        cbin = ybins.get(ybin, Scatter.Bins())
        cbin["occurences"] = cbin.get("occurences", 0) + 1
        for key, value in kwargs.items():
            existing = cbin.get(key, [])
            existing.append(value)
            cbin[key] = existing
        ybins[ybin] = cbin
        self.bins[xbin] = ybins
        return cbin

    def combine(self, other: "Scatter"):
        """Combine with given scatter"""
        if self.bin_size != other.bin_size:
            raise ValueError("Bin sizes differ")
        xbins1 = self.bins
        xbins2 = other.bins
        for (idx, counter) in xbins2.items():
            existing = xbins1.get(idx)
            if existing:
                # Add the counts
                for (ybin, count) in existing.items():
                    newcount = counter.get(ybin)
                    if newcount:
                        existing[ybin] = count + newcount

                for (ybin, count) in counter.items():
                    if ybin not in existing:
                        existing[ybin] = count
            else:
                # New bin
                xbins1[idx] = counter

    def num_rows(self):
        """Number of rows"""
        bins = [int(row) for row in self.bins.keys()]
        return max(bins) + 1

    def num_columns(self):
        """Number of columns"""
        largest = -1
        for ybin in self.bins.values():
            bins = [int(row) for row in ybin.keys()]
            largest = max(largest, max(bins))
        return largest + 1

    def row_values(self) -> ndarray:
        """Upper row values"""
        nrows = self.num_rows() + 1
        return arange(self.bin_size, nrows * self.bin_size, self.bin_size)

    def column_values(self) -> ndarray:
        """Upper column values"""
        ncols = self.num_columns() + 1
        return arange(self.bin_size, ncols * self.bin_size, self.bin_size)

    def occurences(self) -> ndarray:
        """Occurences of all the bins"""
        nrows = self.num_rows()
        ncols = self.num_columns()
        occurences = np.zeros((nrows, ncols), dtype=int)
        for (row, ybins) in self.bins.items():
            for (column, ybin) in ybins.items():
                occurences[row][column] = int(ybin["occurences"])
        return occurences

    def mean_xy(self) -> Tuple[number, number]:
        """Mean x and y"""
        xp = 0.0
        yp = 0.0
        for (row, ybins) in self.bins.items():
            for (column, ybin) in ybins.items():
                occ = float(ybin["occurences"])
                x = (row + 0.5) * self.bin_size
                y = (column + 0.5) * self.bin_size
                xp += occ * x
                yp += occ * y
        all_occurences = float(self.occurences().sum())
        xp = xp / all_occurences
        yp = yp / all_occurences
        return (xp, yp)

    def get_values(self, key, reducer: Callable[[Sequence],float]=None) -> ndarray:
        """Get the values for a given key, reduse the list of values using the reducer or the mean if no reducer is given"""
        nrows = self.num_rows()
        ncols = self.num_columns()
        values = np.zeros((nrows, ncols), dtype=float)
        for (row, ybins) in self.bins.items():
            for (column, ybin) in ybins.items():
                kvalues = ybin.get(key)
                if kvalues:
                    if reducer:
                        values[row][column] = reducer(kvalues)
                    else:
                        values[row][column] = sum(kvalues) / len(kvalues)
        return values

    def __str__(self):
        return json.dumps(
            {
                "row": self.row_values().tolist(),
                "column": self.column_values().tolist(),
                "occurences": self.occurences().tolist(),
            },
        )


def main():
    """Demonstrate the scatter"""
    bin_size = 4.0
    scatter1 = Scatter(bin_size)
    scatter1.add(10.0, 0.1, wavedir=10.0)
    scatter1.add(11.0, 0.2, wavedir=11.0)
    scatter1.add(10.0, 1.0, wavedir=12.0)
    scatter1.add(10.0, 2.0, wavedir=12.0)
    scatter1.add(10.1, 10.0, wavedir=13.0)

    scatter2 = Scatter(bin_size)
    scatter2.add(10.0, 0.1, wavedir=15.0)
    scatter2.add(12.0, 0.2, wavedir=15.0)
    scatter2.add(11.0, 1.0, wavedir=20.0)
    scatter2.add(11.0, 2.0, wavedir=17.0)
    scatter2.add(10.1, 10.0, wavedir=9.0)

    print("scatter1=")
    print(scatter1)
    print("scatter2=")
    print(scatter2)
    print("combined")
    scatter1.combine(scatter2)
    print(scatter1)

    print("hs=" + str(scatter1.row_values()))
    print("tp=" + str(scatter1.column_values()))
    print(scatter1.occurences())
    print("Scatter of wavedir=")


    print(scatter1.get_values("wavedir"))

    print(scatter1.mean_xy())


if __name__ == "__main__":
    main()
