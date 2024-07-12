from uuid import uuid4
from db.session import session, set_session_context, get_session_context, reset_session_context


async def db():
    session_id = str(uuid4())
    context = set_session_context(session_id=session_id)
    try:
        yield get_session_context()
    except Exception as err:
        raise err
    finally:
        await session.remove()
        reset_session_context(context=context)
