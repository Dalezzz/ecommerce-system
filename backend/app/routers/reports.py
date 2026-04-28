from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..db.database import get_db
from ..schemas.report import InventoryReportItemResponse
from ..services.report_service import inventario_alertas, resumen_ventas, top_productos
from ..utils.security import require_admin

router = APIRouter(prefix="/reports", tags=["Reports"])


@router.get("/sales-summary")
def sales_summary(db: Session = Depends(get_db), _=Depends(require_admin)):
	return resumen_ventas(db)


@router.get("/top-products")
def top_products(limite: int = 5, db: Session = Depends(get_db), _=Depends(require_admin)):
	return top_productos(db, limite)


@router.get("/inventory", response_model=list[InventoryReportItemResponse])
def inventory_report(
	categoria_id: int | None = None,
	solo_criticos: bool = False,
	db: Session = Depends(get_db),
	_=Depends(require_admin),
):
	return inventario_alertas(db, categoria_id=categoria_id, solo_criticos=solo_criticos)
