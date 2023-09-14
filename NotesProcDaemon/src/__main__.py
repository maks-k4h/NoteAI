from . import runner
from . import services

runner = runner.Runner()

runner.register_services(
    services.categorization.service.Service(),
)

runner.run()