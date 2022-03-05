import time

print("\r\n##### CREATING MIGRATION #####\r\n")

timestamp = int(time.time())
filename = str(timestamp) + "_Migration.sql"

file = open("migrations/" + filename, "w")
file.close()

print(filename + " generated")

print("\r\n##### MIGRATION CREATED #####\r\n")