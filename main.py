import traceback
from crash_ui import show_fatal_error

try:
    import main_app
except Exception:
    msg = f"Failed to import main_app.py:\n{traceback.format_exc()}"
    show_fatal_error(msg)
    raise

if __name__ == '__main__':
    try:
        main_app.RedAffairApp().run()
    except Exception:
        msg = traceback.format_exc()
        main_app.log_crash(msg)
        show_fatal_error(msg)
        raise
