from fastapi import HTTPException
from database import SessionLocal
from note.domain.note import Note
from note.infra.db_models.note import Note as NoteModel
from note.infra.db_models.note import Tag as TagModel
from note.domain.repository.note_repo import INoteRepository
from sqlalchemy.orm import joinedload

from utils.db_utils import row_to_dict

class NoteRepository(INoteRepository):
    def get_notes(
            self,
            user_id: str,
            page: int,
            items_per_page: int
        ) -> tuple[int, list[Note]]:
        with SessionLocal() as db:
            query = db.query(NoteModel).options(joinedload(NoteModel.tags)).filter(NoteModel.user_id == user_id)
            total_count = query.count()
            note_model = query.offset((page - 1) * items_per_page).limit(items_per_page).all()
        res_note = [Note(**row_to_dict(note)) for note in note_model]
        return total_count, res_note
    
    def find_by_id(self, user_id: str, id: str) -> Note:
        with SessionLocal() as db:
            note_model = (
                db.query(NoteModel)
                .options(joinedload(NoteModel.tags))
                .filter(NoteModel.user_id == user_id, NoteModel.id == id)
                .first()
            )
            if not note_model:
                raise HTTPException(status_code=422)

        return Note(**row_to_dict(note_model))
    
    def save(self, user_id: str, note: Note) -> Note:
        with SessionLocal() as db:
            tags: list[TagModel] = []
            for tag in note.tags:
                existing_tag = db.query(TagModel).filter(TagModel.name == tag.name).first()
                if existing_tag:
                    tags.append(existing_tag)
                else:
                    tags.append(
                        TagModel(
                            id=tag.id,
                            name=tag.name,
                            created_at=tag.created_at,
                            updated_at=tag.updated_at,
                        )
                    )

            new_note_model = NoteModel(
                id=note.id,
                user_id=user_id,
                title=note.title,
                content=note.content,
                memo_date=note.memo_date,
                tags=tags,
                created_at=note.created_at,
                updated_at=note.updated_at,
            )

            db.add(new_note_model)
            db.commit()
        return Note(**row_to_dict(new_note_model))

    def update(self, user_id: str, note: Note) -> Note:
        with SessionLocal() as db:
            self.delete_tags(user_id, note.id)

            note_model = (
                db.query(NoteModel)
                .filter(NoteModel.user_id == user_id, NoteModel.id == note.id)
                .first()
            )
            if not note:
                raise HTTPException(status_code=422)

            note_model.title = note.title  # type: ignore
            note_model.content = note.content  # type: ignore
            note_model.memo_date = note.memo_date  # type: ignore

            tags: list[TagModel] = []
            for tag in note.tags:
                existing_tag = db.query(TagModel).filter(TagModel.name == tag.name).first()
                if existing_tag:
                    tags.append(existing_tag)
                else:
                    tags.append(
                        TagModel(
                            id=tag.id,
                            name=tag.name,
                            created_at=tag.created_at,
                            updated_at=tag.updated_at,
                        )
                    )

            note_model.tags = tags  # type: ignore

            db.add(note_model)
            db.commit()

            return Note(**row_to_dict(note_model))

    def delete_tags(self, user_id: str, id: str) -> None:
        with SessionLocal() as db:
            note_model = db.query(NoteModel).filter(NoteModel.user_id == user_id, NoteModel.id == id).first()
            if not note_model:
                raise HTTPException(status_code=422)

            note_model.tags = []
            db.add(note_model)
            db.commit()

            unused_tags = db.query(TagModel).filter(~TagModel.notes.any()).all()
            for tag in unused_tags:
                db.delete(tag)

            db.commit()

    def delete(self, user_id: str, id: str) -> None:
        with SessionLocal() as db:
            self.delete_tags(user_id, id)

            note_model = db.query(NoteModel).filter(NoteModel.user_id == user_id, NoteModel.id == id).first()
            if not note_model:
                raise HTTPException(status_code=422)

            db.delete(note_model)
            db.commit()
    
    def get_notes_by_tag_name(
            self,
            user_id: str,
            tag_name: str,
            page: int,
            items_per_page: int
        ) -> tuple[int, list[Note]]:
        with SessionLocal() as db:
            tag = db.query(TagModel).filter_by(name=tag_name).first()

            if not tag:
                return 0, []

            query = (
                db.query(NoteModel)
                # .options(joinedload(NoteModel.tags))
                .filter(
                    NoteModel.user_id == user_id,
                    NoteModel.tags.any(id=tag.id),
                )
            )

            total_count = query.count()
            note_model = (
                query.offset((page - 1) * items_per_page).limit(items_per_page).all()
            )

        res_note = [Note(**row_to_dict(note)) for note in note_model]

        return total_count, res_note