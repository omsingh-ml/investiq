
def calculate_financial_ratios(metrics):
    """Calculate basic financial ratios from extracted metrics."""

    ratios = {}

    revenue = metrics.get("Revenue")
    net_income = metrics.get("Net Income")
    operating_income = metrics.get("Operating Income")
    total_assets = metrics.get("Total Assets")
    total_equity = metrics.get("Total Equity")

    if revenue and net_income:
        ratios["Net Profit Margin"] = (
            net_income / revenue
        ) * 100

    if revenue and operating_income:
        ratios["Operating Margin"] = (
            operating_income / revenue
        ) * 100

    if total_assets and net_income:
        ratios["Return on Assets"] = (
            net_income / total_assets
        ) * 100

    if total_equity and net_income:
        ratios["Return on Equity"] = (
            net_income / total_equity
        ) * 100

    return ratios
