class cli:
	def __init__(self, id: int, nombre: str):
		self.ID = id
		self.nombre = nombre

	def __getstate__(self):
		return {'ID': self.ID, 'nombre': self.nombre}

	def __setstate__(self, state):
		self.ID = state['ID']
		self.nombre = state['nombre']