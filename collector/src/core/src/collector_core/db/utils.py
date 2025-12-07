import pandas as pd
from sqlalchemy.orm import sessionmaker

from collector_core.db.engine import get_engine
from collector_core.db.models import Base, MCU_Table
from collector_core.mcu import MCU

engine = get_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    Base.metadata.create_all(bind=engine)


def get_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_mcu(
    name: str,
    description: str,
    type: MCU.MCU_Type,
    connection_type: MCU.MCU_ConnectionType,
    is_connected: bool,
    dev_id: int,
) -> None:
    db = SessionLocal()
    try:
        mcu = MCU_Table(
            name=name,
            description=description,
            type=type,
            connection_type=connection_type,
            is_connected=is_connected,
            dev_id=dev_id,
        )
        db.add(mcu)
        db.commit()
        db.refresh(mcu)
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


def get_mcus() -> pd.DataFrame:
    db = SessionLocal()
    try:
        items = db.query(MCU_Table).all()
        print(vars(items[0]))
        columns = (
            "id",
            "name",
            "description",
            "type",
            "connection_type",
            "is_connected",
            "dev_id",
        )

        return pd.DataFrame(
            data={col: [getattr(item, col) for item in items] for col in columns}
        )
    finally:
        db.close()


def get_mcu_by_id(mcu_id: int):
    db = SessionLocal()
    try:
        return db.query(MCU_Table).filter(MCU_Table.id == mcu_id).first()
    finally:
        db.close()


def update_mcu(mcu_id: int, **kwargs):
    db = SessionLocal()
    try:
        db.query(MCU_Table).filter(MCU_Table.id == mcu_id).update(kwargs)
        db.commit()
        return db.query(MCU_Table).filter(MCU_Table.id == mcu_id).first()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


def delete_mcu(mcu_id: int):
    db = SessionLocal()
    try:
        db.query(MCU_Table).filter(MCU_Table.id == mcu_id).delete()
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()
