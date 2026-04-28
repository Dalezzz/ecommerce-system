from pydantic import BaseModel


class InventoryReportItemResponse(BaseModel):
	producto_id: int
	sku: str
	nombre: str
	categoria: str | None = None
	stock_actual: int
	stock_minimo: int
	umbral_critico: int
	estado: str
	color: str