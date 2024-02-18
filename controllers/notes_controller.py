from models.Note import Note, NoteShare, NoteVersion
from models.User import User
from config.db import db


def create_note(title: str, content: str, author_id: int):
    try:
        if not title or not content:
            return {'message': 'Title and content are required'}, 400

        title = str(title)
        content = str(content)

        new_note = Note(title=title, content=content, author_id=author_id)
        db.session.add(new_note)
        db.session.commit()

        return {'message': 'Note created successfully', 'note_id': new_note.id}, 201
    except Exception as e:
        return {'message': str(e)}, 500


def get_note(note_id: int, author_id: int):
    try:
        # Query for the note, including a check for shared notes
        note = Note.query.filter(
            (Note.id == note_id) &
            ((Note.author_id == author_id) |
             (Note.shared_with.any(User.id == author_id)))
        ).first()

        if note:
            note_data = get_note_data(note)
            return {'message': '', 'note': note_data}, 200

        return {'message': 'Note not found'}, 404
    except Exception as e:
        return {'message': str(e)}, 500


def share_note(note_id: int, usernames: list):
    try:
        users = User.query.filter(User.username.in_(usernames)).all()

        for user in users:
            if not NoteShare.query.filter_by(note_id=note_id, user_id=user.id).first():
                db.session.add(NoteShare(note_id=note_id, user_id=user.id))

        db.session.commit()
        return {'message': 'Note shared successfully'}, 200
    except Exception as e:
        return {'message': str(e)}, 500


def update_note(note_id: int, author_id: int, **kwargs):
    try:
        # Allow user to update shared notes as well
        note = Note.query.filter(
            (Note.id == note_id) &
            ((Note.author_id == author_id) |
             (Note.shared_with.any(User.id == author_id)))
        ).first()

        if not note:
            return {'message': 'Note not found'}, 404

        new_title = str(kwargs.get('title', note.title))
        new_content = str(kwargs.get('content', note.content))

        # Only perform update if there are changes
        if new_title == note.title and new_content == note.content:
            return {'message': 'No changes found'}, 400

        version = NoteVersion(
            note_id=note.id, title=note.title, content=note.content)
        db.session.add(version)

        note.title = new_title
        note.content = new_content

        db.session.commit()

        return {'message': 'Note updated successfully'}, 200
    except Exception as e:
        return {'message': str(e)}, 500


def get_note_version_history(note_id: int, author_id: int):
    # Allow user to get version history of both personal and shared notes
    note = Note.query.filter(
        (Note.id == note_id) &
        ((Note.author_id == author_id) |
            (Note.shared_with.any(User.id == author_id)))
    ).first()

    if not note:
        return {'message': 'Note not found'}, 404

    versions = NoteVersion.query.filter_by(note_id=note.id).order_by(
        NoteVersion.versioned_at.desc()).all()
    version_data = [get_note_data(version) for version in versions]
    return {'message': '', 'versions': version_data}, 200


def get_note_data(note):
    note_data = note.__dict__
    note_data.pop('_sa_instance_state')
    return note_data
