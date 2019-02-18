import wget
from zipfile import ZipFile


'''
data downloader...etc, etc, etc



'''


print('Beginning file download with wget module')


#urls for 2013 and 2015 tweets
urls = ['https://canvas.northwestern.edu/courses/88875/files/6315645/download?verifier=XdmSiOr2uwWs0abm4upCcqWdZDmbCc9KzqVrzZRP&wrap=1',
        'https://canvas.northwestern.edu/courses/88875/files/6315652/download?verifier=oetjl6vjvBWVWYzALCQR7M2E0CdTMtwnt5U7gcei&wrap=1']

for u in urls:
    filename = wget.download(u, './')
    zip = ZipFile(filename)
    zip.printdir()
    zip.extractall(
        '.'
    )
    print(filename, '--extract succesfull')


