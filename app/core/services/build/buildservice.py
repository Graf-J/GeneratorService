import json

from app.core.entities import Build
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

    def build_project(self, project_id: str, build_config: Build):
        # Get and Check Graph
        graph = self.graph_repository.get_graph(project_id)
        if len(graph.vertices) == 0:
            raise BuildException('Graph has to have at least one vertex')

        # Get Project
        project = self.project_repository.get_project(project_id)

        # Create Output Folders
        self.output_repository.delete_output_folder_if_exists(project)
        self.output_repository.create_folder_structure(project)

        # Generate and Move GraphQL Schema to Output
        schema_template = self.template_repository.get_schema_template()
        schema_file = RenderOperation.render_schema(schema_template, graph)
        self.output_repository.save_schema_file(project, schema_file)

        # Generate and Move main.py to Output
        app_template = self.template_repository.get_app_template()
        app_file = RenderOperation.render_app(app_template, graph)
        self.output_repository.save_app_file(project, app_file)

        # Generate and Move docker-compose.yaml to Output
        docker_compose_template = self.template_repository.get_docker_compose_template()
        docker_compose_file = RenderOperation.render_docker_compose(docker_compose_template, build_config)
        self.output_repository.save_docker_compose_file(project, docker_compose_file)

        # Serialize and Save Graph as JSON
        graph_dict = graph.to_dict()
        graph_json_file = File('graph.json', json.dumps(graph_dict, indent=4).encode('utf-8'))
        self.output_repository.save_graph_json_file(project, graph_json_file)

        # Copy Graph-Datastructure Files to Output
        graph_files = self.template_repository.get_graph_files()
        self.output_repository.save_graph_files(project, graph_files)

        # Copy Query-Builder Files to Output
        querybuilder_files = self.template_repository.get_querybuilder_files()
        self.output_repository.save_querybuilder_files(project, querybuilder_files)
        quereybuilder_argument_files = self.template_repository.get_querybuilder_argument_files()
        self.output_repository.save_querybuilder_argument_files(project, quereybuilder_argument_files)

        # Copy Static Files to Output
        static_files = self.template_repository.get_static_files()
        self.output_repository.save_static_files(project, static_files)
