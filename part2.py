import usefullFunctions
import json
import pandas as pd

with open('Part2') as file:
    parc = file.read()

parc2 = json.loads(parc)
load = usefullFunctions.getLoad(parc2)
plants = usefullFunctions.getPlants(parc2)
clearing_prices = parc2["Clearing_Prices"]

# Merit Order
usefullFunctions.getMeritOrder(parc2)
usefullFunctions.printMeritOrder(parc2)
df_merit_order = usefullFunctions.getMeritOrderdf(parc2)

# Plant position
active_plants = usefullFunctions.getActivePlantsWithClearingPrices(clearing_prices, load, parc2)

# CashFlows by Asset
positions, revenues, costs, cashflows = usefullFunctions.getHourlyPositionAndCashFlowByAsset(clearing_prices,
                                                                                             active_plants, plants)

# Data Treatment for Excel export
for key, element in active_plants.items():
    active_plants[key] = pd.Series(element, index=[1, 2, 3])

df_active_plants = pd.DataFrame(active_plants).transpose()
df_positions = usefullFunctions.getHourlyPositionsDf(positions)
df_gf_table, df_tj_table, df_cf_table, df_total_table = usefullFunctions.getHourlyAndDailyCashFlowsByAssetAndTotalDf(
    revenues, costs, cashflows)

# Excel Export
with pd.ExcelWriter("Export_Part2.xlsx") as writer:
    df_merit_order.to_excel(writer, sheet_name="Merit Order")
    df_active_plants.to_excel(writer, sheet_name="HourlyProductionPlan")
    df_positions.to_excel(writer, sheet_name='PlantHourlyPosition - MWh')
    df_gf_table.to_excel(writer, sheet_name='GasFiredCashFlows - €')
    df_cf_table.to_excel(writer, sheet_name='CoalFiredCashFlows - €')
    df_tj_table.to_excel(writer, sheet_name='TurbojetCashFlows - €')
    df_total_table.to_excel(writer, sheet_name='TotalCashFlows - €')

#Final Message

print("Running Completed, Export_Part2.xlsx file successfully exported to project directory.")