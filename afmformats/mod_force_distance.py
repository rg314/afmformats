from .afm_data import AFMData


__all__ = ["AFMForceDistance", "Segment"]


class AFMForceDistance(AFMData):
    """Base class for AFM force-distance data

    A force-distance dataset consists of an approach and
    a retract curve.
    """
    def __setitem__(self, key, values):
        if len(values) != len(self):
            raise ValueError(
                f"Cannot set data '{key}' of length '{len(values)}' "
                + f"for AFMForceDistance of length '{len(self)}'!")
        # do not touch raw data
        self._data[key] = values

    @property
    def appr(self):
        """Dictionary-like interface to the approach segment"""
        return Segment(self._raw_data, self._data, which="approach")

    @property
    def modality(self):
        """Imaging modality"""
        return "force-distance"

    @property
    def retr(self):
        """Dictionary-like interface to the retract segment"""
        return Segment(self._raw_data, self._data, which="retract")


class Segment(object):
    """Simple wrapper around dict-like `data` to expose a single segment"""

    def __init__(self, raw_data, data, which="approach"):
        if which not in ["approach", "retract"]:
            raise ValueError("`which` must be 'approach' or 'retract', "
                             + "got '{}'!".format(which))
        #: The segment type (approach or retract)
        self.which = which
        if which == "approach":
            self.idx = False
        else:
            self.idx = True
        self.raw_data = raw_data
        self.data = data

        # determine segment
        if "segment" in raw_data:
            self.segment_index = raw_data["segment"] == self.idx
        elif "segment" in data:
            self.segment_index = data["segment"] == self.idx
        else:
            raise ValueError("Could not identify segment data!")

    def __getitem__(self, key):
        if key in self.data:
            return self.data[key][self.segment_index]
        elif key in self.raw_data:
            return self.raw_data[key][self.segment_index].copy()
        else:
            raise KeyError("Undefined feature '{}'!".format(key))
