from flask import current_app
from D4F_back.service.materiel_service import MaterielService
from D4F_back.service.commande_service import CommandeService

materiel_service = MaterielService(current_app)
commande_service = CommandeService(current_app)