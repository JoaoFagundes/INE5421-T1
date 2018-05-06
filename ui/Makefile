all: mainwindow dialogs

mainwindow: mainwindow.ui
	pyuic5 mainwindow.ui -o main_window_ui.py

dialogs: okstringdialog.ui notokstringdialog.ui
	pyuic5 okstringdialog.ui -o ok_string_dialog.py
	pyuic5 notokstringdialog.ui -o not_ok_string_dialog.py
	