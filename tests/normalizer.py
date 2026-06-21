from scripts.normalizer import normalize_year, normalize_ticker

print(normalize_year("Mar 2024"))
print(normalize_year("Dec 2012"))
print(normalize_year("TTM"))

print(normalize_ticker("abb"))
print(normalize_ticker(" adaniensol "))