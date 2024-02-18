from models.Note import Note, NoteShare, NoteVersion
from models.User import User
from config.db import db


def create_note(title: str, content: str, author_id: int):
    try:
        if not title or not content:
            return {'message': 'Title and content are required'}, 400

        # Convert to string to avoid type errors
        title = str(title)
        content = str(content)

        # Create new note
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
            # If note is found, return it
            note_data = get_note_data(note)
            return {'message': 'Note retreived successfully', 'note': note_data}, 200

        return {'message': 'Note not found'}, 404
    except Exception as e:
        return {'message': str(e)}, 500


def share_note(note_id: int, usernames: list):
    try:
        users = User.query.filter(User.username.in_(usernames)).all()

        for user in users:
            # Check if note is already shared with user, else add it
            if not NoteShare.query.filter_by(note_id=note_id, user_id=user.id).first():
                db.session.add(NoteShare(note_id=note_id, user_id=user.id))

        db.session.commit()
        return {'message': 'Note shared successfully'}, 200
    except Exception as e:
        return {'message': str(e)}, 500


def update_note(note_id: int, author_id: int, **kwargs):
    try:
        # Allow user to update both personal and shared notes
        note = Note.query.filter(
            (Note.id == note_id) &
            ((Note.author_id == author_id) |
             (Note.shared_with.any(User.id == author_id)))
        ).first()

        if not note:
            # If note is not found, return 404
            return {'message': 'Note not found'}, 404

        # Convert to string to avoid type errors and get new values
        new_title = str(kwargs.get('title', note.title))
        new_content = str(kwargs.get('content', note.content))

        # Only perform update if there are changes
        if new_title == note.title and new_content == note.content:
            return {'message': 'No changes found'}, 400

        # Create a new version of the note before updating
        version = NoteVersion(
            note_id=note.id, title=note.title, content=note.content)
        db.session.add(version)

        # Update note
        note.title = new_title
        note.content = new_content

        db.session.commit()

        return {'message': 'Note updated successfully'}, 200
    except Exception as e:
        return {'message': str(e)}, 500


def get_note_version_history(note_id: int, author_id: int):
    try:
        # Allow user to get version history of both personal and shared notes
        note = Note.query.filter(
            (Note.id == note_id) &
            ((Note.author_id == author_id) |
             (Note.shared_with.any(User.id == author_id)))
        ).first()

        if not note:
            # If note is not found, return 404
            return {'message': 'Note not found'}, 404

        # Get all versions of the note in descending order
        versions = NoteVersion.query.filter_by(note_id=note.id).order_by(
            NoteVersion.versioned_at.desc()).all()
        version_data = [get_note_data(version) for version in versions]

        return {'message': 'Note versions retreived successfully', 'versions': version_data}, 200
    except Exception as e:
        return {'message': str(e)}, 500


def get_note_data(note):
    note_data = note.__dict__
    note_data.pop('_sa_instance_state')
    return note_data
