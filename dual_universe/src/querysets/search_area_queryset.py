import datetime
from typing import Optional, Dict, Tuple

from loguru import logger
from sqlmodel import Session, select

from dual_universe.settings import engine
from dual_universe.src.models.search_area_model import SearchArea


class SearchAreaQuerySet:

    @classmethod
    def select_searcharea(cls):
        with Session(engine) as session:
            return session.exec(select(SearchArea)).all()

    @classmethod
    def get_searcharea_by_name(cls, name: str):
        with Session(engine) as session:
            searcharea = session.exec(
                select(SearchArea).where(SearchArea.region_name == name)
            ).first()
        searcharea.region = region
        return region

    @classmethod
    def create_or_update_search_area(cls, region_name: str, updates: Dict[str, int]):
        try:
            with Session(engine) as session:
                search_area = (
                    session.query(SearchArea).filter_by(region_name=region_name).first()
                )
                if search_area:
                    for key, value in updates.items():
                        setattr(search_area, key, int(value))
                    search_area.center_x = (search_area.left + search_area.right) // 2
                    search_area.center_y = (search_area.top + search_area.bottom) // 2
                    search_area.updated_at = datetime.datetime.now()
                    session.commit()
                    logger.success(
                        f"Search area updated in the database: {region_name}"
                    )
                else:
                    new_search_area = SearchArea(region_name=region_name, **updates)
                    new_search_area.center_x = (
                        new_search_area.left + new_search_area.right
                    ) // 2
                    new_search_area.center_y = (
                        new_search_area.top + new_search_area.bottom
                    ) // 2
                    new_search_area.updated_at = datetime.datetime.now()
                    session.add(new_search_area)
                    session.commit()
                    logger.success(
                        f"New search area created in the database: {region_name}"
                    )
        except Exception as ex:
            logger.error(f"Could not update or create search area: {ex}")
            raise ValueError(f"Could not update or create search area: {ex}")

    @classmethod
    def create_search_area(
        cls, region_name: str, region_bbox: Tuple[int, int, int, int]
    ):
        with Session(engine) as session:
            new_search_area = SearchArea(
                region_name=region_name,
                region_bbox_left=region_bbox[0],
                region_bbox_top=region_bbox[1],
                region_bbox_right=region_bbox[2],
                region_bbox_bottom=region_bbox[3],
            )
            session.add(new_search_area)
            new_search_area.created_at = datetime.datetime.now()
            session.commit()
            print(f"New search area added to the database: {region_name}")

    @classmethod
    def read_search_area_by_name(cls, region_name: str) -> Optional["SearchArea"]:
        with Session(engine) as session:
            search_area = (
                session.query(SearchArea).filter_by(region_name=region_name).first()
            )
            if search_area is not None:
                return search_area
            else:
                logger.info(f"Search area with name '{region_name}' not found.")
                return None

    @classmethod
    def update_search_area(
        cls, region_name: str, region_bbox: Tuple[int, int, int, int]
    ):
        with Session(engine) as session:
            search_area = (
                session.query(SearchArea).filter_by(region_name=region_name).first()
            )
            if search_area:
                search_area.region_bbox = region_bbox
                search_area.updated_at = datetime.datetime.now()
                session.commit()
                print(f"Search area updated in the database: {region_name}")
            else:
                print("Search area not found")

    @classmethod
    def delete_search_area_by_name(cls, region_name: str):
        with Session(engine) as session:
            search_area = (
                session.query(SearchArea).filter_by(region_name=region_name).first()
            )
            if search_area:
                session.delete(search_area)
                session.commit()
                print(f"Search area deleted: {region_name}")
            else:
                print("Search area not found")
