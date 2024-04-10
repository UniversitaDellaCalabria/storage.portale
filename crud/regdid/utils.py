import io

from reportlab.platypus import SimpleDocTemplate, Spacer, PageBreak, Paragraph, XPreformatted
from reportlab.lib.units import mm, inch
from reportlab.rl_config import canvas_basefontname as _baseFontName, defaultPageSize
from reportlab.lib.styles import StyleSheet1, ParagraphStyle, ListStyle, _baseFontNameB
from reportlab.lib.colors import black
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY


PAGE_HEIGHT = defaultPageSize[1]
PAGE_WIDTH = defaultPageSize[0]

def _create_stylesheet():
    stylesheet = StyleSheet1()
    stylesheet.add(ParagraphStyle(name='Normal',
                                  fontName=_baseFontName,
                                  fontSize=10,
                                  leading=12)
                   )

    stylesheet.add(ParagraphStyle(name='BodyText',
                                  parent=stylesheet['Normal'],
                                  spaceBefore=0)
                   )
    stylesheet.add(ParagraphStyle(name='Italic',
                                  parent=stylesheet['BodyText'],
                                  fontName = _baseFontName)
                   )

    stylesheet.add(ParagraphStyle(name='Heading1',
                                  parent=stylesheet['Normal'],
                                  fontName = _baseFontNameB,
                                  fontSize=18,
                                  leading=22,
                                  spaceAfter=0),
                   alias='h1')

    stylesheet.add(ParagraphStyle(name='Title',
                                  parent=stylesheet['Normal'],
                                  fontName = _baseFontNameB,
                                  fontSize=18,
                                  leading=22,
                                  alignment=TA_CENTER,
                                  spaceAfter=0),
                   alias='title')

    stylesheet.add(ParagraphStyle(name='Heading2',
                                  parent=stylesheet['Normal'],
                                  fontName = _baseFontNameB,
                                  fontSize=14,
                                  leading=18,
                                  spaceBefore=0,
                                  spaceAfter=0),
                   alias='h2')

    stylesheet.add(ParagraphStyle(name='Heading3',
                                  parent=stylesheet['Normal'],
                                  fontName = _baseFontNameB,
                                  fontSize=12,
                                  leading=14,
                                  spaceBefore=0,
                                  spaceAfter=0),
                   alias='h3')

    stylesheet.add(ParagraphStyle(name='Heading4',
                                  parent=stylesheet['Normal'],
                                  fontName = _baseFontNameB,
                                  fontSize=10,
                                  leading=12,
                                  spaceBefore=0,
                                  spaceAfter=0),
                   alias='h4')

    stylesheet.add(ParagraphStyle(name='Heading5',
                                  parent=stylesheet['Normal'],
                                  fontName = _baseFontNameB,
                                  fontSize=9,
                                  leading=10.8,
                                  spaceBefore=0,
                                  spaceAfter=0),
                   alias='h5')

    stylesheet.add(ParagraphStyle(name='Heading6',
                                  parent=stylesheet['Normal'],
                                  fontName = _baseFontNameB,
                                  fontSize=7,
                                  leading=8.4,
                                  spaceBefore=0,
                                  spaceAfter=0),
                   alias='h6')

    stylesheet.add(ParagraphStyle(name='Bullet',
                                  parent=stylesheet['Normal'],
                                  firstLineIndent=0,
                                  spaceBefore=0),
                   alias='bu')

    stylesheet.add(ParagraphStyle(name='Definition',
                                  parent=stylesheet['Normal'],
                                  firstLineIndent=0,
                                  leftIndent=36,
                                  bulletIndent=0,
                                  spaceBefore=0,
                                  bulletFontName=_baseFontNameB),
                   alias='df')

    stylesheet.add(ParagraphStyle(name='Code',
                                  parent=stylesheet['Normal'],
                                  fontName='Courier',
                                  fontSize=8,
                                  leading=8.8,
                                  firstLineIndent=0,
                                  leftIndent=36,
                                  hyphenationLang=''))

    stylesheet.add(ListStyle(name='UnorderedList',
                                parent=None,
                                leftIndent=18,
                                rightIndent=0,
                                bulletAlign='left',
                                bulletType='1',
                                bulletColor=black,
                                bulletFontName='Helvetica',
                                bulletFontSize=12,
                                bulletOffsetY=0,
                                bulletDedent='auto',
                                bulletDir='ltr',
                                bulletFormat=None,
                                #start='circle square blackstar sparkle disc diamond'.split(),
                                start=None,
                            ),
                   alias='ul')

    stylesheet.add(ListStyle(name='OrderedList',
                                parent=None,
                                leftIndent=18,
                                rightIndent=0,
                                bulletAlign='left',
                                bulletType='1',
                                bulletColor=black,
                                bulletFontName='Helvetica',
                                bulletFontSize=12,
                                bulletOffsetY=0,
                                bulletDedent='auto',
                                bulletDir='ltr',
                                bulletFormat=None,
                                #start='1 a A i I'.split(),
                                start=None,
                            ),
                   alias='ol')
    return stylesheet

styles = _create_stylesheet()
TITLE_SPACER_HEIGHT = 5 * mm
ART_SPACER_HEIGHT = 1 * mm
TEXT_SPACER_HEIGHT = 4 * mm

def _firstPage(canvas, doc):
    canvas.saveState()
    canvas.setFont('Times-Bold', 16)
    #canvas.drawImage(image, x, y, width=None, height=None, mask=None)
    canvas.drawCentredString(PAGE_WIDTH / 2.0, PAGE_HEIGHT - 108, "TEST")
    canvas.setFont('Times-Roman', 9)
    canvas.drawString(inch, 0.75 * inch, "1")
    canvas.restoreState()

def _otherPages(canvas, doc):
    canvas.saveState()
    canvas.setFont('Times-Roman', 9)
    canvas.drawString(inch, 0.75 * inch, f"{doc.page}")
    canvas.restoreState()
    
def _addParagraph(story, text, spacer_height, style=styles["Normal"]):
    story.append(Paragraph(text, style))
    story.append(Spacer(1, spacer_height))
    
def _addXPreformatted(story, text, spacer_height, style=styles["Normal"]):
    story.append(XPreformatted(text, style=style))
    story.append(Spacer(1, spacer_height))

def generate_regulament_pdf_file(titoli_struttura_articoli_dict):
    buffer = io.BytesIO()
    
    doc = SimpleDocTemplate(buffer)
    story = [PageBreak()]
    

    for title, struct_art_list in titoli_struttura_articoli_dict.items():
        story.append(Spacer(1, TITLE_SPACER_HEIGHT))
        _addParagraph(story, title.descr_titolo_it, ART_SPACER_HEIGHT, styles["Heading4"])
        for struct_art in struct_art_list:
            for struct, art_sub_arts in struct_art.items():
                _addParagraph(story, f"Art {struct.numero} - {struct.titolo_it}", ART_SPACER_HEIGHT, styles["Heading4"])
                for article, sub_articles in art_sub_arts.items():
                    _addXPreformatted(story, article.testo_it if article else "omissis", TEXT_SPACER_HEIGHT)
                    for sub_art in sub_articles:
                        _addParagraph(story, f"Art {struct.numero}.{sub_art.ordine} - {struct.titolo_it}", ART_SPACER_HEIGHT, styles["Heading4"])        
                        _addXPreformatted(story, sub_art.testo_it, TEXT_SPACER_HEIGHT)   
    
    
    doc.build(story, onFirstPage=_firstPage, onLaterPages=_otherPages)
    
    buffer.seek(0)
    
    return buffer