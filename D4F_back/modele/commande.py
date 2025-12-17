from D4F_back.db import db


class Commande(db.Model):
    __tablename__ = 'commande'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    materiel_id = db.Column(db.Integer, db.ForeignKey('materiel.id'), nullable=False)

    materiel = db.relationship('Materiel', back_populates='commande', foreign_keys=[materiel_id])
    nombrePiece = db.Column(db.Integer)

    date_emission = db.Column(db.DateTime(timezone=True), nullable=False)
    commentaire_emission = db.Column(db.String, nullable=True)

