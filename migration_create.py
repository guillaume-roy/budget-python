import time

timestamp = int(time.time())
filename = str(timestamp) + "_Migration.sql"

file = open("migrations/" + filename, "w")
file.close()

print(filename + " generated")