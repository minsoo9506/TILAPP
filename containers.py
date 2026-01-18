from dependency_injector import containers, providers
from note.application.note_service import NoteService
from note.infra.repository.note_repo import NoteRepository
from user.infra.repository.user_repo import UserRepository
from user.application.user_service import UserService

# dependency injection 은 IoC 컨테이너를 사용하여 객체의 생성과 의존성 관리를 담당
class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "user.interface.controllers.user_controller",
            "note.interface.controllers.note_controller",
        ]
    )
    user_repo = providers.Factory(UserRepository)
    user_service = providers.Factory(
        UserService,
        user_repo=user_repo,
    )
    note_repo = providers.Factory(NoteRepository)
    note_service = providers.Factory(
        NoteService,
        note_repo=note_repo,
    )