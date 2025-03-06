import tomllib
from pydantic import BaseModel
from pathlib import Path


class Device(BaseModel):
    serial: str
    name: str | None
    ssh_tunneling_user: str | None
    ssh_tunneling_host: str | None
    ssh_tunneling_serial: str | None


devices: dict[str, Device] = {}
with Path("config.toml").open("rb") as f:
    config: dict = tomllib.load(f)
    for device_info in config["device"]:
        device = Device(**device_info)
        devices[device.serial] = device


def device_list():
    for device in devices.values():
        yield device
