import traceback

# Crash display

def show_fatal_error(msg):
    # CrashApp().run() -> displays msg on screen when Kivy can draw
    try:
        from kivy.app import App
        from kivy.uix.label import Label
        from kivy.core.window import Window

        class CrashApp(App):
            def build(self):
                return Label(
                    text=msg,
                    font_size='12sp',
                    halign='left',
                    valign='top',
                    text_size=(Window.width - 20, None),
                )

        CrashApp().run()
        return
    except Exception:
        pass

    # AlertDialog.Builder(activity).show() -> displays msg on Android when Kivy cannot draw
    try:
        from jnius import autoclass
        from android.runnable import run_on_ui_thread

        @run_on_ui_thread
        def _show():
            AlertDialog = autoclass('android.app.AlertDialog$Builder')
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            dialog = AlertDialog(PythonActivity.mActivity)
            dialog.setTitle('RACF Crash')
            dialog.setMessage(msg[:5000])
            dialog.show()

        _show()
    except Exception:
        pass
