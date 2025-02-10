import os

userDataDir = "userData/"

if not os.path.exists(userDataDir):
    os.mkdir(userDataDir)

class Earnings():
    unit = None
    sales = None
    EBITDA = None
    EBIT = None
    netIncome = None
    capEx = None
    FCF = None

    def loadData(self, msg, unit=False, extended=False):
        if extended and unit:
            raise ValueError("Cannot have extended data with unit.")
        while True:
            try:
                if unit:
                    earningsInp = input(msg+" (separated by a comma or enter 'q' to quit): Sales,EBITDA,EBIT,Net_Income,Unit[K,M,B]\n: ")
                elif extended:
                    earningsInp = input(msg+" (separated by a comma or enter 'q' to quit): Sales,EBITDA,EBIT,Net_Income,CapEx,FCF\n: ")
                else:
                    earningsInp = input(msg+" (separated by a comma or enter 'q' to quit): Sales,EBITDA,EBIT,Net_Income\n: ")
                if earningsInp == "q":
                    os._exit(0)
                earnings = earningsInp.split(",")
                self.sales = float(earnings[0]) if earnings[0] != "" else None
                self.EBITDA = float(earnings[1]) if earnings[1] != "" else None
                self.EBIT = float(earnings[2]) if earnings[2] != "" else None
                self.netIncome = float(earnings[3]) if earnings[3] != "" else None
                if unit:
                    self.unit = earnings[4]
                elif extended:
                    self.capEx = float(earnings[4]) if earnings[4] != "" else None
                    self.FCF = float(earnings[5]) if earnings[5] != "" else None
                break
            except ValueError:
                print("Please enter valid information.")
    def fromList(self, earningsList):
        self.sales = float(earningsList[0]) if earningsList[0] != "" else None
        self.EBITDA = float(earningsList[1]) if earningsList[1] != "" else None
        self.EBIT = float(earningsList[2]) if earningsList[2] != "" else None
        self.netIncome = float(earningsList[3]) if earningsList[3] != "" else None
        if len(earningsList) > 4:
            self.capEx = float(earningsList[4]) if earningsList[4] != "" else None
            self.FCF = float(earningsList[5]) if earningsList[5] != "" else None

def getNextQY(quarter, year):
    if quarter == 4:
        return f"1 {year+1}"
    return f"{quarter+1} {year}"

def getEmoji(diff):
    if diff >= 10: # rocket emoji
        return "🚀"
    elif diff >= 5: # green emoji
        return "🟢"
    elif diff <= -10: # skull emoji
        return "💀"
    elif diff <= -5: # red emoji
        return "🔴"
    else:   # yellow emoji
        return "🟡"

def oneLine(name, actual, expected, unit):
    if actual is None or expected is None:
        return ""
    diff = round((actual - expected) / expected * 100, 2)
    if diff >= 0:
        msg = f"{name}: {actual}{unit} vs. {expected}{unit} expected (+{diff}%) "
    else:
        msg = f"{name}: {actual}{unit} vs. {expected}{unit} expected ({diff}%) "
    msg += f"{getEmoji(diff)}\n"
    return msg

def prepareEarningsReport():
    expectedEarningsQ = Earnings()
    expectedEarningsQ1 = Earnings()
    expectedEarningsY = Earnings()
    expectedEarningsY1 = Earnings()
    while True:
        try:
            metaInp = input("Enter the following information separated by a comma (or 'q' to quit): Quarter,Year,Ticker,Name\n: ")
            if metaInp == "q":
                os._exit(0)
            meta = metaInp.split(",")
            quarter = int(meta[0])
            year = int(meta[1])
            companyTicker = meta[2]
            companyName = meta[3]
            break
        except ValueError:
            print("Please enter valid information.")
    expectedEarningsQ.loadData("Information for this quarter", True)
    expectedEarningsQ1.loadData("Information for the next quarter")
    expectedEarningsY.loadData("Information for this year", extended=True)
    expectedEarningsY1.loadData("Information for the next year", extended=True)
    earningsReport = f"{companyName},{expectedEarningsQ.unit},{expectedEarningsQ.sales},{expectedEarningsQ.EBITDA},{expectedEarningsQ.EBIT},{expectedEarningsQ.netIncome}"
    earningsReport += f",{expectedEarningsQ1.sales},{expectedEarningsQ1.EBITDA},{expectedEarningsQ1.EBIT},{expectedEarningsQ1.netIncome}"
    earningsReport += f",{expectedEarningsY.sales},{expectedEarningsY.EBITDA},{expectedEarningsY.EBIT},{expectedEarningsY.netIncome},{expectedEarningsY.capEx},{expectedEarningsY.FCF}"
    earningsReport += f",{expectedEarningsY1.sales},{expectedEarningsY1.EBITDA},{expectedEarningsY1.EBIT},{expectedEarningsY1.netIncome},{expectedEarningsY1.capEx},{expectedEarningsY1.FCF}"
    with open(f"{userDataDir}{companyTicker}_{year}_{quarter}_earnings.txt", "w") as f:
        f.write(earningsReport)

def evaluateEarningsRelease():
    expectedEarningsQ = Earnings()
    expectedEarningsQ1 = Earnings()
    expectedEarningsY = Earnings()
    expectedEarningsY1 = Earnings()
    actualEarningsQ = Earnings()
    actualEarningsQ1 = Earnings()
    actualEarningsY = Earnings()
    actualEarningsY1 = Earnings()
    while True:
        try:
            metaInp = input("Enter the following information separated by a comma (or 'q' to quit): Quarter,Year,Ticker\n: ")
            if metaInp == "q":
                return
            meta = metaInp.split(",")
            quarter = int(meta[0])
            year = int(meta[1])
            companyTicker = meta[2]
            break
        except ValueError:
            print("Please enter valid information.")
    with open(f"{userDataDir}{companyTicker}_{year}_{quarter}_earnings.txt", "r") as f:
        earningsReport = f.read().split(",")
        companyName = earningsReport[0]
        unit = earningsReport[1]
    expectedEarningsQ.fromList(earningsReport[2:6])
    expectedEarningsQ1.fromList(earningsReport[6:10])
    expectedEarningsY.fromList(earningsReport[10:16])
    expectedEarningsY1.fromList(earningsReport[16:22])
    actualEarningsQ.loadData("Enter actual earnings for this quarter")
    actualEarningsQ1.loadData("Enter actual outlook for the next quarter")
    actualEarningsY.loadData("Enter actual earnings/outlook for this year", extended=True)
    actualEarningsY1.loadData("Enter actual outlook for the next year", extended=True)

    msg = f"{companyName} (${companyTicker}) reports Q{quarter} {year} earnings:\n"
    msg += f"Q{quarter} {year}: \n"
    msg += oneLine("Sales", actualEarningsQ.sales, expectedEarningsQ.sales, unit)
    msg += oneLine("EBITDA", actualEarningsQ.EBITDA, expectedEarningsQ.EBITDA, unit)
    msg += oneLine("EBIT", actualEarningsQ.EBIT, expectedEarningsQ.EBIT, unit)
    msg += oneLine("Net Income", actualEarningsQ.netIncome, expectedEarningsQ.netIncome, unit)
    if quarter == 4:
        msg += f"\nFY{year}: \n"
        msg += oneLine("Sales", actualEarningsY.sales, expectedEarningsY.sales, unit)
        msg += oneLine("EBITDA", actualEarningsY.EBITDA, expectedEarningsY.EBITDA, unit)
        msg += oneLine("EBIT", actualEarningsY.EBIT, expectedEarningsY.EBIT, unit)
        msg += oneLine("Net Income", actualEarningsY.netIncome, expectedEarningsY.netIncome, unit)
        msg += oneLine("CapEx", actualEarningsY.capEx, expectedEarningsY.capEx, unit)
        msg += oneLine("FCF", actualEarningsY.FCF, expectedEarningsY.FCF, unit)
    else:
        msg += f"\nOutlook for FY{year}: \n"
        msg += oneLine("Sales", actualEarningsY.sales, expectedEarningsY.sales, unit)
        msg += oneLine("EBITDA", actualEarningsY.EBITDA, expectedEarningsY.EBITDA, unit)
        msg += oneLine("EBIT", actualEarningsY.EBIT, expectedEarningsY.EBIT, unit)
        msg += oneLine("Net Income", actualEarningsY.netIncome, expectedEarningsY.netIncome, unit)
        msg += oneLine("CapEx", actualEarningsY.capEx, expectedEarningsY.capEx, unit)
        msg += oneLine("FCF", actualEarningsY.FCF, expectedEarningsY.FCF, unit)
    msg += f"\nOutlook for Q{getNextQY(quarter, year)}: \n"
    msg += oneLine("Sales", actualEarningsQ1.sales, expectedEarningsQ1.sales, unit)
    msg += oneLine("EBITDA", actualEarningsQ1.EBITDA, expectedEarningsQ1.EBITDA, unit)
    msg += oneLine("EBIT", actualEarningsQ1.EBIT, expectedEarningsQ1.EBIT, unit)
    msg += oneLine("Net Income", actualEarningsQ1.netIncome, expectedEarningsQ1.netIncome, unit)
    msg += f"\nOutlook for FY{year+1}: \n"
    msg += oneLine("Sales", actualEarningsY1.sales, expectedEarningsY1.sales, unit)
    msg += oneLine("EBITDA", actualEarningsY1.EBITDA, expectedEarningsY1.EBITDA, unit)
    msg += oneLine("EBIT", actualEarningsY1.EBIT, expectedEarningsY1.EBIT, unit)
    msg += oneLine("Net Income", actualEarningsY1.netIncome, expectedEarningsY1.netIncome, unit)
    msg += oneLine("CapEx", actualEarningsY1.capEx, expectedEarningsY1.capEx, unit)
    msg += oneLine("FCF", actualEarningsY1.FCF, expectedEarningsY1.FCF, unit)
    with open("tmp.txt", "w", encoding="utf-8") as f:
        f.write(msg)
    print(msg)
def main():
    userInp = input("Press 'p' to prepare earnings report or 'e' to evaluate the release: ")
    if userInp == "p":
        prepareEarningsReport()
    elif userInp == "e":
        evaluateEarningsRelease()
if __name__ == "__main__":
    main()
