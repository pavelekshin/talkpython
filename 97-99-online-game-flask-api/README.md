# Flask rock-scissor-paper game

Rock-scissor-paper game on Flask and SQLAlchemy ORM.\
User game client realise with uplink.\
Test on pytest.

- SQLAlchemy ORM
- SQLite
- pytest
- uplink
- JSONSchema Validation
- custom global error handlers, DB session context manager,

well-structured code:

```bash
├── client - client app
├── config
├── db - db and csv 
├── models - SQLAlchemy ORM models
├── schema - JSONSchema and validation stuff
├── services - logic
├── tests - pytest
├── views - api views
├──app.py - main app
├──error_handlers.py - global error_handlers
├──exceptions.py  - global exceptions
├──helper_handlers.py - global helper_handlers
└──session_factory.py - global db session_factory
```


