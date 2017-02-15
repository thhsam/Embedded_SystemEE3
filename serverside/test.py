def hahaha(x, z, y = 0):
	global i
	i = i + 1
	return y
def main():
	global i
	while True:
		hahaha()
		print(i)
i = 0
print(hahaha(x=1,y=3))

