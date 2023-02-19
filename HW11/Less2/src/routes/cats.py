

@app.get("/cats", response_model=List[ResponsePet], tags=['cats'])
async def get_cats(limit: int = Query(10, le=1000), offset: int = 0, db: Session = Depends(get_db)):
    cats = db.query(Cat).limit(limit).offset(offset).all()
    return cats


@app.get("/cats/{cat_id}", response_model=ResponsePet, tags=['cats'])
async def get_cat(cat_id: int = Path(1, ge=1), db: Session = Depends(get_db)):
    cat = db.query(Cat).filter_by(id=cat_id).first()
    if cat is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Not Found")
    return cat


@app.post("/cats", response_model=ResponsePet, tags=['cats'])
async def create_cat(body: PetModel, db: Session = Depends(get_db)):
    cat = Cat(**body.dict())
    db.add(cat)
    db.commit()
    db.refresh(cat)
    return cat


@app.put("/cats/{cat_id}", response_model=ResponsePet, tags=['cats'])
async def update_cat(body: PetModel, cat_id: int = Path(1, ge=1), db: Session = Depends(get_db)):
    cat = db.query(Cat).filter_by(id=cat_id).first()
    if cat is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Not Found")
    cat.nickname = body.nickname
    cat.age = body.age
    cat.vaccinated = body.vaccinated
    cat.description = body.description
    cat.owner_id = body.owner_id
    db.commit()
    db.refresh(cat)
    return cat


@app.delete("/cats/{cat_id}", status_code=status.HTTP_204_NO_CONTENT, tags=['cats'])
async def delete_cat(cat_id: int = Path(1, ge=1), db: Session = Depends(get_db)):
    cat = db.query(Cat).filter_by(id=cat_id).first()
    if cat is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Not Found")
    db.delete(cat)
    db.commit()