import PySide6.QtWidgets as QW


class Spacer(QW.QSpacerItem):
    def __init__(self) -> None:
        super().__init__(0, 0, QW.QSizePolicy.Policy.Expanding, QW.QSizePolicy.Policy.Minimum)
