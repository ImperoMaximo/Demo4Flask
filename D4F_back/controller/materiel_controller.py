from flask_restful import Resource
from flask import request
from flask import jsonify
from D4F_back.service.init_service import *

class materielAPI(Resource):

    def post(self):
        data = request.get_json()
        new_materiel_object = materiel_service.createMateriel(
            nom=data.get("nom"),
            description=data.get("description"),
            fournisseur=data.get("fournisseur")
        )

        if new_materiel_object["is_new"]:
            return {"message": "nouveau materiel créer", "error": 0, "new": 1}
        else:
            return {"message": "materiel existe déjà", "error": 0, "new": 0}

    # update
    def put(self, materiel_id):

        data = request.get_json()

        nom = data.get("nom")
        description = data.get("description")
        fournisseur = data.get("fournisseur")

        materiel_service.update_materiel(
            materiel_id=materiel_id,
            nom=nom,
            description=description,
            fournisseur=fournisseur
        )

        return {"message": "update materiel ok"}

    def delete(self, materiel_id):
        return materiel_service.delete(materiel_id)

    def get(self, materiel_id):
        materiel = materiel_service.get_materiel_by_id(materiel_id)
        return {"nom": materiel.nom, "id": materiel.id}


class AllMaterielAPI(Resource):
    def get(self):
        materiels = materiel_service.get_all()
        return [{"nom": materiel.nom, "id": materiel.id} for materiel in materiels]