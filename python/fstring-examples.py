from datetime import datetime

print("\n" + "="*50)
print("DATE/TIME FORMATTING EXAMPLES")
print("="*50 + "\n")

# Get current date/time for examples
now = datetime.now()

print("BASIC DATE COMPONENTS:")
print("-"*30)
print("Before:", now)
print(f"Abbreviated weekday: {now:%a}")  # e.g. Sun
print(f"Full weekday: {now:%A}")  # e.g. Sunday
print(f"Weekday as number (0=Sunday): {now:%w}")  # e.g. 0
print(f"Day of month (zero-padded): {now:%d}")  # e.g. 08
print(f"Day of month (no padding): {now:%-d}")  # e.g. 8
print(f"Abbreviated month: {now:%b}")  # e.g. Sep
print(f"Full month: {now:%B}")  # e.g. September
print(f"Month number (zero-padded): {now:%m}")  # e.g. 09
print(f"Month number (no padding): {now:%-m}")  # e.g. 9
print(f"Year without century: {now:%y}")  # e.g. 13
print(f"Year with century: {now:%Y}")  # e.g. 2013
print("After:", now)

print("\nTIME COMPONENTS:")
print("-"*30)
print("Before:", now)
print(f"Hour 24h (zero-padded): {now:%H}")  # e.g. 07
print(f"Hour 24h (no padding): {now:%-H}")  # e.g. 7
print(f"Hour 12h (zero-padded): {now:%I}")  # e.g. 07
print(f"Hour 12h (no padding): {now:%-I}")  # e.g. 7
print(f"AM/PM: {now:%p}")  # e.g. AM
print(f"Minute (zero-padded): {now:%M}")  # e.g. 06
print(f"Minute (no padding): {now:%-M}")  # e.g. 6
print(f"Second (zero-padded): {now:%S}")  # e.g. 05
print(f"Second (no padding): {now:%-S}")  # e.g. 5
print(f"Microsecond: {now:%f}")  # e.g. 000000
print("After:", now)

print("\nTIME ZONE INFORMATION:")
print("-"*30)
print("Before:", now)
print(f"UTC offset: {now:%z}")  # e.g. +0000
print(f"Time zone name: {now:%Z}")  # e.g. UTC
print("After:", now)

print("\nDAY/WEEK OF YEAR:")
print("-"*30)
print("Before:", now)
print(f"Day of year (zero-padded): {now:%j}")  # e.g. 251
print(f"Day of year (no padding): {now:%-j}")  # e.g. 251
print(f"Week number (Sunday start, zero-padded): {now:%U}")  # e.g. 36
print(f"Week number (Sunday start, no padding): {now:%-U}")  # e.g. 36
print(f"Week number (Monday start, zero-padded): {now:%W}")  # e.g. 35
print(f"Week number (Monday start, no padding): {now:%-W}")  # e.g. 35
print("After:", now)

print("\nCOMBINED FORMATS:")
print("-"*30)
print("Before:", now)
print(f"Locale date and time: {now:%c}")  # e.g. Sun Sep 8 07:06:05 2013
print(f"Locale date: {now:%x}")  # e.g. 09/08/13
print(f"Locale time: {now:%X}")  # e.g. 07:06:05
print("After:", now)

print("\nLITERAL PERCENT SIGN:")
print("-"*30)
print("Before:", now)
print(f"Literal percent sign: {now:%%}")  # e.g. %
print("After:", now)

print("\nCOMBINED EXAMPLES:")
print("-"*30)
print("Before:", now)
print(f"Today is {now:%A}, {now:%B} {now:%-d}, {now:%Y}")  # e.g. Today is Sunday, September 8, 2013
print(f"The time is {now:%I:%M %p}")  # e.g. The time is 07:06 AM
print("After:", now)

print("\nSTRING FORMATTING:")
print("-"*30)
# Padding and alignment
name = "Alice"
print("Before:", name)
print(f"{name:>10}")  # Right align with width 10
print(f"{name:<10}")  # Left align with width 10
print(f"{name:^10}")  # Center align with width 10
print(f"{name:_<10}")  # Left align with underscore padding
print("After:", name)

print("\nNUMBER FORMATTING:")
print("-"*30)
number = 42
pi = 3.14159
print("Before:", number, pi)
print(f"{number:04d}")  # Pad with zeros
print(f"{number:+d}")   # Show sign
print(f"{number: d}")   # Space for positive numbers
print(f"{pi:.2f}")      # 2 decimal places
print(f"{pi:06.2f}")    # Pad with zeros, 2 decimal places
print("After:", number, pi)

print("\nSTRING TRUNCATION:")
print("-"*30)
long_string = "supercalifragilisticexpialidocious"
print("Before:", long_string)
print(f"{long_string:.10}")  # Truncate to 10 chars
print(f"{long_string:>15.10}")  # Right align, truncate to 10 chars
print("After:", long_string)

print("\nNUMBER SYSTEMS:")
print("-"*30)
value = 42
print("Before:", value)
print(f"{value:b}")  # Binary
print(f"{value:o}")  # Octal
print(f"{value:x}")  # Hex lowercase
print(f"{value:X}")  # Hex uppercase
print("After:", value)

print("\nPERCENTAGE AND SCIENTIFIC NOTATION:")
print("-"*30)
percentage = 0.856
big_number = 1234567.89
print("Before:", percentage, big_number)
print(f"{percentage:.1%}")  # Show as percentage with 1 decimal
print(f"{big_number:e}")  # Scientific notation
print(f"{big_number:.2e}")  # Scientific notation with 2 decimals
print("After:", percentage, big_number)

print("\nVARIABLE FORMAT SPECS:")
print("-"*30)
width = 10
precision = 2
value = 12.3456
print("Before:", value)
print(f"{value:{width}.{precision}f}")
print("After:", value)

print("\nDICTIONARY VALUES:")
print("-"*30)
person = {"name": "Alice", "age": 30}
print("Before:", person)
print(f"{person['name']} is {person['age']} years old")
print("After:", person)

print("\nOBJECT ATTRIBUTES:")
print("-"*30)
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __str__(self):
        return f"Point({self.x}, {self.y})"

point = Point(3, 4)
print("Before:", point)
print(f"{point}")  # Uses __str__
print(f"{point!r}")  # Uses __repr__
print("After:", point)

print("\n" + "="*50)
print("END OF EXAMPLES")
print("="*50 + "\n")
