from flask import jsonify
from flask_restful import Resource
from flask import request
from D4F_back.service.init_service import *
import os

from datetime import datetime


class commandeAPI(Resource):
    #nouvelle commande = creer
    def post(self):
        data = request.get_json()

        materiel_id = data.get("materiel_id")
        if not materiel_id:
            return {"error": "materiel_id is required"}, 400

        materiel = materiel_service.get_materiel_by_id(materiel_id)
        if not materiel:
            return {"error": "materiel not found"}, 404

        try:
            nombre_piece = int(data.get("nombre_piece", 1))
        except Exception:
            return {"error": "nombre_piece must be an integer"}, 400

        date_emission = data.get("date_emission")
        commentaire = data.get("commentaire_emission")

        new_commande_id = commande_service.create_commande(
            materiel=materiel,
            nombre_piece_commande=nombre_piece,
            date_emission=date_emission,
            commentaire_emission=commentaire,
        )
        if not new_commande_id:
            return {"error": "failed to create commande"}, 500
        return {"message": "commande created", "id": new_commande_id}, 201

    # lire une commande
    def get(self, commande_id):
        commande = commande_service.get_commande_by_id(commande_id)
        if not commande:
            return {"error": "commande not found"}, 404
        return {
            "id": commande.id,
            "materiel_id": commande.materiel_id,
            "materiel_nom": getattr(commande.materiel, "nom", None),
            "nombrePiece": commande.nombrePiece,
            "date_emission": str(commande.date_emission),
            "commentaire_emission": commande.commentaire_emission,
        }
    # modifier/update une commande
    def put(self, commande_id):
        data = request.get_json()

        materiel_id = data.get("materiel_id")
        nombre_piece = int(data.get("nombre_piece"))
        date_emission = data.get("date_emission")
        commentaire = data.get("commentaire_emission")
        #materiel = materiel_service.get_materiel_by_id(materiel_id)

        updated = commande_service.update_commande(
            commande_id,
            materiel_id=materiel_id,
            nombre_piece=nombre_piece,
            date_emission=date_emission,
            commentaire_emission=commentaire,
        )

        if isinstance(updated, tuple) and updated[1] == 404:
            return updated

        if isinstance(updated, dict) and updated.get('deleted'):
            return {"message": "commande deleted", "id": updated.get('id')}, 200

        if isinstance(updated, dict):
            return {"message": "commande updated", "id": updated.get('id'), "nombrePiece": updated.get('nombrePiece')}, 200

        return {"message": "commande updated"}, 200

    def delete(self, commande_id):
        # suppr a commande
        result = commande_service.delete(commande_id)
        return result
        
class AllCommandeAPI(Resource):
    def get(self):
        commandes = commande_service.get_all()
        return [{"id": commande.id,
                 "nom materiel": commande.materiel.nom,
                 "nombre piece": commande.nombrePiece,
                 "commentaire": commande.commentaire_emission
                 } for commande in commandes]