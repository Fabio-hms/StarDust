# generate_ll1.py
from .grammar import generate

if __name__ == "__main__":
    print("Gerando ll1_table.json...")
    print(generate("stardust_ll1/ll1_table.json"))
    print("Pronto!")
