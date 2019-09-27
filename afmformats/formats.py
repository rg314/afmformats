import pathlib

from .fmt_jpk import fmt_jpk_force, fmt_jpk_force_map
from .afm_fdist import AFMForceDistance


def load_data(path, mode=None, diskcache=False, callback=None):
    path = pathlib.Path(path)
    if path.suffix in formats_by_suffix:
        if mode is None:
            # TODO:
            # - Try to figure out the mode somehow
            mode = "force-distance"
        # TODO:
        # - if multiple file types exist, get the right one (not the 1st)
        loader = formats_by_suffix[path.suffix][0]["loader"]
        afmdata = []
        if mode == "force-distance":
            for dd in loader(path, callback=callback):
                ddi = AFMForceDistance(data=dd["data"],
                                       metadata=dd["metadata"],
                                       diskcache=diskcache)
                afmdata.append(ddi)
    else:
        raise ValueError("Unsupported file extension: '{}'!".format(path))
    return afmdata


#: available/supported file formats
formats_available = [
    fmt_jpk_force,
    fmt_jpk_force_map,
    ]
#: available file formats in a dictionary with suffix keys
formats_by_suffix = {}
# Populate list of available fit models
for _item in formats_available:
    _suffix = _item["suffix"]
    if _suffix not in formats_by_suffix:
        formats_by_suffix[_suffix] = []
        formats_by_suffix[_suffix].append(_item)
#: available file formats in a dictionary with modality keys
formats_by_mode = {}
for _item in formats_available:
    _mode = _item["mode"]
    if _mode not in formats_by_mode:
        formats_by_mode[_mode] = []
        formats_by_mode[_mode].append(_item)
#: list of supported extensions
supported_extensions = sorted(formats_by_suffix.keys())