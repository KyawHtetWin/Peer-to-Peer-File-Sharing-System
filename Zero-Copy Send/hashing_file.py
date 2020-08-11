
'''
Detecting changes in a file:

If you had a file has before it was modified, you can rehash the file
and compare it against the original hash to see if it has been modified.

'''
import hashlib
# Shows hashing algorithms found in the module
print(hashlib.algorithms_guaranteed)

# Construct a hash object using one of the hashing algorithm
#h = hashlib.sha256()

# Update the hash using a bytes object
#h.update('Hello World!'.encode('utf-8'))

'''
# Print the hash value as a hex string
print(h.hexdigest())

print(h.digest())
'''

filename = "hello_world.py"
BLOCK_SIZE = 65536 # The size of each read from the file

file_hash = hashlib.sha3_256()

with open(filename, 'rb') as f:
	while True:
		data = f.read(BLOCK_SIZE)

		if not data:
			break
		# Update the hash if there is data
		file_hash.update(data) 

# Get hexadecimal digest of hash
print(file_hash.hexdigest())








