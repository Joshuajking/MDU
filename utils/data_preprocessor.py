import csv
import os
import sys
from typing import Any

import pandas as pd


class DataPreprocessor:
	"""
	"""
	allowed_extensions = ['csv', 'xlsx', 'json', 'tsv', 'ods', 'txt']
	allowed_headers = ['username', 'password', 'email']

	def __init__(self, file_path: str, extension: str = None):
		# self.allowed_headers = allowed_headers
		self.file_path = file_path
		self.extension = extension
		self.df = self.preprocess()

	def _validate_file_path(self):
		"""
		Validate if the file path is valid and exists.
		"""
		if not isinstance(self.file_path, str):
			return False, "File path must be a string."

		if not os.path.exists(self.file_path):
			return False, "File does not exist."

		if not os.path.isfile(self.file_path):
			return False, "Path does not point to a file."

		return True, "File path is valid."

	def _validate_csv_headers(self, df):
		"""
		Validate if the headers of the CSV DataFrame match the allowed headers.
		"""
		print(df.columns)
		print(df.head())
		df.columns = df.columns.str.lower()
		print(df)

		if df.columns != self.allowed_headers:
			raise ValueError(f"CSV headers {df.columns} do not match allowed headers {self.allowed_headers}.")
		print("CSV headers are valid.")
		return df

	def _process_csv(self, *args, **kwargs):
		# NotImplemented
		pass

	def _process_json(self, *args, **kwargs):
		pass

	def _process_xlsx(self, *args, **kwargs):
		pass

	def _process_tsv(self, *args, **kwargs):
		pass

	def _process_ods(self, *args, **kwargs):
		pass

	def _process_txt(self, *args, **kwargs):
		pass

	def _process_data(self, *args, **kwargs):
		pass

	def _read_file_to_dataframe(self, *args, **kwargs):
		"""
		Read a file into a DataFrame based on its extension.
		"""
		if self.extension == 'csv':
			return pd.read_csv(self.file_path)
		elif self.extension == 'xlsx':
			return pd.read_excel(self.file_path)
		elif self.extension == 'json':
			return pd.read_json(self.file_path)
		elif self.extension == 'tsv':
			return pd.read_csv(self.file_path, sep='\t')
		elif self.extension == 'ods':
			return pd.read_excel(self.file_path)
		elif self.extension == 'txt':
			return pd.read_csv(self.file_path, sep='\t')
		else:
			raise ValueError(f"Extension {self.extension} is not supported.")

	def preprocess(self):
		"""
		Preprocess the incoming data and return it as a pandas DataFrame
		:param file_path:
		:param allowed_headers:
		:return: Dataframe object
		"""
		if not self._validate_file_path():
			raise FileNotFoundError("File does not exist.")

		self.extension = self.file_path.split(".")[-1]
		if self.extension not in self.allowed_extensions:
			raise ValueError(f"Extension {self.extension} is not supported.")
		try:
			# Read file into DataFrame
			df = self._read_file_to_dataframe()
			df.columns = df.columns.str.lower()

			# Process the DataFrame as needed
			print(df.head())  # Example: printing the first few rows of the DataFrame
		except Exception as e:
			print(f"Error preprocessing file: {e}")

		# TODO: implement for the process_csv, process_xlsx methods, maybe use for writing a file and not reading.
		# method_name = f"_process_{ext}"
		# if hasattr(self, method_name):
		# 	processing_method = getattr(self, method_name)
		# 	return processing_method(df)
		# raise NotImplementedError(f"Processing method for extension {ext} is not implemented.")
		# if not set(df.columns.str.lower()).issubset(set(header.lower() for header in self.allowed_headers)):
			# All DataFrame columns are present in the allowed headers
			print("Some DataFrame columns are not allowed.")
			raise ValueError(f"Some DataFrame columns are not allowed.")
		print("All DataFrame columns are allowed.")
		return df.to_dict()











