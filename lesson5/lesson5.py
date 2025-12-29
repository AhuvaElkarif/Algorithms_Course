import sys
from PIL import Image

def main():
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} image-filename")
        return

    filename = sys.argv[1]

    img = Image.open(filename).convert("RGB")
    img.show()
    r, g, b = img.split()

    blank = Image.new("L", img.size, 0)

    red_img   = Image.merge("RGB", (r, blank, blank))
    green_img = Image.merge("RGB", (blank, g, blank))
    blue_img  = Image.merge("RGB", (blank, blank, b))

    red_img.show(title="Red Channel")
    green_img.show(title="Green Channel")
    blue_img.show(title="Blue Channel")

if __name__ == "__main__":
    main()
