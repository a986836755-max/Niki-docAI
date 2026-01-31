import re

TAG_REGEX = re.compile(
    r"^\s*(?:#+|//|<!--|>)?\s*([@!][A-Z_]+)(?:\s+(.*?))?(?:\s*(?:-->))?\s*$",
    re.MULTILINE,
)

text = """
Inner docstring for test_func.
    @INTERNAL
"""

print(f"Text:\n{repr(text)}")
matches = list(TAG_REGEX.finditer(text))
print(f"Matches: {len(matches)}")
for m in matches:
    print(f"  - {m.group(1)}")

text2 = """
# @CORE
# This is a core function.
"""
print(f"\nText2:\n{repr(text2)}")
matches2 = list(TAG_REGEX.finditer(text2))
print(f"Matches2: {len(matches2)}")
for m in matches2:
    print(f"  - {m.group(1)}")
