from D4F_back.modele.commande import Commande
from D4F_back.modele.materiel import Materiel   #au cas ou pour une suite ?
from D4F_back.db import db
from sqlalchemy import or_, and_

class CommandeService:

    def __init__(self, app):
        self.app = app
        self.db = db

    def create_commande(self, materiel, nombre_piece_commande, date_emission, commentaire_emission):

        with self.app.app_context():

            materiel = db.session.merge(materiel)
            new_commande = Commande(materiel_id=materiel.id,
                    materiel=materiel,
                    nombrePiece=nombre_piece_commande,
                    date_emission=date_emission,
                    commentaire_emission=commentaire_emission)

            db.session.add(new_commande)
            db.session.commit()
            # Return the new record's id to avoid DetachedInstance issues
            return new_commande.id

    def getById(self, commande_id):
        commande = Commande.query.get(commande_id)
        return commande

    def get_commande_by_id(self, commande_id):
        commande =  Commande.query.get(commande_id)
        return commande
    
    def get_all(self):
        return Commande.query.all()

    def delete(self, commande_id):
        commande = Commande.query.get(commande_id)
        if not commande:
            return {'error': 'commande not found'}, 404
        db.session.delete(commande)
        db.session.commit()
        return {'message': 'commande deleted successfully'}, 200

    def update_commande(self, commande_id, materiel_id, nombre_piece, date_emission, commentaire_emission):
        with self.app.app_context():
            commande = Commande.query.get(commande_id)
            if not commande:
                return {'error': 'commande not found'}, 404
            # si nombre de piece <= 0 on supprime

            if nombre_piece is not None:
                try:
                    np = int(nombre_piece)
                except Exception:
                    np = None
                if np is not None and np <= 0:
                    db.session.delete(commande)
                    db.session.commit()
                    return {'deleted': True, 'id': commande_id}
    #mettre a jour si possible
            if materiel_id is not None:
                materiel = db.session.get(Materiel, materiel_id)
                if materiel:
                    commande.materiel = db.session.merge(materiel)
                    commande.materiel_id = materiel.id

            if nombre_piece is not None:
                commande.nombrePiece = int(nombre_piece)
            if date_emission is not None:
                commande.date_emission = date_emission
            if commentaire_emission is not None:
                commande.commentaire_emission = commentaire_emission

            db.session.commit()
            return {'id': commande.id, 'nombrePiece': commande.nombrePiece}