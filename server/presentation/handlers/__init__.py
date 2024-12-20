from .health_check_handler import router as health_check_router
from .insert_fp_model_handler import router as insert_fp_model_router

__all__ = [
    "health_check_router",
    "insert_fp_model_router",
]
