import pdfplumber
import pandas as pd


pdf = pdfplumber.open("saturated.pdf")

substances = [
    "water",
    "ammonia",
    "carbondioxide",
    "r-410a",
    "r-134a",
    "methane",
]
vcolumns = ["T", "P", "vf", "vfg", "vg", "uf", "ufg", "ug"]
hcolumns = ["T", "P", "hf", "hfg", "hg", "sf", "sfg", "sg"]


def saturated():
    pages = len(pdf.pages)
    num = 0
    for i in range(len(substances)):
        volume_tables = pd.DataFrame(columns=vcolumns)
        enthalpy_tables = pd.DataFrame(columns=hcolumns)
        
        while True:
            text = pdf.pages[num].extract_text()
            if "saturated" in text.lower():
                sat = True
                substance = substances[i]
                if "volume" in text.lower():
                    table = pdf.pages[num].extract_table()
                    new_table = []
                    for k in table:
                        for j in k:
                            new_table.extend(j.split("\n"))
                    new_table = new_table[4:]
                    new_table = [n.split(" ") for n in new_table]

                    for row in new_table:
                        for l in range(len(row)):
                            row[l] = row[l].replace("−", "-")
                            row[l] = float(row[l])
                    if volume_tables.empty:
                        volume_tables = pd.DataFrame(new_table, columns=vcolumns)
                    else:
                        volume_tables = pd.concat(
                            [
                                volume_tables,
                                pd.DataFrame(new_table[0:], columns=vcolumns),
                            ]
                        )

                if "enthalpy" in text.lower():
                    table = pdf.pages[num].extract_table()
                    new_table = []
                    for k in table:
                        for j in k:
                            new_table.extend(j.split("\n"))
                    new_table = new_table[4:]
                    new_table = [n.split(" ") for n in new_table]

                    for row in new_table:
                        for l in range(len(row)):
                            row[l] = row[l].replace("−", "-")
                            row[l] = float(row[l])
                    if enthalpy_tables.empty:
                        enthalpy_tables = pd.DataFrame(new_table[0:], columns=hcolumns)
                    else:
                        enthalpy_tables = pd.concat(
                            [
                                enthalpy_tables,
                                pd.DataFrame(new_table[0:], columns=hcolumns),
                            ]
                        )
            num += 1
            if num == pages:
                break
            if substances[i] not in pdf.pages[num].extract_text().lower():
                while substances[i + 1] not in pdf.pages[num].extract_text().lower():
                    if substances[i + 1] in pdf.pages[num].extract_text().lower():
                        num += 1
                        break
                    num += 1
                break
        
        saturated = pd.merge(volume_tables, enthalpy_tables, on=["T", "P"])
        saturated.to_csv(f"saturated_{substances[i]}.csv", index=False)
def pressure_entry():    
    pdf = pdfplumber.open("pressure_entry.pdf")
    pvcolumns = ["P","T","vf", "vfg", "vg", "uf", "ufg", "ug"]
    phcolumns = ["P","T","hf", "hfg", "hg", "sf", "sfg", "sg"]


    pages = len(pdf.pages)
    num = 0
    volume_tables = pd.DataFrame(columns=pvcolumns)
    enthalpy_tables = pd.DataFrame(columns=phcolumns)
    while True:
        text = pdf.pages[num].extract_text()
        if "volume" in text.lower():
                    table = pdf.pages[num].extract_table()
                    new_table = []
                    for k in table:
                        for j in k:
                            new_table.extend(j.split("\n"))
                    new_table = new_table[4:]
                    new_table = [n.split(" ") for n in new_table]

                    for row in new_table:
                        for l in range(len(row)):
                            row[l] = row[l].replace("−", "-")
                            row[l] = float(row[l])
                    if volume_tables.empty:
                        volume_tables = pd.DataFrame(new_table, columns=pvcolumns)
                    else:
                        volume_tables = pd.concat(
                            [
                                volume_tables,
                                pd.DataFrame(new_table[0:], columns=pvcolumns),
                            ]
                        )

        if "enthalpy" in text.lower():
                    table = pdf.pages[num].extract_table()
                    new_table = []
                    for k in table:
                        for j in k:
                            new_table.extend(j.split("\n"))
                    new_table = new_table[4:]
                    new_table = [n.split(" ") for n in new_table]

                    for row in new_table:
                        for l in range(len(row)):
                            row[l] = row[l].replace("−", "-")
                            row[l] = float(row[l])
                    if enthalpy_tables.empty:
                        enthalpy_tables = pd.DataFrame(new_table[0:], columns=phcolumns)
                    else:
                        enthalpy_tables = pd.concat(
                            [
                                enthalpy_tables,
                                pd.DataFrame(new_table[0:], columns=phcolumns),
                            ]
                        )        
        num += 1
        if num == pages:
            break
    pressure_entry = pd.merge(volume_tables, enthalpy_tables, on=["P", "T"])
    pressure_entry.to_csv(f"pressure_water.csv", index=False)


saturated()
pressure_entry()