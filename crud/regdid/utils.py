import re, fitz

RE_PAGE_NUMBER = re.compile(r"^\d+$")
RE_SECTION_TITLE_I = re.compile(r"\s*TITOLO\s+[I]\s(\-|\–)+")
RE_SECTION_TITLE = re.compile(r"\s*TITOLO\s+[I|V|X]+\s(\-|\–)+.*")
RE_ARTICLE_TITLE = re.compile(r"^(Art(\.){0,1})\s*\d.*")
RE_MISSING_ARTICLE = re.compile(r"Articolo non applicabile", re.IGNORECASE)

def extractArticlesFromPdf(file, firstPage, lastPage):
    fileStream = file.read()
    doc = fitz.Document(stream=fileStream, filetype="pdf")
    articles_list = []
    
    # function local
    f_current_content = ''
    f_current_num = 1
    f_first_title_occurrences_count = 0
        
    def save_article():        
        nonlocal f_current_content
        nonlocal f_current_num
        
        f_current_content = re.sub(r"\n", "", f_current_content)
        f_current_content = re.sub(r"\s(\s)+", " ", f_current_content)
        
        if RE_MISSING_ARTICLE.match(f_current_content):
            f_current_content = None
        
        articles_list.append({"numero": f_current_num,
                              "testo_it": f_current_content})
        f_current_content = ''
    
    def handle_text(lines):
        nonlocal f_current_content
        nonlocal f_current_num
        
        for line in lines:
            _line = line.strip()
            if RE_PAGE_NUMBER.match(_line): continue #skip pagenumber
            if RE_SECTION_TITLE.match(_line) or RE_ARTICLE_TITLE.match(_line):
                if f_current_content:
                    save_article()
                    f_current_num += 1
            else:
                f_current_content += _line
                
    for page in doc.pages(start=int(firstPage)-1, stop=int(lastPage)):
        lines = page.get_text().split('\n')
        handle_text(lines)
        # save last article
    save_article()
        
    return articles_list
    