from fastapi import APIRouter, HTTPException
from services.pnr_service import get_pnr_status

router = APIRouter(tags=["PNR"])


@router.get("/{pnr}")
async def check_pnr(pnr: str):

    try:
        result = await get_pnr_status(pnr)

        if not result:
            raise HTTPException(
                status_code=404,
                detail="PNR not found"
            )

        return {
            "success": True,
            "data": result
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
