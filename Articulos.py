class art:
	def __init__(self,
				id: int,
				descripcion: str,
				conteo: str,
				precio_unitario: int):
		self.ID = id
		self.descripcion = descripcion
		self.conteo = conteo
		self.precio_unitario = precio_unitario

	def __getstate__(self):
		return {'ID': self.ID,
				'descripcion': self.descripcion,
				'conteo': self.conteo,
				'precio_unitario': self.precio_unitario}

	def __setstate__(self, state):
		self.ID = state['ID']
		self.descripcion = state['descripcion']
		self.conteo = state['conteo']
		self.precio_unitario = state['precio_unitario']