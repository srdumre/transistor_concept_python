class NMOS:
    def __init__(self,threshold=1.0):
        self.threshold = threshold
        self.gate = 0


    def conduct(self):
        return self.gate > self.threshold
    


class PMOS:
    def __init__(self,threshold=1.0,vdd=5.0):
        self.threshold = threshold
        self.vdd = vdd
        self.gate = 0 


    def conduct(self):
        return self.gate < self.threshold




class CMOSInverter:
    def __init__(self,vdd = 5.0, vth =1.0):
        self.vdd = vdd
        self.nmos = NMOS(vth)
        self.pmos = PMOS(vth,vdd)


    def output(self,vin):
        self.nmos.gate = vin 
        self.pmos.gate = vin


        if self.nmos.conduct():
            return 0
        
        if self.pmos.conduct():
            return self.vdd
        

        return None
    

class CMOSNAND2:
    def __init__(self, vdd=5.0, vth=1.0):
        self.vdd = vdd
        self.inverter = CMOSInverter(vdd, vth)

    def output(self, a, b):
        and_out = int((a > 0) and (b > 0)) * self.vdd
        return self.inverter.output(and_out)


class CMOSNOR2:
    def __init__(self, vdd=5.0, vth=1.0):
        self.vdd = vdd
        self.inverter = CMOSInverter(vdd, vth)

    def output(self, a, b):
        or_out = int((a > 0) or (b > 0)) * self.vdd
        return self.inverter.output(or_out)


class CMOSAND2:
    def __init__(self, vdd=5.0, vth=1.0):
        self.nand = CMOSNAND2(vdd, vth)
        self.inverter = CMOSInverter(vdd, vth)

    def output(self, a, b):
        nand_out = self.nand.output(a, b)
        return self.inverter.output(nand_out)


class CMOSOR2:
    def __init__(self, vdd=5.0, vth=1.0):
        self.nor = CMOSNOR2(vdd, vth)
        self.inverter = CMOSInverter(vdd, vth)

    def output(self, a, b):
        nor_out = self.nor.output(a, b)
        return self.inverter.output(nor_out)


class CMOSXOR2:
    def __init__(self, vdd=5.0, vth=1.0):
        self.nand = CMOSNAND2(vdd, vth)
        self.or2 = CMOSOR2(vdd, vth)
        self.and2 = CMOSAND2(vdd, vth)

    def output(self, a, b):
        nand_out = self.nand.output(a, b)
        or_out = self.or2.output(a, b)
        return self.and2.output(nand_out, or_out)


class HalfAdder:
    def __init__(self, vdd=5.0):
        self.xor2 = CMOSXOR2(vdd)
        self.and2 = CMOSAND2(vdd)

    def output(self, a, b):
        return {
            "sum": self.xor2.output(a, b),
            "carry": self.and2.output(a, b)
        }


class FullAdder:
    def __init__(self, vdd=5.0):
        self.ha1 = HalfAdder(vdd)
        self.ha2 = HalfAdder(vdd)
        self.or2 = CMOSOR2(vdd)

    def output(self, a, b, cin):
        ha1_res = self.ha1.output(a, b)
        ha2_res = self.ha2.output(ha1_res["sum"], cin)
        cout = self.or2.output(ha1_res["carry"], ha2_res["carry"])
        return {
            "sum": ha2_res["sum"],
            "carry": cout
        }


def truth_table(gate, inputs=2, name=None):
    title = name if name else gate.__class__.__name__
    print(f"Truth Table for {title}")
    if inputs == 1:
        for a in [0, 5]:
            print(f"In={a} -> Out={gate.output(a)}")
    elif inputs == 2:
        for a in [0, 5]:
            for b in [0, 5]:
                print(f"A={a}, B={b} -> Out={gate.output(a, b)}")
    elif inputs == 3:  
        for a in [0, 5]:
            for b in [0, 5]:
                for cin in [0, 5]:
                    res = gate.output(a, b, cin)
                    print(f"A={a}, B={b}, Cin={cin} -> Sum={res['sum']}, Cout={res['carry']}")
    print("-" * 40)



if __name__ == "__main__":
    inverter = CMOSInverter()
    nand2 = CMOSNAND2()
    nor2 = CMOSNOR2()
    xor2 = CMOSXOR2()
    ha = HalfAdder()
    fa = FullAdder()

    truth_table(inverter, inputs=1)
    truth_table(nand2, inputs=2)
    truth_table(nor2, inputs=2)
    truth_table(xor2, inputs=2)
    truth_table(ha, inputs=2, name="HalfAdder")
    truth_table(fa, inputs=3, name="FullAdder")



