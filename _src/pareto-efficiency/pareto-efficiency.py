
def utility(x, y):
	return x*y


# Pareto efficiency
#
# A Pareto efficient point equates the marginal rates of substitution of the two parties.

# Marginal rate of substitution
# 
# The Marginal Rate of Substitution (MRS) is the rate at which a consumer can give up some amount of one good 
# in exchange for another good while maintaining the same level of utility. 
# 
# Assume the consumer utility function is defined by U(x,y), where U is consumer utility function, and x and y are goods.
# Then the marginal rate of substitution is the ratio of the marginal utilities:
#
# MRS_{xy} = MU_{x}/MU_{y}
#
# where MU_{x} = \partial U / \partial x, and MU_{y} = \partial U / \partial y

# Pareto efficient allocations



x_A = 12
y_A = 2

x_B = 8
y_B = 18

print((144.0 * y_A) / x_A)

print("[*] baseline: u_A = %d, u_B = %d\n--------------------------------" % (utility(x_A, y_A), utility(x_B, y_B) ))