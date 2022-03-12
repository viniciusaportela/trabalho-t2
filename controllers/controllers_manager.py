import controllers.users_controller
import controllers.address_controller
import controllers.reports_controller
import controllers.events_controller
import controllers.locals_controller
import controllers.organizers_controller

class ControllersManager:
    def __init__(self):
        self.user = controllers.users_controller.UsersController(self)
        self.address = controllers.address_controller.AddressController(self)
        self.report = controllers.reports_controller.ReportsController(self)
        self.event = controllers.events_controller.EventsController(self)
        self.local = controllers.locals_controller.LocalsController(self)
        self.organizer = controllers.organizers_controller.OrganizersController(self)

controllers_manager = ControllersManager()