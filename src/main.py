import uvicorn
from starlette.background import BackgroundTasks

from src.car.tasks import set_car_random_location_id
from src.config import settings


def main():
    background_tasks = BackgroundTasks()
    background_tasks.add_task(
        set_car_random_location_id
    )

    uvicorn.run(
        app='src.app:app',
        host=settings.server_host,
        port=settings.server_port,
        reload=True,
    )


if __name__ == '__main__':
    main()
