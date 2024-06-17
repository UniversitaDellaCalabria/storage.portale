import re, fitz, unicodedata
from django.utils.text import normalize_newlines

RE_PAGE_NUMBER = re.compile(r"^\d+$")
RE_BLANK_LINE = re.compile(r"^(\n+|\s+\n+)(\s|\n)+$|(^$)")
RE_SECTION_TITLE_I = re.compile(r"\s*TITOLO\s+[I]\s(\-|\–)+")
RE_SECTION_TITLE = re.compile(r"(\s*TITOLO\s+[I|V|X]+)((\s*(\-|\–)+.*)|($))")
RE_ARTICLE_TITLE = re.compile(r"^(Art(\.){0,1})\s*\d.*", re.IGNORECASE)
RE_MISSING_ARTICLE = re.compile(r"Articolo non applicabile", re.IGNORECASE)
RE_FIRST_TITLE = re.compile(r"TITOLO\s+I")
RE_FIRST_ARTICLE = re.compile(r"^(Art(\.){0,1})\s*1\.{0,1}(\s+|-|–)", re.IGNORECASE)
RE_LI = re.compile(r"^\s*((\d+\.)|([a-z-A-Z]\))|([i|v|x]+\)))\s*((\w).*|$)")

def extractArticlesFromPdf(file, first_page, last_page):
    file_stream = file.read()
    doc = fitz.Document(stream=file_stream, filetype="pdf")
    articles_list = []
    
    current_content = ''
    current_num = 1
    found_first_title = False
    found_first_article = False
    skip_lines = False
        
    def format_as_html():
        nonlocal current_content
        current_content = normalize_newlines(current_content)
        current_content = unicodedata.normalize("NFC", current_content)
        paras = re.split("\n{2,}", str(current_content))
        paras = list(filter(None, paras))
        paras = ["<p>%s</p>" % p.strip() for p in paras]
        current_content = "".join(paras)

            
    def save_article():        
        nonlocal current_content
        nonlocal current_num
        
        if RE_MISSING_ARTICLE.match(current_content):
            current_content = None
        else:
            format_as_html()
                    
        articles_list.append({"numero": current_num,
                              "testo_it": current_content})
        
        current_content = ''
    
    def handle_text(lines):
        nonlocal current_content
        nonlocal current_num
        nonlocal found_first_title
        nonlocal found_first_article
        nonlocal skip_lines

        for line in lines:
            _stripped_line = line.strip()
            if RE_PAGE_NUMBER.match(_stripped_line): continue #skip pagenumber
            if not (found_first_title and found_first_article): 
                if RE_FIRST_TITLE.match(_stripped_line):
                    found_first_title = True
                if RE_FIRST_ARTICLE.match(_stripped_line):
                    found_first_article = True
                continue
                
            if RE_SECTION_TITLE.match(_stripped_line):
                skip_lines = True
            if RE_ARTICLE_TITLE.match(_stripped_line):
                if current_content.strip():
                    save_article()
                    current_num += 1
                    skip_lines = False
            elif not skip_lines:
                if RE_LI.match(line):
                    line = '\n\n' + line
                current_content += line
                
    for page in doc.pages(start=int(first_page)-1, stop=int(last_page)):
        lines = page.get_text().split('\n')
        handle_text(lines)
    # save last article
    save_article()
            
    return articles_list
    