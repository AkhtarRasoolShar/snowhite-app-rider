import xml.etree.ElementTree as ET

tree = ET.parse('app/src/main/res/values/strings.xml')
root = tree.getroot()
for string in root.findall('string'):
    if string.get('name') == 'app_name':
        string.text = 'SnowWhite Captain'
tree.write('app/src/main/res/values/strings.xml')
