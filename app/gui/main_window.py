import gui.components as components
import pandas as pd
import PySide6.QtCore as QC
import PySide6.QtGui as QG
import PySide6.QtWidgets as QW
import util
from modules import ModuleManager


class ImportExportSection(QW.QWidget):
    def __init__(self, parent: QW.QWidget) -> None:
        super().__init__(parent)

        self._import = components.IconTextButton(
            'IMPORT', lambda: print('import'), spacing=5, parent=self
        )
        self._import.set_pixmap(util.gui.file_to_pixmap(':/icons/import.svg', QC.QSize(30, 30)))

        # self._separator = components.Line(QW.QFrame.Shape.VLine, parent=self)
        # util.gui.add_class(self._separator, 'separator')

        # self._export = components.IconTextButton(
        #     'EXPORT', lambda: print('export'), spacing=5, parent=self
        # )
        # self._export.set_pixmap(util.gui.file_to_pixmap(':/icons/export.svg', QC.QSize(30, 30)))

        self._layout = QW.QHBoxLayout(self)
        self._layout.addWidget(self._import)
        # self._layout.addWidget(self._separator)
        # self._layout.addWidget(self._export)


class Header(QW.QWidget):
    def __init__(self, parent: QW.QWidget | None) -> None:
        super().__init__(parent)

        self.bits_logo = components.ClickableLabel(self)
        self.bits_logo.setPixmap(
            util.gui.file_to_pixmap(':/icons/bitsxlamarato.png', QC.QSize(192, 50))
        )

        self._spacer_1 = components.Spacer()

        self.model_selector = QW.QComboBox(self)
        self.model_selector.addItems(util.path.get_available_models())

        self._spacer_2 = components.Spacer()

        self.import_export = ImportExportSection(self)

        self._layout = QW.QHBoxLayout(self)
        self.setSizePolicy(QW.QSizePolicy.Policy.Expanding, QW.QSizePolicy.Policy.Minimum)

        self._layout.setContentsMargins(10, 2, 10, 2)
        self._layout.setSpacing(10)

        self._layout.addWidget(self.bits_logo)
        self._layout.addItem(self._spacer_1)
        self._layout.addWidget(self.model_selector)
        self._layout.addItem(self._spacer_2)
        self._layout.addWidget(self.import_export)


class Form(QW.QWidget):
    def __init__(self, module_manager: ModuleManager, parent: QW.QWidget | None) -> None:
        super().__init__(parent)

        self._module_manager = module_manager

        self._layout = QW.QFormLayout(self)
        self.setSizePolicy(QW.QSizePolicy.Policy.Expanding, QW.QSizePolicy.Policy.Expanding)

        self._params = {}

        for name, modalities in self._module_manager.model.get_features().items():
            if isinstance(modalities, float):
                self._params[name] = QW.QLineEdit('1', self)
            else:
                self._params[name] = QW.QComboBox(self)
                self._params[name].addItems(modalities)

            self._layout.addRow(name, self._params[name])

    def data_to_df(self) -> None:

        new_row = {}
        for feature, modalities in self._module_manager.model.get_features().items():

            if isinstance(self._params[feature], QW.QLineEdit):
                new_row[feature] = float(self._params[feature].text())
            else:
                for modality in modalities:
                    new_row[f'{feature}_{modality}'] = (
                        modality == self._params[feature].currentText()
                    )

        return pd.DataFrame([new_row])


class FormControls(QW.QWidget):
    def __init__(self, parent: QW.QWidget | None) -> None:
        super().__init__(parent)

        self._spacer = components.Spacer()

        self.reset = components.IconTextButton(
            'RESET', spacing=5, margins=(10, 10, 10, 10), parent=self
        )
        self.reset.set_pixmap(
            util.gui.file_to_pixmap(
                ':/icons/reset.svg', QC.QSize(30, 30), color=util.gui.Colors.RED.value
            )
        )
        self.reset.setObjectName('reset_button')

        self.predict = components.IconTextButton(
            'CALCULAR', spacing=5, margins=(10, 10, 10, 10), parent=self
        )
        self.predict.set_pixmap(
            util.gui.file_to_pixmap(
                ':/icons/magic.svg', QC.QSize(30, 30), color=util.gui.Colors.BLUE.value
            )
        )
        self.predict.setObjectName('predict_button')

        self._layout = QW.QHBoxLayout(self)
        self._layout.setSpacing(20)

        self._layout.addItem(self._spacer)
        self._layout.addWidget(self.reset)
        self._layout.addWidget(self.predict)


class CentralWidget(QW.QWidget):
    def __init__(self, module_manager: ModuleManager, parent: QW.QWidget | None) -> None:
        super().__init__(parent)

        self._module_manager = module_manager

        self.header = Header(self)
        self.form = Form(self._module_manager, self)
        self.controls = FormControls(self)
        self.predicted = QW.QLabel(self)
        self.predicted_bar = QW.QProgressBar(self)
        self.predicted_bar.setVisible(False)
        self.predicted_bar.setAlignment(QC.Qt.AlignCenter)
        self.predicted_bar.setMinimum(0)
        self.predicted_bar.setMaximum(100)

        self.controls.reset.set_action(self.reset_form)

        self._layout = QW.QVBoxLayout(self)
        self._layout.addWidget(self.header)
        self._layout.addWidget(self.form)
        self._layout.addWidget(self.predicted)
        self._layout.addWidget(self.predicted_bar)
        self._layout.addWidget(self.controls)

    def reset_form(self) -> None:
        # Clear predicted value
        self.predicted.clear()
        self.predicted_bar.setVisible(False)
        self.predicted_bar.setValue(0)

        # Change Form for a new one, no mercy
        new_form = Form(self._module_manager, self)
        self._layout.replaceWidget(self.form, new_form)

        self.form.deleteLater()
        self.form = new_form


class MainWindow(QW.QMainWindow):
    def __init__(self, module_manager: ModuleManager) -> None:
        super().__init__()

        self._module_manager = module_manager

        self._central_widget = CentralWidget(self._module_manager, self)
        self.setCentralWidget(self._central_widget)

        self._central_widget.header.model_selector.currentTextChanged.connect(
            self._module_manager.change_model
        )
        self._central_widget.header.model_selector.currentTextChanged.connect(
            self._central_widget.reset_form
        )
        self._central_widget.controls.predict.set_action(self._predict)

        self._central_widget.header.import_export._import.clicked.connect(self._import)

        self.setWindowTitle('bitsxlamarato - fibropred')
        self.resize(800, 600)
        self.showFullScreen()

    def keyPressEvent(self, event: QG.QKeyEvent) -> None:
        '''
        Handles key presses.

        Parameters
        ----------
        event: QG.QKeyEvent
            Key press event
        '''

        match event.key():
            # Close app
            case QC.Qt.Key.Key_Q:
                self.close()
            # Fullscreen
            case QC.Qt.Key.Key_F:
                if self.isFullScreen():
                    self.showNormal()
                else:
                    self.showFullScreen()
            # Polish
            case QC.Qt.Key.Key_P:
                app = QW.QApplication.instance()

                if app is not None:
                    app.setStyleSheet(util.gui.get_style_sheet('resources/styles/style.css'))
                    QW.QApplication.style().polish(self)

    def _predict(self) -> None:

        try:
            df = self._central_widget.form.data_to_df()

            raw_pred = self._module_manager.model.predict(df)
            pred = raw_pred[0][1]

            self._central_widget.predicted.setText(
                f"Confiança d'empitorament del pacient: {pred*100:.2f}%"
            )
            self._central_widget.predicted_bar.setValue(pred * 100)
            self._central_widget.predicted_bar.setVisible(True)

            for color in ('green', 'yellow', 'red'):
                util.gui.remove_class(self._central_widget.predicted_bar, color)
            if pred < 0.33:
                util.gui.add_class(self._central_widget.predicted_bar, 'green')
            elif pred < 0.66:
                util.gui.add_class(self._central_widget.predicted_bar, 'yellow')
            else:
                util.gui.add_class(self._central_widget.predicted_bar, 'red')
        except Exception as e:
            print(e)
            self.show_alert(str(e))

    def show_alert(self, message: str) -> None:
        dialog = QW.QDialog(self)

        layout = QW.QVBoxLayout(dialog)
        label = QW.QLabel(message, dialog)
        layout.addWidget(label)

        dialog.exec()

    def _import(self) -> None:
        import_csv = QW.QFileDialog.getOpenFileName(self, 'Select csv')[0]

        df = pd.read_csv(import_csv)

        for feature, value in df.iloc[0].to_dict().items():
            print(feature, value)

            if feature in self._central_widget.form._params:
                if isinstance(self._central_widget.form._params[feature], QW.QLineEdit):
                    self._central_widget.form._params[feature].setText(str(value))
                else:
                    self._central_widget.form._params[feature].setCurrentText(str(value))
