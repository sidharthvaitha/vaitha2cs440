def set_bit(value, bit):
    return value | (1<<bit)

def clear_bit(value, bit):
    return value & ~(1<<bit)

def ispow2(value):
	return value & (value - 1)

def set_all_bits(n):
	value = 0
	for i in range(n):
		value = set_bit(value, i)
	print(value)

def check_if_bitset(val, n):
	return val & (1<<n)

print(check_if_bitset(6, 0))