import sentry_sdk


def sentry_log_exception(exception):
    """Capture une exception avec Sentry."""
    sentry_sdk.capture_exception(exception)


def sentry_log_event(message, level="info"):
    """Enregistre un message personnalisé dans Sentry."""
    sentry_sdk.capture_message(message, level=level)
