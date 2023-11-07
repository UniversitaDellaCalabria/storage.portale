from django.conf import settings

#PAGES TOPICS
CMS_STORAGE_CDS_WEBSITES_PAGE_TOPICS = getattr(settings, "CMS_STORAGE_CDS_WEBSITES_PAGE_TOPICS",
    {
        'iscriversi': [1,2,3,4,5],
        'studiare': [7,8,9],
        'opportunità': [15,16,17,18],
        'organizzazione': [26],
    })