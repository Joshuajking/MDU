from typing import Type

from sqlmodel import Session, select, SQLModel

from dual_universe.settings import model_mapping


def find_existing_item(session: Session, model_class: Type[SQLModel], **filters):
    existing_item = session.exec(select(model_class).filter_by(**filters)).first()
    return existing_item, model_class
