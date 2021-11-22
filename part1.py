import json
import pandas as pd
import usefullFunctions

with open('Part1') as file:
    parc = file.read()

js_parc = json.loads(parc)

#Marginal Costs Calculation
js_parc = usefullFunctions.getMeritOrder(js_parc)
usefullFunctions.printMeritOrder(js_parc)
df_merit_order = usefullFunctions.getMeritOrderdf(js_parc)

#Optimizing an hour's revenues

load = usefullFunctions.getLoad(js_parc)
active_plants = usefullFunctions.getActivePlantsAndOutputs(load, js_parc)
usefullFunctions.printActivePlantsOutputsAndMarginalCosts(active_plants)
df_power_output = usefullFunctions.getPowerOutputdf(active_plants)


# Excel Export
with pd.ExcelWriter("Export_Part1.xlsx") as writer:
    df_merit_order.to_excel(writer, sheet_name="Merit Order")
    df_power_output.to_excel(writer, sheet_name= "Power Output")

print("Running Completed, Export_Part1.xlsx file successfully exported to project directory.")