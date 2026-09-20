#!/usr/bin/env python3
"""Validated JSON recipe -> Adobe Camera Raw develop preset; stdlib only."""
import argparse
import json
import math
from pathlib import Path
import uuid
import xml.etree.ElementTree as ET

NS = {'x': 'adobe:ns:meta/', 'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#', 'crs': 'http://ns.adobe.com/camera-raw-settings/1.0/'}
for prefix, uri in NS.items():
    ET.register_namespace(prefix, uri)
def q(prefix, name):
    return '{' + NS[prefix] + '}' + name
RANGES = {k: (-100, 100) for k in ['Contrast2012','Highlights2012','Shadows2012','Whites2012','Blacks2012','Clarity2012','Texture','Dehaze','Vibrance','Saturation','SplitToningBalance','PostCropVignetteAmount']}
for color in ['Red','Orange','Yellow','Green','Aqua','Blue','Purple','Magenta']:
    for action in ['Hue','Saturation','Luminance']:
        RANGES[action+'Adjustment'+color] = (-100,100)
for zone in ['Shadow','Highlight']:
    RANGES['SplitToning'+zone+'Hue'] = (0,360)
    RANGES['SplitToning'+zone+'Saturation'] = (0,100)
RANGES.update({'Exposure2012':(-5,5),'GrainAmount':(0,100),'GrainSize':(0,100),'GrainFrequency':(0,100),'Temperature':(2000,50000),'Tint':(-150,150),'IncrementalTemperature':(-100,100),'IncrementalTint':(-100,100)})
CURVES = {'ToneCurvePV2012'+suffix for suffix in ['', 'Red','Green','Blue']}
def numeric(value, lo, hi):
    return type(value) in (int,float) and math.isfinite(value) and lo <= value <= hi

def export(recipe, output):
    if not isinstance(recipe, dict):
        raise ValueError('Recipe must be an object')
    unknown = set(recipe) - {'name','group','description','settings','curves'}
    if unknown:
        raise ValueError('Unknown recipe fields: '+str(sorted(unknown)))
    for key in ['name','group']:
        if not isinstance(recipe.get(key), str) or not recipe[key].strip():
            raise ValueError(key+' must be a nonempty string')
    if not isinstance(recipe.get('description',''), str):
        raise ValueError('description must be a string')
    settings, curves = recipe.get('settings',{}), recipe.get('curves',{})
    if not isinstance(settings,dict) or not isinstance(curves,dict) or not (settings or curves):
        raise ValueError('Provide settings/curves objects with at least one adjustment')
    for key,value in settings.items():
        if key not in RANGES or not numeric(value,*RANGES[key]):
            raise ValueError('Unsupported control or out-of-range value: '+key)
        if key != 'Exposure2012' and value != int(value):
            raise ValueError('Control must use an integer: '+key)
    absolute_wb = bool(set(settings) & {'Temperature', 'Tint'})
    incremental_wb = bool(set(settings) & {'IncrementalTemperature', 'IncrementalTint'})
    if absolute_wb and incremental_wb:
        raise ValueError('Do not mix RAW Kelvin WB with non-RAW incremental WB')
    for key,points in curves.items():
        if key not in CURVES or not isinstance(points,list) or len(points)<2:
            raise ValueError('Invalid curve: '+key)
        if any(not isinstance(p,list) or len(p)!=2 or any(type(v) is not int or not 0<=v<=255 for v in p) for p in points):
            raise ValueError('Curve points must be integer x,y pairs from 0 to 255')
        if points[0][0]!=0 or points[-1][0]!=255 or any(b[0]<=a[0] or b[1]<a[1] for a,b in zip(points,points[1:])):
            raise ValueError('Curve endpoints or monotonicity invalid')
    root = ET.Element(q('x','xmpmeta'))
    rdf = ET.SubElement(root,q('rdf','RDF'))
    attrs = {'PresetType':'Normal','UUID':uuid.uuid4().hex.upper(),'ProcessVersion':'11.0','HasSettings':'True','SupportsAmount':'False','CameraModelRestriction':''}
    for key in ['SupportsColor','SupportsMonochrome','SupportsHighDynamicRange','SupportsNormalDynamicRange','SupportsSceneReferred','SupportsOutputReferred']:
        attrs[key]='True'
    attrs.update({key:format(value,'g') for key,value in settings.items()})
    if absolute_wb or incremental_wb:
        attrs['WhiteBalance']='Custom'
    if curves:
        attrs['ToneCurveName2012']='Custom'
    desc = ET.SubElement(rdf,q('rdf','Description'),{q('rdf','about'):'',**{q('crs',k):v for k,v in attrs.items()}})
    for tag,value in [('Name',recipe['name']),('Group',recipe['group']),('Description',recipe.get('description',''))]:
        alt=ET.SubElement(ET.SubElement(desc,q('crs',tag)),q('rdf','Alt'))
        ET.SubElement(alt,q('rdf','li'),{'{http://www.w3.org/XML/1998/namespace}lang':'x-default'}).text=value
    for key,points in curves.items():
        seq=ET.SubElement(ET.SubElement(desc,q('crs',key)),q('rdf','Seq'))
        for x,y in points:
            ET.SubElement(seq,q('rdf','li')).text=f'{x}, {y}'
    ET.indent(root,space='  ')
    data=ET.tostring(root,encoding='utf-8',xml_declaration=True)
    ET.fromstring(data)
    output=Path(output)
    if output.suffix.lower()!='.xmp':
        raise ValueError('Output must have .xmp extension')
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_bytes(data+b'\n')
    return attrs['UUID']

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('recipe',type=Path)
    parser.add_argument('output',type=Path)
    args=parser.parse_args()
    try:
        preset_id=export(json.loads(args.recipe.read_text()),args.output)
    except (ValueError, OSError, ET.ParseError) as exc:
        parser.exit(1,f'Error: {exc}\n')
    print(f'Validated XMP written: {args.output} (UUID {preset_id})')
