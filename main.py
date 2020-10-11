import json
from requests.auth import HTTPBasicAuth
import requests
from io import BytesIO
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib import pagesizes
from reportlab.lib import colors
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.units import cm
import os
import base64
import shutil

logo = 'iVBORw0KGgoAAAANSUhEUgAAAGEAAAAxCAYAAADKiMdUAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsQAAA7EAZUrDhsAAA7USURBVHhe7Zp3XFRJtsd/TU6KggQRRMERCQKCjogC4hieY85pnTXg6jiuO6M+ndkx7KzrOMYxOwoCCgqOGJ+JBUEFF0VMgGDGSJKkNNDE2nMv5QCK0rZ+nv1Hfz+f++mqU+HeW6fq1Dl1W8IIqPikqPFfFZ8QlRKUAJUSlACVEpQAlRKUAJUSlACVEpQAlRKUAJUSlACVEpSAj6qEPUfuYPzcKLgPjUDXoQcxdVEsjpx5yEvruJycCwv3IPy68zqXNI60uBy2vmHQcwuC//40Ln07oYfuwGvCUUicdkFi7197OQbAY/Qh7Nqfzmu9nbAjd6FP9zLxDMHde4Vc2jQugw/AqGcIJn8XzSXvx0dRwm+hqZBYbMGf50ajVFqB5oa6MDbXQ+bjYowYdxTqHXciNuEZrw10czbF97O6YN7MU0i8kculjfMkqwRlmVKUlVRyyZsciXwAbRrwyfNiEH+V+pNVAUJ9KV2yalxKzoPforOQ2O1E4IFbvNWblJZVojSrFHlFFbAffohL382omaeRnJqPwudlyM8v49L344OVMGjqCXw9Jxren5ujIGU6jgUOwqxxdvj7TFdEhg1FZpof7Noboo/PPixddZG3AubOcMWwmW7wGX+US95EQpemJj2ipjrU1YXcmyxZcwkjppxEBdVBRRUcrZtj3rTO2LWuD0I298XiOW7wcGpFZdViP9O/PYNp88/w1g1RV6N7CPfT10B1FUOXgQd4SeP8FngDh47eA0x0xXbq6goOp3CKqigT5kYxNFvPZLIqllNQxkwc/dnitRfZlAUxbM5PcWzRLwmsnUsAyy8sY3czihjwC9sWmMxbM1ZTU8PQfD3zD7vJJQ2RvpQxPaddDJZb2ZbgG1xaR8D+dAbzzQyOAUzd3p+dTXjGS94k7VY+a9U1mKHTTrG/H1Zf5CV1BIWnMVhtY3ALYnDwZ2i/nf3l+7O8tCE3bj5nMN7A4BLI4BQg1h885TgvfT8UXgmx8U8QtvUaZDlzUFJSgSX/iENuqh+Wz+8Ox44t4d7ZBL8s8kDG9enwWxgLM5otl5OnYvbsSGRll4h9SCQSLPyxBxavSRTz70Mx3dNv8XnAVA/qpMvs+Enw8bDgpW9ib2eE7IuTYW6oDbTQxspNV3H3QSN2n6aKPq2I8f3bi+mdITcR9Np+Iryvi7BKzA1g00oHvRxppVXV8NL3R2ElDPkmCra9LRFw7B4s+4TDtENLzF99EQvXJeJMUjZOJ2RS+pIoc+5iBpcvwpGUng/YtMT0H8/xXoCvJzki53YBMrOlXCIfK7ZcrX3xQhkOb/oCrYzIJDSBYC7i9g0FXpQDehqY+68EXtKQkuIK+C/3gruDMWCgiWn/G4v02/TsHPeBv5OmNMV73zw6ipRCe9AHoJASUu8UoCQ5B2mnx+Ha5WwkRQzDrLH2mEsD+s14e4STPR7vY4n5U5yxcLoL3DsaY9XSniijlzu3+0ucOnwHJaW1G227Ns0gaW2Ak2efiHl5CTtxnwZSEzak/CF9adbKSQebFujXx5o0IkH0pUxUVdJe8Tq0smQkTzo+htKkaEMdOI88LBZN+jYat5/ShCkow4mQwdDR10JZ+SdQwrF/Z8CutzW0NNRQQQ/p0MEIbcz0YU0DKlyPnxZj2drLMDPWFa+fNyehLclvk9vn3bU1oKWOqyl1XpGTvTEuXs/huaZ5llOCx7mlohc0yMeKS+Vn1thOtBoqUFVWhYvJz7m0IeUVNPi0T6fQTAeZzyoyUWZeodh38oGopAWzu+BLQZkfAYWUkEgumXFzLVwg9zL1Wi7+Q35/7OUs7Dt+D09yS+AfnoZCWvLrKQ7YTzKdZlq4RnUePpNi9+/kIhpoYenmqwigejvIva0gz6WSXEl5KaL4AZU0SOXV6OVmzqXy4yqYGWGGk80vfofrK+Bk3wr+G/oApPRcweyQMtxcTLBmaS9e48NRSAkyGgQ1WqIFtCTX/uyNJbQPzCDXr42FAWaRr+43zh6DBtpARjPm1sMX5EfnoV8vSwSTmXKmWf/o3ETs//ULBFNwNXqgLUrJtdQl2ysv9b+Kq0nqZeSkupra8GbkGzSJH5nZP9MlrAh9Wv1Xjo7mJR8HhZSg3UwT7XU1MMTXGn16tMGkwbbIeVkOH5qVVqSIjCwpvNzNoclqkEWmo4AUsYsG3NxED13IaxJMkymlHW1bwpjM1TMK6ny6kZmSE6Pm5OFo0aOTWYu//u5grzFiLmaJbQVz04JWqTwEr+8DTxdTxFHs87FRSAk9KOKNrhfpjhpgC2lqLm49KEIlzbJKMi8tyFtxdTAhm90WWzf2hZ2NIZLIJCVcycb1m3lYH3AD7awMEEmubk2BDP29LXlvTWNB+087U31AVx3HYh5zqfyEHL4N0OBrU1Dm4WrGpU1z4dQYcRJ9bBRSwoDebZF16SnPkfNA+4P7CDt4jTmCYf3a4dufLuDxk5dIv18kxgRx5IU8evSSfrOQeC0HJ2IeYQ/tB060EkaTGevV1xrGLZt2MeszZVRH8VgigxS//9hdLm2aq7QRXxBWAk2UYb7tuPTTopASujhQcGLeDCs2JXEJcHBTX+TR6rAiU5MeNQFJtFHPmdYZ40d8BgsKqFxoL5g52ZHsqwOupeXhevQEGNNsllLsELTGl/ciP4tmukKTXFSQaRq/4CxSbtX58W/jBTkL/aaeAFrq0MZejQ0UKCoDCilBYOMKHyxeFs9zgLVlc6zZMQBurkF4+uwlFi/qDjvPUAQduI0XpVV49rwUGwKT0c13HwJX+yKRXNSe3fdg9do+6GBtyHuRHx1tDUSQ4kH9QkcdzkMisG1PKi99k0OnH6C1115y78kLyy/FNgrGWpNZUwr48YVCoPVmNmluFM/VsuTXRAb9dcymZyh7nFUsyoLD0lhxcbmYvvPoBbP23Ud11rIfViWIsrchnh11fvvZkYD/3lQGi80MDgEMbbcxo27BbNjsSPbj+ktsyYbLbBQ9n4VnCIPVVgZ7f/GZV269wls3RDw7stzG8NkO9jRbyqVN06lfOEPHHf//Z0cC5w6NxN5NidhIm+wr/vltN8RGjUMxLfe2zoHo/D+/Y2VwMkb8NQoO/cLRsWswpNIKxESNx88LPXirxiEPFzIKqEBXpRAXNILfREcknRoLGzM9sUFBvgxHIzOwYsMVLF93GQeP30dmJkW41Jc1zfx4Cr6+n+3GWzekUjgG4fcTzhblRSbEOGWVYryjCB/8X9SVv12D/740RO4ehM/at+DSWuLIE4qkTTg+9Tmq6AV9yRMZ+IU1POUMsEopkBr5dSTyiivw/QwXjP7Slpc0TjztQ4EHb+Mi3a/wZQXUKLBqSXuGl7MJJg/7DJ5NuMEnzzzEki1XoU/mLWJLf5iS+ywPk+edwT1StDcFcat+8ORS+VH9IVgJ+CBzpOLjoJASpGQmZMInRE452cJisvMCgu2WvXaqKJwjVTdiY4V+RDtcj4IiGU9RO0rXCEcM9Xj4tBhpdwtQVl5nf4X7P6UoPSePPKVGkJZWvjqlEI88hLqZFL8UFMrwTEjTJVBdXSM+a33yqE7KnXwUvWwoF9q+Tn4jMrkQzNH78t2yOLZpe52HQXaYjZh5SkyfPv+YwXQjq6DQ+RW9Bv/Obt8p4Lk6Fq1MYK27BPIcY0eiMxhabWSFL2Ri3to7lN1IzxPT0pIK5t43nDn0D2e+E4+xVi6B7O79QrFMeJbW5BW1p/p/W3xelNXHwi2IbQtNFdPF1I/b8AjmPDSCwXY7cx95kHmMPiyWXU3KYp4Dw8W0wJyl55mhkz9zG3GQfgPY35fH8xLqs2sQW7Y+kecYK5GWM8eude/yPii0ErS11KGhUddUQ0MCTdrMBISvZW0pmHOgGOAVujoaYp3X0VGXQJ82vz/9LQqZuSVY8GMcTO2M/lifmroaUNeo7ddj1GHMnOGMm5HjELN3CJ5fnyoeGAqUk++/ebEnHpybhEO0MZfV81KEI3PhFPe33Sli3oACvCuHR+EGeUk2FFgmHRyJhAPDxTIN2sh1+XvsoX4iYx6jKMUPV8gLLEqZjrCTDxBx6r5YbmFmgN0HbomnxAJq9C562vIfQtZHwT1BIn6Ef4VwEvkqX06uaf9elliyyAMuPntF2ds+0pcUV2LlvK7QIaW26bATF06MRgstDTJdteVCK+HjewmZPkl+GWaMtRfl2RSgCWZES/goT+g318Ry8tK6jzmC/oNtoSscznEWrrqEWFKaC02M/4uu+/vNSzJRsne4lDvI49uypjfP1bJ/W39s31H7N53K4nJk/GcyJk0/hYTrpGgdUkDjr9kkCimhpqYG6vVeVKKuhvKqOtudVyDDV2M7waOXFf4yPwat3nYuRA+dRQMasKYPEs5PEF1CKfnoDd+F4jpaSUU0YFXckdsamgrLbrtxSPjAQlSU14inuS62LWBAdV8h2OgzsY+xYD65kLQiFq2+xEtqx+tdY2ZoqI2cnIZ7jPBF0YRH2cJBpfA0hRmz4OkViqzMYmjxVfu+KKSEHuRvr9527Y/NbtXaRAz1rv3CJWzAlfyT4Y4V3sikgQgNSoYOmZbXqaJNvEL4gkV4uNbGDkLAU8MHW/i6VcmVO5BihL4Tjonly7/7HH8a3vGPT5NCQNeOBmfnL73Fw8Gj/84Q5bTnYN2ynggJG4b4MxOhRV3FJWWLZYKfIGzo9WHis9c+z2Zq99W0E0ingRe4cfM5pn0ThTX/9BLzwklxGa3QZmTeHqT7wcIxAAYWih2DKKSE4QPa46/TnNHCLQg6nXdhIgVCU7mpMCL769SuLmg7HvglvAbY0LR7c95ZWRrAzIQi3Xp87mQMTbXax+pmbwRd7dr0jp99MKpvO7TpEQI91yA8J8/Jl1aagHlrPbQ00hHTcQdHYNX2q2LEm0sB1DdTnaFN9xZ62b7SG/sjav/8JfxFqLtjw2NpbX1N2NkZi2lba0OkJHyF0TNOQdLJHzMWxOAB7UNWfCV0Fv5hwV+pvWVzRB0fA0vheF0BVMGaEqDQSlDxcVEpQQlQKUEJUClBCVApQQlQKUEJUClBCVApQQlQKUEJUCnhkwP8F+Wox1kwigLdAAAAAElFTkSuQmCC'
imgdata = base64.b64decode(logo)
print('getcwd:      ', os.getcwd())
print('__file__:    ', __file__)

DateString = input("Enter Date Like 2020-09-09  ")

directory = str(os.getcwd()) + '/exported data on - ' + str(DateString)

if not os.path.exists(directory):
    os.mkdir(directory)

kuser = 'iomammemergencymande'
kpass = 'IOM@Amman_2018'

KoboUrl = 'https://kc.humanitarianresponse.info/api/v1/data/623205?format=jsonp'  #Kobo JSON Link

response = requests.get(
    KoboUrl, auth=HTTPBasicAuth(kuser, kpass))  #Get JSON Data from Kobo Link

JsonReady = str(
    response.content
)[11:
  -3]  #.replace('callback(','').replace(');','').replace('b','')  #Remove extra text to make it JSON

ListFormated = json.loads(JsonReady)  #Load JSON to LIST

linkbase = 'https://kc.humanitarianresponse.info/media/large?media_file=' + kuser + '%2Fattachments'
linkjoin = '%2F'

counter = 0

while counter < len(ListFormated):

    if DateString == ListFormated[counter]['Date'][0:10]:
        print(ListFormated[counter]['_uuid'])
        print(ListFormated[counter]['formhub/uuid'])
        bensn = str(
            ListFormated[counter]
            ['group_mh8nj39/group_za0rs72/Serial_Number_for_Beneficiary']
        )  #ben SN
        print('date ' + ListFormated[counter]['Date'][0:10])  #date
        staffname = str(ListFormated[counter]
                        ['group_mh8nj39/Name_of_IOM_Staff'])  # staff name
        benname = str(
            ListFormated[counter]
            ['group_mh8nj39/group_za0rs72/Name_of_Beneficiary_Voucher_Receipt']
        )  #ben name
        fuuid = str(ListFormated[counter]['formhub/uuid'])
        uuid = str(ListFormated[counter]['_uuid'])

        bnsig = linkbase + linkjoin + fuuid + linkjoin + uuid + linkjoin + str(
            ListFormated[counter]
            ['group_mh8nj39/group_za0rs72/Beneficiary_Signature_Voucher'])

        vpho = linkbase + linkjoin + fuuid + linkjoin + uuid + linkjoin + str(
            ListFormated[counter]['group_mh8nj39/group_za0rs72/Voucher_Photo'])

        ssig = linkbase + linkjoin + fuuid + linkjoin + uuid + linkjoin + str(
            ListFormated[counter]
            ['group_mh8nj39/group_za0rs72/Signature_of_IOM_Staff'])

        idpho = linkbase + linkjoin + fuuid + linkjoin + uuid + linkjoin + str(
            ListFormated[counter]['group_mh8nj39/group_za0rs72/ID_Photo'])

        print('Data Imported')
        # Doc Details
        fileName = directory + '/' + bensn + '.pdf'

        # 0) Create document
        pdf = canvas.Canvas(fileName, pagesize=pagesizes.A4)
        pdf.setTitle('Omar Twait')
        pdf.setAuthor('Omar Twait')
        pdf.setSubject('Omar Twait')
        pdf.setKeywords('Omar Twait')
        pdf.setFillColor(colors.black)
        # Set Font Type and Size
        pdfmetrics.registerFont(TTFont('abc', 'arial.ttf'))
        pdf.setFont('abc', 12)

        # Darw Rectangle
        def stafName(c):
            c.setFillColorRGB(0.87109375, 0.91796875,
                              0.96484375)  #choose fill colour
            c.rect(
                1.67 * cm, 27.22 * cm, 17.52 * cm, 1.01 * cm, stroke=0,
                fill=1)  #draw rectangle
            c.setFillColor(colors.black)
            c.drawString(1.8 * cm, 27.6 * cm, 'IOM staff member name:')
            c.drawString(14 * cm, 27.6 * cm,
                         ' ' + staffname)  #########################

        stafName(pdf)

        # Darw Rectangle
        def benName(c):
            c.setFillColorRGB(0.87109375, 0.91796875,
                              0.96484375)  #choose fill colour
            c.rect(
                1.67 * cm, 21.6 * cm, 17.52 * cm, 1.01 * cm, stroke=0,
                fill=1)  #draw rectangle
            c.setFillColor(colors.black)
            c.drawString(1.8 * cm, 21.9 * cm,
                         'Beneficiary name (Voucher Receipt):')
            c.drawString(14 * cm, 21.9 * cm,
                         ' ' + benname)  ######################

        benName(pdf)

        def benSuuuuuig(c):
            c.drawString(1.8 * cm, 19.5 * cm,
                         'Beneficiary Signature (Voucher)')
            c.drawString(3.6 * cm, 16 * cm, 'ID Photo')
            c.drawString(14 * cm, 16 * cm, 'Voucher Photo')
            c.drawString(3.6 * cm, 3.5 * cm, 'IOM staff signature')

        benSuuuuuig(pdf)

        def benSerial(c):
            c.setFillColorRGB(0.87109375, 0.91796875,
                              0.96484375)  #choose fill colour
            c.rect(
                1.67 * cm, 16.6 * cm, 17.52 * cm, 1.01 * cm, stroke=0,
                fill=1)  #draw rectangle
            c.setFillColor(colors.black)
            c.drawString(1.8 * cm, 16.9 * cm, 'Beneficiary serial number:')
            c.drawString(14 * cm, 16.9 * cm,
                         ' ' + bensn)  #################################

        benSerial(pdf)

        def consent(c):
            c.setFillColorRGB(0.84765625, 0.84765625,
                              0.84765625)  #choose fill colour
            c.rect(
                1.67 * cm, 23 * cm, 17.52 * cm, 3.86 * cm, stroke=0,
                fill=1)  #draw rectangle
            c.setFillColor(colors.black)
            c.drawString = [
                'Receipt Voucher I the undersigned certify that I have received three vouchers from IOM',
                'Jordan, each voucher is equal to 70 JOD and can be used for purchase of food and Nonfood',
                'Items (NFIs) from any branch of Sameh Mall inside Jordan. I understand that I can use',
                'each voucher one time  only before 10 September 2020. I understand that if the voucher',
                'gets lost or damaged, I will not get another one as a replacement of the lost one.',
                'I have received the voucher by an IOM staff member/ "Tamkeen Fields For Aid" staff member.'
            ]
            c.text = pdf.beginText(1.8 * cm, 26 * cm)
            c.text.setFont("abc", 11.5)
            c.text.setFillColor(colors.black)
            for line in c.drawString:
                c.text.textLine(line)
            pdf.drawText(c.text)

        consent(pdf)

        # Text Data For From
        title = ['Consent Form and Receipt Voucher SDC 3']
        text = pdf.beginText(150, 28.88 * cm)
        text.setFont("abc", 16)
        text.setFillColor(colors.black)
        for line in title:
            text.textLine(line)
        pdf.drawText(text)

        #Load Image From URL
        resbnsig = requests.get(bnsig, auth=HTTPBasicAuth(kuser, kpass))
        bnsigimage = Image.open(BytesIO(resbnsig.content))
        new_width = 150
        new_height = 90
        bnsigimage = bnsigimage.resize((new_width, new_height),
                                       Image.ANTIALIAS)
        pdf.drawInlineImage(bnsigimage, 13.5 * cm, 18 * cm)

        #Load Image From URL
        resvpho = requests.get(vpho, auth=HTTPBasicAuth(kuser, kpass))
        vphoimage = Image.open(BytesIO(resvpho.content))
        new_width = 150
        new_height = 150
        vphoimage = vphoimage.resize((new_width, new_height), Image.ANTIALIAS)
        pdf.drawInlineImage(vphoimage, 3 * cm, 10 * cm)

        #Load Image From URL
        resssig = requests.get(ssig, auth=HTTPBasicAuth(kuser, kpass))
        ssigimage = Image.open(BytesIO(resssig.content))
        new_width = 150
        new_height = 150
        ssigimage = ssigimage.resize((new_width, new_height), Image.ANTIALIAS)
        pdf.drawInlineImage(ssigimage, 13.5 * cm, 2 * cm)

        #Load Image From URL
        residpho = requests.get(idpho, auth=HTTPBasicAuth(kuser, kpass))
        idphoimage = Image.open(BytesIO(residpho.content))
        new_width = 150
        new_height = 150
        idphoimage = idphoimage.resize((new_width, new_height),
                                       Image.ANTIALIAS)
        pdf.drawInlineImage(idphoimage, 14 * cm, 10 * cm)

        #Load Image From URL
        #residpho = requests.get(idpho, auth=HTTPBasicAuth(kuser, kpass))
        idphoimage = Image.open(BytesIO(imgdata))
        new_width = 97
        new_height = 49
        l = idphoimage.resize((new_width, new_height), Image.ANTIALIAS)
        pdf.drawInlineImage(l, 17.5 * cm, 28.22 * cm)

        pdf.save()
        print('PDF Created')

    counter += 1

print('Task Completed Successfully')
shutil.make_archive(str(directory) + '-archive', 'zip', directory)
print('Zip File Created')
#uploade to Google Drive

#Cleaning and removing Temp files and folders

shutil.rmtree(directory)
print('Temp Folder Deleted')
#removefile = pathlib.Path(str(directory)+'-archive.zip')
#removefile.unlink()
