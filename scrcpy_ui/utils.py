import subprocess
import threading
import logging
import time

# 配置日志记录
_logger = logging.getLogger(__name__)

_ssh_tunneling_dict = {}


def make_ssh_tunneling(local_port, remote_serial, remote_host, ssh_key_path=None):
    """
    创建一个SSH隧道，将本地端口转发到远程主机上的指定端口。

    :param local_port: 本地端口号
    :param remote_serial: 远程主机上的端口号
    :param remote_host: 远程主机的地址
    :param ssh_key_path: SSH私钥路径（可选）
    :return: 返回SSH进程对象
    """

    try:
        # 构建SSH命令
        ssh_command = ["ssh"]

        # 添加SSH密钥路径（如果提供）
        if ssh_key_path:
            ssh_command.extend(["-i", ssh_key_path])

        # 添加端口转发参数
        ssh_command.extend(["-o", "ControlMaster=no", "-L", f"{local_port}:{remote_serial}", remote_host, "-N"])

        _logger.info(f"SSH命令: {ssh_command}")
        _ssh_tunneling_dict[local_port] = (remote_serial, remote_host, ssh_key_path)
        # 启动SSH进程
        ssh_process = subprocess.run(ssh_command, check=True)

        return ssh_process

    except subprocess.CalledProcessError as e:
        _logger.error(f"SSH隧道进程返回非零退出码: {e}")
    except Exception as e:
        _logger.error(f"启动SSH隧道时发生错误: {e}")
        raise
    finally:
        if local_port in _ssh_tunneling_dict:
            del _ssh_tunneling_dict[local_port]


def start_ssh_tunnel_in_thread(local_port, remote_serial, remote_host, ssh_key_path=None):
    """
    在一个单独的线程中启动SSH隧道并监控其状态。

    :param local_port: 本地端口号
    :param remote_serial: 远程主机上的端口号
    :param remote_host: 远程主机的地址
    :param ssh_key_path: SSH私钥路径（可选）
    :param ssh_user: SSH用户名（可选）
    """
    try:
        # 启动SSH隧道
        if local_port in _ssh_tunneling_dict:
            return

        # 启动监控线程
        monitor_thread = threading.Thread(
            target=make_ssh_tunneling, args=(local_port, remote_serial, remote_host, ssh_key_path)
        )
        monitor_thread.daemon = True  # 设置为守护线程，主程序退出时自动结束
        monitor_thread.start()
        time.sleep(1)

        _logger.info("SSH隧道监控线程已启动")

    except Exception as e:
        _logger.error(f"启动SSH隧道线程时发生错误: {e}")
        raise


if __name__ == "__main__":
    from adbutils import adb
    from . import config as cfg

    for device_info in cfg.devices_info().values():
        break

    local_port = device_info.serial.split(":")[1]
    remote_serial = device_info.ssh_tunneling_serial
    remote_host = device_info.ssh_tunneling_host
    logging.basicConfig(level=logging.INFO)
    start_ssh_tunnel_in_thread(local_port, remote_serial, remote_host)
    adb.connect(f"localhost:{local_port}")
    device = adb.device(serial=f"localhost:{local_port}")
    print(device.shell("ls /"))
