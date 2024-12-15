import typing as tp
from enum import Enum

import PySide6.QtCore as QC
import PySide6.QtGui as QG
import PySide6.QtSvg as QS
import PySide6.QtWidgets as QW
import PySide6.QtXml as QX


class Colors(Enum):
    WHITE = QG.QColor(QC.Qt.GlobalColor.white)
    BLACK = QG.QColor(QC.Qt.GlobalColor.black)
    BLUE = QG.QColor(QC.Qt.GlobalColor.blue)
    RED = QG.QColor(QC.Qt.GlobalColor.red)


def add_class(obj: QW.QWidget, clss: str | tp.List[str]) -> None:

    if isinstance(clss, str):
        clss = [clss]

    class_list = obj.property('class')

    if isinstance(class_list, list):
        # Already exists, modify

        for cls in clss:
            if cls not in class_list:
                class_list.append(cls)

        obj.setProperty('class', class_list)
    else:
        obj.setProperty('class', clss)
    obj.style().polish(obj)


def remove_class(obj: QW.QWidget, cls: str) -> None:
    class_list = obj.property('class')

    if isinstance(class_list, list):

        while cls in class_list:
            class_list.remove(cls)

        obj.setProperty('class', class_list)
        obj.style().polish(obj)


def _svg_to_pixmap(
    file: str,
    size=QC.QSize(),
    color=Colors.BLACK.value,
    margin=0,
    aspect_ratio_mode=QC.Qt.AspectRatioMode.KeepAspectRatio,
) -> QG.QPixmap:
    '''
    Convert a svg to a pixmap.

    '''

    data = QC.QByteArray()

    q_file = QC.QFile(file)

    if q_file.open(QC.QIODevice.OpenModeFlag.ReadOnly):
        data = q_file.readAll()
        q_file.close()

    if data.isEmpty():
        pixmap = QG.QPixmap(size)

        if color.isValid():
            pixmap.fill(color)
        else:
            pixmap.fill(QC.Qt.GlobalColor.black)

        return pixmap

    s_data = data.data().decode('utf-8')

    if color.isValid():
        fill = f'fill:{color.name()}'
        stroke = f'stroke:{color.name()}'

        s_data = s_data.replace('fill:#000000', fill)
        s_data = s_data.replace('stroke:#000000', stroke)

    doc = QX.QDomDocument()
    doc.setContent(s_data)

    if color.isValid():

        elem = doc.documentElement()

        if elem.tagName() == 'svg':
            elem.setAttribute('fill', color.name())

    svg_renderer = QS.QSvgRenderer(doc.toByteArray())

    image = QG.QImage()

    if size.isValid():
        svg_size = svg_renderer.defaultSize()
        svg_size.scale(size, aspect_ratio_mode)

        image = QG.QImage(svg_size, QG.QImage.Format.Format_ARGB32)
    else:
        image = QG.QImage(svg_renderer.defaultSize(), QG.QImage.Format.Format_ARGB32)

    image.fill(QC.Qt.GlobalColor.transparent)

    painter = QG.QPainter(image)
    svg_renderer.render(painter)

    rect = QC.QRect()

    if size.isValid():

        x = int((image.width() - size.width()) / 2)
        y = int((image.height() - size.height()) / 2)

        rect = QC.QRect(
            x - margin, y - margin, size.width() + margin * 2, size.height() + margin * 2
        )
    else:
        rect = QC.QRect(
            0 - margin, 0 - margin, image.width() + margin * 2, image.height() + margin * 2
        )

    painter.end()

    return QG.QPixmap.fromImage(image.copy(rect))


def file_to_pixmap(
    file: str,
    size=QC.QSize(),
    color=Colors.BLACK.value,
    margin=0,
    aspect_ratio_mode=QC.Qt.AspectRatioMode.KeepAspectRatio,
) -> QG.QPixmap:
    '''
    Convert a file to a pixmap.

    '''

    if file.endswith('.svg'):
        return _svg_to_pixmap(file, size, color, margin, aspect_ratio_mode)
    else:
        image = QG.QImage(file)

        rect = QC.QRect()

        if size.isValid():
            image = image.scaled(
                size, aspect_ratio_mode, QC.Qt.TransformationMode.SmoothTransformation
            )

            x = int((image.width() - size.width()) / 2)
            y = int((image.height() - size.height()) / 2)

            rect = QC.QRect(
                x - margin, y - margin, size.width() + margin * 2, size.height() + margin * 2
            )
        else:
            rect = QC.QRect(
                0 - margin, 0 - margin, image.width() + margin * 2, image.height() + margin * 2
            )

        return QG.QPixmap.fromImage(image.copy(rect))


def get_style_sheet(file_name: str) -> str:
    file = QC.QFile(file_name)
    file.open(QC.QFile.OpenModeFlag.ReadOnly | QC.QFile.OpenModeFlag.Text)

    ret = file.readAll().toStdString()

    return ret
