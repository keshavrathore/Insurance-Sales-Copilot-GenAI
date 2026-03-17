import re

#income filteration

# Income conversion to integers
def income_conv(income):
    if isinstance(income, str) and income.isdigit():
        income_in_rupees = int(income)
    elif isinstance(income, str) and '-' in income:
        income_range = income.split('-')
        income_range = [i.strip() for i in income_range]
        income_end_range = income_range[1].split(" ")
        if "lakhs" in income or "Lakhs" in income:
            income_in_rupees = int(income_end_range[0])*100000
    else:
        income_in_rupees = int(re.findall(r'\d+', str(income))[0])*100000
    return income_in_rupees

# Income check to filter the plans
def income_check(income, jsons):
    plans_ = []
    income = income_conv(income)   # less then 5 --> 5
    for i in jsons:
        min_ = i["minimum_premium_amount"]
        if income == 500000:
            if income > min_:
                plans_.append(i["plan_name"])
        else:
            if income >= min_:
                plans_.append(i["plan_name"])
    return plans_



#age filteration

# Age conversion to numerical
def age_conv(age):
    if isinstance(age, str) and age.isdigit():
        age_in_years = int(age)
    elif isinstance(age, str) and '-' in age:
        age_range = age.split('-')
        age_range = [i.strip() for i in age_range]
        end_age_range = age_range[1].split(" ")[0]
        if "years" in age or "year" in age or "Years" in age or "Year" in age:
            age_in_years = [int(age_range[0]), int(end_age_range)]
        elif "days" in age or "day" in age or "Days" in age or "Day" in age:
            age_in_years = [round(int(age_range[0]) / 365, 2), round(int(end_age_range) / 365, 2)]
        return age_in_years

    else:
        ages = age.split(" ")
        if len(ages) == 2:
            if ages[1] == "years" or ages[1]=="year" or ages[1]=="Years" or ages[1]=="Year":
                age_in_years = round(int(ages[0]) * 1, 2)
            elif ages[1] == "days" or ages[1]=="day" or ages[1]=="Days" or ages[1]=="Day":
                age_in_years = round(int(ages[0]) / 365, 2)
        else:
            age_in_years = [0.08]+[int(re.findall(r'\d+', age)[0])]
    return age_in_years

# Age check to filter the plans
def age_check(age, jsons):
    age = age_conv(age)
    plans = []
    for i in jsons:
        min_ = age_conv(i["minimum_age"])
        max_ = age_conv(i["maximum_age"])
        if age[0] >= min_ and age[1] <= max_:
            plans.append(i["plan_name"])
    return plans