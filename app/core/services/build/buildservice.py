import json

from app.core.exceptions import BuildException
from app.core.operations import RenderOperation
from app.core.repositories import IGraphRepository, IProjectRepository, IOutputRepository, ITemplateRepository
from app.core.services.build.buildserviceinterface import IBuildService
from app.core.valueobjects import File


class BuildService(IBuildService):
    def __init__(
            self,
            graph_repository: IGraphRepository,
            project_repository: IProjectRepository,
            template_repository: ITemplateRepository,
            output_repository: IOutputRepository
    ):
        self.graph_repository = graph_repository
        self.project_repository = project_repository
        self.template_repository = template_repository
        self.output_repository = output_repository

    def build_project(self, project_id: str):
        # Get and Check Graph
        graph = self.graph_repository.get_graph(project_id)
        if len(graph.vertices) == 0:
            raise BuildException('Graph has to have at least one vertex')

        # Get Project
        project = self.project_repository.get_project(project_id)

        # Create Output Folder
        self.output_repository.create_folder_structure(project.name)

        # Generate and Move GraphQL Schema to Output
        schema_template = self.template_repository.get_schema_template()
        schema_file = RenderOperation.render_schema(schema_template, graph)
        self.output_repository.save_file([project.name], schema_file)

        # Generate and Move main.py to Output
        app_template = self.template_repository.get_app_template()
        app_file = RenderOperation.render_app(app_template, graph)
        self.output_repository.save_file([project.name], app_file)

        # TODO: Generate Dockerfile

        # Serialize and Save Graph as JSON
        graph_dict = graph.to_dict()
        graph_json_file = File('graph.json', json.dumps(graph_dict, indent=4).encode('utf-8'))
        self.output_repository.save_file([project.name], graph_json_file)

        # Copy Graph-Datastructure Files to Output
        graph_files = self.template_repository.get_files(['graph'])
        self.output_repository.save_files([project.name, 'graph'], graph_files)

        # Copy Query-Builder Files to Output
        querybuilder_files = self.template_repository.get_files(['querybuilder'])
        self.output_repository.save_files([project.name, 'querybuilder'], querybuilder_files)
        quereybuilder_argument_files = self.template_repository.get_files(['querybuilder', 'arguments'])
        self.output_repository.save_files([project.name, 'querybuilder', 'arguments'], quereybuilder_argument_files)

        # Copy Static Files to Output
        static_files = self.template_repository.get_files(['static'])
        self.output_repository.save_files([project.name], static_files)
