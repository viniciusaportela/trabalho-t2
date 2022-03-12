from datetime import datetime
import traceback
from controllers.controllers_manager import controllers_manager
from views.main_view import MainView

DEBUG_MODE = True

class App:
    def __init__(self):
        self.view = MainView()

    def __inject_data(self):
        controllers_manager.user.add_user('123', 'Vinicius', datetime(2001, 7, 4), '8800000', 'rua Porto', '220', 'Apt 100')
        controllers_manager.user.add_user('12312312313', 'Jose', datetime(2000, 2, 5), '8800000', 'rua Almeida', '10', '', True)
        controllers_manager.organizer.add_organizer('1234', 'Jose', datetime(2000, 2, 5), '8800000', 'rua Almeida', '10', '')
        controllers_manager.local.add_local('Shopping Trindade', '8800000', 'rua Almeida', '30', 'Loja 2')
        
        local, _ = controllers_manager.local.get_local_by_name('Shopping Trindade')
        organizer, _ = controllers_manager.organizer.get_organizer_by_cpf('1234')
        controllers_manager.event.add_event('E', 25, local, '01/01/2020 17:30', [organizer])
        controllers_manager.event.add_event('E2', 10, local, '22/02/2022 17:30', [organizer])
        controllers_manager.event.add_event('E3', 10, local, '22/04/2022 17:30', [organizer])

    def run(self):
        try:
            self.__inject_data()

            bindings = {
                1: controllers_manager.user.open_user_menu,
                2: controllers_manager.event.open_events_menu,
                3: controllers_manager.organizer.open_organizers_menu,
                4: controllers_manager.local.open_locals_menu,
                5: controllers_manager.report.open_reports_menu,
            }

            while True:
                option = self.view.show_menu()

                if (option == 0):
                    return

                bindings[option]()
        except Exception:
            print('An unexpected error happened ...')
            if (DEBUG_MODE):
                print('=====================')
                traceback.print_exc()
                print('=====================')
            self.run()

App().run()
