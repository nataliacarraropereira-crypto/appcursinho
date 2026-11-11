from __future__ import annotations

from datetime import date

import pandas as pd
import streamlit as st

if __package__:
    from .db import SessionLocal, init_db
    from .models import (
        Disciplina,
        Estudante,
        Horario,
        Mensalidade,
        Professor,
        ProfessorDisciplinaTurma,
        Turma,
    )
else:
    from db import SessionLocal, init_db
    from models import (
        Disciplina,
        Estudante,
        Horario,
        Mensalidade,
        Professor,
        ProfessorDisciplinaTurma,
        Turma,
    )

st.set_page_config(page_title="AppCursinho UFSC", layout="wide")
st.markdown(
    """
    <style>
    .stApp {
        background-color: #f2f7f4;
    }

    [data-testid="stSidebar"] {
        background-color: #dceee8;
        border-right: 1px solid #c3ded3;
    }

    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
        color: #174b3a;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
init_db()


def render_crud_page(
    model_cls,
    title: str,
    form_builder,
    row_builder,
    selection_label,
    key_prefix: str,
):
    st.subheader(title)

    with st.form(f"create_{key_prefix}"):
        values = form_builder(None, f"create_{key_prefix}")
        if st.form_submit_button("Adicionar"):
            with SessionLocal() as session:
                session.add(model_cls(**values))
                session.commit()
            st.success("Registro adicionado com sucesso!")
            st.rerun()

    with SessionLocal() as session:
        records = session.query(model_cls).order_by(model_cls.id).all()

    if records:
        st.markdown("### Registros cadastrados")
        dataframe = pd.DataFrame([row_builder(record) for record in records])
        st.dataframe(dataframe, use_container_width=True)

        selected = st.selectbox(
            f"Selecione o registro para editar ou excluir",
            options=records,
            format_func=selection_label,
            key=f"select_{key_prefix}",
        )

        with st.form(f"edit_{key_prefix}"):
            edit_values = form_builder(selected, f"edit_{key_prefix}")
            col1, col2 = st.columns([1, 1])
            update_clicked = col1.form_submit_button("Salvar alterações")
            delete_clicked = col2.form_submit_button("Excluir")

            if update_clicked:
                with SessionLocal() as session:
                    obj = session.get(model_cls, selected.id)
                    if obj is not None:
                        for field, value in edit_values.items():
                            setattr(obj, field, value)
                        session.commit()
                st.success("Registro atualizado com sucesso!")
                st.rerun()

            if delete_clicked:
                with SessionLocal() as session:
                    obj = session.get(model_cls, selected.id)
                    if obj is not None:
                        session.delete(obj)
                        session.commit()
                st.warning("Registro excluído!")
                st.rerun()
    else:
        st.info("Nenhum registro cadastrado até o momento.")


def estudante_form(record, key_prefix: str):
    defaults = {
        "nome": "",
        "email": "",
        "telefone": "",
        "data_nascimento": date.today(),
    }
    if record is not None:
        defaults = {
            "nome": record.nome,
            "email": record.email,
            "telefone": record.telefone,
            "data_nascimento": record.data_nascimento,
        }

    nome = st.text_input("Nome", value=defaults["nome"], key=f"{key_prefix}_nome")
    email = st.text_input("E-mail", value=defaults["email"], key=f"{key_prefix}_email")
    telefone = st.text_input("Telefone", value=defaults["telefone"], key=f"{key_prefix}_telefone")
    data_nascimento = st.date_input(
        "Data de nascimento",
        value=defaults["data_nascimento"],
        key=f"{key_prefix}_data_nascimento",
    )

    return {
        "nome": nome,
        "email": email,
        "telefone": telefone,
        "data_nascimento": data_nascimento,
    }


def professor_form(record, key_prefix: str):
    defaults = {
        "nome": "",
        "email": "",
        "telefone": "",
        "especialidade": "",
    }
    if record is not None:
        defaults = {
            "nome": record.nome,
            "email": record.email,
            "telefone": record.telefone,
            "especialidade": record.especialidade,
        }

    nome = st.text_input("Nome", value=defaults["nome"], key=f"{key_prefix}_nome")
    email = st.text_input("E-mail", value=defaults["email"], key=f"{key_prefix}_email")
    telefone = st.text_input("Telefone", value=defaults["telefone"], key=f"{key_prefix}_telefone")
    especialidade = st.text_input("Especialidade", value=defaults["especialidade"], key=f"{key_prefix}_especialidade")

    return {
        "nome": nome,
        "email": email,
        "telefone": telefone,
        "especialidade": especialidade,
    }


def disciplina_form(record, key_prefix: str):
    defaults = {"nome": "", "carga_horaria": 0, "descricao": ""}
    if record is not None:
        defaults = {
            "nome": record.nome,
            "carga_horaria": record.carga_horaria,
            "descricao": record.descricao,
        }

    nome = st.text_input("Nome", value=defaults["nome"], key=f"{key_prefix}_nome")
    carga_horaria = st.number_input(
        "Carga horária (horas)",
        min_value=1,
        value=int(defaults["carga_horaria"]),
        key=f"{key_prefix}_carga_horaria",
    )
    descricao = st.text_area("Descrição", value=defaults["descricao"], key=f"{key_prefix}_descricao")

    return {
        "nome": nome,
        "carga_horaria": int(carga_horaria),
        "descricao": descricao,
    }


def turma_form(record, key_prefix: str):
    with SessionLocal() as session:
        disciplinas = session.query(Disciplina).order_by(Disciplina.nome).all()

    default_disciplina_id = disciplinas[0].id if disciplinas else None

    if record is not None:
        default_disciplina_id = record.disciplina_id

    nome = st.text_input("Nome da turma", value=record.nome if record else "", key=f"{key_prefix}_nome")
    disciplinas_options = [disciplina for disciplina in disciplinas]
    disciplina = st.selectbox(
        "Disciplina",
        options=disciplinas_options,
        format_func=lambda item: f"{item.nome} (#{item.id})",
        index=(disciplinas_options.index(next((item for item in disciplinas_options if item.id == default_disciplina_id), disciplinas_options[0]))) if disciplinas_options else 0,
        key=f"{key_prefix}_disciplina",
    ) if disciplinas_options else None
    numero_vagas = st.number_input(
        "Número de vagas",
        min_value=1,
        value=int(record.numero_vagas) if record else 30,
        key=f"{key_prefix}_numero_vagas",
    )
    data_inicio = st.date_input(
        "Data de início",
        value=record.data_inicio if record else date.today(),
        key=f"{key_prefix}_data_inicio",
    )
    data_fim = st.date_input(
        "Data de fim",
        value=record.data_fim if record else date.today(),
        key=f"{key_prefix}_data_fim",
    )

    return {
        "nome": nome,
        "disciplina_id": disciplina.id if disciplina else default_disciplina_id,
        "numero_vagas": int(numero_vagas),
        "data_inicio": data_inicio,
        "data_fim": data_fim,
    }


def horario_form(record, key_prefix: str):
    with SessionLocal() as session:
        turmas = session.query(Turma).order_by(Turma.nome).all()

    default_turma_id = turmas[0].id if turmas else None
    if record is not None:
        default_turma_id = record.turma_id

    turma = st.selectbox(
        "Turma",
        options=turmas,
        format_func=lambda item: f"{item.nome} (#{item.id})",
        index=(turmas.index(next((item for item in turmas if item.id == default_turma_id), turmas[0]))) if turmas else 0,
        key=f"{key_prefix}_turma",
    ) if turmas else None

    dia_semana = st.selectbox(
        "Dia da semana",
        options=["Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira", "Sábado"],
        index=["Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira", "Sábado"].index(record.dia_semana) if record else 0,
        key=f"{key_prefix}_dia_semana",
    )
    horario_inicio = st.text_input(
        "Horário de início",
        value=record.horario_inicio if record else "08:00",
        key=f"{key_prefix}_horario_inicio",
    )
    horario_fim = st.text_input(
        "Horário de fim",
        value=record.horario_fim if record else "10:00",
        key=f"{key_prefix}_horario_fim",
    )

    return {
        "turma_id": turma.id if turma else default_turma_id,
        "dia_semana": dia_semana,
        "horario_inicio": horario_inicio,
        "horario_fim": horario_fim,
    }


def professor_disciplina_turma_form(record, key_prefix: str):
    with SessionLocal() as session:
        professores = session.query(Professor).order_by(Professor.nome).all()
        disciplinas = session.query(Disciplina).order_by(Disciplina.nome).all()
        turmas = session.query(Turma).order_by(Turma.nome).all()

    professor_default = professores[0] if professores else None
    disciplina_default = disciplinas[0] if disciplinas else None
    turma_default = turmas[0] if turmas else None

    if record is not None:
        with SessionLocal() as session:
            professor_default = session.get(Professor, record.professor_id)
            disciplina_default = session.get(Disciplina, record.disciplina_id)
            turma_default = session.get(Turma, record.turma_id)

    professor = st.selectbox(
        "Professor",
        options=professores,
        format_func=lambda item: f"{item.nome} (#{item.id})",
        index=(professores.index(professor_default)) if professores and professor_default in professores else 0,
        key=f"{key_prefix}_professor",
    ) if professores else None
    disciplina = st.selectbox(
        "Disciplina",
        options=disciplinas,
        format_func=lambda item: f"{item.nome} (#{item.id})",
        index=(disciplinas.index(disciplina_default)) if disciplinas and disciplina_default in disciplinas else 0,
        key=f"{key_prefix}_disciplina",
    ) if disciplinas else None
    turma = st.selectbox(
        "Turma",
        options=turmas,
        format_func=lambda item: f"{item.nome} (#{item.id})",
        index=(turmas.index(turma_default)) if turmas and turma_default in turmas else 0,
        key=f"{key_prefix}_turma",
    ) if turmas else None

    return {
        "professor_id": professor.id if professor else None,
        "disciplina_id": disciplina.id if disciplina else None,
        "turma_id": turma.id if turma else None,
    }


def mensalidade_form(record, key_prefix: str):
    with SessionLocal() as session:
        turmas = session.query(Turma).order_by(Turma.nome).all()

    turma_default = turmas[0] if turmas else None
    if record is not None:
        turma_default = next((item for item in turmas if item.id == record.turma_id), turma_default)

    turma = st.selectbox(
        "Turma",
        options=turmas,
        format_func=lambda item: f"{item.nome} (#{item.id})",
        index=(turmas.index(turma_default)) if turmas and turma_default in turmas else 0,
        key=f"{key_prefix}_turma",
    ) if turmas else None
    valor = st.number_input(
        "Valor da mensalidade",
        min_value=0.0,
        value=float(record.valor) if record else 150.00,
        step=0.01,
        format="%.2f",
        key=f"{key_prefix}_valor",
    )
    data_vigencia = st.date_input(
        "Data de vigência",
        value=record.data_vigencia if record else date.today(),
        key=f"{key_prefix}_data_vigencia",
    )
    descricao = st.text_input(
        "Descrição",
        value=record.descricao if record else "Mensalidade do cursinho",
        key=f"{key_prefix}_descricao",
    )

    return {
        "turma_id": turma.id if turma else None,
        "valor": float(valor),
        "data_vigencia": data_vigencia,
        "descricao": descricao,
    }


def render_dashboard():
    st.title("📚 Sistema Web do Cursinho UFSC")
    st.caption("Painel administrativo para organização do cursinho")

    with SessionLocal() as session:
        total_estudantes = session.query(Estudante).count()
        total_professores = session.query(Professor).count()
        total_disciplinas = session.query(Disciplina).count()
        total_turmas = session.query(Turma).count()
        total_mensalidades = session.query(Mensalidade).count()

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Estudantes", total_estudantes)
    col2.metric("Professores", total_professores)
    col3.metric("Disciplinas", total_disciplinas)
    col4.metric("Turmas", total_turmas)
    col5.metric("Mensalidades", total_mensalidades)

    st.markdown("### Visão geral")
    with SessionLocal() as session:
        turmas = session.query(Turma).order_by(Turma.id).all()
        linhas = []
        for turma in turmas:
            disciplina = session.get(Disciplina, turma.disciplina_id)
            linhas.append({
                "Turma": turma.nome,
                "Disciplina": disciplina.nome if disciplina else "-",
                "Vagas": turma.numero_vagas,
                "Início": turma.data_inicio,
                "Fim": turma.data_fim,
            })

    if linhas:
        st.dataframe(pd.DataFrame(linhas), use_container_width=True)
    else:
        st.info("Ainda não há turmas cadastradas.")


def render_estudante_page():
    render_crud_page(
        model_cls=Estudante,
        title="CRUD de Estudantes",
        form_builder=estudante_form,
        row_builder=lambda item: {
            "id": item.id,
            "nome": item.nome,
            "email": item.email,
            "telefone": item.telefone,
            "data_nascimento": item.data_nascimento,
        },
        selection_label=lambda item: f"{item.nome} (#{item.id})",
        key_prefix="estudante",
    )


def render_professor_page():
    render_crud_page(
        model_cls=Professor,
        title="CRUD de Professores",
        form_builder=professor_form,
        row_builder=lambda item: {
            "id": item.id,
            "nome": item.nome,
            "email": item.email,
            "telefone": item.telefone,
            "especialidade": item.especialidade,
        },
        selection_label=lambda item: f"{item.nome} (#{item.id})",
        key_prefix="professor",
    )


def render_disciplina_page():
    render_crud_page(
        model_cls=Disciplina,
        title="CRUD de Disciplinas",
        form_builder=disciplina_form,
        row_builder=lambda item: {
            "id": item.id,
            "nome": item.nome,
            "carga_horaria": item.carga_horaria,
            "descricao": item.descricao,
        },
        selection_label=lambda item: f"{item.nome} (#{item.id})",
        key_prefix="disciplina",
    )


def render_turma_page():
    render_crud_page(
        model_cls=Turma,
        title="CRUD de Turmas",
        form_builder=turma_form,
        row_builder=lambda item: {
            "id": item.id,
            "nome": item.nome,
            "disciplina": item.disciplina.nome if item.disciplina else "-",
            "numero_vagas": item.numero_vagas,
            "data_inicio": item.data_inicio,
            "data_fim": item.data_fim,
        },
        selection_label=lambda item: f"{item.nome} (#{item.id})",
        key_prefix="turma",
    )


def render_horario_page():
    render_crud_page(
        model_cls=Horario,
        title="CRUD de Horários das Aulas",
        form_builder=horario_form,
        row_builder=lambda item: {
            "id": item.id,
            "turma": item.turma.nome if item.turma else "-",
            "dia_semana": item.dia_semana,
            "horario_inicio": item.horario_inicio,
            "horario_fim": item.horario_fim,
        },
        selection_label=lambda item: f"{item.dia_semana} - {item.turma.nome if item.turma else '-'} (#{item.id})",
        key_prefix="horario",
    )


def render_professor_disciplina_turma_page():
    render_crud_page(
        model_cls=ProfessorDisciplinaTurma,
        title="CRUD de Vínculos Professor-Disciplina-Turma",
        form_builder=professor_disciplina_turma_form,
        row_builder=lambda item: {
            "id": item.id,
            "professor": item.professor_id,
            "disciplina": item.disciplina_id,
            "turma": item.turma_id,
        },
        selection_label=lambda item: f"Professor #{item.professor_id} / Disciplina #{item.disciplina_id} / Turma #{item.turma_id}",
        key_prefix="vinculo",
    )


def render_mensalidade_page():
    render_crud_page(
        model_cls=Mensalidade,
        title="CRUD de Mensalidades",
        form_builder=mensalidade_form,
        row_builder=lambda item: {
            "id": item.id,
            "turma": item.turma.nome if item.turma else "-",
            "valor": item.valor,
            "data_vigencia": item.data_vigencia,
            "descricao": item.descricao,
        },
        selection_label=lambda item: f"{item.turma.nome if item.turma else '-'} - R$ {item.valor:.2f} (#{item.id})",
        key_prefix="mensalidade",
    )


def main():
    pages = {
        "Dashboard": render_dashboard,
        "Estudantes": render_estudante_page,
        "Professores": render_professor_page,
        "Disciplinas": render_disciplina_page,
        "Turmas": render_turma_page,
        "Horários": render_horario_page,
        "Vínculos": render_professor_disciplina_turma_page,
        "Mensalidades": render_mensalidade_page,
    }

    page = st.sidebar.radio("📚 Navegação", list(pages.keys()))
    pages[page]()


if __name__ == "__main__":
    main()
