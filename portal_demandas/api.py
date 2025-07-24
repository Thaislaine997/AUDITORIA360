from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from portal_demandas.models import Ticket, TicketCreate
from portal_demandas.db import SessionLocal, TicketDB

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/tickets/", response_model=Ticket)
def criar_ticket(ticket: TicketCreate, db: Session = Depends(get_db)):
    db_ticket = TicketDB(**ticket.dict(), criado_em=datetime.now(), atualizado_em=datetime.now())
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    ticket_dict = db_ticket.__dict__.copy()
    for field in ["prazo", "criado_em", "atualizado_em"]:
        if field in ticket_dict and ticket_dict[field] is not None:
            ticket_dict[field] = ticket_dict[field].isoformat() if hasattr(ticket_dict[field], "isoformat") else ticket_dict[field]
    return Ticket(**ticket_dict)

@app.get("/tickets/{ticket_id}", response_model=Ticket)
def obter_ticket(ticket_id: int, db: Session = Depends(get_db)):
    db_ticket = db.query(TicketDB).filter(TicketDB.id == ticket_id).first()
    if not db_ticket:
        raise HTTPException(status_code=404, detail="Ticket não encontrado")
    ticket_dict = db_ticket.__dict__.copy()
    for field in ["prazo", "criado_em", "atualizado_em"]:
        if field in ticket_dict and ticket_dict[field] is not None:
            ticket_dict[field] = ticket_dict[field].isoformat() if hasattr(ticket_dict[field], "isoformat") else ticket_dict[field]
    return Ticket(**ticket_dict)

@app.get("/tickets/", response_model=list[Ticket])
def listar_tickets(db: Session = Depends(get_db)):
    tickets = db.query(TicketDB).all()
    result = []
    for t in tickets:
        ticket_dict = t.__dict__.copy()
        for field in ["prazo", "criado_em", "atualizado_em"]:
            if field in ticket_dict and ticket_dict[field] is not None:
                ticket_dict[field] = ticket_dict[field].isoformat() if hasattr(ticket_dict[field], "isoformat") else ticket_dict[field]
        result.append(Ticket(**ticket_dict))
    return result

@app.patch("/tickets/{ticket_id}", response_model=Ticket)
def atualizar_ticket(ticket_id: int, ticket: Ticket, db: Session = Depends(get_db)):
    db_ticket = db.query(TicketDB).filter(TicketDB.id == ticket_id).first()
    if not db_ticket:
        raise HTTPException(status_code=404, detail="Ticket não encontrado")
    for key, value in ticket.dict(exclude_unset=True).items():
        setattr(db_ticket, key, value)
    db_ticket.atualizado_em = datetime.now()
    db.commit()
    db.refresh(db_ticket)
    return Ticket(**db_ticket.__dict__)
