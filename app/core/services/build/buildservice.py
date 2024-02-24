from app.core.exceptions import BuildException
from app.core.operations import SchemaOperation
from app.core.repositories import IGraphRepository, IProjectRepository, IOutputRepository
from app.core.services.build.buildserviceinterface import IBuildService


class BuildService(IBuildService):
    def __init__(
            self,
            graph_repository: IGraphRepository,
            project_repository: IProjectRepository,
            output_repository: IOutputRepository
    ):
        self.graph_repository = graph_repository
        self.project_repository = project_repository
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
        schema_template = self.output_repository.get_schema_template(project.name)
        schema_content = SchemaOperation.render_schema(schema_template, graph)
        self.output_repository.insert_schema(project.name, schema_content)

        # Generate and Move main.py with all the Resolvers to Output
        # TODO: Operator Create main.py with Resolvers
        # TODO: Add main.py via Repository

        # Copy all the remaining Files to Output
        self.output_repository.copy_static_files(project.name)
