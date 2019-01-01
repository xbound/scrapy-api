from enum import Enum

class ENVIRONMENT(Enum):
    DEVELOPMENT='development'
    PRODUCTION='production'
    STAGING='staging'

class MESSAGE(Enum):
    ERROR_404='Requested resource was not found.'
    ERROR_500='Internal server error.'
    DOCUMENT_TASK_404 = 'Requested document task was not found.'
    IMAGE_TASK_404 = 'Requested image task was not found.'