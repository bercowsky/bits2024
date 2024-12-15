import signal
import sys

import PySide6.QtCore as QC
import PySide6.QtWidgets as QW
import util
from gui.main_window import MainWindow
from modules import ModuleManager

import resources


def main():
    '''
    Main function
    '''

    # Create qt app
    app = QW.QApplication(sys.argv)

    # Create module manager
    module_manager = ModuleManager()

    # Create GUI
    main_window = MainWindow(module_manager)

    # Apply stylesheet
    app.setStyleSheet(util.gui.get_style_sheet(':/styles/style.css'))
    app.style().polish(main_window)

    # Control C to quit the app
    signal.signal(signal.SIGINT, lambda *_: QC.QCoreApplication.quit())

    create_timer_for_signal_handling()

    # Run the application
    app.exec()


def create_timer_for_signal_handling() -> None:
    '''
    Create Timer to process events for signal handling
    '''

    timer = QC.QTimer()
    timer.timeout.connect(lambda: None)  # Timer does nothing but keeps the app responsive
    timer.start(1000)  # Interval in milliseconds


if __name__ == "__main__":
    sys.exit(main())
