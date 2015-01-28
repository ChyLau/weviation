import lxml.etree as ET

f = open("test.txt")
lines = f.readlines()
root = ET.Element("root")
for l in lines:
  elems = l.split(":")
  if len(elems) == 2:
    elems = map(lambda x: x.strip(), elems)
    line = ET.SubElement(root, "line")
    item1 = ET.SubElement(line, "item1")
    item2 = ET.SubElement(line, "item2")
    item1.text = elems[0]
    item2.text = elems[1]

tree = ET.ElementTree(root)
tree.write("test.xml", pretty_print=True)
