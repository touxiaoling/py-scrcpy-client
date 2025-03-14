from argparse import ArgumentParser
from typing import Optional

from adbutils import adb
from PySide6.QtGui import QImage, QKeyEvent, QMouseEvent, QPixmap, Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox
from .ui_main import Ui_MainWindow
from . import config as cfg
from . import utils
import scrcpy

if not QApplication.instance():
    app = QApplication([])
else:
    app = QApplication.instance()


def turn_coord_info(x, y, w, h, light):
    coord_info = [
        f"x:{x:4.0f} y:{y:4.0f} ex{x-w:4.0f} ey:{y-h:4.0f}",
        f"w: {x/w:.3f} h: {y/h:.3f}",
        f"mx:{x-w//2:4.0f} my:{y-h//2:4.0f}",
        f"rx:{(x-w//2)*1920/h:4.0f} ry:{(y-h//2)*1080/w:4.0f}",
        f"light: {light:4.1f}",
    ]
    return "\n".join(coord_info)


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
        self.devices = self.list_devices()
        if serial:
            self.choose_device(serial)
        self.device = adb.device(serial=self.ui.combo_device.currentText())
        self.alive = True

        # Setup client
        self.client = scrcpy.Client(
            device=self.device,
            flip=self.ui.flip.isChecked(),
            bitrate=1000000000,
            encoder_name=encoder_name,
            max_fps=15,
        )
        self.client.add_listener(scrcpy.EVENT_INIT, self.on_init)
        self.client.add_listener(scrcpy.EVENT_FRAME, self.on_frame)

        # Bind controllers
        self.ui.button_home.clicked.connect(self.on_click_home)
        self.ui.button_back.clicked.connect(self.on_click_back)

        # Bind config
        self.ui.combo_device.currentTextChanged.connect(self.choose_device)
        self.ui.flip.stateChanged.connect(self.on_flip)

        # Bind mouse event
        self.ui.label.mousePressEvent = self.on_mouse_event(scrcpy.ACTION_DOWN)
        self.ui.label.mouseMoveEvent = self.on_mouse_event(scrcpy.ACTION_MOVE)
        self.ui.label.mouseReleaseEvent = self.on_mouse_event(scrcpy.ACTION_UP)

        # Keyboard event
        self.keyPressEvent = self.on_key_event(scrcpy.ACTION_DOWN)
        self.keyReleaseEvent = self.on_key_event(scrcpy.ACTION_UP)

    def choose_device(self, device):
        if device not in self.devices:
            msgBox = QMessageBox()
            msgBox.setText(f"Device serial [{device}] not found!")
            msgBox.exec()
            return

        # Ensure text
        self.ui.combo_device.setCurrentText(device)
        # Restart service
        if getattr(self, "client", None):
            device_info = cfg.devices[device]
            if device_info.ssh_tunneling_serial:
                local_port = device_info.serial.split(":")[1]
                utils.start_ssh_tunnel_in_thread(
                    local_port,
                    device_info.ssh_tunneling_serial,
                    device_info.ssh_tunneling_host,
                    ssh_user=device_info.ssh_tunneling_user,
                )
            self.client.stop()
            adb.connect(device)
            self.client.device = adb.device(serial=device)

    def list_devices(self):
        self.ui.combo_device.clear()
        items = [i.serial for i in cfg.device_list()]
        self.ui.combo_device.addItems(items)
        return items

    def on_flip(self, _):
        self.client.flip = self.ui.flip.isChecked()

    def on_click_home(self):
        self.client.control.keycode(scrcpy.KEYCODE_HOME, scrcpy.ACTION_DOWN)
        self.client.control.keycode(scrcpy.KEYCODE_HOME, scrcpy.ACTION_UP)

    def on_click_back(self):
        self.client.control.back_or_turn_screen_on(scrcpy.ACTION_DOWN)
        self.client.control.back_or_turn_screen_on(scrcpy.ACTION_UP)

    def on_mouse_event(self, action=scrcpy.ACTION_DOWN):
        def handler(evt: QMouseEvent):
            focused_widget = QApplication.focusWidget()
            if focused_widget is not None:
                focused_widget.clearFocus()
            ratio = self.max_width / max(self.client.resolution)
            w, h = self.client.resolution
            x, y = evt.position().x() / ratio, evt.position().y() / ratio
            self.client.control.touch(x, y, action)
            light = 0
            if self.client.last_frame is not None:
                bgr24 = self.client.last_frame[int(y), int(x)]
                light = 0.114 * bgr24[0] + 0.587 * bgr24[1] + 0.299 * bgr24[2]
            coord_info = turn_coord_info(x, y, w, h, light)
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

        print(f"Unknown keycode: {code}")
        return -1

    def on_init(self):
        self.setWindowTitle(f"Serial: {self.client.device_name}")

    def on_frame(self, frame):
        app.processEvents()
        if frame is not None:
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

    m.client.start()
    while m.alive:
        m.client.start()


if __name__ == "__main__":
    main()
