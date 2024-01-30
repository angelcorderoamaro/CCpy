from channels.db import database_sync_to_async
from django.db import connection, IntegrityError
from .models import Project
import asyncio

@database_sync_to_async
def guardar_en_mi_tabla(datos):
    with connection.cursor() as cursor:
        sql_query = "INSERT INTO tb_projects (ProjectName, AggregationID, CounterpartID) VALUES ('{project_name}', '{aggregation_id}', '{counterpart_id}')"   
        cursor.execute(sql_query, [datos['ProjectName'], datos['AggregationID'], datos['CounterpartID']])
    
@database_sync_to_async
def get_max_id():
    try:
        with connection.cursor() as cursor:
            query = "SELECT MAX(ProjectID) FROM tb_projects"
            cursor.execute(query)
            result = cursor.fetchone()
            return result[0] if result else None
    except IntegrityError as e:
        print(f"IntegrityError: {e}")
        return None

@database_sync_to_async
def create_project(datos):
    try:
        new_project = Project(
            ProjectName=datos['ProjectName'],
            AggregationID=datos['AggregationID'],
            CounterpartID=datos['CounterpartID'],
            Cve_Geo=datos['Cve_Geo'],
            Cve_Unica=datos['Cve_Unica']
            )
        new_project.save()
        return new_project.ProjectID
    except IntegrityError as e:
        print(f"IntegrityError al agregar proyectos: {e}")
        return None
    except Exception as e:
        print(f"Error al agregar proyectos: {e}")
        return None

async def fn_agregar_nuevos_proyectos(datos):
    try:
        await asyncio.sleep(2)
        project_id = await create_project(datos)
        if project_id is not None:
            return {
                'valido': 1,
                'error': 'Se guardó correctamente',
                'projects': project_id
            }
        else:
            raise Exception('Error al agregar proyectos')
    except Exception as e:
        print(f"Error al agregar proyectos: {e}")
        return {
            'valido': 0,
            'error': str(e)
        }
