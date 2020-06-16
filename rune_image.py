from PIL import Image
import re
import sys
regex = re.compile('[^a-zA-Z]')
import requests as r
runesReforged = r.get('http://ddragon.leagueoflegends.com/cdn/10.11.1/data/en_US/runesReforged.json').json()
complete_runes = {}
for rune in runesReforged:
    for sub_rune in rune['slots']:
        for sub_sub_rune in sub_rune['runes']:
            complete_runes[sub_sub_rune['key']] = sub_sub_rune['icon']
primary_images = {'Domination':'perk-images/Styles/7200_Domination.png',
                 'Inspiration':'perk-images/Styles/7203_Whimsy.png',
                 'Precision':'perk-images/Styles/7201_Precision.png',
                 'Resolve':'perk-images/Styles/7204_Resolve.png',
                 'Sorcery':'perk-images/Styles/7202_Sorcery.png'}
shard_images = [
    ['https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/perk-images/statmods/statmodsadaptiveforceicon.png','https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/perk-images/statmods/statmodsattackspeedicon.png','https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/perk-images/statmods/statmodscdrscalingicon.png'],
    ['https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/perk-images/statmods/statmodsadaptiveforceicon.png','https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/perk-images/statmods/statmodsarmoricon.png','https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/perk-images/statmods/statmodsmagicresicon.png'],
    ['https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/perk-images/statmods/statmodshealthscalingicon.png','https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/perk-images/statmods/statmodsarmoricon.png','https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/perk-images/statmods/statmodsmagicresicon.png']]


def get_img(filename,which_rune,rune_type):
    if rune_type == 0:
        url = primary_images[which_rune.title()]
        img_data = r.get(cdn + url).content
        with open(filename, 'wb') as handler:
            handler.write(img_data)
    elif rune_type == 1:
        secondary = regex.sub('', which_rune.title())
        url = complete_runes[secondary]
        img_data = r.get(cdn + url).content
        with open(filename, 'wb') as handler:
            handler.write(img_data)
    elif rune_type == 2:
        url = shard_images[which_rune[0]][which_rune[1]]
        img_data = r.get(url).content
        with open(filename, 'wb') as handler:
            handler.write(img_data)
def runes_to_image(runes,primary_images,complete_runes,shard_images):
    get_img('1.png',runes[0][0],0)
    get_img('2.png',runes[0][1][0],1)
    get_img('3.png',runes[0][1][1],1)
    get_img('4.png',runes[0][1][2],1)
    get_img('5.png',runes[0][1][3],1)

    images = [Image.open(x).resize((64, 64)) for x in ['1.png', '2.png', '3.png', '4.png', '5.png']]
    widths, heights = zip(*(i.size for i in images))

    y_offset = 10
    total_height = sum(heights) + (y_offset*len(images)) + y_offset
    max_width = 84
    primary_runes = Image.new('RGB', (max_width, total_height))
    for im in images:
      primary_runes.paste(im, (10,y_offset))
      y_offset += im.size[1] + 10
    get_img('1.png',runes[1][0],0)
    get_img('2.png',runes[1][1][0],1)
    get_img('3.png',runes[1][1][1],1)
    get_img('4.png',runes[2][0],2)
    get_img('5.png',runes[2][1],2)
    get_img('6.png',runes[2][2],2)
    images = [Image.open(x).resize((64, 64)) for x in ['1.png', '2.png', '3.png', '4.png', '5.png','6.png']]
    widths, heights = zip(*(i.size for i in images))
    y_offset = 10
    total_height = sum(heights) + (y_offset*len(images)) + y_offset
    max_width = 84
    secondary = Image.new('RGB', (max_width, total_height))
    for im in images:
      secondary.paste(im, (10,y_offset))
      y_offset += im.size[1] + 10
    images = [primary_runes,secondary]
    widths, heights = zip(*(i.size for i in images))
    total_width = sum(widths)
    max_height = max(heights)
    new_im = Image.new('RGB', (total_width, max_height))
    x_offset = 0
    for im in images:
      new_im.paste(im, (x_offset,0))
      x_offset += im.size[0]
    new_im.save('rune.jpg')
    return
