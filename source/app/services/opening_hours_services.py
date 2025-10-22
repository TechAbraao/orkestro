from source.app.repository.opening_hours_repository import OpeningHoursRepository
from source.app.entities.opening_hours_entity import OpeningHoursEntity
from source.app.utils.decorators.database import database_connection
from source.app.settings.logging_settings import get_logger

logger = get_logger(__name__)

class OpeningHoursServices:
    def __init__(self):
        self.opening_hours_repository = OpeningHoursRepository()

    @database_connection
    def save_hours_in_menu(self, menu_id, data):
        logger.info(f"Adicionando horários no menu_id: '{menu_id}'.")

        # Verificar se já constam horários, afinal, só pode adicionar 7 horários
        exists_hours = self.opening_hours_repository.exists_hours_in_menu(menu_id=menu_id)
        if exists_hours:
            logger.warning(f"Já existem horários definidos nesse menu_id '{menu_id}'")
            raise ValueError("Schedules are already included in this menu.")

        entities = [
            OpeningHoursEntity(
                menu_id=menu_id,
                day=item["day"],
                open=item["open"],
                close=item["close"]
            )
            for item in data
        ]

        self.opening_hours_repository.save_many(entities)
        logger.info(f"{len(entities)} horários adicionados ao menu '{menu_id}'.")
        return True

    @database_connection
    def get_menu_opening_hours(self, menu_id: str):
        hours_menu = self.opening_hours_repository.get_hours_in_menu(menu_id=menu_id)
        logger.info(f"Você encontrou os horários: {hours_menu}")

        all_hours_menu = []
        for items in hours_menu:
            all_hours_menu.append(items.serialize)
        logger.info(f"Horários serializados: {all_hours_menu}")

        return all_hours_menu

    @database_connection
    def delete_all_hours(self, menu_id: str) -> bool:
        deleted_count = self.opening_hours_repository.delete_all_hours(menu_id=menu_id)
        return bool(deleted_count)
