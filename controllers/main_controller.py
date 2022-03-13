import traceback
from controllers.controllers_manager import controllers_manager
from core.exceptions.user_exit_exception import UserExitException
from views.main_view import MainView

DEBUG_MODE = True


class MainController:
    def __init__(self):
        self.view = MainView()

    # def __inject_data(self):
    #     controllers_manager.event.add_event('E', 25, local, '01/01/2020 17:30', [organizer])
    #     controllers_manager.event.add_event('E2', 10, local, '22/02/2022 17:30', [organizer])
    #     controllers_manager.event.add_event('E3', 10, local, '22/04/2022 17:30', [organizer])

    def run(self):
        try:
            while True:
                bindings = {
                    'people': controllers_manager.user.open_user_menu,
                    'events': controllers_manager.event.open_events_menu,
                    'organizers': controllers_manager.organizer.open_organizers_menu,
                    'locals': controllers_manager.local.open_locals_menu,
                    'reports': controllers_manager.report.open_reports_menu,
                }

                option = self.view.show_menu()
                print('option', option)
                bindings[option]()
                print('after bindings[option]')
        except UserExitException:
            return
        except Exception:
            self.view.close()
            controllers_manager.user.view.close()
            controllers_manager.address.view.close()

            self.view.show_message('Um erro inesperado ocorreu!')
            print('An unexpected error happened ...')
            if (DEBUG_MODE):
                print('=====================')
                traceback.print_exc()
                print('=====================')
            self.run()
