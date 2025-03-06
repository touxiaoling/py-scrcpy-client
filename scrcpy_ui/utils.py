import subprocess
import threading
import logging
import time

# 配置日志记录
_logger = logging.getLogger(__name__)

_ssh_tunneling_dict = {}


def make_ssh_tunneling(local_port, remote_serial, remote_host, ssh_key_path=None, ssh_user=None):
    """
    创建一个SSH隧道，将本地端口转发到远程主机上的指定端口。

    :param local_port: 本地端口号
    :param remote_serial: 远程主机上的端口号
    :param remote_host: 远程主机的地址
    :param ssh_key_path: SSH私钥路径（可选）
    :param ssh_user: SSH用户名（可选）
    :return: 返回SSH进程对象
    """

    try:
        # 构建SSH命令
        ssh_command = ["ssh"]

        # 添加SSH密钥路径（如果提供）
        if ssh_key_path:
            ssh_command.extend(["-i", ssh_key_path])

        # 添加SSH用户名（如果提供）
        if ssh_user:
            remote_host = f"{ssh_user}@{remote_host}"

        # 添加端口转发参数
        ssh_command.extend(["-L", f"{local_port}:{remote_serial}", remote_host, "-N"])

        _logger.info(f"SSH命令: {ssh_command}")
        # 启动SSH进程
        ssh_process = subprocess.Popen(
            ssh_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        # 记录日志
        _logger.info(f"SSH隧道已启动：本地端口 {local_port} 转发到 {remote_host}:{remote_serial}")

        return ssh_process

    except Exception as e:
        _logger.error(f"启动SSH隧道时发生错误: {e}")
        raise


def monitor_ssh_tunnel(local_port):
    """
    监控SSH隧道进程，确保其正常运行。

    :param ssh_process: SSH进程对象
    """
    ssh_process = _ssh_tunneling_dict[local_port]
    try:
        while True:
            # 检查进程是否仍在运行
            if ssh_process.poll() is not None:
                _logger.error("SSH隧道进程已终止")
                del _ssh_tunneling_dict[local_port]
                break

            # 读取标准输出和错误输出
            stdout, stderr = ssh_process.communicate()
            if stdout:
                _logger.info(f"SSH隧道输出: {stdout.decode().strip()}")
            if stderr:
                _logger.error(f"SSH隧道错误: {stderr.decode().strip()}")

            # 每隔一段时间检查一次
            time.sleep(5)

    except Exception as e:
        del _ssh_tunneling_dict[local_port]
        _logger.error(f"监控SSH隧道时发生错误: {e}")
        raise


def start_ssh_tunnel_in_thread(local_port, remote_serial, remote_host, ssh_key_path=None, ssh_user=None):
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
        ssh_process = make_ssh_tunneling(local_port, remote_serial, remote_host, ssh_key_path, ssh_user)
        _ssh_tunneling_dict[local_port] = ssh_process
        # 启动监控线程
        monitor_thread = threading.Thread(target=monitor_ssh_tunnel, args=(local_port,))
        monitor_thread.daemon = True  # 设置为守护线程，主程序退出时自动结束
        monitor_thread.start()

        _logger.info("SSH隧道监控线程已启动")

    except Exception as e:
        _logger.error(f"启动SSH隧道线程时发生错误: {e}")
        raise


if __name__ == "__main__":
    from adbutils import adb
    from .config import devices

    for device_info in devices.values():
        break

    local_port = device_info.serial.split(":")[1]
    remote_serial = device_info.ssh_tunneling_serial
    remote_host = device_info.ssh_tunneling_host
    ssh_user = device_info.ssh_tunneling_user
    logging.basicConfig(level=logging.INFO)
    start_ssh_tunnel_in_thread(local_port, remote_serial, remote_host, ssh_user=ssh_user)
    adb.connect(f"localhost:{local_port}")
    device = adb.device(serial=f"localhost:{local_port}")
    print(device.shell("ls /"))
