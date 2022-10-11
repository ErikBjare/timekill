from desktop_notifier import DesktopNotifier

_notify = DesktopNotifier(
    app_name="TimeKill", notification_limit=1
)  # app_icon="src/timekill/icon.png"


def notify(title, message):
    _notify.send_sync(title=title, message=message)


if __name__ == "__main__":
    notify("Testing", "Hello World")
