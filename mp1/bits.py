def set_bit(value, bit):
    return value | (1<<bit)

def clear_bit(value, bit):
    return value & ~(1<<bit)

def ispow2(value):
	return value & (value - 1)

value = 2
#print (set_bit(value, 0))
print (ispow2(value))