def hahaha():
	global i
	i = i + 1
def main():
	global i
	while True:
		hahaha()
		print(i)
i = 0
main()

