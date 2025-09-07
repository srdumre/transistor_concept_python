import matplotlib.pyplot as plt
from transistor import CMOSInverter, CMOSNAND2, CMOSXOR2, HalfAdder, FullAdder  

def plot_waveform(time, signals, title="CMOS Simulation"):
    plt.figure(figsize=(10, 6))
    for i, (name, values) in enumerate(signals.items()):
        plt.step(time, [v/5 for v in values], where="post", label=name)  
    plt.title(title)
    plt.xlabel("Time (steps)")
    plt.ylabel("Logic Level (0 / 1)")
    plt.yticks([0, 1])
    plt.grid(True, which="both", linestyle="--", alpha=0.6)
    plt.legend(loc="upper right")
    plt.show()


if __name__ == "__main__":
    time = list(range(8))  
    a_vals = [0, 0, 5, 5, 0, 0, 5, 5]
    b_vals = [0, 5, 0, 5, 0, 5, 0, 5]

    nand2 = CMOSNAND2()
    xor2 = CMOSXOR2()
    ha = HalfAdder()
    fa = FullAdder()

    nand_out, xor_out, sum_out, carry_out = [], [], [], []

    for a, b in zip(a_vals, b_vals):
        nand_out.append(nand2.output(a, b))
        xor_out.append(xor2.output(a, b))
        ha_res = ha.output(a, b)
        sum_out.append(ha_res["sum"])
        carry_out.append(ha_res["carry"])

    signals = {
        "A": a_vals,
        "B": b_vals,
        "NAND": nand_out,
        "XOR": xor_out,
        "HalfAdder SUM": sum_out,
        "HalfAdder CARRY": carry_out
    }

    plot_waveform(time, signals, "CMOS Logic Waveforms")
