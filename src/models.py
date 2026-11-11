from __future__ import annotations

from datetime import date, datetime

from sqlalchemy import Date, DateTime, ForeignKey, Integer, Numeric, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship, declarative_base

Base = declarative_base()


class Estudante(Base):
    __tablename__ = "estudantes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(150), nullable=False)
    email: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    telefone: Mapped[str] = mapped_column(String(30), nullable=False)
    data_nascimento: Mapped[date] = mapped_column(Date, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )


class Professor(Base):
    __tablename__ = "professores"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(150), nullable=False)
    email: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    telefone: Mapped[str] = mapped_column(String(30), nullable=False)
    especialidade: Mapped[str] = mapped_column(String(150), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )


class Disciplina(Base):
    __tablename__ = "disciplinas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(150), nullable=False, unique=True)
    carga_horaria: Mapped[int] = mapped_column(Integer, nullable=False)
    descricao: Mapped[str] = mapped_column(String(200), nullable=False, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )
    turmas: Mapped[list["Turma"]] = relationship(back_populates="disciplina")


class Turma(Base):
    __tablename__ = "turmas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(150), nullable=False)
    disciplina_id: Mapped[int] = mapped_column(ForeignKey("disciplinas.id"), nullable=False)
    numero_vagas: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    data_inicio: Mapped[date] = mapped_column(Date, nullable=False)
    data_fim: Mapped[date] = mapped_column(Date, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    disciplina: Mapped[Disciplina] = relationship(back_populates="turmas")
    horarios: Mapped[list["Horario"]] = relationship(back_populates="turma")
    mensalidades: Mapped[list["Mensalidade"]] = relationship(back_populates="turma")


class Horario(Base):
    __tablename__ = "horarios"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    turma_id: Mapped[int] = mapped_column(ForeignKey("turmas.id"), nullable=False)
    dia_semana: Mapped[str] = mapped_column(String(30), nullable=False)
    horario_inicio: Mapped[str] = mapped_column(String(10), nullable=False)
    horario_fim: Mapped[str] = mapped_column(String(10), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    turma: Mapped[Turma] = relationship(back_populates="horarios")


class ProfessorDisciplinaTurma(Base):
    __tablename__ = "professores_disciplinas_turmas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    professor_id: Mapped[int] = mapped_column(ForeignKey("professores.id"), nullable=False)
    disciplina_id: Mapped[int] = mapped_column(ForeignKey("disciplinas.id"), nullable=False)
    turma_id: Mapped[int] = mapped_column(ForeignKey("turmas.id"), nullable=False)

    __table_args__ = (
        UniqueConstraint("professor_id", "disciplina_id", "turma_id", name="uq_professor_disciplina_turma"),
    )


class Mensalidade(Base):
    __tablename__ = "mensalidades"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    turma_id: Mapped[int] = mapped_column(ForeignKey("turmas.id"), nullable=False)
    valor: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    data_vigencia: Mapped[date] = mapped_column(Date, nullable=False)
    descricao: Mapped[str] = mapped_column(String(200), nullable=False, default="Mensalidade")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    turma: Mapped[Turma] = relationship(back_populates="mensalidades")
