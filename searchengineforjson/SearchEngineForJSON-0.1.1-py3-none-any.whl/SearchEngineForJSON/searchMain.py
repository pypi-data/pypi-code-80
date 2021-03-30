

""" SearchEngine for JSON
	
	Todo:
		* Practice
"""

class Search(object):
	""" SearchEngine for json

		Json形式のデータを検索するためのモジュール(小技)

		Attributes:
			None
	"""
	
	@classmethod
	def moldSearch(cls, documents, mold, name=None):
		""" SearchEngine for json by mold
			
			json形式のデータを型を基にvalueで検索
			指定の型のデータを取得可能

			Args:
				documents(dict(json)): 探索したいjson形式のデータ
				mold(型オブジェクト): 検索したい値の型を指定
				name(string): 呼び出し時不要, 指定必要なし

			returns:
				list: 値までの絶対パス(仮称)と値
		"""
		
		def nameSurgery(targetItems):
			answears = []
			for targetItem in targetItems:
				answears.append([name+"."+targetItem[0], targetItem[1]])
			return answears

		# 対象データの下位層に存在する対象のデータ型の取得(keyとvalueを取得(配列として取得[key, value]))
		targetMoldItems = [[key, value] for key, value in documents.items() if type(value) is mold]
		
		targetMoldAnswears = nameSurgery(targetMoldItems) if name else targetMoldItems

        	# 対象データの下位層に存在するjson型のデータの取得(keyとvalueを取得(配列として取得[key, value]))
		targetJsonItems = [[key, value] for key, value in documents.items() if isinstance(value, dict)]

		targetJsonAnswears = nameSurgery(targetJsonItems) if name else targetJsonItems

		if not targetJsonAnswears:
			return targetMoldAnswears
		else:
			for targetJsonAnswear in targetJsonAnswears:
				targetMoldAnswears.extend(cls.moldSearch(documents=targetJsonAnswear[1], mold=mold, name=targetJsonAnswear[0]))
			return targetMoldAnswears

	@staticmethod
	def test(string: str):
		print(string)





