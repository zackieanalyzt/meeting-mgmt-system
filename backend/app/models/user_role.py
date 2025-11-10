from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

class UserRole(Base):
    __tablename__ = "user_roles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users_local.user_id"))
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.role_id"))

    user: Mapped["User"] = relationship(
        "User", back_populates="user_roles", foreign_keys=[user_id]
    )

    role: Mapped["Role"] = relationship(
        "Role", back_populates="user_roles", foreign_keys=[role_id]
    )
