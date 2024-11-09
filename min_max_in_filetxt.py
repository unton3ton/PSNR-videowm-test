from glob import glob
from os import system

namedir1 = 'videos'
namedir2 = 'videowatermark'

videos_empty = glob(f'{namedir1}/*_rescale.mp4'); print(videos_empty)
videos_wm = glob(f'{namedir2}/*_encoded.mp4'); print(videos_wm)

i = 1
for video_em in videos_empty:
    for video_wm in videos_wm:
        if video_em[len(namedir1):-4] == video_wm[len(namedir2):-12]:
            print(f'{video_em[:-4]} == {video_wm[:-12]}')
            system(f"java -jar StegoVideo.jar psnr -c {video_em} -s {video_wm} > {i}.txt")
            i += 1
            

system('cat *.txt > all.txt')

system("perl -ne 'print if /PSNR/i' all.txt > result.txt")

system("awk '{print $NF}' result.txt > res.txt")

number_list = []
with open('res.txt', 'r') as fp:
    number_list = [float(item.replace(',', '.')) for item in fp.readlines()]

minimum = min(number_list)
maximum = max(number_list)
average = sum(number_list)/len(number_list)

print(f'min: {minimum}\nmax: {maximum}\navg: {average}')
with open(f'psnr_for_{namedir2}.csv', 'w') as file:
    file.write(f'min: {minimum},\nmax: {maximum},\navg: {average},\n')

system('rm *.txt')