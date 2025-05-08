from utils import extract_text_from_html 

loaded_text = extract_text_from_html('output.html', withTags=True)
print(loaded_text)

from lxml import html
from lxml import etree

doc = html.fromstring(loaded_text)
count = len(doc.xpath('//span'))
print(f"There are {count} <span> elements")

# Find all data-error attributes using XPath
data_errors = doc.xpath('//span[@data-error]/@data-error')

# Get distinct values
distinct_errors = set(data_errors)

print("Distinct data-error types:", distinct_errors)
print("Count of distinct data-error types:", len(distinct_errors))


# Parse as XML
tree = etree.fromstring("<xml>" + loaded_text + "</xml>")

# Use XPath to extract all data-error attribute values
data_errors = tree.xpath('//span[@data-error]/@data-error')

# Count distinct values
distinct_errors = set(data_errors)

print("Distinct data-error types:", distinct_errors)
print("Count of distinct data-error types:", len(distinct_errors))