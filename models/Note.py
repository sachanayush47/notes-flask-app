from datetime import datetime
from config.db import db


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete='CASCADE'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    shared_with = db.relationship(
        'User', secondary='note_share', backref=db.backref('shared_notes', lazy='dynamic'))


class NoteShare(db.Model):
    __tablename__ = 'note_share'
    note_id = db.Column(db.Integer, db.ForeignKey(
        'note.id', ondelete='CASCADE'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete='CASCADE'), primary_key=True)
    shared_at = db.Column(db.DateTime, default=datetime.utcnow)


class NoteVersion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    note_id = db.Column(db.Integer, db.ForeignKey(
        'note.id', ondelete='CASCADE'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    versioned_at = db.Column(db.DateTime, default=datetime.utcnow)

    note = db.relationship(
        'Note', backref=db.backref('versions', lazy='dynamic'))
