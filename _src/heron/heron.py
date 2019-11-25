def new(r, k):
	return 0.5 * (k + float(r)/k)

	
def heron(r, k, n):
	for i in range(0,n):
		k = new(r, k)
		print("=> %d: %.10f" % (i, k))


heron(52900, 100, 5)
