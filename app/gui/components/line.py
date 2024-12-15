import PySide6.QtWidgets as QW


class Line(QW.QFrame):

    def __init__(self, shape=QW.QFrame.Shape.HLine, parent: QW.QWidget | None = None) -> None:
        super().__init__(parent)

        self.setFrameShape(shape)
        self.setFrameShadow(QW.QFrame.Shadow.Sunken)
