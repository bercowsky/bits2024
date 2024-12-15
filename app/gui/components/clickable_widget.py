import PySide6.QtCore as QC
import PySide6.QtWidgets as QW
import util
from PySide6.QtGui import QMouseEvent


class ClickableWidget(QW.QFrame):
    clicked = QC.Signal()

    def __init__(self, parent: QW.QWidget | None = None) -> None:
        super().__init__(parent)

        self.setFocusPolicy(QC.Qt.FocusPolicy.ClickFocus)

        self._checked = False

    @property
    def checked(self) -> bool:
        return self._checked

    @checked.setter
    def checked(self, value: bool) -> None:
        self._checked = value

    def mousePressEvent(self, ev: QMouseEvent) -> None:
        util.gui.add_class(self, 'pressed')

        self.clicked.emit()
        return super().mousePressEvent(ev)

    def mouseReleaseEvent(self, ev: QMouseEvent) -> None:
        util.gui.remove_class(self, 'pressed')

        return super().mouseReleaseEvent(ev)
