from src import runner, services

runner = runner.Runner()

runner.register_services(
    services.note_categorization.service.Service(),
    services.note_category_processor.service.Service()
)

runner.run()
