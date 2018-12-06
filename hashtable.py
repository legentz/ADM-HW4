class HashTable:
	def __init__(self, size=10000):
		self.size = size
		self.data = [[] for _ in range(self.size)]

	def __setitem__(self, key, value):
		hash_k = self.__hash(key)
		bucket = self.data[hash_k]
		key_exists = False

		for i, kv in enumerate(bucket):
			k, v = kv
			if key == k:
				key_exists = True
				break

		if key_exists:
			bucket[i] = ((key, value))
		else:
			bucket.append((key,value))

	def __getitem__(self, key):
		hash_k = self.__hash(key)
		bucket = self.data[hash_k]

		for i, kv in enumerate(bucket):
			k, v = kv
			return v
		raise KeyError

	def __hash(self, key):
		return sum([ord(k) for k in key]) % self.size