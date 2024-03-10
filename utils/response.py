STATUS_CODES = {
	200: "ok everything passed",
	201: "created successfully",
	300: "failed pass",
	301: "error there was a problem",
}


class Result:
	def __init__(self, data=None, status_code=200):
		self._data = data
		self._status_code = status_code

	def __getattr__(self, item):
		if item == 'data':
			return self._data
		elif item == 'status_code':
			return self._status_code
		elif item == 'status_message':
			return STATUS_CODES.get(self._status_code, 'Unknown')
		else:
			raise AttributeError(f"'CustomResponse' object has no attribute '{item}'")

	def to_dict(self):
		return {
			'data': self._data,
			'status_code': self._status_code,
			'status_message': STATUS_CODES.get(self._status_code, 'Unknown')
		}


# Usage
# response = Result(data={'message': 'Data processed successfully'}, status_code=201)
# print(response.data)
# print(response.status_code)
# print(response.status_message)
# print(response.to_dict())
