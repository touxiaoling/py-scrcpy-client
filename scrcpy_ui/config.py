import tomllib
import tomli_w
from pydantic import BaseModel
from pathlib import Path

config_path = Path("config.toml")


class Device(BaseModel):
    serial: str
    name: str | None
    ssh_tunneling_user: str | None
    ssh_tunneling_host: str | None
    ssh_tunneling_serial: str | None


def get_config():
    with config_path.open("rb") as f:
        config: dict = tomllib.load(f)
    return config


def set_config(config: dict):
    with config_path.open("wb") as f:
        tomli_w.dump(config, f)


def devices_info():
    devices: dict[str, Device] = {}
    config = get_config()
    for device_info in config["device"]:
        device = Device(**device_info)
        devices[device.name] = device

    return devices


def add_device(device: Device):
    config = get_config()

    if "device" not in config:
        config["device"] = []

    config["device"].append(device.model_dump())
    set_config(config)
