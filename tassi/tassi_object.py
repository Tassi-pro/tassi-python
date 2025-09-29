"""Classe de base pour tous les objets Tassi"""


class TassiObject:
    def __init__(self, id=None):
        if id:
            self.id = id

    def refresh_from(self, values, options):
        """Rafraîchit l'objet avec les valeurs"""
        for key, value in values.items():
            setattr(self, key, value)

    def serialize_parameters(self):
        """Sérialise les paramètres"""
        params = {}

        for key, value in self.__dict__.items():
            if key != 'id' and not callable(value):
                params[key] = value

        return params

    def __repr__(self):
        id_str = f" id={self.id}" if hasattr(self, 'id') else ""
        return f"<{self.__class__.__name__}{id_str}>"