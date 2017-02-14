import time
print('Hello world! I can count:')
i = 1
while True:
	print(i)
	i += 1
	time.sleep(1.0)  # Delay for 1 second.

	red = 256 + 128*256
        green = 256 + 8*256
        blue = 256 + 16*256

	hsvR = float(red * 16.0 / 4096.0)
	hsvG = float(blue* 16.0 / 4096.0)
	hsvB = float(green*16.0 / 4096.0)


	if hsvR > hsvG and hsvR > hsvB:
		if hsvB > hsvG:
			hsv = (60 * ((hsvG - hsvB) / (hsvR - hsvG)) % 6)
		else:
			hsv = (60 * ((hsvG - hsvB) / (hsvR - hsvB)) % 6)
	elif hsvG > hsvB and hsvG > hsvR:
		if hsvB > hsvR:
			hsv = (60 * ((hsvB - hsvR) / (hsvG - hsvR)) + 2)
		else:
			hsv = (60 * ((hsvB - hsvR) / (hsvG - hsvB)) + 2)
	elif hsvG > hsvR:
		 hsv = (60 * ((hsvR - hsvG) / (hsvB - hsvR)) + 4)
	else:
		hsv = (60 * ((hsvR - hsvG) / (hsvB - hsvG)) + 4)

	print(red)
	print(hsvR)
	print(green)
	print(hsvG)
	print(blue)
	print(hsvB)
	print(hsv)
