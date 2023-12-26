import pandas as pd
import tables
from thefuzz import fuzz

substances = tables.substances
def volume(substance, T, x):
    df = pd.read_csv(f"saturated_{substance}.csv")
    if(T%5 !=0):
        #interpolate
        T1 = T - (T%5)
        T2 = T1 + 5
        vf1 = df[df["T"] == T1]["vf"].values[0]
        vg1 = df[df["T"] == T1]["vg"].values[0]
        vf2 = df[df["T"] == T2]["vf"].values[0]
        vg2 = df[df["T"] == T2]["vg"].values[0]
        vf = vf1 + (vf2-vf1)*(T-T1)/5
        vg = vg1 + (vg2-vg1)*(T-T1)/5
        return vf + x * (vg - vf)
    vf = df[df["T"] == T]["vf"].values[0]
    vg = df[df["T"] == T]["vg"].values[0]
    return vf + x * (vg - vf)
def internal_energy(substance, T, x):
    df = pd.read_csv(f"saturated_{substance}.csv")
    if(T%5 !=0):
        #interpolate
        T1 = T - (T%5)
        T2 = T1 + 5
        uf1 = df[df["T"] == T1]["uf"].values[0]
        ug1 = df[df["T"] == T1]["ug"].values[0]
        uf2 = df[df["T"] == T2]["uf"].values[0]
        ug2 = df[df["T"] == T2]["ug"].values[0]
        uf = uf1 + (uf2-uf1)*(T-T1)/5
        ug = ug1 + (ug2-ug1)*(T-T1)/5
        return uf + x * (ug - uf)
    uf = df[df["T"] == T]["uf"].values[0]
    ug = df[df["T"] == T]["ug"].values[0]
    return uf + x * (ug - uf)
def enthalpy(substance, T, x):
    df = pd.read_csv(f"saturated_{substance}.csv")
    if(T%5 !=0):
        #interpolate
        T1 = T - (T%5)
        T2 = T1 + 5
        hf1 = df[df["T"] == T1]["hf"].values[0]
        hg1 = df[df["T"] == T1]["hg"].values[0]
        hf2 = df[df["T"] == T2]["hf"].values[0]
        hg2 = df[df["T"] == T2]["hg"].values[0]
        hf = hf1 + (hf2-hf1)*(T-T1)/5
        hg = hg1 + (hg2-hg1)*(T-T1)/5
        return hf + x * (hg - hf)
    hf = df[df["T"] == T]["hf"].values[0]
    hg = df[df["T"] == T]["hg"].values[0]
    return hf + x * (hg - hf)
def entropy(substance, T, x):
    df = pd.read_csv(f"saturated_{substance}.csv")
    if(T%5 !=0):
        #interpolate
        T1 = T - (T%5)
        T2 = T1 + 5
        sf1 = df[df["T"] == T1]["sf"].values[0]
        sg1 = df[df["T"] == T1]["sg"].values[0]
        sf2 = df[df["T"] == T2]["sf"].values[0]
        sg2 = df[df["T"] == T2]["sg"].values[0]
        sf = sf1 + (sf2-sf1)*(T-T1)/5
        sg = sg1 + (sg2-sg1)*(T-T1)/5
        return sf + x * (sg - sf)
    sf = df[df["T"] == T]["sf"].values[0]
    sg = df[df["T"] == T]["sg"].values[0]
    return sf + x * (sg - sf)
def menu():
    print("1. Search for a substance")
    print("2. Exit")
    choice = input("Enter your choice: ")
    if choice == "1":
        search_substance()
    elif choice == "2":
        exit()
    else:
        print("Invalid choice")
        menu()
def search_substance():
    substance = input("Enter the substance you want to search for: \n")

    ratios=[]
    for i in substances:
        ratios.append(fuzz.ratio(i, substance))
    if max(ratios) < 10:
        print("\nNo matches found")
        search_substance()
    print(substances[ratios.index(max(ratios))], max(ratios),"% Match")
    substance = substances[ratios.index(max(ratios))]
    print("Choose the property that is given: \n")
    print("1.) T and x")
    print("2.) T and v")
    print("3.) T and h")
    print("4.) T and u")
    print("5.) T and s")
    print("6.) Back")
    print("7.) Exit\n")
    inp = input("Enter your choice: \n")
    if inp == "1":
        T = float(input("Enter the temperature: "))
        x = float(input("Enter the quality: "))
        print("\nv = ",volume(substance, T, x),"kg/m^3")
        print("u = ",internal_energy(substance, T, x),"kJ/kg")
        print("h = ",enthalpy(substance, T, x),"kJ/kg")
        print("s = ",entropy(substance, T, x),"kJ/kgK")
    elif inp == "2":
        T = float(input("Enter the temperature: "))
        v = float(input("Enter the specific volume: "))
        x = (v-volume(substance,T,0)) / (volume(substance,T,1)-volume(substance,T,0))
        print("\nquality = ",x*100,"%")
        print("u = ",internal_energy(substance, T, x),"kJ/kg")
        print("h = ",enthalpy(substance, T, x),"kJ/kg")
        print("s = ",entropy(substance, T, x),"kJ/kgK")
    elif inp == "3":
        T = float(input("Enter the temperature: "))
        h = float(input("Enter the enthalpy: "))
        x = (h-enthalpy(substance,T,0)) / (enthalpy(substance,T,1)-enthalpy(substance,T,0))
        print("\nquality = ",x*100,"%")
        print("u = ",internal_energy(substance, T, x),"kJ/kg")
        print("v = ",volume(substance, T, x),"kg/m^3")
        print("s = ",entropy(substance, T, x),"kJ/kgK")
    elif inp == "4":
        T = float(input("Enter the temperature: "))
        u = float(input("Enter the internal energy: "))
        x = (u-internal_energy(substance,T,0)) / (internal_energy(substance,T,1)-internal_energy(substance,T,0))
        print("\nquality = ",x*100,"%")
        print("h = ",enthalpy(substance, T, x),"kJ/kg")
        print("v = ",volume(substance, T, x),"kg/m^3")
        print("s = ",entropy(substance, T, x),"kJ/kgcK")
    elif inp == "5":
        T = float(input("Enter the temperature: "))
        s = float(input("Enter the entropy: "))
        x = (s-entropy(substance,T,0)) / (entropy(substance,T,1)-entropy(substance,T,0))
        print("\nquality = ",x*100,"%")
        print("h = ",enthalpy(substance, T, x),"kJ/kg")
        print("v = ",volume(substance, T, x),"kg/m^3")
        print("u = ",internal_energy(substance, T, x),"kJ/kg")
    elif inp == "6":
        search_substance()
    else:
        exit()
menu()