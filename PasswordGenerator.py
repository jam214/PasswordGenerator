#PasswordGenerator.py
"""
Creator: James S.
Purpose: To create a random password based on input and then search for a hash that matches the password.
"""


import random
import hashlib

# Function to get valid input for initials
def FirstInitials():
    while True:
        initials = input("Enter First Name initials (alphabet only, unique, uppercase): ").upper()
        InitialsSet = "".join(sorted(set(initials)))  # Remove duplicates and sort
        if initials.isalpha():
            print(f"Initial Characters (duplicates removed): {InitialsSet}")
            return InitialsSet
        else:
            print("Invalid input. Please enter alphabetical characters only.")

# Function to get valid input for special characters
def GetSpecialChars():
    while True:
        SpecialChars = input("Enter special characters (unique): ")
        SpecialCharsSet = "".join(sorted(set(SpecialChars)))  # Remove duplicates and sort
        if SpecialChars:
            print(f"Special Characters (duplicates removed): {SpecialCharsSet}")
            return SpecialCharsSet
        else:
            print("Invalid input. Please enter at least one special character.")

# Function to get valid year range
def YearRange():
    while True:
        try:
            StartYear = int(input("Enter the beginning 4-digit year of birth: "))
            EndYear = int(input("Enter the ending 4-digit year of birth: "))
            if 1000 <= StartYear <= 9999 and 1000 <= EndYear <= 9999 and EndYear > StartYear:
                return StartYear, EndYear
            else:
                print("Invalid input. Ensure years are 4 digits and the ending year is greater than the starting year.")
        except ValueError:
            print("Invalid input. Please enter valid 4-digit years.")

# Function to generate passwords
def CreatePasswords(initials, SpecialChars, TimeSpan, lnames):
    PWList = []
    for initial in initials:
        for lname in lnames:
            lname = lname.strip()  # Remove extra whitespace or newline
            for year in range(TimeSpan[0], TimeSpan[1] + 1):
                for char in SpecialChars:
                    PWList.append(f"{initial}{lname}{year}{char}")
    return PWList

# Main program logic
def main():
    initials = FirstInitials()
    SpecialChars = GetSpecialChars()
    TimeSpan = YearRange()

    # Read last names from the file
    try:
        with open("Lnames.txt", "r") as file:
            lnames = file.readlines()
    except FileNotFoundError:
        print("Lnames.txt file not found. Please ensure the file is in the same directory.")
        return

    # Generate passwords
    PWList = CreatePasswords(initials, SpecialChars, TimeSpan, lnames)
    print(f"Total passwords generated: {len(PWList)}")

    # Shuffle and display the last 10 passwords
    random.shuffle(PWList)
    print("Last 10 passwords from the shuffled list:")
    print("\n".join(PWList[-10:]))

    # Password cracker class
    class SanchezPWCrackerClass:
        def __init__(self, PWList):
            self.PWList = PWList

        def SearchHash(self):
            while True:
                SearchHash = input("Enter an SHA256 hash to search (or type 'exit' to quit): ").strip()
                if SearchHash.lower() == "exit":
                    break
                found = False
                for pw in self.PWList:
                    HashedPass = hashlib.sha256(pw.encode()).hexdigest()
                    if HashedPass == SearchHash:
                        print(f"Found Hash! Password: {pw}, Hash: {HashedPass}")
                        found = True
                        break
                if not found:
                    print(f"Hash Not Found: {SearchHash}")

    # Instantiate the password cracker class and search hashes
    cracker = SanchezPWCrackerClass(PWList)
    cracker.SearchHash()

if __name__ == "__main__":
    main()
