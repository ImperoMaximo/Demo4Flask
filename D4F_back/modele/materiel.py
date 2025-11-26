import os
from D4F_back.db import db

class Materiel(db.Model):
    __tablename__ = 'materiel'

    id = db.Column(db.Integer(), primary_key=True,  autoincrement=True)
    nom = db.Column(db.String(), unique=True, nullable=False)
    description = db.Column(db.String(), nullable=False)
    fournisseur = db.Column(db.String(), nullable=True)

    commande = db.relationship(
        'Commande', back_populates='materiel', cascade='all, delete-orphan', lazy='select'
    )
  
    def __repr__(self):
        return f"<Materiel (id={self.id}, nom={self.nom}, description={self.description}, , fournisseur={self.fournisseur})>"