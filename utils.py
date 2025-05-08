def extract_text_from_html(filePath, withTags=False):
    from bs4 import BeautifulSoup
    with open(filePath, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
    # Find the <body>
    body = soup.body
    # Remove all <script> tags inside <body> and its contents
    for script_tag in body.find_all('script'):
        script_tag.decompose()
    #remove all <span> tags
    if not withTags:
        for span in body.find_all('span'):
            span.unwrap()
    # Get only the inner HTML (without <body> tags)
    inner_html = body.decode_contents()
    return inner_html