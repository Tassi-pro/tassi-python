"""Fonctions utilitaires"""
from .tassi_object import TassiObject


def array_to_tassi_object(data, options):
    """Convertit un tableau en objet Tassi"""
    if isinstance(data, list):
        return [_convert_to_tassi_object(item, options) for item in data]

    return _convert_to_tassi_object(data, options)


def _convert_to_tassi_object(data, options):
    """Convertit en objet Tassi"""
    if isinstance(data, dict):
        obj = TassiObject()
        obj.refresh_from(data, options)

        # Convertir récursivement les sous-objets
        for key, value in data.items():
            if isinstance(value, dict):
                setattr(obj, key, _convert_to_tassi_object(value, options))
            elif isinstance(value, list):
                setattr(obj, key, [
                    _convert_to_tassi_object(item, options) if isinstance(item, dict) else item
                    for item in value
                ])
            else:
                setattr(obj, key, value)

        return obj
    else:
        return data