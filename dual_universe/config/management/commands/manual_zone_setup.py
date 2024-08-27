# obj = DbConfig()
# obj.create_db_and_tables()
# obj.manual_load_character()
# obj.load_image_entries_to_db()
#
# obj.delete_image_from_db()
# from models.models import SearchAreaLocation

def area_setup():
    area = {
        "ACTIVE_TAKEN_MISSIONS": {
            "region_name": SearchAreaLocation.ACTIVE_TAKEN_MISSIONS,
            "image_path": r"C:\Repositories\Dual Universe\Missions Dual Universe\data\search_areas\ACTIVE_TAKEN_MISSIONS.png"
        },
        "AVAILABLE_MISSIONS": {
            "region_name": SearchAreaLocation.AVAILABLE_MISSIONS,
            "image_path": r"C:\Repositories\Dual Universe\Missions Dual Universe\data\search_areas\AVAILABLE_MISSIONS.png"
        },
        "RETRIEVE_DELIVERY_STATUS": {
            "region_name": SearchAreaLocation.RETRIEVE_DELIVERY_STATUS,
            "image_path": r"C:\Repositories\Dual Universe\Missions Dual Universe\data\search_areas\unselected_deliver_package.png"
        },
    }

    obj.get_image_bbox(region_name=SearchAreaLocation.ACTIVE_TAKEN_MISSIONS,
                       image_path=r"C:\Repositories\Dual Universe\MDU\data\search_areas\ACTIVE_TAKEN_MISSIONS.png")

    obj.get_image_bbox(region_name=SearchAreaLocation.AVAILABLE_MISSIONS,
                   image_path=r"C:\Users\joshu\Pictures\Screenshots\Screenshot 2024-03-02 091333.png")

    obj.get_image_bbox(region_name=SearchAreaLocation.RETRIEVE_DELIVERY_STATUS,
                       image_path=r"C:\Users\joshu\Pictures\Screenshots\Screenshot 2024-03-02 091451.png")

    obj.get_image_bbox(region_name=SearchAreaLocation.ABANDON_MISSION,
                   image_path=r"C:\Users\joshu\Pictures\Screenshots\Screenshot 2024-03-02 091601.png")

    obj.get_image_bbox(region_name=SearchAreaLocation.WARP_TARGET_DEST,
                   image_path=r"C:\Users\joshu\Pictures\Screenshots\Screenshot 2024-03-02 092011.png")

    obj.get_image_bbox(region_name=SearchAreaLocation.ORBITAL_HUD_LANDED,
                       image_path=r"C:\Users\joshu\Pictures\Screenshots\Screenshot 2024-03-02 092202.png",
                       confidence=0.6,
                       )

    obj.get_image_bbox(region_name=SearchAreaLocation.SPACE_FUEL,
                       image_path=r"C:\Users\joshu\Pictures\Screenshots\Screenshot 2024-03-02 093227.png")

    obj.get_image_bbox(region_name=SearchAreaLocation.ATMO_FUEL,
                       image_path=r"C:\Users\joshu\Pictures\Screenshots\Screenshot 2024-03-02 093227.png")

    region_dict = {
        "DEST_INFO": {
            "region_name": SearchAreaLocation.DEST_INFO,
            "image_path": r"C:\Users\joshu\Pictures\Screenshots\Screenshot 2024-03-02 085354.png"
        },
        "SAFE_ZONE": {
            "region_name": SearchAreaLocation.SAFE_ZONE,
            "image_path": r"C:\Users\joshu\Pictures\Screenshots\Screenshot 2024-03-02 085458.png"
        },
        "RIDE": {
            "region_name": SearchAreaLocation.RIDE,
            "image_path": r"C:\Users\joshu\Pictures\Screenshots\Screenshot 2024-03-02 085513.png"
        },
        "DISTANCE": {
            "region_name": SearchAreaLocation.DISTANCE,
            "image_path": r"C:\Users\joshu\Pictures\Screenshots\Screenshot 2024-03-02 085507.png"
        },
        "STATUS": {
            "region_name": SearchAreaLocation.STATUS,
            "image_path": r"C:\Users\joshu\Pictures\Screenshots\Screenshot 2024-03-02 085616.png"
        },
        "ORIGIN_INFO": {
            "region_name": SearchAreaLocation.ORIGIN_INFO,
            "image_path": r"C:\Users\joshu\Pictures\Screenshots\Screenshot 2024-03-02 085344.png"
        },
        "MASS": {
            "region_name": SearchAreaLocation.MASS,
            "image_path": r"C:\Users\joshu\Pictures\Screenshots\Screenshot 2024-03-02 085436.png"
        },
        "VOLUME": {
            "region_name": SearchAreaLocation.VOLUME,
            "image_path": r"C:\Users\joshu\Pictures\Screenshots\Screenshot 2024-03-02 085447.png"
        },
        "REWARD_INFO": {
            "region_name": SearchAreaLocation.REWARD_INFO,
            "image_path": r"C:\Users\joshu\Pictures\Screenshots\Screenshot 2024-03-02 085154.png"
        },
        "TITLE_INFO": {
            "region_name": SearchAreaLocation.TITLE_INFO,
            "image_path": r"C:\Users\joshu\Pictures\Screenshots\Screenshot 2024-03-02 085603.png"
        },
        "ORIGIN_POS": {
            "region_name": SearchAreaLocation.ORIGIN_POS,
            "image_path": r"C:\Users\joshu\Pictures\Screenshots\Screenshot 2024-03-03 014408.png"
        },
        "DEST_POS": {
            "region_name": SearchAreaLocation.DEST_POS,
            "image_path": r"C:\Users\joshu\Pictures\Screenshots\Screenshot 2024-03-03 020140.png"
        },
            "ORBITAL_HUD_LANDED": {
                "region_name": SearchAreaLocation.ORBITAL_HUD_LANDED,
                "image_path": r"C:\Repositories\Dual Universe\Missions Dual Universe\data\search_areas\ORBITAL_HUD_LANDED.png"
            },
        }
        "GAME_CONSOLE_WINDOW": {
            "region_name": SearchAreaLocation.GAME_CONSOLE_WINDOW,
            "image_path": r"C:\Users\joshu\Pictures\Screenshots\Screenshot 2024-03-28 180709.png",
        },
    }
    for key, value in region_dict.items():
        region_name = value["region_name"]
        image_path = value["image_path"]

        obj.get_image_bbox(region_name=region_name, image_path=image_path)
