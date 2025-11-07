from esprit import Esprit

# Test 1: Incorrect ID
print("=" * 50)
print("Test 1: Testing with incorrect ID")
print("=" * 50)
esprit = Esprit()
result = esprit.login('WRONG_ID', 'PASSWORD')
if not result:
    print("Login failed as expected with incorrect ID\n")

# Test 2: Correct ID but incorrect password
print("=" * 50)
print("Test 2: Testing with correct ID but incorrect password")
print("=" * 50)
# Replace 'CORRECT_ID' with your actual ID for testing
esprit2 = Esprit()
result2 = esprit2.login('CORRECT_ID', 'WRONG_PASSWORD')
if not result2:
    print("Login failed as expected with incorrect password\n")

# Test 3: Correct credentials
print("=" * 50)
print("Test 3: Testing with correct credentials")
print("=" * 50)
# Replace with your actual credentials
esprit3 = Esprit()
result3 = esprit3.login('YOUR_ID', 'YOUR_PASSWORD')
if result3:
    print("Login successful!\n")
else:
    print("Login failed\n")

