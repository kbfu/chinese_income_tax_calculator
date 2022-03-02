import importlib
import sys

import tax

region_dict = {'上海': 'shanghai'}

if __name__ == '__main__':
    region = input('输入地区：')
    region_lib = importlib.import_module(f'.{region_dict[region]}', 'regions')
    salary_monthly = input('税前月薪：')
    base = input('社保公积金月缴纳基数：')
    extra_housing_fund = input('是否有补充公积金 y/n：')
    if extra_housing_fund != 'y' and extra_housing_fund != 'n':
        print('输入错误')
        sys.exit(0)

    bonus = input('年终奖：')
    bonus_taxed_alone = input('年终奖是否单独计算 y/n：')

    if bonus_taxed_alone != 'y' and bonus_taxed_alone != 'n':
        print('输入错误')
        sys.exit(0)

    social_insurance_base = int(base)
    housing_fund_base = int(base)
    if housing_fund_base > region_lib.housing_fund_monthly_max:
        housing_fund_base = region_lib.housing_fund_monthly_max
    elif housing_fund_base < region_lib.housing_fund_monthly_min:
        housing_fund_base = region_lib.housing_fund_monthly_min
    if social_insurance_base > region_lib.social_insurance_monthly_max:
        social_insurance_base = region_lib.social_insurance_monthly_max
    elif social_insurance_base < region_lib.social_insurance_monthly_min:
        social_insurance_base = region_lib.social_insurance_monthly_min

    net_salary_annual = int(salary_monthly) * 12 + int(bonus)
    # 先扣除社保公积金
    total_housing_fund = housing_fund_base * (
            region_lib.housing_fund_individual_rate + region_lib.housing_fund_individual_rate_extra) * 12 if \
        extra_housing_fund == 'y' else housing_fund_base * region_lib.housing_fund_individual_rate * 12
    total_social_insurance = social_insurance_base * region_lib.social_insurance_individual_rate * 12
    net_salary_annual = net_salary_annual - total_housing_fund - total_social_insurance
    # 然后减去免征额
    to_be_taxed_salary_annual = net_salary_annual - tax.annual_tax_free
    # 最后计算纳税额度
    if bonus_taxed_alone == 'y':
        # 年终奖单独计算
        total_tax = tax.calc_tax(to_be_taxed_salary_annual - int(bonus))
        total_tax += tax.calc_tax(int(bonus))
    else:
        # 年终奖合计计算
        total_tax = tax.calc_tax(to_be_taxed_salary_annual)
    net_salary_annual -= total_tax

    print(f'税前总收入：{int(salary_monthly) * 12 + int(bonus)}')
    print(f'公积金个人总支出：{round(total_housing_fund, 2)}')
    print(f'个人社保总支出：{round(total_social_insurance, 2)}')
    print(f'总缴纳税：{round(total_tax, 2)}')
    print(f'总净收入：{round(net_salary_annual, 2)}')
