CREATE DATABASE personal_finance;
CREATE USER finance_user WITH ENCRYPTED PASSWORD 'yourpassword';
GRANT ALL PRIVILEGES ON DATABASE personal_finance TO finance_user;
