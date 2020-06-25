import math

def derivateofsigmoid(sigvalue):
    return sigvalue*(1-sigvalue)

def sigmoid(x):
    return 1 / (1 + math.exp(-x))

x=(0.9*4.5)+(0.17*-5.2)+(-2)

sig = sigmoid(x)
dsig = derivateofsigmoid(sig)

print("sigmoid of {} = {} and \nDerivate of this sigmoid {} = {}".format(x,sig,sig,dsig))