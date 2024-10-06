import datetime
from typing import Optional, Dict, Any

from sqlmodel import Session, select

from dual_universe.logs.logging_config import logger


class MissionMetaQuerySet:

    @classmethod
    def create_or_update_round_trips(cls, round_trip: int):
        with Session(engine) as session:
            metadata = (
                session.query(MissionMetadata).filter_by(round_trips=round_trip).first()
            )
            if metadata:
                session.query(MissionMetadata).filter_by(id=metadata.id).update(
                    {"round_trips": metadata.round_trips + 1}
                )
            else:
                session.add(MissionMetadata(round_trips=1))

            session.commit()

    @classmethod
    def read_round_trips(cls) -> int:
        with Session(engine) as session:
            metadata = session.query(MissionMetadata).first()
            if metadata:
                return metadata.round_trips
            return 0  # Default value if no metadata is found


class MissionQuerySet:
    @classmethod
    def select_all_missions(cls):
        with Session(engine) as session:
            Missions = session.query(Mission).all()
            return Missions

    @classmethod
    def read_mission_by_title(cls, title: str) -> Optional["Mission"]:
        """
        Read mission by title
        :param title:
        :return:
        """
        with Session(engine) as session:
            mission = session.query(Mission).filter_by(title=title).first()
            return mission

    @classmethod
    def update_mission(cls, title: str, updates: Dict[str, Any]):
        with Session(engine) as session:
            mission = session.query(Mission).filter_by(title=title).first()
            if mission:
                for key, value in updates.items():
                    setattr(mission, key, value)
                mission.updated_at = datetime.datetime.now()
                session.commit()
                print(f"Mission updated in the database: {title}")
                return True
            else:
                # Create a new mission if not found
                new_mission = Mission(
                    title=title,
                    **updates,
                    created_at=datetime.datetime.now(),
                    updated_at=datetime.datetime.now(),
                )
                session.add(new_mission)
                session.commit()
                print(f"New mission created in the database: {title}")
                return True

    @classmethod
    def delete_mission_by_title(cls, title: str):
        with Session(engine) as session:
            mission = session.query(Mission).filter_by(title=title).first()
            if mission:
                session.delete(mission)
                session.commit()
                print(f"Mission deleted: {title}")
            else:
                print("Mission not found")

    @classmethod
    def create_or_update_mission(cls, update_dict: dict[str, Any]) -> None:
        title = update_dict.pop(
            "title", None
        )  # Remove 'title' from update_dict if present
        if not title:
            raise ValueError("Title is required for creating or updating a mission.")

        with Session(engine) as session:
            existing_mission = session.exec(
                select(Mission).where(Mission.title == title)
            ).first()

            if not existing_mission:
                new_mission = Mission(title=title, **update_dict)
                session.add(new_mission)
                session.commit()
                logger.info(f"New mission added to the database: {title}")
            else:
                for key, value in update_dict.items():
                    setattr(existing_mission, key, value)
                session.commit()
                logger.info(f"Mission updated in the database: {title}")
