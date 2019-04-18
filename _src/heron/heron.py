# what has always fascinated me about mathematics is that you can really
# touch upon the ideas from the previous centuries and even millenia!
# a case in point: here's a 2000 years old algorithm that is a.. to Heron
# of Alexandria (60 AD) who was allegedly from Syracus. However, this algorithm
# is already written in a Babylonian Keilschrift that is dated to about
# 1600 BC (so it's actually 3600 years old!!)

def neu(alt, r):
    return 0.5 * (alt + (float(r) / alt))


print("%f" % (neu(3,11)))
