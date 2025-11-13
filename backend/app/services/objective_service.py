from sqlalchemy.orm import Session
from app.models.objective import AgendaObjective
from app.schemas.objective import ObjectiveCreate

class ObjectiveService:
    @staticmethod
    def create_objective(db: Session, objective_data: ObjectiveCreate) -> AgendaObjective:
        """Create a new objective"""
        objective = AgendaObjective(
            objective_name=objective_data.objective_name
        )
        db.add(objective)
        db.commit()
        db.refresh(objective)
        return objective
    
    @staticmethod
    def get_objectives(db: Session) -> list[AgendaObjective]:
        """Get all objectives"""
        return db.query(AgendaObjective).all()
    
    @staticmethod
    def get_objective(db: Session, objective_id: int) -> AgendaObjective:
        """Get objective by ID"""
        return db.query(AgendaObjective).filter(
            AgendaObjective.objective_id == objective_id
        ).first()
    
    @staticmethod
    def seed_default_objectives(db: Session):
        """Seed default objectives if they don't exist"""
        default_objectives = [
            "เพื่อทราบ",
            "เพื่อพิจารณา",
            "เพื่ออนุมัติ",
            "เพื่อสั่งการ"
        ]
        
        for obj_name in default_objectives:
            existing = db.query(AgendaObjective).filter(
                AgendaObjective.objective_name == obj_name
            ).first()
            
            if not existing:
                objective = AgendaObjective(objective_name=obj_name)
                db.add(objective)
        
        db.commit()