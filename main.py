from mpmath import mp

def find_position_in_pi(seq):
    step = 100000
    max_digits = 10000000
    curr = step
    while curr < max_digits:
        mp.dps = curr
        pi = str(mp.pi)[2:]
        pos = pi.find(seq)
        print(f"Checked {curr} digits...",end='\r')
        if pos != -1:
            print(f"\nSequence '{seq}' found at position {pos + 1} in π after the decimal")
            return
        curr += step
        print(f"\nSequence '{seq}' not found in first {max_digits} digits of π")

if __name__ == "__main__":
    #seq = input("Enter which number sequence you want to find in π: ")
    seq = "1239"
    if not seq.isdigit():
        print("Digits only!")
    else:
        find_position_in_pi(seq)

