from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies import get_build_service
from app.api.dto import BuildRequestDto
from app.core.exceptions import ProjectNotFoundException, BuildException
from app.core.services import IBuildService
from app.mappers import BuildMapper

router = APIRouter(
    prefix="/projects/{project_id}/build",
    tags=["Build"]
)


@router.post('/')
def build_project(
        build_request_dto: BuildRequestDto,
        project_id: str,
        service: IBuildService = Depends(get_build_service)
):
    try:
        service.build_project(project_id, BuildMapper.to_entity(build_request_dto))
    except ProjectNotFoundException as ex:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=[{'msg': ex.message}])
    except BuildException as ex:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=[{'msg': ex.message}])
