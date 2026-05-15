import pyautogui
import time

# Set a small pause between actions
pyautogui.PAUSE = 0.5

# Wait for the GUI window to be in focus
print("Testing TASMA Booking System...")
time.sleep(2)

# Test 1: Add a booking
print("\n1. Testing 'Add Booking' functionality...")

# Fill in Date (already has today's date)
# Click on Time field
pyautogui.click(555, 150)
time.sleep(0.3)
pyautogui.typewrite("14:30")

# Click on Department field
pyautogui.click(260, 181)
time.sleep(0.3)
pyautogui.typewrite("Finance")

# Click on User Name field
pyautogui.click(555, 181)
time.sleep(0.3)
pyautogui.typewrite("John Smith")

# Click on Reason field
pyautogui.click(407, 212)
time.sleep(0.3)
pyautogui.typewrite("Quarterly Budget Review")

# Click Book Room button
print("  - Clicking 'Book Room' button...")
pyautogui.click(211, 259)
time.sleep(1.5)  # Wait for success message

# Click OK on success message
pyautogui.press("enter")
time.sleep(1)

# Test 2: Refresh List
print("\n2. Testing 'Refresh List' functionality...")
pyautogui.click(347, 259)
time.sleep(1)

# Test 3: Add another booking
print("\n3. Adding another booking to test delete...")
pyautogui.click(555, 150)
time.sleep(0.3)
pyautogui.typewrite("15:00")

pyautogui.click(260, 181)
time.sleep(0.3)
pyautogui.typewrite("HR")

pyautogui.click(555, 181)
time.sleep(0.3)
pyautogui.typewrite("Jane Doe")

pyautogui.click(407, 212)
time.sleep(0.3)
pyautogui.typewrite("Team Meeting")

pyautogui.click(211, 259)
time.sleep(1.5)
pyautogui.press("enter")
time.sleep(1)

# Test 4: Delete a booking
print("\n4. Testing 'Delete Selected' functionality...")
# Click on first booking in the list
pyautogui.click(438, 420)
time.sleep(0.5)

# Click Delete Selected button
pyautogui.click(483, 259)
time.sleep(0.5)

# Click Yes on confirmation
pyautogui.press("tab")
pyautogui.press("enter")
time.sleep(1)

print("\n✓ All tests completed!")
print("Check the application window to verify all bookings are working correctly.")
