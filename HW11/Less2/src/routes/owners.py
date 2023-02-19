from typing import List

from fastapi import APIRouter, Depends, Path, HTTPException, status
from sqlalchemy.orm import Session

from HW11.Less2.src.schemas import ResponseOwner, OwnerModel

router = APIRouter(prefix='/owners', tags=['owners'])



@router.get("/owners", response_model=List[ResponseOwner], tags=['owners'])
async def get_owners(db: Session = Depends(get_db)):
    owners = db.query(Owner).all()
    return owners


@router.get("/owners/{owner_id}", response_model=ResponseOwner, tags=['owners'])
async def get_owner(owner_id: int = Path(1, ge=1), db: Session = Depends(get_db)):
    owner = db.query(Owner).filter_by(id=owner_id).first()
    if owner is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Not Found")
    return owner


@router.post("/owners", response_model=ResponseOwner, tags=['owners'])
async def create_owners(body: OwnerModel, db: Session = Depends(get_db)):
    owner = Owner(**body.dict())
    db.add(owner)
    db.commit()
    db.refresh(owner)
    return owner


@router.put("/owners/{owner_id}", response_model=ResponseOwner, tags=['owners'])
async def update_owner(body: OwnerModel, owner_id: int = Path(1, ge=1), db: Session = Depends(get_db)):
    owner = db.query(Owner).filter_by(id=owner_id).first()
    if owner is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Not Found")
    owner.email = body.email
    db.commit()
    db.refresh(owner)
    return owner


@router.delete("/owners/{owner_id}", status_code=status.HTTP_204_NO_CONTENT, tags=['owners'])
async def delete_owner(owner_id: int = Path(1, ge=1), db: Session = Depends(get_db)):
    owner = db.query(Owner).filter_by(id=owner_id).first()
    if owner is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Not Found")
    db.delete(owner)
    db.commit()