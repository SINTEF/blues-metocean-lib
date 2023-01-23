import json
from collections import Counter
from math import floor
from typing import Dict, Sequence, Tuple

import numpy as np
from numpy import arange, ndarray, number


class Scatter:
    def __init__(self, bin_size=1.0, scatter_dict: Dict = None) -> None:
        self.bin_size = bin_size
        bins = Counter()
        if scatter_dict:
            for (idx, sdict) in scatter_dict.items():
                cbin = Counter()
                for jdx, dict2 in sdict.items():
                    cbin[int(jdx)] = Counter(dict2.copy())
                bins[int(idx)] = cbin
        self.bins = bins

    def add(self, x: number, y: number, **kwargs) -> Dict:
        xbin = floor(x / self.bin_size)
        ybin = floor(y / self.bin_size)
        ybins: Counter = self.bins.get(xbin, Counter())
        cbin = ybins.get(ybin, Counter())
        cbin["occurences"] = cbin.get("occurences", 0) + 1
        for key, value in kwargs.items():
            existing = cbin.get(key, 0.0)
            cbin[key] = existing + value
        ybins[ybin] = cbin
        self.bins[xbin] = ybins
        return cbin

    def combine(self, other):
        if self.bin_size != other.bin_size:
            raise ValueError("Bin sizes differ")
        xbins1 = self.bins
        xbins2: Counter = other.bins
        for (idx, counter) in xbins2.items():
            existing: Counter = xbins1.get(idx)
            if existing:
                # Add the counts
                for (bin, count) in existing.items():
                    newcount = counter.get(bin)
                    if newcount:
                        existing[bin] = count + newcount

                for (bin, count) in counter.items():
                    if bin not in existing:
                        existing[bin] = count
            else:
                # New bin
                xbins1[idx] = counter

    def num_rows(self):
        bins = [int(row) for row in self.bins.keys()]
        return max(bins) + 1

    def num_columns(self):
        largest = -1
        for ybin in self.bins.values():
            bins = [int(row) for row in ybin.keys()]
            largest = max(largest, max(bins))
        return largest + 1

    def upper_rows(self) -> Sequence[number]:
        nrows = self.num_rows() + 1
        return arange(self.bin_size, nrows * self.bin_size, self.bin_size)

    def upper_columns(self) -> Sequence[number]:
        ncols = self.num_columns() + 1
        return arange(self.bin_size, ncols * self.bin_size, self.bin_size)

    def occurences(self) -> ndarray:
        nrows = self.num_rows()
        ncols = self.num_columns()
        occurences = np.zeros((nrows, ncols), dtype=int)
        for (row, ybins) in self.bins.items():
            for (column, bin) in ybins.items():
                occurences[row][column] = int(bin["occurences"])
        return occurences

    def mean_xy(self) -> Tuple[number, number]:
        xp = 0.0
        yp = 0.0
        for (row, ybins) in self.bins.items():
            for (column, bin) in ybins.items():
                occ = float(bin["occurences"])
                x = (row + 0.5) * self.bin_size
                y = (column + 0.5) * self.bin_size
                xp += occ * x
                yp += occ * y
        all_occurences = float(self.occurences().sum())
        xp = xp / all_occurences
        yp = yp / all_occurences
        return (xp, yp)

    def mean_of(self, key: str) -> number:
        vp = 0.0
        nvalues = 0
        for ybins in self.bins.values():
            for bin in ybins.values():
                occ = float(bin["occurences"])
                value = bin[key]
                if occ > 0:
                    vp += value
                    nvalues += occ
        if nvalues > 0:
            return vp / nvalues
        return 0.0

    def get(self, key) -> ndarray:
        nrows = self.num_rows()
        ncols = self.num_columns()
        values = np.zeros((nrows, ncols), dtype=float)
        for (row, ybins) in self.bins.items():
            for (column, bin) in ybins.items():
                occurence = int(bin["occurences"])
                if occurence > 0:
                    values[row][column] = float(bin.get(key, 0.0)) / occurence
        return values

    def __str__(self):
        return json.dumps(
            {"nrows": self.num_rows(), "ncols": self.num_columns(), "bins": self.bins},
            indent=4,
        )


def main():
    bin_size = 2.0
    scatter1 = Scatter(bin_size)
    scatter1.add(10.0, 0.1, wavedir=10.0)
    scatter1.add(11.0, 0.2, wavedir=10.0)
    scatter1.add(10.0, 1.0, wavedir=10.0)
    scatter1.add(10.0, 2.0, wavedir=10.0)
    scatter1.add(10.1, 10.0, wavedir=10.0)

    scatter2 = Scatter(bin_size, scatter1.bins)
    scatter2.add(10.0, 0.1, wavedir=10.0)
    scatter2.add(12.0, 0.2, wavedir=10.0)
    scatter2.add(11.0, 1.0, wavedir=10.0)
    scatter2.add(11.0, 2.0, wavedir=10.0)
    scatter2.add(10.1, 10.0, wavedir=10.0)

    print("scatter1=")
    print(scatter1)
    print("scatter2=")
    print(scatter2)
    print("combined")
    scatter1.combine(scatter2)
    print(scatter1)

    print("hs=" + str(scatter1.upper_rows()))
    print("tp=" + str(scatter1.upper_columns()))
    print(scatter1.occurences())
    print(scatter1.get("wavedir"))

    print(scatter1.mean_xy())
    print(scatter1.mean_of("wavedir"))


if __name__ == "__main__":
    main()
