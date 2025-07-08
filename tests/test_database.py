import pytest
from sqlalchemy.orm import Session
from app.connection import SessionLocal, engine
from app import models
# Ensure tables are created
models.Base.metadata.create_all(bind=engine)
@pytest.fixture(scope="function")
def db_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
        for tbl in reversed(models.Base.metadata.sorted_tables):
            engine.execute(tbl.delete())
def test_insert_real_model(db_session: Session):
    new_item = models.Item(name="Test Item")
    db_session.add(new_item)
    db_session.commit()
    assert new_item.id is not None
def test_query_real_model(db_session: Session):
    item = models.Item(name="Query Test")
    db_session.add(item)
    db_session.commit()
    result = db_session.query(models.Item).filter_by(name="Query Test").first()
    assert result is not None
    assert result.name == "Query Test"
