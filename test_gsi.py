from db import dynamodb

table = dynamodb.Table("shopsphere")

print(table.global_secondary_indexes)