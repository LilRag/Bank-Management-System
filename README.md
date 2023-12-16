# GUI Based - Bank-Management-System
Develop a python program that models a banking system, including bank accounts. Users can interact with the system to create and manage their accounts, each with specific details like account number, name, Email , Phone No., Passwords.


# Implementation details
A bank management system is a complex software application that involves the storage, retrieval, and manipulation of financial data. The system typically relies on an SQL database to organize and manage this information efficiently. Below are some key implementation details for a bank management system with essential functions:

Database Schema:
Create tables to store information about customers, accounts, transactions, and login credentials. Define relationships between these tables for efficient data retrieval.
For this project MySQL was used as the DBMS. The MySQl - connector python library enabled python programs to connect and interact with MySQL databases.
User Authentication 
To Implement a secure user authentication system to ensure that only authorized users can access the system. Passwords are encrypted upon entry. Providing a ‘forgot password feature’ to help customers access their accounts in case they forgot their password. Uses their account number , email and phone number for verification.
Money Deposition/Withdrawal:
Create functions to handle the deposit and withdrawal of money from customer accounts. Ensure that the system updates account balances accurately and maintains data integrity.
Money Transfer:
   Fund Transfer:
    Implement a transfer function to facilitate the transfer of funds between different accounts. This involves deducting the amount from the sender's account and crediting it to the recipient's account.
   Transfer History:
    Maintain a transaction history table to record details of each transfer.This provides an audit trail and facilitates account reconciliation.
Update Details:
Allow customers to update their personal information, such as name, email, contact details. Implement validation checks to ensure data accuracy.  
User Registration:
Implement a user registration function to add new users to the system. Takes in user details like name, email , phone number , age , gender and a password. It assigns a unique account number to each new user.
