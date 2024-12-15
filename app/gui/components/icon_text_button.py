import typing as tp

import PySide6.QtCore as QC
import PySide6.QtGui as QG
import PySide6.QtWidgets as QW
import util

from .clickable_lablel import ClickableLabel
from .clickable_widget import ClickableWidget


class IconTextButton(ClickableWidget):
    def __init__(
        self,
        text: str,
        action: tp.Callable | None = None,
        margins=(0, 0, 0, 0),
        spacing=0,
        object_name='',
        parent: QW.QWidget | None = None,
    ) -> None:
        super().__init__(parent)

        if object_name:
            self.setObjectName(object_name)

        self._layout = QW.QHBoxLayout(self)
        self._layout.setContentsMargins(*margins)
        self._layout.setSpacing(spacing)
        if action:
            self.clicked.connect(action)

        self._icon = ClickableLabel(self)
        util.gui.add_class(self._icon, 'icon')

        self._label = ClickableLabel(self)
        self._label.setText(text)

        self._layout.addWidget(self._icon)
        self._layout.addWidget(self._label)

    def set_text(self, text: str) -> None:
        self._label.setText(text)

    def set_pixmap(self, pixmap: QG.QPixmap) -> None:
        self._icon.setPixmap(pixmap)

    def set_action(self, callable) -> None:
        self.clicked.connect(callable)
