# Project plans

- [ ] I need a raycast script that opens the directory of `~/notebook/media/figures/{YYYY}/{MM}/{DD}/` where YYYY, MM, DD are default by the current date (but can be modified in 3 input fields). Use python script with subprocess command `open {dir}` to open the folder in finder.

magick IMG_9617.HEIC \
  \( +clone -resize 1080x1920^ -gravity center -extent 1080x1920 -blur 0x30 \) \
  \( +clone -resize 1080x810 \) \
  -delete 0 -gravity center -compose over -composite \
  output.HEIC
