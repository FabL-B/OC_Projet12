from contextlib import contextmanager


@contextmanager
def transactional_session(session):
    """
    Context manager that handles a transaction.
    It automatically commits on success,
    or performs a rollback in case of an exception.
    """
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
