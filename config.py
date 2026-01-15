import yaml


class DotDict(dict):
    __getattr__ = dict.__getitem__


type ConfigValue = int | bool | str | dict[str, ConfigValue]


# Converts nested dictionaries to DotDict instances recursively
def wrap_dict(data: ConfigValue) -> DotDict | int | str | bool:
    if isinstance(data, dict):
        return DotDict(
            {
                key: wrap_dict(value) for key, value in data.items()
            }
        )
    else:
        return data


def load_config(path: str = "config.yaml") -> dict[str, ConfigValue]:
    """
    Loads YAML type config data and returns a nested dictionary.

    Args:
        path: Absolute or relative path to a YAML (.yaml or .yml) file.

    Returns:
        Dictionary containing program configurations from the provided file.
    """

    with open(path) as f:
        cfg = wrap_dict(yaml.safe_load(f))

    # Recursively substitutes scope variables from wrapped config data
    def expand_config(config, root_config):
        f_data = {}
        for key in config:
            if isinstance(config[key], dict):
                f_data[key] = expand_config(config[key], root_config)
            elif isinstance(config[key], str):
                f_data[key] = config[key].format(**root_config)
            else:
                f_data[key] = config[key]

        return f_data

    return expand_config(cfg, cfg)
