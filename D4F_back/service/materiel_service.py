from flask import current_app
from D4F_back.utils import est_un_nouvel_objet
from D4F_back.modele.materiel import Materiel
from D4F_back.db import db
import os 
import chardet
import csv

class MaterielService:
    def __init__(self, app):
        self.app = app
        self.db = db

    def createMateriel(self, nom="", description="", fournisseur=""):
        with self.app.app_context():
            # Check if the user with a specific username exists
            materiel_existant = Materiel.query.filter_by(nom=nom).first()

            if not materiel_existant:
                # User does not exist, create and add to the database

                if(description is None or description == ""): 
                    description = "pas de description"
                if(nom is None or nom == ""): 
                    nom = "pas de nom"

                nouveau_materiel= Materiel(nom = nom,
                                            description = description, 
                                            fournisseur =fournisseur)
                self.db.session.add(nouveau_materiel)
                self.db.session.commit()
                nouveau_materiel = Materiel.query.filter_by(nom=nom).first()

                return est_un_nouvel_objet(True, nouveau_materiel)
            else:
                return est_un_nouvel_objet(False, materiel_existant)
    
    def get_materiel_by_id(self, materiel_id):
        materiel =  Materiel.query.get(materiel_id)
        return materiel
    
    def get_all(self):
        return Materiel.query.all()

    def delete(self, materiel_id):
        materiel = Materiel.query.get(materiel_id)
        if not materiel:
            return {'error': 'materiel not found'}, 404
        db.session.delete(materiel)
        db.session.commit()
        return {'message': 'materiel deleted successfully'}, 200
    
    def update_materiel(self, materiel_id, nom = "", description = "", fournisseur = ""):
        materiel = Materiel.query.get(materiel_id)
        
        if (nom != "" or nom is not None):
            materiel.nom = nom
        if (description != "" or description is not None):
            materiel.description = description
        if (description != "" or description is not None):
            materiel.description = description
        if (fournisseur != "" or fournisseur is not None):
            materiel.fournisseur = fournisseur

        db.session.commit()

        return {'message': 'materiel updated successfully'}, 200
    
    def import_materiels_from_csv(self, file_path="D4F_back/materiels.csv"):
        with self.app.app_context():
        
            if os.path.isfile(os.path.join(self.app.root_path, file_path)):
                with open(os.path.join(self.app.root_path,file_path), 'rb') as file:
                    result = chardet.detect(file.read())
                    encoding = result['encoding']
                
                with open(os.path.join(self.app.root_path,file_path), 'r', encoding=encoding) as file:

                    csvFile = csv.reader(file,  delimiter=';',)

                    # ne prends pas en compte el header du csv
                    next(csvFile, None)

                    for line in csvFile:
                        lineSplit = line

                        # espere exacte format du csv: nom;description;fournisseur
                        self.createMateriel(nom = lineSplit[0],
                                            description = lineSplit[1],
                                            fournisseur = lineSplit[2])
                print("Import materiels terminé.")
            else:
                print("Fichier materiel non trouvé.")
