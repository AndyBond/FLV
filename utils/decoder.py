text = """
/regions/mt/doclib/РџРћРЎРўРђР’РљР_РЈРЎР›РЈР“Р/РћР Р“РўР•РҐРќРРљРђ/РљРћРќРљРЈР РЎ/2024/РќРѕРІС‹Р№+РєРѕРЅРєСѓСЂСЃ+РњРў/РљРџ/Р’СЃРµ+РљРџ.pdf
"""

text = """
п⌠я┐п╠п╦п╫п╟ п∙п╩п╣п╫п╟ п╝я─я▄п╣п╡п╫п╟; п÷я─п╬я┘п╬я─п╬п╡ п²п╦п╨п╬п╩п╟п╧ п²п╦п╨п╬п╩п╟п╣п╡п╦я┤; п╗п╣п╩п╣я│я┌ п╝я─п╦п╧ п▓п╩п╟п╢п╦п╪п╦я─п╬п╡п╦я┤; п°п╬п╩п╬п╢п╦я┤п╣п╫п╨п╬ 
"""
"""
file_in = "C:\\Projects\\IISLogAnalyzer-master\\input\\u_ex250318_x.log"
file_out = "C:\\Projects\\IISLogAnalyzer-master\\input\\u_ex250318_x-out.log"
output = open(file_out, "w", encoding='utf8')
with open(file_in, "r", encoding='utf8', errors='ignore') as log_file:
    for line in log_file:
        print(line)
        output.writelines(line)
#        self.write_file(os.getcwd() + "/output/output.log", lines)
output.flush()
output.close()
"""
print("from file2", text)
text = text.encode('cp1252', errors='ignore')
print("after encode\n", text)
text = text.decode('cp1252', errors='ignore')
print("after decode", text)
