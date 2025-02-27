from contextlib import contextmanager


@contextmanager
def transactional_session(session):
    """
    Contexte qui gère une transaction.
    Il commit automatiquement en cas de succès,
    ou effectue un rollback en cas d'exception.
    """
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
