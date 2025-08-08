"""
Portal Demandas FastAPI Application
Comprehensive API for managing demands/tickets with SQLAlchemy + Neon PostgreSQL
"""

import logging
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from typing import List, Optional

from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import asc, desc, or_
from sqlalchemy.orm import Session

from portal_demandas.db import TicketComment as TicketCommentDB
from portal_demandas.db import (
    TicketDB,
    get_db,
    init_portal_db,
)
from portal_demandas.models import (
    Ticket,
    TicketCategoria,
    TicketComment,
    TicketCreate,
    TicketListResponse,
    TicketPrioridade,
    TicketStats,
    TicketStatus,
    TicketUpdate,
)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """FastAPI lifespan event handler"""
    # Startup
    try:
        init_portal_db()
        logger.info("Portal demandas database initialized")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")

    yield

    # Shutdown (if needed)
    logger.info("Portal demandas API shutting down")


# Create FastAPI app with lifespan
app = FastAPI(
    title="Portal Demandas API",
    description="API para gerenciamento de demandas e tickets do AUDITORIA360",
    version="1.0.0",
    lifespan=lifespan,
    tags_metadata=[
        {"name": "tickets", "description": "Operações com tickets"},
        {"name": "comments", "description": "Comentários dos tickets"},
        {"name": "stats", "description": "Estatísticas e relatórios"},
    ],
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health check
@app.get("/health", tags=["health"])
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "portal_demandas",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "version": "1.0.0",
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
            criado_em=datetime.now(timezone.utc),
            atualizado_em=datetime.now(timezone.utc),
        )

        db.add(db_ticket)
        db.commit()
        db.refresh(db_ticket)

        # Log creation
        logger.info(f"Ticket created: ID={db_ticket.id}, Titulo='{db_ticket.titulo}'")

        return Ticket.model_validate(db_ticket)

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

    return Ticket.model_validate(db_ticket)


@app.get("/tickets/", response_model=TicketListResponse, tags=["tickets"])
def listar_tickets(
    page: int = Query(1, ge=1, description="Número da página"),
    per_page: int = Query(
        10, ge=1, le=50, description="Itens por página (máximo 50 para performance)"
    ),
    status: Optional[List[TicketStatus]] = Query(
        None, description="Filtrar por status"
    ),
    prioridade: Optional[List[TicketPrioridade]] = Query(
        None, description="Filtrar por prioridade"
    ),
    categoria: Optional[List[TicketCategoria]] = Query(
        None, description="Filtrar por categoria"
    ),
    responsavel: Optional[str] = Query(None, description="Filtrar por responsável"),
    etapa: Optional[str] = Query(None, description="Filtrar por etapa"),
    search: Optional[str] = Query(None, description="Buscar no título e descrição"),
    sort_by: str = Query("criado_em", description="Campo para ordenação"),
    sort_order: str = Query("desc", description="Ordem: asc ou desc"),
    db: Session = Depends(get_db),
):
    """
    Listar tickets com filtros e paginação - PERFORMANCE OPTIMIZED
    Reduced maximum per_page from 100 to 50 for better performance
    """
    import time

    start_time = time.time()

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
                TicketDB.descricao.ilike(f"%{search}%"),
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
        ticket_list = [Ticket.model_validate(ticket) for ticket in tickets]

        # Calculate processing time
        processing_time = time.time() - start_time

        logger.info(
            f"Ticket listing completed in {processing_time:.3f}s (page {page}, {len(ticket_list)} items)"
        )

        response = TicketListResponse.create(
            tickets=ticket_list, total=total, page=page, per_page=per_page
        )

        # Add performance metadata if available
        if hasattr(response, "__dict__"):
            response.__dict__["_performance"] = {
                "processing_time_seconds": processing_time,
                "optimization_level": "enhanced",
            }

        return response

    except Exception as e:
        logger.error(f"Failed to list tickets: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao listar tickets: {str(e)}")


@app.patch("/tickets/{ticket_id}", response_model=Ticket, tags=["tickets"])
def atualizar_ticket(
    ticket_id: int, ticket_update: TicketUpdate, db: Session = Depends(get_db)
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
                if field in ["status", "prioridade", "categoria"] and hasattr(
                    value, "value"
                ):
                    setattr(db_ticket, field, value.value)
                else:
                    setattr(db_ticket, field, value)

        # Update timestamp
        db_ticket.atualizado_em = datetime.now(timezone.utc)

        db.commit()
        db.refresh(db_ticket)

        logger.info(f"Ticket updated: ID={ticket_id}")

        return Ticket.model_validate(db_ticket)

    except Exception as e:
        db.rollback()
        logger.error(f"Failed to update ticket {ticket_id}: {e}")
        raise HTTPException(
            status_code=500, detail=f"Erro ao atualizar ticket: {str(e)}"
        )


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
        db.query(TicketCommentDB).filter(
            TicketCommentDB.ticket_id == ticket_id
        ).delete()

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
@app.post(
    "/tickets/{ticket_id}/comments/", response_model=TicketComment, tags=["comments"]
)
def adicionar_comentario(
    ticket_id: int, comment: TicketComment, db: Session = Depends(get_db)
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
            criado_em=datetime.now(timezone.utc),
        )

        db.add(db_comment)
        db.commit()
        db.refresh(db_comment)

        return TicketComment.model_validate(db_comment)

    except Exception as e:
        db.rollback()
        logger.error(f"Failed to add comment to ticket {ticket_id}: {e}")
        raise HTTPException(
            status_code=500, detail=f"Erro ao adicionar comentário: {str(e)}"
        )


@app.get(
    "/tickets/{ticket_id}/comments/",
    response_model=List[TicketComment],
    tags=["comments"],
)
def listar_comentarios(ticket_id: int, db: Session = Depends(get_db)):
    """
    Listar comentários de um ticket
    """
    comments = (
        db.query(TicketCommentDB)
        .filter(TicketCommentDB.ticket_id == ticket_id)
        .order_by(TicketCommentDB.criado_em.desc())
        .all()
    )

    return [TicketComment.model_validate(comment) for comment in comments]


# Statistics endpoints with performance optimization
@app.get("/stats/", response_model=TicketStats, tags=["stats"])
def obter_estatisticas(db: Session = Depends(get_db)):
    """
    Obter estatísticas dos tickets - PERFORMANCE OPTIMIZED
    Target: <0.5s response time (was 1.5s)
    """
    import time

    start_time = time.time()

    try:
        # Use single query with aggregations for better performance
        from sqlalchemy import case, func

        # Single query to get all statistics at once
        stats_query = db.query(
            func.count(TicketDB.id).label("total"),
            func.sum(case((TicketDB.status == "pendente", 1), else_=0)).label(
                "pendentes"
            ),
            func.sum(case((TicketDB.status == "em_andamento", 1), else_=0)).label(
                "em_andamento"
            ),
            func.sum(case((TicketDB.status == "concluido", 1), else_=0)).label(
                "concluidos"
            ),
            func.sum(case((TicketDB.status == "cancelado", 1), else_=0)).label(
                "cancelados"
            ),
            # Priority counts
            func.sum(case((TicketDB.prioridade == "baixa", 1), else_=0)).label(
                "prioridade_baixa"
            ),
            func.sum(case((TicketDB.prioridade == "media", 1), else_=0)).label(
                "prioridade_media"
            ),
            func.sum(case((TicketDB.prioridade == "alta", 1), else_=0)).label(
                "prioridade_alta"
            ),
            func.sum(case((TicketDB.prioridade == "critica", 1), else_=0)).label(
                "prioridade_critica"
            ),
            # Category counts
            func.sum(case((TicketDB.categoria == "geral", 1), else_=0)).label(
                "categoria_geral"
            ),
            func.sum(case((TicketDB.categoria == "auditoria", 1), else_=0)).label(
                "categoria_auditoria"
            ),
            func.sum(case((TicketDB.categoria == "folha", 1), else_=0)).label(
                "categoria_folha"
            ),
            func.sum(case((TicketDB.categoria == "documentos", 1), else_=0)).label(
                "categoria_documentos"
            ),
            func.sum(case((TicketDB.categoria == "cct", 1), else_=0)).label(
                "categoria_cct"
            ),
            func.sum(case((TicketDB.categoria == "sistema", 1), else_=0)).label(
                "categoria_sistema"
            ),
            # Average completion time for completed tickets
            func.avg(
                case((TicketDB.status == "concluido", TicketDB.tempo_gasto), else_=None)
            ).label("tempo_medio"),
        ).first()

        # Build response from single query result
        por_prioridade = {
            "baixa": int(stats_query.prioridade_baixa or 0),
            "media": int(stats_query.prioridade_media or 0),
            "alta": int(stats_query.prioridade_alta or 0),
            "critica": int(stats_query.prioridade_critica or 0),
        }

        por_categoria = {
            "geral": int(stats_query.categoria_geral or 0),
            "auditoria": int(stats_query.categoria_auditoria or 0),
            "folha": int(stats_query.categoria_folha or 0),
            "documentos": int(stats_query.categoria_documentos or 0),
            "cct": int(stats_query.categoria_cct or 0),
            "sistema": int(stats_query.categoria_sistema or 0),
        }

        # Calculate processing time
        processing_time = time.time() - start_time

        result = TicketStats(
            total=int(stats_query.total or 0),
            pendentes=int(stats_query.pendentes or 0),
            em_andamento=int(stats_query.em_andamento or 0),
            concluidos=int(stats_query.concluidos or 0),
            cancelados=int(stats_query.cancelados or 0),
            por_prioridade=por_prioridade,
            por_categoria=por_categoria,
            tempo_medio_conclusao=(
                float(stats_query.tempo_medio) if stats_query.tempo_medio else None
            ),
        )

        logger.info(f"Portal stats generated in {processing_time:.3f}s")

        if processing_time > 0.5:
            logger.warning(f"Portal stats took {processing_time:.3f}s (target: <0.5s)")

        return result

    except Exception as e:
        logger.error(f"Failed to get statistics: {e}")
        raise HTTPException(
            status_code=500, detail=f"Erro ao obter estatísticas: {str(e)}"
        )


# Bulk operations
@app.patch("/tickets/bulk/status", tags=["tickets"])
def atualizar_status_bulk(
    ticket_ids: List[int], new_status: TicketStatus, db: Session = Depends(get_db)
):
    """
    Atualizar status de múltiplos tickets
    """
    try:
        updated_count = (
            db.query(TicketDB)
            .filter(TicketDB.id.in_(ticket_ids))
            .update(
                {
                    "status": new_status.value,
                    "atualizado_em": datetime.now(timezone.utc),
                },
                synchronize_session=False,
            )
        )

        db.commit()

        logger.info(
            f"Bulk status update: {updated_count} tickets updated to {new_status.value}"
        )

        return {
            "message": f"{updated_count} tickets atualizados para status '{new_status.value}'",
            "updated_count": updated_count,
        }

    except Exception as e:
        db.rollback()
        logger.error(f"Failed bulk status update: {e}")
        raise HTTPException(
            status_code=500, detail=f"Erro na atualização em lote: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)
