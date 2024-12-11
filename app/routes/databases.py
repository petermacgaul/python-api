import json
from typing import NoReturn
from fastapi import APIRouter, Depends, HTTPException
from fastapi import status as http_status
import logging

from ..exceptions.databases import DatabaseNotConnected
from app.services.connect_database import ConnectedDatabase
from ..models.scans import ScanDatabaseSerializer, ScanDatabase
from ..repositories.databases import DatabaseRepository
from ..models.databases import DatabaseCreate, DatabaseRead, Database
from ..repositories.scans import ScanDatabaseRepository
from ..repositories.scans_history import ScanDatabaseHistoryRepository
from ..services.database_scanner import DatabaseScanner
from ..services.jwt_service import validate_user

router = APIRouter(prefix="/database", tags=["Database"])


def _not_found(database_id: str) -> NoReturn:
    raise HTTPException(
        status_code=http_status.HTTP_404_NOT_FOUND,
        detail=f"Database with id {database_id} not found",
    )


def _unhandled_error(database_id: str) -> NoReturn:
    raise HTTPException(
        status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Some error occurred while processing database {database_id}",
    )


@router.post("/", status_code=http_status.HTTP_201_CREATED)
async def create_database(
        data: DatabaseCreate,
        repo: DatabaseRepository = Depends(DatabaseRepository),
        _: str = Depends(validate_user)
) -> DatabaseRead:

    try:
        connected_db = ConnectedDatabase(data)
        await connected_db.verify_connection()

        database = Database()

        database.password = data.password
        database.username = data.username
        database.host = data.host
        database.port = data.port

        return await repo.create(database)
    except DatabaseNotConnected as e:
        logging.error("Database not connected")
        raise HTTPException(
            status_code=http_status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except ValueError as e:
        logging.error(f"Error creating database: {e}")
        _unhandled_error("")


@router.post("/scan/{database_id}", status_code=http_status.HTTP_201_CREATED)
async def scan_database(
    database_id: str,
    database_repo: DatabaseRepository = Depends(DatabaseRepository),
    scan_repo: ScanDatabaseRepository = Depends(ScanDatabaseRepository),
    scan_history_repo: ScanDatabaseHistoryRepository = Depends(ScanDatabaseHistoryRepository),
    _: str = Depends(validate_user)
) -> DatabaseRead:

    try:
        database = await database_repo.get_by_id(database_id)

        if not database:
            logging.error("Database not found")
            _not_found(database_id)

        logging.debug(f"Connecting to database {database_id}")
        try:
            connected_db = ConnectedDatabase(database)
            await connected_db.verify_connection()
        except DatabaseNotConnected as e:
            logging.error("Database not connected")
            raise HTTPException(
                status_code=http_status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )

        logging.info(f"Scanning database {database_id}")
        scanner = DatabaseScanner(connected_db)
        scan = await scanner.scan()

        logging.info(f"Saving scan for database {database_id}")
        scan_create = ScanDatabase(
            database_id=database_id,
        )
        scan_create.scan = json.dumps(scan.json())
        previous_scan = await scan_repo.get_by_database_id(database_id)

        if previous_scan:
            logging.info("Updating previous scan")
            await scan_repo.update(previous_scan.id, scan_create.__dict__)
        else:
            logging.info("Creating new scan")
            await scan_repo.create(scan_create)

        logging.info("Saving scan history")
        await scan_history_repo.create(scan_create)

        return database
    except ValueError as e:
        logging.error(f"Error processing database {database_id}: {e}")
        _unhandled_error(database_id)


@router.get("/scan/{database_id}", status_code=http_status.HTTP_200_OK)
async def view_scan_database(
    database_id: str,
    scan_repo: ScanDatabaseRepository = Depends(ScanDatabaseRepository),
    _: str = Depends(validate_user)
) -> ScanDatabaseSerializer:

    try:
        scan = await scan_repo.get_by_database_id(database_id)

        if not scan:
            logging.error(f"Scan not found for database {database_id}")
            _not_found(database_id)

        return ScanDatabaseSerializer(
            scan=json.loads(scan.scan)
        )
    except ValueError as e:
        logging.error(f"Error processing database {database_id}: {e}")
        _unhandled_error(database_id)
