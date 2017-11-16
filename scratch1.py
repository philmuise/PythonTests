import os

working_folder = r"K:\GEM1__\2016_NotDone\RS2_OK78288_PK692642_DK621902_W2_20160814_232802_VV_SGF"
aa  = os.path.join(os.path.dirname(working_folder),"{}_RSImageInfo".format(os.path.basename(working_folder)))
print os.path.dirname(working_folder)
print os.path.basename(working_folder)
print aa
print os.path.abspath('K:\Projects\GEM1\GEM1toGEM2\Products\Scratch')
inputMaskShp = r'K:\Projects\GEM1\GEM1toGEM2\Products\NOS_2017.shp'
print inputMaskShp
outMask = os.path.join(os.path.dirname(inputMaskShp),"{}_RSImageInfo".format(os.path.splitext(os.path.basename(inputMaskShp))[0]))
print outMask
nosRSImageadded = '{}.shp'.format(outMask)
print nosRSImageadded
