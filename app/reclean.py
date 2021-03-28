
def reclean(text):
    texti = text.encode('ascii', 'ignore').decode()
    return texti