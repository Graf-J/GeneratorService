import os
import shutil

from jinja2 import Environment, FileSystemLoader, Template


class OutputFolderAdapter:
    def __init__(self, output_folder='outputs', template_folder='templates', static_folder='static'):
        self.output_folder = output_folder
        self.template_folder = template_folder
        self.static_folder = static_folder

    def get_schema_template(self, schema_template_folder='schema', schema_template_name='schema.jinja') -> Template:
        base_directory = os.getcwd()
        path = os.path.join(base_directory, self.template_folder, schema_template_folder)

        env = Environment(loader=FileSystemLoader(path))
        template = env.get_template(schema_template_name)

        return template

    def delete_output_folder_if_exists(self, folder_name: str):
        base_directory = os.getcwd()
        path = os.path.join(base_directory, self.output_folder, folder_name)

        if os.path.exists(path):
            shutil.rmtree(path)

    def create_output_folder(self, folder_name: str):
        base_directory = os.getcwd()
        path = os.path.join(base_directory, self.output_folder, folder_name)

        os.makedirs(path, exist_ok=True)

    def save_content_to_file(self, folder_name: str, file_name: str, content: str):
        base_directory = os.getcwd()
        path = os.path.join(base_directory, self.output_folder, folder_name, file_name)

        with open(path, 'w') as file:
            file.write(content)

    def get_static_files(self):
        base_directory = os.getcwd()
        path = os.path.join(base_directory, self.template_folder, self.static_folder)
        static_files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

        return static_files

    def copy_static_files(self, folder_name: str, static_file_names: str):
        base_directory = os.getcwd()
        destination = os.path.join(base_directory, self.output_folder, folder_name)

        for file_name in static_file_names:
            path = os.path.join(base_directory, self.template_folder, self.static_folder, file_name)
            shutil.copy(path, destination)
