"""
Portal Demandas FastAPI Application
Comprehensive API for managing demands/tickets with SQLAlchemy + Neon PostgreSQL
"""

from fastapi import FastAPI, Depends, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func, desc, asc
from datetime import datetime, timedelta
from typing import List, Optional
import logging

from portal_demandas.models import (
    Ticket, TicketCreate, TicketUpdate, TicketListResponse, 
    TicketComment, TicketStats, TicketFilter,
    TicketStatus, TicketPrioridade, TicketCategoria
)
from portal_demandas.db import TicketDB, TicketComment as TicketCommentDB, get_db, init_portal_db

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Portal Demandas API",
    description="API para gerenciamento de demandas e tickets do AUDITORIA360",
    version="1.0.0",
    tags_metadata=[
        {"name": "tickets", "description": "Operações com tickets"},
        {"name": "comments", "description": "Comentários dos tickets"},
        {"name": "stats", "description": "Estatísticas e relatórios"},
    ]
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    try:
        init_portal_db()
        logger.info("Portal demandas database initialized")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")

# Health check
@app.get("/health", tags=["health"])
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "portal_demandas",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    }

# Ticket CRUD operations
@app.post("/tickets/", response_model=Ticket, tags=["tickets"])
def criar_ticket(ticket: TicketCreate, db: Session = Depends(get_db)):
    """
    Criar um novo ticket
    """
    try:
        # Create database ticket
        db_ticket = TicketDB(
            titulo=ticket.titulo,
            descricao=ticket.descricao,
            etapa=ticket.etapa,
            prazo=ticket.prazo,
            responsavel=ticket.responsavel,
            prioridade=ticket.prioridade.value,
            categoria=ticket.categoria.value,
            tags=ticket.tags,
            tempo_estimado=ticket.tempo_estimado,
            criado_em=datetime.utcnow(),
            atualizado_em=datetime.utcnow()
        )
        
        db.add(db_ticket)
        db.commit()
        db.refresh(db_ticket)
        
        # Log creation
        logger.info(f"Ticket created: ID={db_ticket.id}, Titulo='{db_ticket.titulo}'")
        
        return Ticket.from_orm(db_ticket)
        
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to create ticket: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao criar ticket: {str(e)}")

@app.get("/tickets/{ticket_id}", response_model=Ticket, tags=["tickets"])
def obter_ticket(ticket_id: int, db: Session = Depends(get_db)):
    """
    Obter um ticket específico por ID
    """
    db_ticket = db.query(TicketDB).filter(TicketDB.id == ticket_id).first()
    if not db_ticket:
        raise HTTPException(status_code=404, detail="Ticket não encontrado")
    
    return Ticket.from_orm(db_ticket)

@app.get("/tickets/", response_model=TicketListResponse, tags=["tickets"])
def listar_tickets(
    page: int = Query(1, ge=1, description="Número da página"),
    per_page: int = Query(10, ge=1, le=100, description="Itens por página"),
    status: Optional[List[TicketStatus]] = Query(None, description="Filtrar por status"),
    prioridade: Optional[List[TicketPrioridade]] = Query(None, description="Filtrar por prioridade"),
    categoria: Optional[List[TicketCategoria]] = Query(None, description="Filtrar por categoria"),
    responsavel: Optional[str] = Query(None, description="Filtrar por responsável"),
    etapa: Optional[str] = Query(None, description="Filtrar por etapa"),
    search: Optional[str] = Query(None, description="Buscar no título e descrição"),
    sort_by: str = Query("criado_em", description="Campo para ordenação"),
    sort_order: str = Query("desc", description="Ordem: asc ou desc"),
    db: Session = Depends(get_db)
):
    """
    Listar tickets com filtros e paginação
    """
    try:
        # Build query
        query = db.query(TicketDB)
        
        # Apply filters
        if status:
            query = query.filter(TicketDB.status.in_([s.value for s in status]))
        
        if prioridade:
            query = query.filter(TicketDB.prioridade.in_([p.value for p in prioridade]))
        
        if categoria:
            query = query.filter(TicketDB.categoria.in_([c.value for c in categoria]))
        
        if responsavel:
            query = query.filter(TicketDB.responsavel.ilike(f"%{responsavel}%"))
        
        if etapa:
            query = query.filter(TicketDB.etapa.ilike(f"%{etapa}%"))
        
        if search:
            search_filter = or_(
                TicketDB.titulo.ilike(f"%{search}%"),
                TicketDB.descricao.ilike(f"%{search}%")
            )
            query = query.filter(search_filter)
        
        # Apply sorting
        if hasattr(TicketDB, sort_by):
            sort_column = getattr(TicketDB, sort_by)
            if sort_order.lower() == "desc":
                query = query.order_by(desc(sort_column))
            else:
                query = query.order_by(asc(sort_column))
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        offset = (page - 1) * per_page
        tickets = query.offset(offset).limit(per_page).all()
        
        # Convert to Pydantic models
        ticket_list = [Ticket.from_orm(ticket) for ticket in tickets]
        
        return TicketListResponse.create(
            tickets=ticket_list,
            total=total,
            page=page,
            per_page=per_page
        )
        
    except Exception as e:
        logger.error(f"Failed to list tickets: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao listar tickets: {str(e)}")

@app.patch("/tickets/{ticket_id}", response_model=Ticket, tags=["tickets"])
def atualizar_ticket(
    ticket_id: int, 
    ticket_update: TicketUpdate, 
    db: Session = Depends(get_db)
):
    """
    Atualizar um ticket existente
    """
    # Find ticket
    db_ticket = db.query(TicketDB).filter(TicketDB.id == ticket_id).first()
    if not db_ticket:
        raise HTTPException(status_code=404, detail="Ticket não encontrado")
    
    try:
        # Update fields
        update_data = ticket_update.dict(exclude_unset=True)
        
        for field, value in update_data.items():
            if hasattr(db_ticket, field) and value is not None:
                # Handle enum fields
                if field in ['status', 'prioridade', 'categoria'] and hasattr(value, 'value'):
                    setattr(db_ticket, field, value.value)
                else:
                    setattr(db_ticket, field, value)
        
        # Update timestamp
        db_ticket.atualizado_em = datetime.utcnow()
        
        db.commit()
        db.refresh(db_ticket)
        
        logger.info(f"Ticket updated: ID={ticket_id}")
        
        return Ticket.from_orm(db_ticket)
        
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to update ticket {ticket_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar ticket: {str(e)}")

@app.delete("/tickets/{ticket_id}", tags=["tickets"])
def deletar_ticket(ticket_id: int, db: Session = Depends(get_db)):
    """
    Deletar um ticket
    """
    db_ticket = db.query(TicketDB).filter(TicketDB.id == ticket_id).first()
    if not db_ticket:
        raise HTTPException(status_code=404, detail="Ticket não encontrado")
    
    try:
        # Delete related comments first
        db.query(TicketCommentDB).filter(TicketCommentDB.ticket_id == ticket_id).delete()
        
        # Delete ticket
        db.delete(db_ticket)
        db.commit()
        
        logger.info(f"Ticket deleted: ID={ticket_id}")
        
        return {"message": "Ticket deletado com sucesso"}
        
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to delete ticket {ticket_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao deletar ticket: {str(e)}")

# Comments endpoints
@app.post("/tickets/{ticket_id}/comments/", response_model=TicketComment, tags=["comments"])
def adicionar_comentario(
    ticket_id: int, 
    comment: TicketComment, 
    db: Session = Depends(get_db)
):
    """
    Adicionar comentário a um ticket
    """
    # Verify ticket exists
    ticket_exists = db.query(TicketDB).filter(TicketDB.id == ticket_id).first()
    if not ticket_exists:
        raise HTTPException(status_code=404, detail="Ticket não encontrado")
    
    try:
        db_comment = TicketCommentDB(
            ticket_id=ticket_id,
            autor=comment.autor,
            comentario=comment.comentario,
            tipo=comment.tipo,
            criado_em=datetime.utcnow()
        )
        
        db.add(db_comment)
        db.commit()
        db.refresh(db_comment)
        
        return TicketComment.from_orm(db_comment)
        
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to add comment to ticket {ticket_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao adicionar comentário: {str(e)}")

@app.get("/tickets/{ticket_id}/comments/", response_model=List[TicketComment], tags=["comments"])
def listar_comentarios(ticket_id: int, db: Session = Depends(get_db)):
    """
    Listar comentários de um ticket
    """
    comments = db.query(TicketCommentDB).filter(
        TicketCommentDB.ticket_id == ticket_id
    ).order_by(TicketCommentDB.criado_em.desc()).all()
    
    return [TicketComment.from_orm(comment) for comment in comments]

# Statistics endpoints
@app.get("/stats/", response_model=TicketStats, tags=["stats"])
def obter_estatisticas(db: Session = Depends(get_db)):
    """
    Obter estatísticas dos tickets
    """
    try:
        # Basic counts
        total = db.query(TicketDB).count()
        pendentes = db.query(TicketDB).filter(TicketDB.status == "pendente").count()
        em_andamento = db.query(TicketDB).filter(TicketDB.status == "em_andamento").count()
        concluidos = db.query(TicketDB).filter(TicketDB.status == "concluido").count()
        cancelados = db.query(TicketDB).filter(TicketDB.status == "cancelado").count()
        
        # Priority distribution
        por_prioridade = {}
        for prioridade in TicketPrioridade:
            count = db.query(TicketDB).filter(TicketDB.prioridade == prioridade.value).count()
            por_prioridade[prioridade.value] = count
        
        # Category distribution
        por_categoria = {}
        for categoria in TicketCategoria:
            count = db.query(TicketDB).filter(TicketDB.categoria == categoria.value).count()
            por_categoria[categoria.value] = count
        
        # Average completion time
        completed_tickets = db.query(TicketDB).filter(
            TicketDB.status == "concluido",
            TicketDB.tempo_gasto.isnot(None)
        ).all()
        
        tempo_medio_conclusao = None
        if completed_tickets:
            total_time = sum(ticket.tempo_gasto for ticket in completed_tickets if ticket.tempo_gasto)
            tempo_medio_conclusao = total_time / len(completed_tickets) if total_time > 0 else None
        
        return TicketStats(
            total=total,
            pendentes=pendentes,
            em_andamento=em_andamento,
            concluidos=concluidos,
            cancelados=cancelados,
            por_prioridade=por_prioridade,
            por_categoria=por_categoria,
            tempo_medio_conclusao=tempo_medio_conclusao
        )
        
    except Exception as e:
        logger.error(f"Failed to get statistics: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao obter estatísticas: {str(e)}")

# Bulk operations
@app.patch("/tickets/bulk/status", tags=["tickets"])
def atualizar_status_bulk(
    ticket_ids: List[int],
    new_status: TicketStatus,
    db: Session = Depends(get_db)
):
    """
    Atualizar status de múltiplos tickets
    """
    try:
        updated_count = db.query(TicketDB).filter(
            TicketDB.id.in_(ticket_ids)
        ).update(
            {
                "status": new_status.value,
                "atualizado_em": datetime.utcnow()
            },
            synchronize_session=False
        )
        
        db.commit()
        
        logger.info(f"Bulk status update: {updated_count} tickets updated to {new_status.value}")
        
        return {
            "message": f"{updated_count} tickets atualizados para status '{new_status.value}'",
            "updated_count": updated_count
        }
        
    except Exception as e:
        db.rollback()
        logger.error(f"Failed bulk status update: {e}")
        raise HTTPException(status_code=500, detail=f"Erro na atualização em lote: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
