from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies import get_project_service
from app.api.dto import ProjectRequestDto, ProjectResponseDto
from app.core.exceptions import ProjectException, ProjectNotFoundException
from app.core.services import IProjectService
from app.mappers import ProjectMapper

router = APIRouter(
    prefix='/projects',
    tags=['Project']
)


@router.get('/')
def get_projects(service: IProjectService = Depends(get_project_service)) -> List[ProjectResponseDto]:
    projects = service.get_projects()

    return [ProjectMapper.to_dto(project) for project in projects]


@router.get('/{project_id}')
def get_project(project_id: str, service: IProjectService = Depends(get_project_service)) -> ProjectResponseDto:
    try:
        project = service.get_project(project_id)

        return ProjectMapper.to_dto(project)
    except ProjectNotFoundException as ex:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=[{'msg': ex.message}])


@router.post('/')
def create_project(
        project_request_dto: ProjectRequestDto,
        service: IProjectService = Depends(get_project_service)
) -> ProjectResponseDto:
    try:
        project = service.create_project(ProjectMapper.to_entity(project_request_dto))

        return ProjectMapper.to_dto(project)
    except ProjectException as ex:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=[{'msg': ex.message}])


@router.delete('/{project_id}')
def delete_project(project_id: str, service: IProjectService = Depends(get_project_service)):
    try:
        service.delete_project(project_id)
    except ProjectNotFoundException as ex:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=[{'msg': ex.message}])
