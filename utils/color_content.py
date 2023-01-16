import pandas as pd
import matplotlib.pyplot as plt
import extcolors

from PIL import Image
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from colormap import rgb2hex

def color_to_df(input):
    colors_pre_list = str(input).replace('([(','').split(', (')[0:-1]
    df_rgb = [i.split('), ')[0] + ')' for i in colors_pre_list]
    df_percent = [i.split('), ')[1].replace(')','') for i in colors_pre_list]
    
    # convert RGB to HEX code
    df_color_up = [rgb2hex(int(i.split(", ")[0].replace("(","")),
                          int(i.split(", ")[1]),
                          int(i.split(", ")[2].replace(")",""))) for i in df_rgb]
    
    df = pd.DataFrame(zip(df_color_up, df_percent), columns = ['c_code','occurence'])
    return df

def exact_color(input_image, resize, tolerance, zoom):
    
    #resize
    output_width = resize
    img = Image.open(input_image)
    if img.size[0] >= resize:
        wpercent = (output_width/float(img.size[0]))
        hsize = int((float(img.size[1])*float(wpercent)))
        img = img.resize((output_width,hsize), Image.ANTIALIAS)
        resize_name = 'resize_'+ input_image.split("/")[-1]
        img.save(f"images/color-content/{resize_name}")
    else:
        resize_name = input_image.split("/")[1]
    
    #crate dataframe
    img_url = resize_name
    colors_x = extcolors.extract_from_path(f"images/color-content/{img_url}", tolerance = tolerance, limit = 13)
    df_color = color_to_df(colors_x)
    
    #annotate text
    list_color = list(df_color['c_code'])
    #print(list_color)
    list_precent = [int(i) for i in list(df_color['occurence'])]
    #print(list_precent)
    text_c = [c + ' ' + str(round(p*100/sum(list_precent),1)) +'%' for c, p in zip(list_color, list_precent)]
    return text_c