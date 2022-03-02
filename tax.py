# 年免税额
annual_tax_free = 60000
# 个人所得税区间
tax_rate_dict = {36000: .03, 144000 - 36000: .1, 300000 - 144000: .2, 420000 - 300000: .25, 660000 - 420000: .3,
                 960000 - 660000: .35}
max_tax_rate = .45


def calc_tax(to_be_taxed: int) -> int:
    total_tax = 0
    if to_be_taxed > 0:
        for k, v in tax_rate_dict.items():
            if to_be_taxed - k <= 0:
                total_tax += to_be_taxed * v
                to_be_taxed = 0
                break
            else:
                total_tax += k * v
                to_be_taxed -= k
        if to_be_taxed > 0:
            total_tax += to_be_taxed * max_tax_rate
    return total_tax
