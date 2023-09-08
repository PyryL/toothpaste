
# This script removes any existing database named "toothpaste"
# and initializes new one with correct schema

dropdb --if-exists toothpaste
createdb toothpaste
psql -d toothpaste -f docs/schema.sql
