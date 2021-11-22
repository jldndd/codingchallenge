## PDA TEST

# Welcome! 

In this page you can find the description of a coding challenge that we ask candidates to perform when applying for a VIE position in our team. This test is not only a coding challenge: knowledge around energy markets will be useful. 

The goal of this coding challenge is to provide the applicant with some insights into the business we're in as well as notions on the challenges she/he will be confronted with. Next, during the recruitment interviews we will use the applicant's implementation as a seed to discuss.

# Role description:

The role consists of providing development support on all market operations ran by the Power Day-ahead (PDA) team within Engie Global Energy Management (GEM) in Brussels. The PDA team is in charge of bidding the capacities of the power plant portfolios on the spot auctions (day-ahead) of all Central Western Europe (CWE) countries. This includes setting up optimal strategies that emphasize the use of smart bidding products and that result in schedules for each plant that maximize revenues, all the while ensuring physical balance and strict compliance with market rules.

An important part of the operations is related to ancillary services. PDA also ensures the bidding of all ancillary capacities available in the portfolios on the reserve tenders organized by national TSOs. This tender activity is evolving fast, with new products and more frequent deadlines becoming the norm in CWE. There are ongoing efforts to improve the current processes (and develop new ones where applicable) that enable PDA to cost and price these contracts, but there remains a strong need for analytical support and market follow-up.

# Projects on the pipeline:

The VIE role is expected to contribute to the most pressing projects currently at work at PDA. These include a range of both business-related and IS-related developments:
- Algorithm preparing bidding strategies for flexible assets on the spot auctions automatically. A functioning algorithm exists for flexible thermal assets, but a new algorithm needs to be developed for the pump storage assets in the portfolios (more complex bidding).
- Forecasting of ancillary capacity prices for the day-ahead markets. A proof-of-concept (POC) has been developed to forecast prices for the reserve tenders (aFRR and mFRR) in Germany, leveraging machine learning techniques. This POC should now be extended to other markets (e.g. France).
- Migration of the Excel EUA landscape to a server-side environment (Python-based). This would entail running all bidding processes on the server. It will allow simplifying the Excel EUAs to become only user interfaces calling data from the server (APIs).
- Development of a framework (environment) operating all DA tasks in sequence (from server). This development will enable all operations in the DA shifts to be ran at their appropriate times (when the required inputs are available). 

Depending on the progress made by the team on these projects and any other needs that may arise, the VIE role may be required to contribute on other topics.

All market operations performed at PDA are organized in shifts. Subject to availability and to the interest of the candidate, the VIE role may be extended to include training to perform any of these shifts.

# Rules of the coding challenge: 

The exercise consists of two separate, independent parts (with two input files). You can use code lines for both parts and resolve them independently.

=> Inputs

Each of the two inputs files contains similar information, namely:

• Load: the load is the amount of energy (MWh) that needs to be delivered during any single hour.

• Fuel costs: based on the cost of the fuels of each power plant, the merit-order of the portfolio can be determined.

- Gas (euro/MWh): the price of gas per MWh. If the gas price is at 6 euro/MWh and the efficiency of the powerplant is 50% (i.e. 2 units of gas will generate one unit of electricity), the cost of generating 1 MWh is 12 euro.
- Kerosene (euro/MWh): the price of kerosene per MWh.
- Co2 (euro/ton): the price of emission allowances (to be taken into account only optionally, not mandatory for the exercise).
- Wind (%): wind coefficient. Example: if there is on average 25% wind during one hour, a wind-turbine with a capacity of 4 MW will generate 1 MWh of energy.

• Power plants: describes the assets at disposal to generate the demanded load. For each power plant, the information specified is the following:

-	Name
-	Type: gas fired, turbojet or wind turbine.
-	Efficiency: the rate at which they convert a MWh of fuel into a MWh of electrical energy. Wind turbines do not consume fuel and thus do not to incur any fuel costs.
-	Pmax: the maximum amount of power the plant can generate.
-	Pmin: the minimum amount of power the plant generates when switched on.

• Market spot prices (only for part 2).

=> Test

The response should be as clean as possible. You can devise any type of output to display your results (data frame, an Excel spreadsheet sorted by a Python command, a sentence printed via Python, etc.). Keep in mind that, as an operational team, the recipient should be able to interpret results quickly. We will evaluate the quality of your code.

Part 1:

1.	Determine the merit order of the portfolio.
2.	Specify the power output of each asset in order for the portfolio to cover the given load and maximize its total revenues.

Part 2:

For this part, the commitment of the portfolio is independent of the load. The load can be covered by either buying the necessary energy from the market or, else, scheduling the assets to cover the load. In addition to that, assets can be scheduled to produce power up to their maximum capacity (and beyond the required load).

1.	Determine an hourly production plan that maximizes overall portfolio revenues.
2.	Display the position of the power plants (MWh) on the market for each of these hours.
3.	Display the hourly cash flow for each asset as well as the hourly and the daily cash flow for the entire portfolio.

