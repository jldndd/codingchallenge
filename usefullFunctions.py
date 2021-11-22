import numpy as numpy
import pandas as pd


def getLoad(js_parc):
    return js_parc["load"]


def getPlants(js_parc):
    plants = [js_parc["powerplants"][i]["name"] for i in range(len(js_parc["powerplants"]))]
    return plants


def getMeritOrder(js_parc):
    gas_price = js_parc["fuels"]["gas(euro/MWh)"]
    coal_calorifical_power_MWhperton = -(33500 - 34900) / (2 * 3600)
    coal_price = js_parc["fuels"]["coal (euro/ton)"] / coal_calorifical_power_MWhperton
    for i in range(0, len(js_parc["powerplants"]), 1):
        type = js_parc["powerplants"][i]["type"]
        if type == "CCGT" or type == "GT" or type == "turbojet":
            js_parc["powerplants"][i]["marginal cost"] = gas_price / js_parc["powerplants"][i]["efficiency"]
        elif type == "Coal":
            js_parc["powerplants"][i]["marginal cost"] = coal_price / js_parc["powerplants"][i]["efficiency"]
        else:
            js_parc["powerplants"][i]["marginal cost"] = 0.0
    js_parc["powerplants"] = sorted(js_parc["powerplants"], key=lambda k: k["marginal cost"])
    return js_parc


def printMeritOrder(js_parc):
    print()
    print("Merit order:")
    index = 0
    for i in js_parc["powerplants"]:
        index += 1
        print("Plant number %s : %s with a marginal price of %s EUR/MWh." % (
        index, i["name"], round(i["marginal cost"], 1)))
    return None


def getMeritOrderdf(js_parc):
    mo = []
    for elem in js_parc["powerplants"]:
        toadd = [elem["name"], elem["marginal cost"]]
        mo.append(toadd)
    df_merit_order = pd.DataFrame(mo, index=numpy.arange(len(js_parc["powerplants"])) + 1,
                                  columns=["Plant Names", "Marginal Costs - €/MWh"])
    return df_merit_order


def getActivePlantsAndOutputs(load, js_parc):
    capa = 0
    index = -1
    active_plants = {}

    while capa < load:
        index += 1
        pmax = js_parc["powerplants"][index]["pmax"]
        if js_parc["powerplants"][index]["type"] == "windturbine":
            adding = pmax * js_parc["fuels"]["wind(%)"] / 100
        else:
            adding = pmax
        capa += adding
        active_plants[index + 1] = js_parc["powerplants"][index]
        if capa < load:
            active_plants[index + 1]["prod"] = adding
        else:
            active_plants[index + 1]["prod"] = adding - (capa - load)
    active_plants = pmin_check(active_plants)
    return active_plants

def getPowerOutputdf(active_plants):
    po = []
    for key, elem in active_plants.items():
        toadd = [elem["name"], elem["marginal cost"], elem["prod"]]
        po.append(toadd)
    df_power_output = pd.DataFrame(po, index=numpy.arange(len(active_plants)) + 1,
                                  columns=["Plant Names", "Marginal Costs - €/MWh", "Production - MWh"])
    return df_power_output

def pmin_check(active_plants):
    n = max(active_plants)
    for i in range(n, 0, -1):
        output = active_plants[n]["prod"]
        pmin = active_plants[n]["pmin"]
        if output >= pmin:
            break
        else:
            diff = pmin - output
            active_plants[n - 1]["prod"] -= diff
            active_plants[n]["prod"] = pmin
    return active_plants


def printActivePlantsOutputsAndMarginalCosts(active_plants):
    print()
    print("Power Output:")
    check = 0
    for n, i in active_plants.items():
        output = i["prod"]
        cost = i["marginal cost"]
        print("Plant number %s - %s produces %s MWh at a cost of %s EUR/MWh." % (n, i["name"], output, round(cost, 1)))
        check += output

    return None


# Part 2 Specific Functions

def getActivePlantsWithClearingPrices(clearing_prices, load, js_parc):
    active_plants = dict()
    n_hours = len(clearing_prices)
    n_powerplants = len(js_parc["powerplants"])

    for i in range(n_hours):
        price = clearing_prices[i]
        index = 0
        marginal_cost = js_parc["powerplants"][index]["marginal cost"]

        total_prod = 0
        active_plants[i + 1] = dict()

        while marginal_cost < price and index <= n_powerplants - 1:
            plant = js_parc["powerplants"][index]
            marginal_cost = plant["marginal cost"]

            if marginal_cost < price:
                pmax = js_parc["powerplants"][index]["pmax"]
                active_plants[i + 1][index + 1] = plant

                if plant["type"] == "windturbine":
                    adding = pmax * js_parc["fuels"]["wind(%)"] / 100
                else:
                    adding = pmax
                active_plants[i + 1][index + 1]["prod"] = adding
                total_prod += adding

            index += 1

        if total_prod < load:
            active_plants[i + 1] = dict()
            active_plants[i + 1][index + 1] = dict()
            active_plants[i + 1][index + 1]["name"] = "Spot Market"
            active_plants[i + 1][index + 1]["marginal cost"] = price
            active_plants[i + 1][index + 1]["prod"] = load - total_prod

    return active_plants


def getHourlyPositionAndCashFlowByAsset(clearing_prices, active_plants, plants):
    positions = dict()
    revenues = dict()
    costs = dict()
    cashflows = dict()
    for plant in plants:
        positions[plant] = []
        revenues[plant] = []
        costs[plant] = []
        cashflows[plant] = []

    for hour in active_plants:
        currently_on = [active_plants[hour][i + 1]["name"] for i in range(len(active_plants[hour]))]
        price = clearing_prices[hour - 1]
        for plant in plants:
            if plant in currently_on:
                working_plant = active_plants[hour][currently_on.index(plant) + 1]
                prod = working_plant["prod"]
                revenue = prod * price
                cost = working_plant["marginal cost"] * prod
                cf = revenue - cost
                positions[plant].append(prod)
                revenues[plant].append(revenue)
                costs[plant].append((round(cost, 2)))
                cashflows[plant].append(round(cf, 2))
            else:
                positions[plant].append(0)  # append 0 when off
                revenues[plant].append(0)
                costs[plant].append(0)
                cashflows[plant].append(0)
    return positions, revenues, costs, cashflows


def getHourlyTotalCashFlow(cashflows):
    hourlytotalcf = []
    cf_gf = cashflows['gasfiredbig1']
    cf_tj = cashflows['tj1']
    cf_cf = cashflows['Coalfired1']
    for i in range(len(cf_gf)):
        hourlytotalcf.append(cf_gf[i] + cf_tj[i] + cf_cf[i])
    return hourlytotalcf


def getDailyCashFlowByAsset(cashflows):
    dailycf = dict()
    for plant in cashflows:
        dailycf[plant] = sum(cashflows[plant])
    return dailycf


def getDailyTotalCashFlow(hourlytotalcf):
    return sum(hourlytotalcf)


def getHourlyPositionsDf(positions):
    columns = positions.keys()
    index = numpy.arange(24)
    result_nparra = numpy.array([positions[plant] for plant in positions])
    df_positions = pd.DataFrame(numpy.transpose(result_nparra), index=index, columns=columns)
    return df_positions


def getHourlyAndDailyCashFlowsByAssetAndTotalDf(revenues, costs, cashflows):
    index = ["revenues", "costs", "cashflows"]
    columns = numpy.arange(24)
    gf_table = pd.DataFrame(numpy.array([revenues["gasfiredbig1"], costs["gasfiredbig1"], cashflows["gasfiredbig1"]]),
                            index=index, columns=columns)
    gf_table["daily results"] = [sum(revenues["gasfiredbig1"]), sum(costs["gasfiredbig1"]),
                                 sum(cashflows["gasfiredbig1"])]
    tj_table = pd.DataFrame(numpy.array([revenues["tj1"], costs["tj1"], cashflows["tj1"]]), index=index,
                            columns=columns)
    tj_table["daily results"] = [sum(revenues["tj1"]), sum(costs["tj1"]), sum(cashflows["tj1"])]
    cf_table = pd.DataFrame(numpy.array([revenues["Coalfired1"], costs["Coalfired1"], cashflows["Coalfired1"]]),
                            index=index, columns=columns)
    cf_table["daily results"] = [sum(revenues["Coalfired1"]), sum(costs["Coalfired1"]), sum(cashflows["Coalfired1"])]
    total_table = gf_table + tj_table + cf_table

    return gf_table, tj_table, cf_table, total_table


# ToDo #Add Rasing Exception code
"""
    if check != load:
        raise Exception"""
