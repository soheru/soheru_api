import os
from bing_image_downloader import downloader

def image_bing(query, images:int):
    
    downloader.download(
        query,
        limit=images,
        output_dir="/var/www/API/main/static/store",
        adult_filter_off=False,
        force_replace=False,
        timeout=180,
    )
    kes = []
    for x in os.listdir('/var/www/API/main/static/store/'+query):
        kes.append(f'api.soheru.in/images/static/store/{query}/{x}')
    return kes
