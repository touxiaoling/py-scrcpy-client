from argparse import ArgumentParser
from typing import Optional
from typing import Callable
import logging
import queue
from pprint import pprint

import adbutils
import numpy as np
from PySide6.QtGui import QImage, QKeyEvent, QMouseEvent, QPixmap, Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox, QDialog
from .ui_main import Ui_MainWindow
from .ui_add_device import Ui_AddDeviceWindow
from . import config as cfg
from . import utils
import scrcpy

if not QApplication.instance():
    app = QApplication([])
else:
    app = QApplication.instance()


_logger = logging.getLogger(__name__)


def turn_coord_info(x, y, w, h, rgb24):
    rgb24 = np.uint64(np.asarray(rgb24) / 252 * 255)
    light_scale = np.array([0.299, 0.587, 0.114], dtype=np.float64)
    light = np.sum(rgb24 * light_scale)

    coord_info = [
        f"x:{x:4.0f} y:{y:4.0f} ex{x - w:4.0f} ey:{y - h:4.0f}",
        f"w: {x / w:.3f} h: {y / h:.3f}",
        f"mx:{x - w // 2:4.0f} my:{y - h // 2:4.0f}",
        f"rx:{(x - w // 2) * 1920 / h:4.0f} ry:{(y - h // 2) * 1080 / w:4.0f}",
        f"light: {light:4.1f} rgb:{rgb24}",
    ]
    return "\n".join(coord_info)


class AddDeviceWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_AddDeviceWindow()
        self.ui.setupUi(self)
        self.ui.okButton.clicked.connect(self.on_click_ok)

        self.device_info = None

    def on_click_ok(self):
        try:
            self.device_info = self.get_device_info()
            self.accept()
        except Exception as e:
            _logger.error(f"{e}")

    def get_device_info(self):
        name = self.ui.nameEdit.text()
        serial = self.ui.serialEdit.text()
        tunnel = self.ui.tunnelEdit.text()
        if tunnel:
            device_serial, tunnel_serial = serial.split(":", maxsplit=1)
            device_serial = f"localhost:{device_serial}"

            tunnel_host = tunnel

            device_info = cfg.Device(
                name=name,
                serial=device_serial,
                ssh_tunneling_host=tunnel_host,
                ssh_tunneling_serial=tunnel_serial,
            )
        else:
            device_info = cfg.Device(name=name, serial=serial)
        return device_info


class MainWindow(QMainWindow):
    def __init__(
        self,
        max_width: Optional[int],
        serial: Optional[str] = None,
        encoder_name: Optional[str] = None,
    ):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.max_width = max_width

        # Setup devices
        self.ui.combo_device.clear()
        self.ui.combo_device.addItem("Add device")
        self.ui.combo_device.addItems(self.devices_info.keys())

        # Bind controllers
        self.ui.button_home.clicked.connect(self.on_click_home)
        self.ui.button_back.clicked.connect(self.on_click_back)
        self.ui.button_xml.clicked.connect(self.on_click_xml)

        # Bind config
        self.ui.combo_device.currentTextChanged.connect(self.choose_device)
        self.ui.combo_resolution.currentTextChanged.connect(self.set_resolution)

        # Bind mouse event
        self.ui.label.mousePressEvent = self.on_mouse_event(scrcpy.ACTION_DOWN)
        self.ui.label.mouseMoveEvent = self.on_mouse_event(scrcpy.ACTION_MOVE)
        self.ui.label.mouseReleaseEvent = self.on_mouse_event(scrcpy.ACTION_UP)

        # Keyboard event
        self.keyPressEvent = self.on_key_event(scrcpy.ACTION_DOWN)
        self.keyReleaseEvent = self.on_key_event(scrcpy.ACTION_UP)

        # Setup client
        self.frames = queue.Queue(maxsize=1)
        self.client = None
        self.device: adbutils.AdbDevice = None
        self.alive = True

        if self.devices_info:
            self.choose_device(next(iter(self.devices_info)))
        else:
            self.choose_device(self.ui.combo_device.currentText())

    @property
    def devices_info(self):
        return cfg.devices_info()

    def client_init(self, device, on_init: Callable, on_frame: Callable, encoder_name: Optional[str] = None):
        _logger.info(f"Init client for device: {device.serial}")
        client = scrcpy.Client(
            device=device,
            bitrate=1000000000,
            encoder_name=encoder_name,
            max_fps=15,
        )
        client.add_listener(scrcpy.EVENT_INIT, on_init)
        client.add_listener(scrcpy.EVENT_FRAME, on_frame)
        _logger.info(f"Client for device: {device.serial} initialized")
        return client

    def client_start(self, device_info: cfg.Device):
        _logger.info(f"Start client for device: {self.device.serial}")
        try:
            if device_info.ssh_tunneling_serial:
                local_port = device_info.serial.split(":")[1]
                utils.start_ssh_tunnel_in_thread(
                    local_port,
                    device_info.ssh_tunneling_serial,
                    device_info.ssh_tunneling_host,
                )
            adbutils.adb.connect(device_info.serial)
            self.client.start(daemon_threaded=True)
            _logger.info(f"Client for device: {self.device.serial} started")
        except Exception as e:
            _logger.error(str(e))

    def choose_device(self, name):
        if name == "Add device":
            add_device_window = AddDeviceWindow()
            add_device_window.exec()
            device_info = add_device_window.device_info
            if device_info is not None:
                cfg.add_device(device_info)
                self.ui.combo_device.addItem(device_info.name)
                name = device_info.name
            else:
                return
        else:
            device_info = self.devices_info[name]
        # Ensure text
        self.ui.combo_device.setCurrentText(name)
        self.ui.combo_resolution.setCurrentIndex(0)
        # Restart service
        if getattr(self, "client", None):
            self.client.stop()

        device = adbutils.adb.device(serial=device_info.serial)

        self.device = device
        self.client = self.client_init(device, self.on_init, self.on_frame)
        self.client_start(device_info)

    def set_resolution(self, resolution):
        if resolution != "default":
            self.device.shell(f"wm size {resolution}")

    def on_flip(self, _):
        self.client.flip = self.ui.flip.isChecked()

    def on_click_home(self):
        self.client.control.keycode(scrcpy.KEYCODE_HOME, scrcpy.ACTION_DOWN)
        self.client.control.keycode(scrcpy.KEYCODE_HOME, scrcpy.ACTION_UP)

    def on_click_back(self):
        self.client.control.back_or_turn_screen_on(scrcpy.ACTION_DOWN)
        self.client.control.back_or_turn_screen_on(scrcpy.ACTION_UP)

    def on_click_xml(self):
        from lxml import etree
        import time

        now_time = time.time()
        xml = self.device.dump_hierarchy()
        use_time = time.time() - now_time
        _logger.info(f"Dump hierarchy use time: {use_time:.2f}s")
        xml = etree.fromstring(xml.encode("utf-8"))
        xml = etree.tostring(xml, pretty_print=True, encoding="unicode")
        pprint(xml)
        msg = QMessageBox()
        msg.setWindowTitle("XML")
        msg.setText(xml)
        msg.exec()

    def on_mouse_event(self, action=scrcpy.ACTION_DOWN):
        def handler(evt: QMouseEvent):
            focused_widget = QApplication.focusWidget()
            if focused_widget is not None:
                focused_widget.clearFocus()
            if self.client.resolution is None:
                return
            ratio = self.max_width / max(self.client.resolution)
            x, y = evt.position().x() / ratio, evt.position().y() / ratio
            w, h = self.client.resolution
            x = max(0, min(w - 1, int(x)))
            y = max(0, min(h - 1, int(y)))

            try:
                bgr24 = self.client.last_frame[y, x]
            except (IndexError, TypeError):
                bgr24 = (0, 0, 0)

            try:
                self.client.control.touch(x, y, action)
            except OSError as e:
                _logger.error(f"Touch error: {e}")
            rgb24 = (bgr24[2], bgr24[1], bgr24[0])
            coord_info = turn_coord_info(x, y, w, h, rgb24)
            self.ui.coord_label.setText(coord_info)

        return handler

    def on_key_event(self, action=scrcpy.ACTION_DOWN):
        def handler(evt: QKeyEvent):
            code = self.map_code(evt.key())
            if code != -1:
                self.client.control.keycode(code, action)

        return handler

    def map_code(self, code):
        """
        Map qt keycode ti android keycode

        Args:
            code: qt keycode
            android keycode, -1 if not founded
        """

        if code == -1:
            return -1
        if 48 <= code <= 57:
            return code - 48 + 7
        if 65 <= code <= 90:
            return code - 65 + 29
        if 97 <= code <= 122:
            return code - 97 + 29

        hard_code = {
            32: scrcpy.KEYCODE_SPACE,
            16777219: scrcpy.KEYCODE_DEL,
            16777248: scrcpy.KEYCODE_SHIFT_LEFT,
            16777220: scrcpy.KEYCODE_ENTER,
            16777217: scrcpy.KEYCODE_TAB,
            16777249: scrcpy.KEYCODE_CTRL_LEFT,
        }
        if code in hard_code:
            return hard_code[code]

        _logger.error(f"Unknown keycode: {code}")
        return -1

    def on_init(self):
        self.setWindowTitle(f"Serial: {self.client.device_name}")

    def on_frame(self, frame):
        try:
            self.frames.get_nowait()
        except queue.Empty:
            pass
        self.frames.put(frame)

    def show_fame(self, frame):
        if frame is not None:
            if self.client.resolution is None:
                return

            ratio = self.max_width / max(self.client.resolution)
            image = QImage(
                frame,
                frame.shape[1],
                frame.shape[0],
                frame.shape[1] * 3,
                QImage.Format_BGR888,
            )
            pix = QPixmap(image)
            pix.setDevicePixelRatio(1 / ratio)
            self.ui.label.setPixmap(pix)
            self.resize(1, 1)

    def closeEvent(self, _):
        self.client.stop()
        self.alive = False


def main():
    logging.basicConfig(level=logging.DEBUG)

    parser = ArgumentParser(description="A simple scrcpy client")
    parser.add_argument(
        "-m",
        "--max_width",
        type=int,
        default=640,
        help="Set max width of the window, default 720",
    )
    parser.add_argument(
        "-d",
        "--device",
        type=str,
        help="Select device manually (device serial required)",
    )
    parser.add_argument("--encoder_name", type=str, help="Encoder name to use")
    args = parser.parse_args()

    m = MainWindow(args.max_width, args.device, args.encoder_name)
    m.show()

    while m.alive:
        app.processEvents()
        try:
            frame = m.frames.get(timeout=0.1)
            m.show_fame(frame)
        except queue.Empty:
            pass


if __name__ == "__main__":
    main()
